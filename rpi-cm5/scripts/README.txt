rpi-cm5/scripts — düzen (özet)
===========================

ha_helpers.sh          Ortak .env yükleme, HA API, SSH (tüm betikler ../ha_helpers.sh ile yükler)

check_ha_connectivity.sh   LAN (HA_URL) vs Tailscale (HA_URL_REMOTE) API + route özeti — görev başında çalıştır

deploy/                HAOS /config senkronu
  sync_ha_config.sh    homeassistant/ → tar+ssh (rsync uzak tarafta yok), yedek, secret birleştir, check, restart

setup/                 Kurulum zinciri (setup_ha.sh)
  setup_ssh.sh … setup_relay.sh, provision_analog_ai8ch.sh, setup_areas.py

lovelace/              Lovelace push (WebSocket API)
  lovelace_push_admin_bench.py, lovelace_push_tank_levels.py

tools/                 Bakım / tek seferlik YAML patch, entity registry, Victron
  repo_paths.py        Repo kökünü bulur (homeassistant/configuration.yaml)

probes/                RTU/REST hızlı test (yerel .env: ../../.env)

legacy/                DEPRECATED fragment YAML — gerçek tanımlar ../homeassistant/

sync_ha_config.sh      → deploy/sync_ha_config.sh yönlendirmesi
