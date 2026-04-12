#!/usr/bin/env bash
# Uyumluluk: gerçek betik scripts/deploy/sync_ha_config.sh
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/deploy/sync_ha_config.sh" "$@"
