#!/usr/bin/env bash
# Waveshare Modbus RTU Analog Input 8CH: RS485 adresini 3 yap + HA configuration.yaml'a sensörleri ekle.
#
# ÖNEMLİ (Waveshare wiki): Fabrika adresi genelde 1; IO 8CH de slave 1 ise aynı hatta iki "1" olmaz.
# Adres yazma komutu (broadcast 00 06 40 00 00 03) gönderilirken hatta yalnızca bu modülün slave 1
# olarak yanıt vermesi gerekir — IO8'in A/B uçlarını geçici ayırın (röle slave 2 kalabilir).
#
# Kullanım:
#   ./provision_analog_ai8ch.sh              # adres + yaml (onay ister)
#   ./provision_analog_ai8ch.sh -y           # onaysız (CI / agent)
#   ./provision_analog_ai8ch.sh --yaml-only  # adres atlamışsan sadece yaml
#   ./provision_analog_ai8ch.sh --addr-only  # sadece Modbus adres yaz (HA durur)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../ha_helpers.sh"

YAML_ONLY=false
ADDR_ONLY=false
ASSUME_YES=false
for a in "$@"; do
  case "$a" in
    --yaml-only) YAML_ONLY=true ;;
    --addr-only) ADDR_ONLY=true ;;
    -y|--yes) ASSUME_YES=true ;;
  esac
done

FRAGMENT="$SCRIPT_DIR/../legacy/ha_modbus_rs485_analog_8ch.fragment.yaml"
REMOTE_CFG="/config/configuration.yaml"
LOCAL_MERGE="/tmp/ha_cfg_analog_merge.$$"

require_sshpass
ensure_websockets

if [[ ! -f "$FRAGMENT" ]]; then
  echo "ERROR: $FRAGMENT yok"
  exit 1
fi

if [[ "$YAML_ONLY" != "true" && "$ASSUME_YES" != "true" ]]; then
  echo ""
  echo "Analog 8CH adresi (→ slave 3) yazılacaksa:"
  echo "  - IO 8CH modülünün RS485 A/B kablolarını geçici çıkarın (slave 1 çakışmasın)."
  echo "  - Analog modül + USB RS485 aynı hat üzerinde kalsın; röle (slave 2) takılı kalabilir."
  echo ""
  read -r -p "Hazır mısın? [y/N] " ans || true
  if [[ "${ans:-}" != "y" && "${ans:-}" != "Y" ]]; then
    echo "İptal. Sadece YAML için: $0 --yaml-only -y"
    exit 1
  fi
fi

# --- Modbus: broadcast ile cihaz adresi = 3 (wiki: 00 06 40 00 00 03 DD DA) ---
if [[ "$YAML_ONLY" != "true" ]]; then
  echo "=== Modbus: slave adresi 3 yazılıyor (HA core stop) ==="
  ssh_ha "ha core stop" || true
  sleep 4

  sshpass -p "${SSH_PASS}" scp -o PreferredAuthentications=password \
    "$SCRIPT_DIR/_ha_remote_set_analog_slave3.py" "root@${HA_HOST}:/tmp/_ha_remote_set_analog_slave3.py"
  ssh_ha "python3 /tmp/_ha_remote_set_analog_slave3.py"

  echo "=== HA core start ==="
  ssh_ha "ha core start" || true
  echo "HA ayağa kalkması için bekleniyor (45 sn)..."
  for _ in $(seq 1 18); do
    code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/" 2>/dev/null || echo 000)
    if [[ "$code" == "200" ]]; then break; fi
    sleep 5
  done
fi

if [[ "$ADDR_ONLY" == "true" ]]; then
  echo "Tamam (--addr-only). YAML için: $0 --yaml-only -y"
  exit 0
fi

# --- Analog Modbus YAML (modüler: sync_ha_config.sh; eski: tek configuration.yaml birleştir) ---
echo "=== Analog Modbus YAML ==="
if ssh_ha "grep -rqs 'rs485_ai_ch1' /config/modbus/ /config/configuration.yaml 2>/dev/null"; then
  echo "  [SKIP] rs485_ai_ch1 zaten tanımlı (modbus/ veya configuration.yaml)"
elif [[ "${LEGACY_ANALOG_YAML_MERGE:-}" == "1" ]]; then
  echo "  [LEGACY] configuration.yaml içine fragment ekleniyor (LEGACY_ANALOG_YAML_MERGE=1)"
  sshpass -p "${SSH_PASS}" scp -o PreferredAuthentications=password \
    "root@${HA_HOST}:${REMOTE_CFG}" "$LOCAL_MERGE"
  CFG_MERGE="$LOCAL_MERGE" FRAG_MERGE="$FRAGMENT" python3 << 'PY'
import pathlib, os, sys
cfg_path = pathlib.Path(os.environ["CFG_MERGE"])
frag_path = pathlib.Path(os.environ["FRAG_MERGE"])
text = cfg_path.read_text(encoding="utf-8")
if "rs485_ai_ch1" in text:
    print("  [SKIP] rs485_ai_ch1 zaten tanımlı")
    sys.exit(0)
frag = frag_path.read_text(encoding="utf-8")
lines = [ln for ln in frag.splitlines() if not ln.strip().startswith("#")]
block = "\n".join(lines).rstrip() + "\n"
anchor = """      - name: "DI8 — Future use"
        unique_id: rs485_io8_di8
        address: 7
        slave: 1
        input_type: discrete_input
        scan_interval: 15"""
if anchor in text:
    text = text.replace(anchor, anchor + "\n" + block, 1)
else:
    print("  [ERROR] IO8 DI8 bloğu bulunamadı (legacy birleştirme).")
    sys.exit(1)
cfg_path.write_text(text, encoding="utf-8")
print("  [OK] Analog sensör bloğu eklendi")
PY
  sshpass -p "${SSH_PASS}" scp -o PreferredAuthentications=password \
    "$LOCAL_MERGE" "root@${HA_HOST}:${REMOTE_CFG}"
  rm -f "$LOCAL_MERGE"
else
  echo "  [INFO] Analog tanım yok. Modüler kurulum: bash $SCRIPT_DIR/../deploy/sync_ha_config.sh"
  echo "         Eski tek dosya birleştirmesi: LEGACY_ANALOG_YAML_MERGE=1 $0 --yaml-only -y"
fi

echo "=== ha core check ==="
ssh_ha "ha core check"

echo "=== ha core restart ==="
ssh_ha "ha core restart"

echo ""
echo "=== Admin Bench Lovelace (WS-AI-01 sekmesi) ==="
export RELAY_IP="${RELAY_IP:-10.0.0.200}"
export RELAY_PORT="${RELAY_PORT:-4196}"
python3 "$SCRIPT_DIR/../lovelace/lovelace_push_admin_bench.py" || echo "  [WARN] Lovelace API başarısız; HA_TOKEN ile yerelde: python3 scripts/lovelace/lovelace_push_admin_bench.py"

echo ""
echo "Bitti. Developer Tools → States: sensor.ws_ai_ch1 … ws_ai_ch8"
