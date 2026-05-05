# RPi CM5 - Home Assistant Production Setup

Raspberry Pi Compute Module 5 (veya mevcut HA donanımı) üzerinde çalışan Home Assistant kurulumu. **IP ve Modbus uçları** için kaynak: `.env` ve HA `/config/secrets.yaml` (`secrets.yaml.example`).

**Teltonika LAN (örnek production):**

- **Subnet:** `192.168.50.0/24` (gateway çoğu kurulumda `192.168.50.1`)
- **Home Assistant:** `192.168.50.10` — örnek: `http://192.168.50.10:8123`
- **Waveshare 16CH PoE Ethernet relay (Modbus):** `192.168.50.20:4196` (RTU over TCP, Unit ID 1)

Eski mimarideki ayrı kontrol bus (`10.0.0.x` / ikinci Ethernet) bu repoda **hedeflenmiyor**; MQTT, Modbus TCP ve HA aynı LAN içindedir.

- **HA Version**: ör. `2026.4.x` — `GET /api/config` ile doğrulayın
- **OS**: Home Assistant OS (Supervisor)

## UI language (Admin vs user)

- **English:** Admin Bench (developer/test Lovelace), Settings-driven **friendly names** in `configuration.yaml` (helpers, Modbus labels used from the bench), and related automation titles — keep these consistent in **English** so hardware/debugging stays one language.
- **Turkish:** End-user dashboards (e.g. **Tanks** / `tank-levels`) and on-screen copy meant for daily use stay in **Turkish**.
- **Note:** Some template entities may keep an older `entity_id` in the registry (e.g. `sensor.clean_water_mod_metin`) even after English **friendly names** in YAML; Lovelace references use the stable IDs.

## Areas (rooms)

Karavan alanları Home Assistant **Areas** olarak tanımlanır (cihazları odaya atamak için). Script idempotent — eksik olanları oluşturur:

| Area | Icon (MDI) |
|------|----------------|
| Bedroom | `mdi:bed` |
| Bathroom | `mdi:shower` |
| Kitchen | `mdi:stove` |
| Saloon | `mdi:sofa-outline` |
| Utility | `mdi:wrench-outline` |

```bash
python3 scripts/setup/setup_areas.py
```

Varsayılan **Living Room** gibi alanları kaldırmak için:

```bash
python3 scripts/tools/cleanup_areas.py
```

**Not:** Ana ekrandaki **Devices** kutusu çoğu kurulumda bir *area* değil; HA’nın cihaz / keşif kısayolu olabilir. Alan listesinde görünmüyorsa `config/area_registry` ile silinmez — dashboard düzeninden kaldırılır.

## Hızlı Başlangıç

```bash
# Bağımlılıklar (sshpass artık opsiyonel — SSH key-based; sadece password fallback için gerek)
brew install mosquitto
pip3 install websockets

# .env dosyasını oluştur
cp .env.example .env
nano .env   # Token ve şifreleri düzenle

# Sıfırdan her şeyi kur (SSH → System Monitor → MQTT)
cd scripts/setup && bash setup_ha.sh
```

## Kurulum Sırası

| # | Script | Ne yapar | Bağımlılık |
|---|--------|----------|------------|
| 1 | `setup/setup_ssh.sh` | Terminal & SSH addon (port 22) | WebSocket API |
| 2 | `setup/setup_network.sh` | LAN + Ethernet relay doğrulama (ping / TCP / Modbus) | SSH (step 1) |
| 3 | `setup/setup_system_monitor.sh` | CPU, RAM, disk, sıcaklık sensörleri | REST API |
| 4 | `setup/setup_mqtt.sh` | Mosquitto broker + MQTT integration | SSH (step 1) |
| 5 | `setup/setup_sensors.sh` | Tank + sistem MQTT sensörleri | MQTT (step 4) |
| 6 | `setup/setup_relay.sh` | Modbus doğrulama + Admin Bench Lovelace (önce `deploy/sync_ha_config.sh` önerilir) | SSH (step 1), Network (step 2) |
| — | `deploy/sync_ha_config.sh` (veya `sync_ha_config.sh`) | Repodaki `homeassistant/` → HA `/config/` | SSH, `.env` |
| — | `deploy/sync_esphome.sh` | Repodaki `esphome/` → HA `/config/esphome/` + opsiyonel build / OTA upload | SSH, `.env`, ESPHome add-on |
| 7 | `setup/setup_areas.py` | Alanlar: Bedroom, Bathroom, Kitchen, Saloon, Utility | WebSocket API |

`setup_ha.sh` hepsini sırayla çalıştırır. Her script idempotent - tekrar çalıştırmak güvenli.

## Modüler Home Assistant YAML (`homeassistant/`)

HA tarafında **tek dev `configuration.yaml` yerine** `!include` / `!include_dir_merge_list` ile parçalanmış kaynak bu dizindedir. **Taşınabilir “alias”:** seri port, Ethernet relay IP ve Modbus **slave** numaraları `secrets.yaml` içinde tutulur (`secrets.yaml.example` → `/config/secrets.yaml` kopyalayın).

| Ne | Nerede |
|----|--------|
| Kök `configuration.yaml` | `homeassistant/configuration.yaml` |
| Modbus hub’ları (Ethernet 16CH + `rs485_bus`) | `homeassistant/modbus/*.yaml` |
| RS485 üzerindeki cihazlar (IO8, Relay E, Analog) | `homeassistant/rs485_bus_devices/{switches,binary_sensors,sensors}/` ( `modbus/` merge ile karışmaması için ayrı klasör ) |
| Analog mod seçiciler + tank / Victron şablonları | `homeassistant/input_select/`, `homeassistant/templates/` |
| Otomasyon (ör. analog holding yazımı) | `homeassistant/automations.yaml` |

**Dağıtım:** `scripts/deploy/sync_ha_config.sh` (kısayol: `scripts/sync_ha_config.sh`) repodaki `homeassistant/` ağacını HA `/config/` ile **eşitler**; `/config/backups/` altında yedek alır; `secrets.yaml` üzerine yazmaz, eksik anahtarları `secrets.yaml.example` ile birleştirir; ardından `ha core check` ve `ha core restart` çalıştırır (`--no-restart` ile atlanabilir).

**Kurulum sırası:** İlk Modbus kurulumundan önce bir kez `sync_ha_config.sh` çalıştırın; `setup/setup_relay.sh` modüler `include_dir_merge_list modbus` görürse tekrar YAML yapıştırmaz, yalnızca Admin Bench Lovelace’i günceller.

**Analog mod otomasyonları (input_select → Modbus holding):** HA **2026.4.1** sürümünde `ha core check`, YAML’da `state` tetikleyicili otomasyonları doğrularken bazı kurulumlarda iç hata verebiliyor. Bu yüzden `homeassistant/automations.yaml` şu an **boş liste** (`[]`); Modbus hatı ve sensörler yine yüklenir. Otomasyonları **Ayarlar → Otomasyonlar** üzerinden oluşturun veya `homeassistant/optional/analog_modbus_automations.RESTORE.yaml` içeriğini (HA düzeltmesinden sonra) `automations.yaml` ile birleştirin.

Eski **fragment** dosyaları `scripts/legacy/` altında yönlendirme notudur; gerçek içerik `homeassistant/` altında. Ayrıntı: `scripts/README.txt`.

## ESPHome (ESP32 / ESP8266)

Karavan içi ekstra sensörler için ESPHome cihazları. Konfigürasyon `rpi-cm5/esphome/` altında, deploy + OTA upload tek script ile:

```bash
# Yalnızca YAML'ı yükle + validate et
bash scripts/deploy/sync_esphome.sh --device cv-sensors-01

# YAML yükle + compile (OTA göndermez)
bash scripts/deploy/sync_esphome.sh --device cv-sensors-01 --build

# YAML yükle + compile + OTA upload + canlı log
bash scripts/deploy/sync_esphome.sh --device cv-sensors-01 --ota
```

Script HA WebSocket API üzerinden ESPHome dashboard'un internal `/run` endpoint'ine bağlanır; ESPHome dashboard'u UI'dan açmaya gerek yok. Cihaz ekleme:

1. ESPHome dashboard UI'dan **+ NEW DEVICE** ile başlangıç YAML üret (api/ota anahtarları otomatik oluşur).
2. Üretilen YAML'ı `rpi-cm5/esphome/<device-name>.yaml` olarak kopyala; api/ota şifrelerini `secrets.yaml` referansına çevir (`!secret <device>_api_key` vs.).
3. Yeni anahtarları `esphome/secrets.yaml.example`'a ekle (gerçek değerler HAOS'taki `/config/esphome/secrets.yaml`'da).
4. `bash scripts/deploy/sync_esphome.sh --device <name> --ota` ile yükle.

| Cihaz | Donanım | Aktif sensörler |
|---|---|---|
| `cv-sensors-01` | ESP32 WROOM-32 (rev 3.x) | WiFi sinyal, uptime, internal temp, free heap, IP/MAC/SSID, restart butonları |

## Klasör Yapısı

```
rpi-cm5/
├── .env                              # HA_URL + HA_TOKEN + MQTT + SSH creds (gitignore)
├── .env.example                      # Örnek env dosyası
├── .gitignore
├── README.md
├── homeassistant/                  # Modüler HA YAML (sync_ha_config.sh → /config/)
│   ├── configuration.yaml
│   ├── secrets.yaml.example
│   ├── modbus/
│   ├── rs485_bus_devices/
│   ├── input_select/
│   ├── templates/
│   └── automations.yaml
├── esphome/                        # ESPHome cihaz YAML'ları (sync_esphome.sh → /config/esphome/)
│   ├── cv-sensors-01.yaml         # ESP32 WROOM-32 — diagnostic + (lehim sonrası) sensörler
│   └── secrets.yaml.example
└── scripts/
    ├── README.txt                    # Klasör düzeni özeti
    ├── ha_helpers.sh                 # REST, WebSocket, SSH
    ├── repo_paths.py                 # Repo kökü (Python araçları)
    ├── sync_ha_config.sh             # → deploy/sync_ha_config.sh
    ├── deploy/
    │   └── sync_ha_config.sh         # homeassistant/ → HA /config/
    ├── setup/
    │   ├── setup_ha.sh               # Ana kurulum zinciri
    │   ├── setup_ssh.sh … setup_relay.sh
    │   ├── provision_analog_ai8ch.sh
    │   └── setup_areas.py
    ├── lovelace/
    │   └── lovelace_push_*.py
    ├── tools/
    │   ├── ha_enable_entities.py, ha_remove_entity_registry.py
    │   └── insert_victron_gauge_templates.py, cleanup_areas.py, …
    ├── probes/
    │   └── modbus_rtu_probe.sh, ha_test_rtu_relay_api.sh
    └── legacy/
        └── *.fragment.yaml (deprecated)
```

## Mimari

```
  Teltonika LAN (örn. 192.168.50.0/24)
        │
        ├── Gateway 192.168.50.1
        ├── Home Assistant (192.168.50.10) ←── Mosquitto (MQTT :1883)
        ├── Waveshare 16CH relay (192.168.50.20:4196) ── HA Modbus (rtuovertcp)
        │
        └── RS485 cihazlar (analog input, IO, Relay E) ── HA Modbus ─┐
                                                                      ├──→ HA
        Victron EasySolar GX / BLE / M5Dial (MQTT) ───────────────────┘
```

## Network Topolojisi

| Bileşen | Örnek adres | Not |
|---------|-------------|-----|
| Router (Teltonika) | `192.168.50.1` | LAN gateway |
| Home Assistant | `192.168.50.10` | `.env` → `HA_URL` |
| Waveshare 16CH Ethernet relay | `192.168.50.20:4196` | Modbus RTU over TCP; `secrets.yaml` → `waveshare_ws01_*` |

HAOS arayüz isimleri (`wlan0`, `end0`, …) System Monitor’da görülebilir; **tek LAN** kurulumunda asıl adresler yukarıdaki rezervasyonlarla uyumlu olmalıdır.

## RS485 USB hattı — Master / Slave ve devreye alma sırası

Bu projede **USB–RS485 adaptörü** CM5’e takılıdır; Home Assistant **Modbus RTU** ile hattaki cihazlara konuşur.

### Kim master, kim slave?

| Rol | Cihaz | Not |
|-----|--------|-----|
| **Master (tek)** | HA’nın kullandığı **USB–RS485** (RPi üzerinde bir seri port) | Modbus’ta bus üzerinde **yalnızca bir master** olur. |
| **Slave** | [Waveshare Modbus RTU IO 8CH](https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH) (DI/DO) | DIP ile adres (genelde 1). |
| **Slave** | [Waveshare Modbus RTU Relay (E)](https://www.waveshare.com/wiki/Modbus_RTU_Relay_(E)) (8CH RTU röle) | **DIP yok**; adres **yazılım** ile (holding `4x4000`, FC06). Varsayılan genelde **1** — hatta başka “1” varsa **çakışır**. |
| **Slave** | Waveshare analog input (RS485) | Modeline göre DIP veya register; dokümana bak. |

**Özet:** “Slave master ayarı” diye bir şey yok; tüm modüller **slave**, master sadece **bilgisayar tarafı**.

### Modbus adres planı (öneri)

Aynı RS485 hattında **adresler birbirinden farklı** olmalı:

| Slave ID | Cihaz | HA YAML |
|----------|--------|---------|
| **1** | IO 8CH (DI/DO) | `rs485_bus_devices/*.yaml` içinde `slave: 1` |
| **2** | Relay (E) | `slave: 2` |
| **3** | Analog input | `slave: 3` |

YAML’da **tek** `- name: rs485_bus` bloğu olmalı; coil/sensor satırları **farklı `slave`** ile aynı hub’a eklenir. İki ayrı aynı isimli hub kullanma.

### Devreye alma sırası (önerilen)

1. **Relay (E) adresini ayır** — fabrika adresi çoğu zaman **1**; IO da **1** ise ikisi aynı anda hatta **olmamalı** (çakışma). Güvenli yol: DI/DO’yu geçici **RS485’tan sök**, sadece **USB–485 ↔ Relay (E)** + besleme ile çalış; wiki’deki **Set Device Address** ile röleyi **2** yap ([Modbus_RTU_Relay_(E) — 2.3.7](https://www.waveshare.com/wiki/Modbus_RTU_Relay_(E))).
2. **DI/DO’yu hatta geri tak** — adres **1** kalsın; HA’da `slave: 1`.
3. **Analog modülü ekle** — adres **3** (veya dokümandaki prosedür); HA’da `slave: 3`.

Broadcast ile adres yazarken **aynı komuta cevap veren başka modül** kalmasın; yoksa yanlışlıkla onun adresi de değişebilir.

### Kablo ve sonlandırma

- **Daisy chain:** `485 A+` → `A+` → `A+`, `485 B-` → `B-` → `B-` (düz zincir).
- **Kısa hat** (birkaç metre altı): çoğu tezgâhta **120 Ω terminasyon gerekmez**; sorun yaşanırsa wiki gibi hat sonuna direnç denenebilir.
- **GND:** Uzun veya gürültülü ortamda ortak referans için dokümana uy.

### HA entity örnekleri (RS485)

| Tip | Örnek entity |
|-----|----------------|
| IO 8CH DO | `switch.do1_warning_light`, `do2_error_buzzer`, `ws_io8_do3` … `do8` (`name` alanından slug) |
| IO 8CH DI | `binary_sensor.di1_bed_left_reading_light`, … `di8_future_use` |
| Relay (E) | `switch.ch1_220v_outlets`, `ch2_clesana_c1`, `ch3_usb_outlets`, `ch4_air_condition`, … (slave **2**) |

**Kontrol paneli:** Lovelace **Admin Bench** → **`WS-Relay-02`** sekmesi Relay (E) için 8 kanal anahtarı gösterir (`scripts/setup/setup_relay.sh` ile güncellenir). **WS-Relay-01** = Ethernet 16CH (`waveshare_ws01`). Aynı panoda **`rpi-cm5`** (RPi / System Monitor) ve **`victron-bluesmart`** (BLE şarj) sekmeleri `scripts/lovelace/lovelace_push_admin_bench.py` içindedir; Victron entity ID’leri cihaz yeniden eşlenirse scriptteki listeyi güncelle.

Ethernet üzerindeki 16CH röle (`waveshare_ws01`) bu tabloda değildir; o **ayrı** Modbus TCP (`192.168.50.20:4196` — `.env` / `secrets.yaml`).

### RS485 kararsız / UI ile röle uyuşmuyor

- **Çok cihaz + sık poll** hattı doyurur: `message_wait_milliseconds` artır (ör. **90**), `timeout` / `retries` yükselt; DI/DO/röle **scan_interval** değerlerini gevşet.
- Modbus switch’te **`verify`** yoksa HA bazen **son komuta göre** gösterir; okuma başarısızsa yanlış görünür. Coil için `verify:` + `delay` (yazdıktan sonra okuma öncesi ms) eklemek **gerçek durumu** senkronlar.
- Uzun kabloda **A/B**, **toprak**, gerekiyorsa **terminasyon** kontrol et.

## MQTT Topic Yapısı

```
campervan/
├── tank/
│   ├── status                   # online/offline (availability)
│   ├── clean-water/
│   │   ├── level                # 0-100% (180L temiz su)
│   │   └── attributes           # {capacity_liters, sensor_type, source}
│   ├── grey-water/
│   │   ├── level                # 0-100% (100L kirli su)
│   │   └── attributes
│   └── fuel/
│       ├── level                # 0-100% (90L yakıt - CAN bus)
│       └── attributes
└── system/
    └── rpi/
        ├── status               # online/offline
        ├── temperature          # °C
        └── uptime               # hours
```

**Not:** Relay kontrol artık MQTT üzerinden değil, HA native Modbus entegrasyonu ile yapılıyor.
Relay switch entity'leri: `switch.ch1_macerator_pump`, `switch.ch2_refrigerator`, … (isimler `modbus/10_waveshare_ws01.yaml` içindeki `name` alanından slug üretilir)

## Bağlantı Bilgileri

| Servis | Adres | Kullanıcı |
|--------|-------|-----------|
| HA UI | `http://192.168.50.10:8123` (örnek) | - |
| SSH | `ssh haos-cv` — port **22** (Terminal & SSH addon) | key-based, `~/.ssh/id_ed25519_haos` |
| MQTT | `192.168.50.10:1883` | `.env` → MQTT_USER/MQTT_PASS |
| Relay Web | `http://192.168.50.20` / `https://…` (cihaz) | fabrika / cihaz şifresi |
| Relay Modbus | `192.168.50.20:4196` | Modbus RTU over TCP, Unit ID: 1 |

## Önemli Entity'ler

| Entity | Açıklama |
|--------|----------|
| `sensor.system_monitor_processor_temperature` | CPU sıcaklığı (°C) |
| `sensor.system_monitor_processor_use` | CPU kullanımı (%) |
| `sensor.system_monitor_memory_usage` | RAM kullanımı (%) |
| `sensor.system_monitor_disk_usage` | Disk kullanımı (%) |
| `sensor.system_monitor_load_1_min` | Load average (1dk) |
| `sensor.system_monitor_pwmfan_fan_speed` | Fan RPM (yalnızca bazı RPi donanımlarında oluşur; yoksa yok sayın) |
| `sensor.system_monitor_ipv4_address_wlan0` | WiFi IP adresi |
| `binary_sensor.rpi_power_status` | Güç durumu (undervoltage) |
| **MQTT Sensörler** | |
| `sensor.campervan_tank_sistemi_temiz_su_deposu` | Temiz su seviyesi (%, 180L) |
| `sensor.campervan_tank_sistemi_kirli_su_deposu` | Kirli su seviyesi (%, 100L) |
| `sensor.campervan_tank_sistemi_yakit_deposu` | Yakıt seviyesi (%, 90L) |
| `sensor.campervan_rpi_cm5_rpi_cpu_sicaklik` | RPi CPU sıcaklık via MQTT (°C) |
| `sensor.campervan_rpi_cm5_rpi_uptime` | RPi uptime via MQTT (h) |
| **Modbus Relay (native)** | |
| `switch.ch1_macerator_pump` | Macerator pump (WS-01 CH1, coil 0) |
| `switch.ch2_refrigerator` … `switch.ch16_future_use` | Diğer kanallar (coil 1–15) |
| **RS485 Relay (E)** | |
| `switch.ch1_220v_outlets` … `ch8_future_use` | USB `rs485_bus`, slave **2** |

## Donanım

| Cihaz | Bağlantı | IP / Adres | Notlar |
|-------|----------|------------|--------|
| HA host (HAOS) | Teltonika LAN | örn. `192.168.50.10` | `.env` `HA_URL` ile uyumlu |
| Waveshare Modbus POE ETH Relay 16CH | Ethernet (aynı LAN) | `192.168.50.20:4196` | 16 röle, Modbus RTU/TCP; MAC ör. `04-EE-E8-17-54-18` |
| Waveshare 8-Ch Analog Acquisition | RS485 USB hattı (daisy chain) | Modbus RTU, slave 3 (plan) | 0-20mA analog input; ETH röle üzerinden değil, aynı RS485 bus |
