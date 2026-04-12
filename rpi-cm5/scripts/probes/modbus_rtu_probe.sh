#!/bin/sh
# Ham Modbus RTU testi — Waveshare Modbus RTU Relay (E), slave 1, 9600 8N1
# Kullanım: sh modbus_rtu_probe.sh [/dev/ttyACM0]
# USB-RS485 takılı ve relay güçlü olmalı; HA'da rs485_bus yok (port kilidi yok).

set -eu

PORT="${1:-}"
if [ -z "$PORT" ]; then
  if [ -d /dev/serial/by-id ]; then
    PORT=$(ls /dev/serial/by-id/usb-* 2>/dev/null | head -1 || true)
  fi
fi
if [ -z "$PORT" ] || [ ! -e "$PORT" ]; then
  PORT=/dev/ttyACM0
fi

if [ ! -e "$PORT" ]; then
  echo "HATA: Seri port yok. USB-RS485 tak."
  exit 1
fi

echo "Port: $PORT"

stty -F "$PORT" 9600 cs8 -cstopb -parenb raw -echo min 0 time 2 2>/dev/null || {
  echo "HATA: stty (port kullanımda?)"
  exit 1
}

dd if="$PORT" bs=1 count=256 iflag=nonblock 2>/dev/null || true

read_response() {
  # 1 sn içinde en fazla 64 byte
  timeout 1 dd if="$PORT" bs=1 count=64 2>/dev/null | od -An -tx1 | tr -s '\n' ' ' | sed 's/^ *//;s/ *$//'
}

echo ""
echo "=== 1) Read coils FC01 ==="
printf '\x01\x01\x00\x00\x00\x08\x3D\xCC' > "$PORT"
sleep 0.08
echo "Yanıt: $(read_response)"

echo ""
echo "=== 2) Write coil 0 ON FC05 (tıklama beklenir) ==="
printf '\x01\x05\x00\x00\xFF\x00\x8C\x3A' > "$PORT"
sleep 0.08
echo "Yanıt: $(read_response)"

echo ""
echo "=== 3) Read coils tekrar ==="
printf '\x01\x01\x00\x00\x00\x08\x3D\xCC' > "$PORT"
sleep 0.08
echo "Yanıt: $(read_response)"

echo ""
echo "=== 4) Write coil 0 OFF ==="
printf '\x01\x05\x00\x00\x00\x00\xCD\xCA' > "$PORT"
sleep 0.08
echo "Yanıt: $(read_response)"

echo ""
echo "Tamam."
