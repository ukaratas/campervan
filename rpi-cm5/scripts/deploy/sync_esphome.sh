#!/usr/bin/env bash
# Deploy rpi-cm5/esphome/* → HAOS /config/esphome/, opsiyonel build + OTA upload.
#
# Kullanım:
#   ./sync_esphome.sh                              # tüm cihazları yükle, validate yap
#   ./sync_esphome.sh --device cv-sensors-01       # tek cihaz: yükle + validate
#   ./sync_esphome.sh --device cv-sensors-01 --build   # + compile (OTA göndermez)
#   ./sync_esphome.sh --device cv-sensors-01 --ota     # + compile + OTA upload (tetikler ve canlı log)
#   ./sync_esphome.sh --dry-run                    # sadece dosya listesi göster

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
source "$(cd "$SCRIPT_DIR/.." && pwd)/ha_helpers.sh"

DRY_RUN=false
DEVICE=""
ACTION="validate"   # validate | build | ota
for a in "$@"; do
    case "$a" in
        --dry-run) DRY_RUN=true ;;
        --device)  shift_next=1 ;;
        --build)   ACTION="build" ;;
        --ota)     ACTION="ota" ;;
        --validate-only) ACTION="validate" ;;
        *)
            if [[ "${shift_next:-0}" == "1" ]]; then
                DEVICE="$a"; shift_next=0
            fi
            ;;
    esac
done

SRC="$ROOT/esphome"
[[ -d "$SRC" ]] || { echo "ERROR: $SRC bulunamadı"; exit 1; }

ha_check_connection
echo ""

# ── 1) secrets.yaml: example'daki yeni keyleri merge et ─────────
if [[ -f "$SRC/secrets.yaml.example" ]]; then
    echo "=== secrets.yaml merge (example'dan eksik keyler) ==="
    if $DRY_RUN; then
        echo "  [dry-run] secrets merge atlanır"
    else
        # Local'de secrets.yaml var mı kontrol et; yoksa example'dan oluştur
        if [[ ! -f "$SRC/secrets.yaml" ]]; then
            echo "  [INFO] Local secrets.yaml yok; HAOS'taki kullanılacak."
        else
            echo "  [SKIP] Local secrets.yaml var; HAOS dokunulmaz (manuel sync için scp_ha kullan)"
        fi

        # HAOS'ta secrets.yaml yoksa boş oluştur
        ssh_ha "test -f /config/esphome/secrets.yaml || touch /config/esphome/secrets.yaml"

        # Example'daki her key için HAOS'ta yoksa append et (placeholder ile)
        TMPFILE=$(mktemp)
        scp_ha_from /config/esphome/secrets.yaml "$TMPFILE"
        added=0
        while IFS= read -r line || [[ -n "$line" ]]; do
            [[ -z "${line// }" ]] && continue
            [[ "$line" =~ ^[[:space:]]*# ]] && continue
            key="${line%%:*}"
            key="${key// /}"
            [[ -z "$key" ]] && continue
            if ! grep -qE "^${key}:" "$TMPFILE"; then
                echo "$line" >> "$TMPFILE"
                echo "  [+] eklendi: $key"
                added=$((added+1))
            fi
        done < "$SRC/secrets.yaml.example"
        if (( added > 0 )); then
            scp_ha "$TMPFILE" /config/esphome/secrets.yaml
            echo "  [OK] $added yeni key HAOS secrets'a eklendi"
        else
            echo "  [OK] secrets.yaml güncel"
        fi
        rm -f "$TMPFILE"
    fi
    echo ""
fi

# ── 2) YAML cihazlarını listele/yükle ───────────────────────────
echo "=== ESPHome YAML deploy ==="
YAML_FILES=()
if [[ -n "$DEVICE" ]]; then
    YAML_FILES=("$SRC/${DEVICE}.yaml")
else
    while IFS= read -r line; do
        YAML_FILES+=("$line")
    done < <(find "$SRC" -maxdepth 1 -type f -name "*.yaml" \
        ! -name "secrets.yaml" ! -name "secrets.yaml.example")
fi

for f in "${YAML_FILES[@]}"; do
    [[ -f "$f" ]] || { echo "  [SKIP] $f yok"; continue; }
    base="$(basename "$f")"
    if $DRY_RUN; then
        echo "  [dry-run] would upload: $f"
    else
        scp_ha "$f" "/config/esphome/$base"
        echo "  [OK] $base → /config/esphome/$base"
    fi
done

if $DRY_RUN; then exit 0; fi

# ── 3) Build/OTA action (sadece tek cihaz için) ─────────────────
if [[ -z "$DEVICE" ]]; then
    echo ""
    echo "[INFO] Build/OTA için --device ile cihaz belirt: $0 --device cv-sensors-01 --ota"
    exit 0
fi

CONFIG_FILE="${DEVICE}.yaml"

# ESPHome ingress entry'sini al
ensure_websockets
echo ""
echo "=== ESPHome dashboard endpoint keşfi ==="
INGRESS_ENTRY=$(curl -sS -H "Authorization: Bearer $HA_TOKEN" \
    "$HA_URL/api/hassio/addons" 2>/dev/null | \
    python3 -c "
import sys, json
d = json.load(sys.stdin)
for a in d.get('data', {}).get('addons', []):
    if 'esphome' in a.get('slug', '').lower():
        print(a.get('ingress_url', ''))
        break
" 2>/dev/null || echo "")

# Fallback: WebSocket üzerinden supervisor API çağır
if [[ -z "$INGRESS_ENTRY" ]]; then
    INGRESS_ENTRY=$(python3 << PYEOF
import asyncio, json
from websockets.legacy.client import connect

async def main():
    uri = "${HA_URL/http/ws}/api/websocket"
    async with connect(uri, max_size=2**22) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type":"auth","access_token":"$HA_TOKEN"}))
        await ws.recv()
        await ws.send(json.dumps({"id":1,"type":"supervisor/api","endpoint":"/store/addons","method":"get"}))
        d = json.loads(await ws.recv())
        for a in d.get("result",{}).get("addons", []):
            if "esphome" in a.get("slug","").lower() and a.get("installed"):
                slug = a["slug"]
                await ws.send(json.dumps({"id":2,"type":"supervisor/api","endpoint":f"/addons/{slug}/info","method":"get"}))
                d2 = json.loads(await ws.recv())
                print(d2.get("result",{}).get("ingress_url",""))
                return

asyncio.run(main())
PYEOF
)
fi
INGRESS_ENTRY="${INGRESS_ENTRY%/}"
[[ -n "$INGRESS_ENTRY" ]] || { echo "[ERROR] ESPHome ingress URL bulunamadı"; exit 1; }
echo "  [OK] $INGRESS_ENTRY"

# Ingress session aç
SESSION=$(python3 << PYEOF
import asyncio, json
from websockets.legacy.client import connect
async def main():
    uri = "${HA_URL/http/ws}/api/websocket"
    async with connect(uri, max_size=2**22) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type":"auth","access_token":"$HA_TOKEN"}))
        await ws.recv()
        await ws.send(json.dumps({"id":1,"type":"supervisor/api","endpoint":"/ingress/session","method":"post"}))
        d = json.loads(await ws.recv())
        print(d["result"]["session"])
asyncio.run(main())
PYEOF
)

WS_BASE="${HA_URL/http/ws}${INGRESS_ENTRY}"

# Endpoint seçimi
case "$ACTION" in
    validate) WS_PATH="/validate"; PAYLOAD='{"type":"spawn","configuration":"'$CONFIG_FILE'"}' ;;
    build)    WS_PATH="/compile";  PAYLOAD='{"type":"spawn","configuration":"'$CONFIG_FILE'"}' ;;
    ota)      WS_PATH="/run";      PAYLOAD='{"type":"spawn","configuration":"'$CONFIG_FILE'","port":"OTA"}' ;;
esac

echo ""
echo "=== ESPHome action: $ACTION ($CONFIG_FILE) ==="

python3 << PYEOF
import asyncio, json, sys, re
from websockets.legacy.client import connect

ANSI = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

async def main():
    uri = "$WS_BASE$WS_PATH"
    extra = [("Cookie", "ingress_session=$SESSION")]
    print(f"Connecting: {uri}")
    print("-" * 80)
    async with connect(uri, extra_headers=extra, max_size=2**24, ping_interval=20, ping_timeout=900) as ws:
        await ws.send('$PAYLOAD')
        try:
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=1200)
                d = json.loads(msg)
                t = d.get("event")
                if t == "line":
                    line = ANSI.sub("", d.get("data","")).rstrip()
                    if not line: continue
                    if any(x in line for x in ["[D][", "[V][", "[S][", "[C]["]): continue
                    if line.startswith("Compiling .pioenvs") or line.startswith("Indexing"): continue
                    print(line, flush=True)
                    if "$ACTION" == "ota" and "INFO Successfully uploaded" in line:
                        print("\\n--- OTA başarılı, log stream kapatılıyor ---")
                        return
                elif t == "exit":
                    rc = d.get("code")
                    print("-" * 80)
                    print(f"--- $ACTION exit code: {rc} ---")
                    sys.exit(0 if rc == 0 else 2)
        except asyncio.TimeoutError:
            print("[TIMEOUT]"); sys.exit(3)

asyncio.run(main())
PYEOF
