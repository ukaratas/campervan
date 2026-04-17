#!/usr/bin/env bash
# Install and configure System Monitor integration.
# Idempotent - safe to run multiple times.
#
# Usage: ./setup_system_monitor.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
source "$SCRIPT_DIR/../ha_helpers.sh"

echo "=== System Monitor Setup ==="
ha_check_connection

echo ""
echo "Step 1: Install System Monitor integration"
ha_install_integration "systemmonitor"

echo ""
echo "Step 2: Get config entry ID"
entry_id=$(ha_get_entry_id "systemmonitor")
echo "  [OK] entry_id=$entry_id"

echo ""
echo "Step 3: Configure process monitoring"
MONITORED_PROCESSES='["python3", "go2rtc"]'
ha_set_options "$entry_id" "{\"process\": $MONITORED_PROCESSES}"

echo ""
echo "Step 4: Enable all sensor entities"
python3 "$REPO_ROOT/scripts/tools/ha_enable_entities.py" systemmonitor

echo ""
echo "Step 5: Reload integration"
ha_reload_entry "$entry_id"

echo ""
echo "=== System Monitor setup complete ==="
echo ""
echo "Key sensors:"
echo "  sensor.system_monitor_processor_temperature  - CPU Temperature"
echo "  sensor.system_monitor_processor_use          - CPU Usage %"
echo "  sensor.system_monitor_memory_usage           - Memory Usage %"
echo "  sensor.system_monitor_disk_usage             - Disk Usage %"
echo "  sensor.system_monitor_load_1_min             - Load Average 1m"
echo "  sensor.system_monitor_swap_usage             - Swap Usage %"
echo "  sensor.system_monitor_ipv4_address_wlan0     - WiFi IP"
echo "  (PWM fan entity only on some boards — omit if missing)"
echo "  sensor.system_monitor_last_boot              - Last Boot Time"
