#!/usr/bin/env bash
# Waveshare Modbus + Admin Bench Lovelace.
# Modbus tanımı: repodaki homeassistant/ + sync_ha_config.sh (önerilen).
# Eski davranış: LEGACY_HA_RELAY_APPEND=1 ile configuration.yaml sonuna blok ekler.
#
# CH1 = Macerator pump (grey water)
# CH2-CH16 = Generic relay channels
#
# Requires: sshpass, SSH addon running
# Usage: ./setup_relay.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../ha_helpers.sh"

RELAY_IP="${RELAY_IP:-10.0.0.200}"
RELAY_PORT="${RELAY_PORT:-4196}"

require_sshpass
ha_check_connection

echo "=== Relay Setup (Waveshare 16CH - Native Modbus) ==="
echo ""

# ── Step 1: Modbus (önerilen: modüler repo → sync_ha_config.sh) ─────────
echo "Step 1: Modbus integration"

if ssh_ha "grep -q 'include_dir_merge_list modbus' /config/configuration.yaml 2>/dev/null"; then
    echo "  [SKIP] Modüler modbus (include_dir_merge_list) zaten /config/configuration.yaml içinde"
elif ssh_ha "grep -q 'waveshare_ws01' /config/configuration.yaml 2>/dev/null"; then
    echo "  [SKIP] waveshare_ws01 zaten configuration.yaml içinde (tek parça yapı)"
elif [[ "${LEGACY_HA_RELAY_APPEND:-}" == "1" ]]; then
    MODBUS_MARKER="# >>> waveshare_ws01 modbus <<<"
    SWITCH_YAML=""
    SWITCH_YAML+="
      - name: \"CH1 — Macerator pump\"
        unique_id: modbus_ws01_ch1
        address: 0
        slave: 1
        write_type: coil
        scan_interval: 5"
    for i in $(seq 2 16); do
        SWITCH_YAML+="
      - name: \"CH${i}\"
        unique_id: modbus_ws01_ch${i}
        address: $((i - 1))
        slave: 1
        write_type: coil
        scan_interval: 5"
    done
    ssh_ha "cat >> /config/configuration.yaml << MODBUS_EOF

${MODBUS_MARKER}
modbus:
  - name: waveshare_ws01
    type: rtuovertcp
    host: ${RELAY_IP}
    port: ${RELAY_PORT}
    retry_on_empty: true
    retries: 3
    switches:${SWITCH_YAML}
MODBUS_EOF"
    echo "  [OK] Modbus (legacy append) yazıldı"
    echo "  Validating..."
    ssh_ha "ha core check" 2>/dev/null || true
    echo "  Restarting HA core..."
    ssh_ha "ha core restart" 2>/dev/null || true
    echo "  Waiting for HA..."
    for attempt in $(seq 1 12); do
        sleep 5
        code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/" 2>/dev/null || echo "000")
        if [[ "$code" == "200" ]]; then
            echo "  [OK] HA ready"
            break
        fi
    done
else
    echo "  [INFO] Modbus henüz yok. Önerilen: repodan modüler yapıyı gönderin:"
    echo "         bash $SCRIPT_DIR/../deploy/sync_ha_config.sh"
    echo "  Eski davranış (tek dosyaya append): LEGACY_HA_RELAY_APPEND=1 $0"
fi

# Verify Modbus entities exist
echo ""
echo "Step 2: Verify Modbus switch entities"
ENTITY_COUNT=$(curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states" | \
    python3 -c "import json,sys; print(sum(1 for s in json.load(sys.stdin) if s['entity_id'].startswith('switch.ch') and 'modbus' not in s['entity_id']))")

if [[ "$ENTITY_COUNT" -ge 16 ]]; then
    echo "  [OK] $ENTITY_COUNT Modbus switch entities found"
else
    echo "  [WARN] Only $ENTITY_COUNT entities found (expected 16)"
    echo "  Check HA logs for Modbus errors"
fi

# ── Step 3: Create Relay Test Bench dashboard ─────────────────
echo ""
echo "Step 3: Create 'Admin Bench' dashboard (WS-Relay-01 + WS-Relay-02 tabs)"

ensure_websockets

python3 "$SCRIPT_DIR/../lovelace/lovelace_push_admin_bench.py"

echo ""
echo "=== Relay Setup Complete ==="
echo ""
echo "  Integration: HA native Modbus (rtuovertcp)"
echo "  Dashboard:   ${HA_URL}/admin-bench/ws-relay-01  (Ethernet 16CH)"
echo "               ${HA_URL}/admin-bench/ws-relay-02  (RS485 Relay E, 8CH)"
echo "               ${HA_URL}/admin-bench/ws-di-do-01  (RS485 IO 8CH)"
echo "               ${HA_URL}/admin-bench/ws-ai-01       (Analog 8CH)"
echo "               ${HA_URL}/admin-bench/rpi-cm5         (RPi CM5 / host metrics)"
echo "               ${HA_URL}/admin-bench/victron-bluesmart (Victron Blue Smart)"
echo "               ${HA_URL}/admin-bench/bench-status  (Check states)"
echo "  Module:      Waveshare 16CH @ ${RELAY_IP}:${RELAY_PORT}"
echo "  Entities:    switch.ch1_maserator_pompa, switch.ch2 .. switch.ch16"
echo "               switch.ws_io8_do1..do8, binary_sensor.ws_io8_di1..di8"
echo "               switch.ws_rtu_relay_ch1..ch8 (Relay E @ rs485_bus slave 2)"
echo "               sensor.ws_ai_ch1..ch8 (Analog 8CH @ rs485_bus slave 3)"
echo ""
echo "  Test: curl -X POST -H 'Authorization: Bearer ...' \\"
echo "        ${HA_URL}/api/services/switch/toggle \\"
echo "        -d '{\"entity_id\": \"switch.ch2\"}'"
