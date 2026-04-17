#!/usr/bin/env bash
# LAN + Ethernet relay doğrulaması (Teltonika veya benzeri tek subnet kurulumu).
#
# Eski mimarideki end0 / 10.0.0.x kontrol bus yapılandırması kaldırıldı; HA ve Waveshare
# 16CH relay aynı LAN'dadır (örn. 192.168.50.0/24). Adresler .env üzerinden:
#   RELAY_IP, RELAY_PORT
#
# Adımlar:
#   [1/2] HA REST API erişilebilirliği
#   [2/2] SSH ile HA konteynerinden relay ping / TCP / kısa Modbus yanıtı
#
# Gereksinimler: python3, curl, sshpass (relay testi için), setup_ssh.sh tamamlanmış olmalı

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../ha_helpers.sh"

RELAY_IP="${RELAY_IP:-192.168.50.20}"
RELAY_PORT="${RELAY_PORT:-4196}"

echo "── Network Setup (LAN + relay) ─────────────────────────────────"
echo ""

echo "[1/2] Verifying Home Assistant API ..."
ha_check_connection

echo ""
echo "[2/2] Checking relay at ${RELAY_IP}:${RELAY_PORT} ..."

require_sshpass
if ! ssh_ha_check; then
    echo "  [WARN] SSH not available. Run setup_ssh.sh first."
    exit 0
fi

PING_RESULT=$(ssh_ha "ping -c 2 -W 2 ${RELAY_IP} 2>&1" || true)
if echo "$PING_RESULT" | grep -q "bytes from"; then
    echo "  [OK] Relay ping OK"
else
    echo "  [WARN] Relay not responding to ping at ${RELAY_IP}"
    echo "  Check cable, PoE, and DHCP/reservation on the router."
    exit 0
fi

PORT_RESULT=$(ssh_ha "(echo > /dev/tcp/${RELAY_IP}/${RELAY_PORT}) 2>&1 && echo OPEN || echo CLOSED" || echo "CLOSED")
if echo "$PORT_RESULT" | grep -q "OPEN"; then
    echo "  [OK] Modbus TCP port ${RELAY_PORT} open"
else
    echo "  [WARN] Modbus TCP port ${RELAY_PORT} not open"
fi

COIL_RESP=$(ssh_ha "
    RESP=\$(printf '\x01\x01\x00\x00\x00\x10\x3d\xc6' | { cat; sleep 1; } | nc -w 3 ${RELAY_IP} ${RELAY_PORT} 2>/dev/null | xxd -p)
    echo \"\$RESP\"
" 2>/dev/null || echo "")

if [[ -n "$COIL_RESP" && ${#COIL_RESP} -ge 10 ]]; then
    echo "  [OK] Modbus RTU response: ${COIL_RESP}"
    echo "  Relay module is communicating correctly."
else
    echo "  [WARN] No Modbus response (relay may need restart or wrong port)"
fi

echo ""
echo "── Network Summary ────────────────────────────────────────────"
echo "  HA API:   ${HA_URL}"
echo "  Relay:    ${RELAY_IP}:${RELAY_PORT} (Waveshare 16CH, Modbus RTU/TCP)"
echo "  (Typical gateway: 192.168.50.1 on Teltonika LAN)"
echo "  MAC:      04-EE-E8-17-54-18 (device label — verify if multiple units)"
