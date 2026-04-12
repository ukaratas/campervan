#!/usr/bin/env bash
# Register MQTT sensors in Home Assistant via MQTT Discovery.
# Publishes discovery configs with retain so HA picks them up on restart.
# Idempotent - safe to run multiple times (overwrites same configs).
#
# Requires: mosquitto_pub, MQTT broker running
#
# Usage: ./setup_sensors.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../ha_helpers.sh"

MQTT_USER="${MQTT_USER:-campervan}"
MQTT_PASS="${MQTT_PASS:-campervan2026}"
MQTT_HOST="${MQTT_HOST:-$HA_HOST}"
MQTT_PORT="${MQTT_PORT:-1883}"

if ! command -v mosquitto_pub &>/dev/null; then
    echo "[ERROR] mosquitto_pub required. Install: brew install mosquitto"
    exit 1
fi

mqtt_pub() {
    mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" -u "$MQTT_USER" -P "$MQTT_PASS" \
        -r -t "$1" -m "$2"
}

echo "=== MQTT Sensor Setup ==="
echo ""

# ── Tank Sensors ─────────────────────────────────────────────────
echo "Step 1: Register tank sensors"

register_tank() {
    local tank="$1" name="$2" capacity="$3" icon="$4"
    local uid="campervan_tank_${tank//-/_}"
    local uid_vol="${uid}_volume"
    local state_topic="campervan/tank/${tank}/level"
    local volume_topic="campervan/tank/${tank}/volume"
    local json_attr_topic="campervan/tank/${tank}/attributes"

    local device_block='"device": {
    "identifiers": ["campervan_tanks"],
    "name": "CamperVan Tank Sistemi",
    "manufacturer": "Waveshare",
    "model": "8-Ch Analog Acquisition (MP03375)",
    "sw_version": "1.0"
  },
  "availability": {
    "topic": "campervan/tank/status",
    "payload_available": "online",
    "payload_not_available": "offline"
  }'

    # Percentage sensor
    mqtt_pub "homeassistant/sensor/${uid}/config" "{
  \"name\": \"${name} Deposu\",
  \"unique_id\": \"${uid}\",
  \"state_topic\": \"${state_topic}\",
  \"json_attributes_topic\": \"${json_attr_topic}\",
  \"unit_of_measurement\": \"%\",
  \"state_class\": \"measurement\",
  \"icon\": \"${icon}\",
  \"suggested_display_precision\": 1,
  ${device_block}
}"
    echo "  [OK] ${name} Deposu (%) → ${state_topic}"

    # Volume sensor (litres)
    mqtt_pub "homeassistant/sensor/${uid_vol}/config" "{
  \"name\": \"${name} Hacim\",
  \"unique_id\": \"${uid_vol}\",
  \"state_topic\": \"${volume_topic}\",
  \"unit_of_measurement\": \"L\",
  \"state_class\": \"measurement\",
  \"icon\": \"${icon}\",
  \"suggested_display_precision\": 0,
  ${device_block}
}"
    echo "  [OK] ${name} Hacim (L) → ${volume_topic}"

    # Attributes
    mqtt_pub "$json_attr_topic" "{\"capacity_liters\": ${capacity}, \"sensor_type\": \"0-20mA\", \"source\": \"waveshare_analog\"}"
}

register_tank "clean-water" "Temiz Su"  180 "mdi:water"
register_tank "grey-water"  "Kirli Su"  100 "mdi:water-off"
register_tank "fuel"        "Yakıt"      90 "mdi:gas-station"

# Set tanks online
mqtt_pub "campervan/tank/status" "online"
echo "  [OK] Tank status: online"

echo ""

# ── System Sensors (RPi) ────────────────────────────────────────
echo "Step 3: Register system sensors"

# RPi CPU Temperature
mqtt_pub "homeassistant/sensor/campervan_rpi_temperature/config" "$(cat << 'EOF'
{
  "name": "RPi CPU Sıcaklık",
  "unique_id": "campervan_rpi_temperature",
  "state_topic": "campervan/system/rpi/temperature",
  "unit_of_measurement": "°C",
  "device_class": "temperature",
  "state_class": "measurement",
  "icon": "mdi:thermometer",
  "suggested_display_precision": 1,
  "device": {
    "identifiers": ["campervan_rpi"],
    "name": "CamperVan RPi CM5",
    "manufacturer": "Raspberry Pi",
    "model": "Compute Module 5"
  },
  "availability": {
    "topic": "campervan/system/rpi/status",
    "payload_available": "online",
    "payload_not_available": "offline"
  }
}
EOF
)"
echo "  [OK] RPi CPU Sıcaklık → campervan/system/rpi/temperature"

# RPi Uptime
mqtt_pub "homeassistant/sensor/campervan_rpi_uptime/config" "$(cat << 'EOF'
{
  "name": "RPi Uptime",
  "unique_id": "campervan_rpi_uptime",
  "state_topic": "campervan/system/rpi/uptime",
  "unit_of_measurement": "h",
  "device_class": "duration",
  "state_class": "measurement",
  "icon": "mdi:clock-outline",
  "suggested_display_precision": 1,
  "device": {
    "identifiers": ["campervan_rpi"],
    "name": "CamperVan RPi CM5",
    "manufacturer": "Raspberry Pi",
    "model": "Compute Module 5"
  },
  "availability": {
    "topic": "campervan/system/rpi/status",
    "payload_available": "online",
    "payload_not_available": "offline"
  }
}
EOF
)"
echo "  [OK] RPi Uptime → campervan/system/rpi/uptime"

# Set RPi online
mqtt_pub "campervan/system/rpi/status" "online"
echo "  [OK] RPi status: online"

echo ""

# ── Publish initial test values ──────────────────────────────────
echo "Step 4: Publish test values"

publish_tank_test() {
    local tank="$1" pct="$2" capacity="$3"
    local litres
    litres=$(python3 -c "print(round(${pct} * ${capacity} / 100, 1))")
    mqtt_pub "campervan/tank/${tank}/level" "$pct"
    mqtt_pub "campervan/tank/${tank}/volume" "$litres"
    echo "  [OK] ${tank}: ${pct}% = ${litres}L / ${capacity}L"
}

publish_tank_test "clean-water" "72.5" 180
publish_tank_test "grey-water"  "23.0" 100
publish_tank_test "fuel"        "85.0" 90

# Read actual RPi temp via SSH
if ssh_ha_check 2>/dev/null; then
    TEMP=$(ssh_ha "cat /sys/class/thermal/thermal_zone0/temp" 2>/dev/null || echo "0")
    TEMP_C=$(python3 -c "print(round(${TEMP}/1000, 1))")
    mqtt_pub "campervan/system/rpi/temperature" "$TEMP_C"
    echo "  [OK] RPi temperature: ${TEMP_C}°C (live)"

    UPTIME_SEC=$(ssh_ha "cat /proc/uptime 2>/dev/null || echo '0 0'" | python3 -c "
import sys
raw = sys.stdin.read().strip()
try: print(round(float(raw.split()[0])/3600, 1))
except: print('0.0')
")
    mqtt_pub "campervan/system/rpi/uptime" "$UPTIME_SEC"
    echo "  [OK] RPi uptime: ${UPTIME_SEC}h (live)"
else
    mqtt_pub "campervan/system/rpi/temperature" "55.0"
    mqtt_pub "campervan/system/rpi/uptime" "0.5"
    echo "  [OK] Test values published (SSH not available for live data)"
fi


echo ""
echo "=== Sensor Setup complete ==="
echo ""
echo "  MQTT Topics:"
echo "    campervan/tank/clean-water/level              (%, 180L)"
echo "    campervan/tank/clean-water/volume             (L)"
echo "    campervan/tank/grey-water/level               (%, 100L)"
echo "    campervan/tank/grey-water/volume              (L)"
echo "    campervan/tank/grey-water/macerator/state     (ON/OFF)"
echo "    campervan/tank/grey-water/macerator/command   (ON/OFF)"
echo "    campervan/tank/fuel/level                     (%, 90L)"
echo "    campervan/tank/fuel/volume                    (L)"
echo "    campervan/system/rpi/temperature              (°C)"
echo "    campervan/system/rpi/uptime                   (hours)"
echo ""
echo "  Test: mosquitto_pub -h ${MQTT_HOST} -u ${MQTT_USER} -P ${MQTT_PASS} -t campervan/tank/clean-water/level -m 50.0"
