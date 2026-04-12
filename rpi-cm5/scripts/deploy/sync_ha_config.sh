#!/usr/bin/env bash
# Deploy rpi-cm5/homeassistant/* → HA /config/; yedek; eksik secret anahtarları; ha core check + restart.
#
# Kullanım: ./sync_ha_config.sh   [--dry-run]   [--no-restart]

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
source "$(cd "$SCRIPT_DIR/.." && pwd)/ha_helpers.sh"

DRY_RUN=false
NO_RESTART=false
for a in "$@"; do
  case "$a" in
    --dry-run) DRY_RUN=true ;;
    --no-restart) NO_RESTART=true ;;
  esac
done

require_sshpass
ha_check_connection

SRC="$ROOT/homeassistant"
if [[ ! -f "$SRC/configuration.yaml" ]]; then
  echo "ERROR: $SRC/configuration.yaml yok"
  exit 1
fi

echo "=== Yedek: /config/backups/ ==="
if ! $DRY_RUN; then
  ssh_ha "mkdir -p /config/backups && for f in configuration.yaml secrets.yaml; do
    [[ -f /config/\$f ]] && cp /config/\$f /config/backups/\${f}.\$(date +%Y%m%d-%H%M%S) || true
  done"
fi

echo "=== homeassistant/ → /config/ (tar — HAOS’ta uzak rsync olmayabilir) ==="
if $DRY_RUN; then
  echo "  [dry-run] dosya listesi:"
  (cd "$SRC" && find . -name .git -prune -o -print) | head -50
else
  (cd "$SRC" && tar --exclude=".git" --exclude="secrets.yaml" \
    --exclude="._*" --exclude=".DS_Store" -cf - .) | sshpass -p "${SSH_PASS}" ssh \
    -o StrictHostKeyChecking=no -o PreferredAuthentications=password \
    "root@${HA_HOST}" "cd /config && tar xf -"
fi

# Eski yapı: modbus/rs485/ artık kullanılmıyor; merge_list yanlışlıkla hub olarak okur
if ! $DRY_RUN; then
  ssh_ha "rm -rf /config/modbus/rs485 /config/automations 2>/dev/null || true"
fi

if ! $DRY_RUN; then
  echo "=== secrets.yaml birleştirme (example’daki eksik anahtarlar eklenir) ==="
  sshpass -p "${SSH_PASS}" ssh -o PreferredAuthentications=password "root@${HA_HOST}" bash -s << 'REMOTE'
set -e
if [[ ! -f /config/secrets.yaml ]]; then
  if [[ -f /config/secrets.yaml.example ]]; then
    cp /config/secrets.yaml.example /config/secrets.yaml
    echo "  [OK] secrets.yaml oluşturuldu (example'dan)."
  else
    echo "  [WARN] secrets.yaml ve example yok."
  fi
else
  if [[ -f /config/secrets.yaml.example ]]; then
    tmp=$(mktemp)
    cp /config/secrets.yaml "$tmp"
    while IFS= read -r line || [[ -n "$line" ]]; do
      [[ -z "${line// }" ]] && continue
      [[ "$line" =~ ^[[:space:]]*# ]] && continue
      key="${line%%:*}"
      key="${key##+([[:space:]])}"
      key="${key%%+([[:space:]])}"
      [[ -z "$key" ]] && continue
      if ! grep -qE "^[[:space:]]*${key}:" "$tmp"; then
        echo "$line" >> "$tmp"
        echo "  [+] secret eklendi: $key"
      fi
    done < /config/secrets.yaml.example
    mv "$tmp" /config/secrets.yaml
  fi
fi
REMOTE

  echo ""
  echo "=== ha core check ==="
  if ! ssh_ha "ha core check"; then
    echo "[ERROR] ha core check başarısız — yedekler /config/backups/"
    exit 1
  fi

  if $NO_RESTART; then
    echo "=== [SKIP] restart (--no-restart) ==="
  else
    echo "=== ha core restart ==="
    ssh_ha "ha core restart" || true
    echo "  [OK] restart gönderildi."
  fi
fi
