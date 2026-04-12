#!/usr/bin/env bash
# Configure RPi CM5 network interfaces for campervan control bus.
#
# Topology:
#   wlan0 (192.168.1.91/24) → WiFi, internet, HA UI access
#   end0  (10.0.0.1/24)     → Ethernet control bus (relays, sensors, Modbus devices)
#
# The control bus is on a separate 10.0.0.x subnet to avoid routing conflicts
# with the WiFi network. Waveshare relay module is at 10.0.0.200.
#
# Prerequisites:
#   - HA running and accessible via WiFi
#   - python3, websockets, sshpass
#   - Ethernet cable connected to control bus

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../ha_helpers.sh"

RELAY_IP="${RELAY_IP:-10.0.0.200}"
RELAY_PORT="${RELAY_PORT:-4196}"
END0_IP="10.0.0.1"
END0_CIDR="10.0.0.1/24"

echo "── Network Setup ──────────────────────────────────────────────"
echo ""

# ── Step 1: Configure end0 static IP ────────────────────────────
echo "[1/3] Configuring end0: ${END0_CIDR} (no gateway) ..."

ensure_websockets
ha_ws "
async def main():
    async with websockets.connect(WS_URI, max_size=2**22, ping_interval=20, open_timeout=10) as ws:
        await _ws_auth(ws)

        # Check current state
        await ws.send(json.dumps({'id': 1, 'type': 'supervisor/api',
            'endpoint': '/network/interface/end0/info', 'method': 'get'}))
        msg = json.loads(await ws.recv())
        info = msg.get('result', {})
        ipv4 = info.get('ipv4', {})
        current = ipv4.get('address', [])

        if current == ['${END0_CIDR}'] and ipv4.get('method') == 'static':
            print('  [SKIP] end0 already configured as ${END0_CIDR}')
            return

        await ws.send(json.dumps({'id': 2, 'type': 'supervisor/api',
            'endpoint': '/network/interface/end0/update', 'method': 'post',
            'data': {
                'enabled': True,
                'ipv4': {'method': 'static', 'address': ['${END0_CIDR}'], 'nameservers': []},
                'ipv6': {'method': 'disabled'}
            }
        }))
        msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=15))
        if msg.get('success'):
            print('  [OK] end0 set to ${END0_CIDR}')
        else:
            print(f'  [ERROR] {msg.get(\"error\", {})}')
            sys.exit(1)
"

# ── Step 2: Verify HA still reachable via WiFi ──────────────────
echo ""
echo "[2/3] Verifying WiFi connectivity ..."
sleep 2
ha_check_connection

# ── Step 3: Check relay connectivity ────────────────────────────
echo ""
echo "[3/3] Checking relay at ${RELAY_IP}:${RELAY_PORT} ..."

require_sshpass
if ! ssh_ha_check; then
    echo "  [WARN] SSH not available, cannot test relay. Run setup_ssh.sh first."
    exit 0
fi

PING_RESULT=$(ssh_ha "ping -c 2 -W 2 ${RELAY_IP} 2>&1" || true)
if echo "$PING_RESULT" | grep -q "bytes from"; then
    echo "  [OK] Relay ping OK"
else
    echo "  [WARN] Relay not responding at ${RELAY_IP}"
    echo "  Ensure ethernet cable is connected and relay is powered."
    echo "  Relay default IP is 192.168.1.200 - may need reconfiguration."
    exit 0
fi

# Modbus TCP port check
PORT_RESULT=$(ssh_ha "(echo > /dev/tcp/${RELAY_IP}/${RELAY_PORT}) 2>&1 && echo OPEN || echo CLOSED" || echo "CLOSED")
if echo "$PORT_RESULT" | grep -q "OPEN"; then
    echo "  [OK] Modbus TCP port ${RELAY_PORT} open"
else
    echo "  [WARN] Modbus TCP port ${RELAY_PORT} not open"
fi

# Read relay coil states via Modbus RTU over TCP
COIL_RESP=$(ssh_ha "
    RESP=\$(printf '\x01\x01\x00\x00\x00\x10\x3d\xc6' | { cat; sleep 1; } | nc -w 3 ${RELAY_IP} ${RELAY_PORT} 2>/dev/null | xxd -p)
    echo \"\$RESP\"
" 2>/dev/null || echo "")

if [[ -n "$COIL_RESP" && ${#COIL_RESP} -ge 10 ]]; then
    echo "  [OK] Modbus RTU response: ${COIL_RESP}"
    echo "  Relay module is communicating correctly."
else
    echo "  [WARN] No Modbus response (relay may need restart)"
fi

echo ""
echo "── Network Summary ────────────────────────────────────────────"
echo "  wlan0:  192.168.1.91/24 (WiFi, gateway 192.168.1.1)"
echo "  end0:   ${END0_CIDR}    (Control bus, no gateway)"
echo "  Relay:  ${RELAY_IP}:${RELAY_PORT} (Waveshare 16CH, Modbus RTU/TCP)"
echo "  MAC:    04-EE-E8-17-54-18"
