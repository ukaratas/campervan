#!/usr/bin/env bash
# Install and configure Mosquitto MQTT broker + HA MQTT integration.
# Requires SSH addon to be running (setup_ssh.sh must run first).
# Idempotent - safe to run multiple times.
#
# Usage: ./setup_mqtt.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../ha_helpers.sh"

MQTT_USER="${MQTT_USER:-campervan}"
MQTT_PASS="${MQTT_PASS:-campervan2026}"
ADDON_SLUG="core_mosquitto"

echo "=== MQTT Setup (Mosquitto + HA Integration) ==="
ha_check_connection
require_sshpass

if ! ssh_ha_check; then
    echo "[ERROR] SSH not available. Run setup_ssh.sh first."
    exit 1
fi
echo ""

# ── Step 1: Install Mosquitto addon via SSH ──────────────────────
echo "Step 1: Install Mosquitto addon"

INSTALLED=$(ssh_ha "ha apps info $ADDON_SLUG --raw-json" 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print('yes' if d.get('installed') and d.get('version') else 'no')" 2>/dev/null || echo "no")

if [[ "$INSTALLED" == "yes" ]]; then
    VERSION=$(ssh_ha "ha apps info $ADDON_SLUG --raw-json" 2>/dev/null | \
        python3 -c "import sys,json; print(json.load(sys.stdin)['data']['version'])")
    echo "  [SKIP] Mosquitto already installed (v${VERSION})"
else
    echo "  [INSTALL] Downloading Mosquitto addon (may take a few minutes on WiFi)..."
    if ssh_ha "ha apps install $ADDON_SLUG" 2>&1; then
        echo "  [OK] Mosquitto addon installed"
    else
        # Verify despite error exit code (SSH timeout during long pull)
        INSTALLED=$(ssh_ha "ha apps info $ADDON_SLUG --raw-json" 2>/dev/null | \
            python3 -c "import sys,json; print('yes' if json.load(sys.stdin)['data'].get('installed') else 'no')" 2>/dev/null || echo "no")
        if [[ "$INSTALLED" == "yes" ]]; then
            echo "  [OK] Mosquitto addon installed (verified after timeout)"
        else
            echo "  [ERROR] Install failed. Check logs: ssh root@${HA_HOST} ha supervisor logs"
            exit 1
        fi
    fi
fi

echo ""

# ── Step 2: Configure Mosquitto ─────────────────────────────────
echo "Step 2: Configure Mosquitto addon"

ha_ws "
async def main():
    async with websockets.connect(WS_URI, max_size=2**22, ping_interval=20, ping_timeout=60, open_timeout=30) as ws:
        await _ws_auth(ws)

        await ws.send(json.dumps({
            'id': 1, 'type': 'supervisor/api',
            'endpoint': '/addons/${ADDON_SLUG}/options',
            'method': 'post',
            'data': {'options': {
                'logins': [{'username': '${MQTT_USER}', 'password': '${MQTT_PASS}'}],
                'require_certificate': False,
                'certfile': 'fullchain.pem',
                'keyfile': 'privkey.pem',
                'customize': {'active': False, 'folder': 'mosquitto'}
            }}
        }))
        msg = json.loads(await ws.recv())
        if msg.get('success'):
            print('  [OK] Config applied (user=${MQTT_USER})')
        else:
            print(f'  [ERROR] {msg.get(\"error\", {})}')
            sys.exit(1)
"

echo ""

# ── Step 3: Start Mosquitto ─────────────────────────────────────
echo "Step 3: Start Mosquitto"

STATE=$(ssh_ha "ha apps info $ADDON_SLUG --raw-json" 2>/dev/null | \
    python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('state','unknown'))")

if [[ "$STATE" == "started" ]]; then
    echo "  [SKIP] Mosquitto already running"
else
    ssh_ha "ha apps start $ADDON_SLUG" 2>&1 || true
    sleep 3
    if ssh_ha_wait_addon_state "$ADDON_SLUG" "started" 30; then
        echo "  [OK] Mosquitto running"
    else
        echo "  [ERROR] Mosquitto failed to start"
        echo "  Logs: ssh root@${HA_HOST} ha apps logs $ADDON_SLUG"
        exit 1
    fi
fi

echo ""

# ── Step 4: Install MQTT integration in HA ──────────────────────
echo "Step 4: Install MQTT integration"

ha_install_integration "mqtt" '{"next_step_id":"addon"}'

echo ""

# ── Step 5: Verify ──────────────────────────────────────────────
echo "Step 5: Verify MQTT"

VERSION=$(ssh_ha "ha apps info $ADDON_SLUG --raw-json" 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(f'v{d[\"version\"]} state={d[\"state\"]}')")
echo "  Mosquitto: $VERSION"

if command -v mosquitto_pub &>/dev/null; then
    mosquitto_pub -h "$HA_HOST" -p "${MQTT_PORT:-1883}" -u "$MQTT_USER" -P "$MQTT_PASS" \
        -t "campervan/setup/test" -m "{\"status\":\"ok\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" 2>/dev/null && \
        echo "  MQTT publish test: OK" || echo "  MQTT publish test: FAILED"
else
    echo "  [INFO] Install mosquitto clients for publish test: brew install mosquitto"
fi

echo ""
echo "=== MQTT Setup complete ==="
echo ""
echo "  Broker (internal): core-mosquitto:1883"
echo "  Broker (external): ${HA_HOST}:${MQTT_PORT:-1883}"
echo "  Username: ${MQTT_USER}"
echo "  Test:     mosquitto_pub -h ${HA_HOST} -u ${MQTT_USER} -P ${MQTT_PASS} -t test -m hello"
