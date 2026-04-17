#!/usr/bin/env bash
# Shared helper functions for HA API scripts.
# Source this file: source "$(dirname "$0")/ha_helpers.sh"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "ERROR: .env file not found at $ENV_FILE"
    echo "Create it from .env.example and fill in values."
    exit 1
fi

set -a
source "$ENV_FILE"
set +a

# Derived constants (LAN). Uzaktan: .env içinde HA_URL_REMOTE; script öncesi export HA_URL="$HA_URL_REMOTE"
HA_HOST="${HA_URL#http://}"
HA_HOST="${HA_HOST%:*}"

# ── Prerequisites ────────────────────────────────────────────────

require_sshpass() {
    if ! command -v sshpass &>/dev/null; then
        echo "[ERROR] sshpass required. Install: brew install sshpass"
        exit 1
    fi
}

ensure_websockets() {
    python3 -c "import websockets" 2>/dev/null || \
        python3 -m pip install -q websockets
}

# ── REST API helpers ─────────────────────────────────────────────

ha_get() {
    curl -s -H "Authorization: Bearer $HA_TOKEN" \
         -H "Content-Type: application/json" \
         "${HA_URL}${1}"
}

ha_post() {
    curl -s -H "Authorization: Bearer $HA_TOKEN" \
         -H "Content-Type: application/json" \
         -X POST "${HA_URL}${1}" \
         ${2:+-d "$2"}
}

ha_check_connection() {
    local config
    config=$(ha_get "/api/config") || {
        echo "ERROR: Cannot connect to Home Assistant at $HA_URL"
        exit 1
    }
    local version
    version=$(echo "$config" | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])")
    echo "Connected to Home Assistant $version at $HA_URL"
}

# ── SSH helpers ──────────────────────────────────────────────────

ssh_ha() {
    sshpass -p "${SSH_PASS}" ssh \
        -o StrictHostKeyChecking=no \
        -o ConnectTimeout=10 \
        -o ServerAliveInterval=15 \
        "root@${HA_HOST}" "$@"
}

ssh_ha_check() {
    ssh_ha "echo ok" &>/dev/null
}

# Poll until an addon reaches target state (default: started)
# Usage: ssh_ha_wait_addon_state <slug> [target_state] [timeout_sec]
ssh_ha_wait_addon_state() {
    local slug="$1"
    local target="${2:-started}"
    local timeout="${3:-30}"
    local elapsed=0
    while (( elapsed < timeout )); do
        local state
        state=$(ssh_ha "ha apps info $slug --raw-json" 2>/dev/null | \
            python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('state','unknown'))" 2>/dev/null || echo "unknown")
        if [[ "$state" == "$target" ]]; then return 0; fi
        sleep 3
        elapsed=$((elapsed + 3))
    done
    return 1
}

# ── WebSocket helpers ────────────────────────────────────────────

# Run a python+websockets snippet. The snippet gets WS_URI and WS_TOKEN variables.
ha_ws() {
    local pycode="$1"
    ensure_websockets
    python3 << PYEOF
import json, asyncio, sys
sys.stdout.reconfigure(line_buffering=True)
import websockets

WS_URI = "${HA_URL}".replace("http://", "ws://") + "/api/websocket"
WS_TOKEN = "${HA_TOKEN}"

async def _ws_auth(ws):
    await ws.recv()
    await ws.send(json.dumps({"type": "auth", "access_token": WS_TOKEN}))
    msg = json.loads(await ws.recv())
    if msg["type"] != "auth_ok":
        print("[ERROR] WebSocket auth failed"); sys.exit(1)

${pycode}

asyncio.run(main())
PYEOF
}

# ── Integration install (REST config flow) ───────────────────────

ha_install_integration() {
    local domain="$1"
    local flow_input="${2:-}"

    echo "  [INSTALL] $domain ..."
    local flow
    flow=$(ha_post "/api/config/config_entries/flow" "{\"handler\": \"$domain\"}")
    local flow_type
    flow_type=$(echo "$flow" | python3 -c "import sys,json; print(json.load(sys.stdin)['type'])")

    if [[ "$flow_type" == "abort" ]]; then
        local reason
        reason=$(echo "$flow" | python3 -c "import sys,json; print(json.load(sys.stdin).get('reason','unknown'))")
        if [[ "$reason" == "already_configured" || "$reason" == "single_instance_allowed" ]]; then
            echo "  [SKIP] $domain already installed ($reason)"
            return 0
        fi
        echo "  [ERROR] Flow aborted: $reason"
        return 1
    fi

    local flow_id
    flow_id=$(echo "$flow" | python3 -c "import sys,json; print(json.load(sys.stdin)['flow_id'])")

    # Handle menu-type flows (e.g. MQTT offers addon vs manual)
    if [[ "$flow_type" == "menu" ]]; then
        local input="${flow_input:-'{"next_step_id":"addon"}'}"
        local result
        result=$(ha_post "/api/config/config_entries/flow/$flow_id" "$input")
    else
        local result
        result=$(ha_post "/api/config/config_entries/flow/$flow_id" "${flow_input:-{}}")
    fi

    local result_type
    result_type=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin)['type'])")

    if [[ "$result_type" == "create_entry" ]]; then
        local title
        title=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin)['title'])")
        echo "  [OK] $title installed"
    elif [[ "$result_type" == "abort" ]]; then
        local reason
        reason=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('reason','unknown'))")
        echo "  [SKIP] $domain ($reason)"
    else
        echo "  [WARN] Unexpected result: $result_type"
        return 1
    fi
}

ha_get_entry_id() {
    local domain="$1"
    ha_ws "
async def main():
    async with websockets.connect(WS_URI, max_size=2**22, open_timeout=30) as ws:
        await _ws_auth(ws)
        await ws.send(json.dumps({'id': 1, 'type': 'config_entries/get'}))
        msg = json.loads(await ws.recv())
        for e in msg.get('result', []):
            if e['domain'] == '$domain' and e['state'] == 'loaded':
                print(e['entry_id']); return
        sys.exit(1)
"
}

ha_set_options() {
    local entry_id="$1"
    local options_data="$2"

    echo "  [OPTIONS] Configuring entry $entry_id ..."
    local flow_response
    flow_response=$(ha_post "/api/config/config_entries/options/flow" "{\"handler\": \"$entry_id\"}")
    local flow_id
    flow_id=$(echo "$flow_response" | python3 -c "import sys,json; print(json.load(sys.stdin)['flow_id'])")

    ha_post "/api/config/config_entries/options/flow/$flow_id" "$options_data" > /dev/null
    echo "  [OK] Options applied"
}

ha_reload_entry() {
    local entry_id="$1"
    ha_post "/api/config/config_entries/entry/${entry_id}/reload" > /dev/null
    echo "  [OK] Reloaded entry $entry_id"
}
