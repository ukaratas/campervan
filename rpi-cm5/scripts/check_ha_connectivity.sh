#!/usr/bin/env bash
# Home Assistant erişim özeti: LAN vs Tailscale (VPN) hangisi çalışıyor?
#
# Kullanım (repo kökü veya scripts/):  bash scripts/check_ha_connectivity.sh
# Agent / görev başında: önce bunu çalıştır; hangi URL’nin 200 döndüğünü not et.
#
# .env: HA_URL (LAN), HA_URL_REMOTE (Tailscale), HA_TOKEN (ortak).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: $ENV_FILE yok"
  exit 1
fi
set -a
# shellcheck source=/dev/null
source "$ENV_FILE"
set +a

api_ping() {
  local base="$1"
  local label="$2"
  local code
  code=$(curl -sS -o /tmp/ha_ping_$$.json -w "%{http_code}" \
    -H "Authorization: Bearer ${HA_TOKEN}" \
    -H "Content-Type: application/json" \
    "${base%/}/api/config" 2>/dev/null || echo "000")
  rm -f /tmp/ha_ping_$$.json
  echo "$code"
}

route_iface() {
  local ip="$1"
  if command -v route >/dev/null 2>&1; then
    route get "$ip" 2>/dev/null | awk -F': ' '/interface:/{print $2; exit}'
  fi
}

echo "=== HA bağlantı kontrolü ==="
echo ""

LAN_CODE=$(api_ping "$HA_URL" "LAN")
REM_CODE=""
if [[ -n "${HA_URL_REMOTE:-}" ]]; then
  REM_CODE=$(api_ping "$HA_URL_REMOTE" "Tailscale")
fi

echo "  HA_URL (LAN):     ${HA_URL}"
echo "  HTTP:             ${LAN_CODE} $( [[ "$LAN_CODE" == "200" ]] && echo OK || echo FAIL )"

if [[ -n "${HA_URL_REMOTE:-}" ]]; then
  echo "  HA_URL_REMOTE:    ${HA_URL_REMOTE}"
  echo "  HTTP:             ${REM_CODE} $( [[ "$REM_CODE" == "200" ]] && echo OK || echo FAIL )"
fi

echo ""
echo "=== Yönlendirme (bu makine) ==="
HA_LAN_IP="${HA_URL#http://}"
HA_LAN_IP="${HA_LAN_IP%%:*}"
HA_REM_IP=""
if [[ -n "${HA_URL_REMOTE:-}" ]]; then
  HA_REM_IP="${HA_URL_REMOTE#http://}"
  HA_REM_IP="${HA_REM_IP%%:*}"
fi

if [[ -n "$HA_LAN_IP" ]]; then
  IF_LAN=$(route_iface "$HA_LAN_IP" || true)
  echo "  ${HA_LAN_IP} → interface: ${IF_LAN:-unknown} (LAN genelde en0 / bridge; aynı subnet ise doğrudan)"
fi
if [[ -n "${HA_REM_IP:-}" ]]; then
  IF_REM=$(route_iface "$HA_REM_IP" || true)
  echo "  ${HA_REM_IP} → interface: ${IF_REM:-unknown} (Tailscale genelde utun*)"
fi

echo ""
echo "=== Özet ==="
if [[ "$LAN_CODE" == "200" && "$REM_CODE" == "200" ]]; then
  echo "  İkisi de erişilebilir. Şu an hangisini kullandığın tarayıcı / script URL’sine bağlı."
elif [[ "$LAN_CODE" == "200" ]]; then
  echo "  Aktif senaryo: muhtemelen **aynı LAN** (Tailscale kapalı veya uzak IP route yok)."
elif [[ "$REM_CODE" == "200" ]]; then
  echo "  Aktif senaryo: muhtemelen **Tailscale / uzaktan** (LAN IP’ye route yok)."
else
  echo "  UYARI: Ne LAN ne remote API yanıt vermedi; token veya ağı kontrol et."
fi
echo ""
echo "  Scriptler varsayılan olarak HA_URL kullanır (ha_helpers.sh). Uzaktan çalıştırmak için:"
echo "    export HA_URL=\"\$HA_URL_REMOTE\""
echo "  veya geçici:  HA_URL=\$HA_URL_REMOTE bash scripts/setup/setup_network.sh"
