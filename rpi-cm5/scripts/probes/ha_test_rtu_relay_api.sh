#!/usr/bin/env bash
# RS485 Relay (E) — REST ile hızlı test: servis çağrısını bloklamadan ateşle, durumu GET ile izle.
# Kullanım: ./ha_test_rtu_relay_api.sh [ch1-8]
# .env içinde HA_URL ve HA_TOKEN gerekir (source ../.env veya export).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../../.env"
# shellcheck source=/dev/null
[[ -f "$ENV_FILE" ]] && set -a && source "$ENV_FILE" && set +a

CH="${1:-2}"
ENTITY="switch.ws_rtu_relay_ch${CH}"

HDR=(-H "Authorization: Bearer ${HA_TOKEN:?}" -H "Content-Type: application/json")
BASE="${HA_URL:?}/api"

poll_state() {
  curl -s --max-time 8 "${HDR[@]}" "$BASE/states/${ENTITY}" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('state','?'))" 2>/dev/null || echo "?"
}

echo "Entity: $ENTITY"
echo "1) Baseline:"
poll_state

echo "2) turn_off (3s timeout — servis arkada bitebilir)"
curl -s --max-time 3 -X POST "${HDR[@]}" "$BASE/services/switch/turn_off" -d "{\"entity_id\":\"${ENTITY}\"}" -o /dev/null -w "HTTP %{http_code}\n" || true
sleep 2
echo "   state: $(poll_state)"

echo "3) turn_on (3s timeout)"
curl -s --max-time 3 -X POST "${HDR[@]}" "$BASE/services/switch/turn_on" -d "{\"entity_id\":\"${ENTITY}\"}" -o /dev/null -w "HTTP %{http_code}\n" || true
sleep 2
echo "   state: $(poll_state)"

echo "4) 15s boyunca 3s aralıkla okuma (gerçek coil senkronu için verify beklenir)"
for _ in 1 2 3 4 5; do
  echo "   $(date +%T) -> $(poll_state)"
  sleep 3
done

echo "Done."
