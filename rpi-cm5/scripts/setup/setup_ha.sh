#!/usr/bin/env bash
# Master HA setup script - run this to configure everything from scratch.
# Idempotent - safe to run multiple times.
#
# Order matters:
#   1. SSH   - enables direct host access for subsequent steps
#   2. Network - LAN connectivity + Ethernet relay (Modbus) checks
#   3. System Monitor - host metrics (CPU, RAM, temp, disk)
#   4. MQTT  - Mosquitto broker (requires SSH for addon install)
#   5. Sensors - MQTT sensors/actuators (tanks, macerator, RPi stats)
#   6. Relay  - Waveshare 16CH relay switches + test bench dashboard
#   7. Areas  - Bedroom, Bathroom, Kitchen, Saloon, Utility (WebSocket API)
#
# Prerequisites:
#   - Home Assistant running at HA_URL (see ../.env)
#   - Long-Lived Access Token in HA_TOKEN
#   - python3, mosquitto (brew install mosquitto). SSH key tabanlı; sshpass opsiyonel.
#
# Usage: ./setup_ha.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../ha_helpers.sh"

echo "============================================"
echo "  CamperVNext - Home Assistant Setup"
echo "============================================"
echo ""
ha_check_connection
echo ""

# ── 1. SSH (foundation for everything else) ──────────────────────
echo "--------------------------------------------"
echo "  1/7  SSH (Terminal & SSH addon)"
echo "--------------------------------------------"
bash "$SCRIPT_DIR/setup_ssh.sh"
echo ""

# ── 2. Network (control bus) ────────────────────────────────────
echo "--------------------------------------------"
echo "  2/7  Network (LAN + relay)"
echo "--------------------------------------------"
bash "$SCRIPT_DIR/setup_network.sh"
echo ""

# ── 3. System Monitor ───────────────────────────────────────────
echo "--------------------------------------------"
echo "  3/7  System Monitor"
echo "--------------------------------------------"
bash "$SCRIPT_DIR/setup_system_monitor.sh"
echo ""

# ── 4. MQTT ──────────────────────────────────────────────────────
echo "--------------------------------------------"
echo "  4/7  MQTT (Mosquitto Broker)"
echo "--------------------------------------------"
bash "$SCRIPT_DIR/setup_mqtt.sh"
echo ""

# ── 5. MQTT Sensors ──────────────────────────────────────────────
echo "--------------------------------------------"
echo "  5/7  MQTT Sensors (Tanks + System)"
echo "--------------------------------------------"
bash "$SCRIPT_DIR/setup_sensors.sh"
echo ""

# ── 6. Relay Switches ───────────────────────────────────────────
echo "--------------------------------------------"
echo "  6/7  Relay Switches (Waveshare 16CH)"
echo "--------------------------------------------"
bash "$SCRIPT_DIR/setup_relay.sh"
echo ""

# ── 7. Areas (rooms) ────────────────────────────────────────────
echo "--------------------------------------------"
echo "  7/7  Areas (Bedroom, Bathroom, Kitchen, Saloon, Utility)"
echo "--------------------------------------------"
python3 "$SCRIPT_DIR/setup_areas.py"
echo ""

# ── Summary ──────────────────────────────────────────────────────
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "  SSH:      ssh root@${HA_HOST}"
echo "  MQTT:     ${HA_HOST}:${MQTT_PORT:-1883} (user: ${MQTT_USER:-campervan})"
echo "  Relay:    ${RELAY_IP:-192.168.50.20}:${RELAY_PORT:-4196} (Modbus RTU/TCP)"
echo "  HA UI:    ${HA_URL}"
echo "  Sensors:  3 tank + 2 system + 1 switch"
echo ""
echo "  Re-run this script anytime to verify/repair."
