# Modbus TCP Simülatörler

Bu dizin, karavan otomasyon projesi için Modbus TCP simülatörlerini içerir.

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# veya
venv\Scripts\activate  # Windows

# Bağımlılıkları kur
pip install -r requirements.txt
```

### 2. Simülatörleri Çalıştır

Her simülatör ayrı terminalde çalıştırılmalı:

```bash
# Terminal 1 - DI/DO Module
python3 di-do/server.py

# Terminal 2 - Low Latching Relay (Lighting)
python3 relay-low/server.py

# Terminal 3 - Analog Module (Water Tanks)
python3 analog/server.py
```

## 📡 Port Listesi

| Simülatör | Port | Açıklama |
|-----------|------|----------|
| DI/DO Module | 5022 | Push buttons + Bistable relay trigger |
| Low Latching Relay | 5023 | Aydınlatma kontrol |
| Analog Module | 5024 | Su tank sensörleri |
| High Current Relay | 5021 | Yüksek güç röleleri (TODO) |
| RGB Dimmer | 5025 | Ambiyans aydınlatma (TODO) |
| Victron EasySolar-II | 5030 | Enerji yönetimi (TODO) |

## 🏠 Home Assistant Konfigürasyonu

Home Assistant `configuration.yaml` dosyasına ekle:

```yaml
modbus:
  - name: "DI_DO_Module"
    type: tcp
    host: <HOME_ASSISTANT_HOST_IP>  # UTM'de HA IP adresi
    port: 5022
    
    binary_sensors:
      - name: "Sağ Yatak Button"
        slave: 1
        address: 0
        input_type: discrete_input
      
      - name: "Sol Yatak Button"
        slave: 1
        address: 1
        input_type: discrete_input
    
    switches:
      - name: "Buzdolabı"
        slave: 1
        address: 0
        write_type: coil
      
      - name: "24V Klima"
        slave: 1
        address: 2
        write_type: coil

  - name: "Lighting"
    type: tcp
    host: <HOME_ASSISTANT_HOST_IP>
    port: 5023
    
    lights:
      - name: "Mutfak Işık"
        slave: 1
        address: 0
        write_type: coil
      
      - name: "Yatak Alanı Işık"
        slave: 1
        address: 3
        write_type: coil

  - name: "WaterTanks"
    type: tcp
    host: <HOME_ASSISTANT_HOST_IP>
    port: 5024
    
    sensors:
      - name: "Temiz Su Seviyesi"
        slave: 1
        address: 0
        input_type: input
        data_type: uint16
        scale: 0.1
        precision: 1
        unit_of_measurement: "%"
      
      - name: "Temiz Su Hacim"
        slave: 1
        address: 100
        input_type: input
        data_type: uint16
        unit_of_measurement: "L"
```

## 🧪 Test Senaryoları

### Test 1: Push Button → Light Control

```yaml
# automations.yaml
- alias: "Test - Sağ Yatak Button Mutfak Işık"
  trigger:
    - platform: state
      entity_id: binary_sensor.sag_yatak_button
      to: 'on'
  action:
    - service: light.toggle
      target:
        entity_id: light.mutfak_isik
```

### Test 2: Su Seviyesi Uyarısı

```yaml
- alias: "Test - Düşük Su Uyarısı"
  trigger:
    - platform: numeric_state
      entity_id: sensor.temiz_su_seviyesi
      below: 20
  action:
    - service: notify.persistent_notification
      data:
        message: "Temiz su seviyesi %20'nin altında!"
```

## 🛠️ Simülatör Özellikleri

### DI/DO Module
- **8 Digital Input:** Push button simülasyonu
- **8 Digital Output:** Bistable relay tetikleme
- **İnteraktif:** Python console'dan `simulator.simulate_button_press(0)` komutu ile button press simüle edilebilir

### Low Latching Relay
- **8 Röle:** Aydınlatma kontrol
- **Güç İzleme:** Her LED'in güç tüketimi simüle edilir
- **Toplam Güç:** Register 100'de toplam güç tüketimi

### Analog Module
- **Su Seviye Sensörleri:** Temiz ve gri su tankları
- **Dinamik Simülasyon:** Su seviyeleri otomatik değişir
- **İnteraktif Komutlar:**
  - `simulator.refill_fresh_water()` - Temiz su doldur
  - `simulator.drain_grey_water()` - Gri su boşalt

## 📊 Dashboard Örneği

Home Assistant Lovelace dashboard için örnek kartlar:

```yaml
# Dashboard Card - Water Tanks
type: entities
title: Su Tankları
entities:
  - entity: sensor.temiz_su_seviyesi
    name: Temiz Su
    icon: mdi:water
  - entity: sensor.temiz_su_hacim
    name: Temiz Su Hacim
  - entity: sensor.gri_su_seviyesi
    name: Gri Su
    icon: mdi:water-off
  - entity: sensor.gri_su_hacim
    name: Gri Su Hacim

# Dashboard Card - Lighting Control
type: entities
title: Aydınlatma
entities:
  - entity: light.mutfak_isik
  - entity: light.yatak_alani_isik
  - entity: light.orta_alan_isik
  - entity: light.sol_okuma_isik
  - entity: light.sag_okuma_isik

# Dashboard Card - Push Buttons
type: entities
title: Push Buttons
entities:
  - entity: binary_sensor.sag_yatak_button
    name: Sağ Yatak
  - entity: binary_sensor.sol_yatak_button
    name: Sol Yatak
  - entity: binary_sensor.mutfak_button
    name: Mutfak
```

## 🔧 Troubleshooting

### Port zaten kullanımda
```bash
# Port'u kullanan process'i bul
lsof -i :5022

# Process'i sonlandır
kill -9 <PID>
```

### Home Assistant bağlanamıyor
1. UTM network ayarlarını kontrol et (bridge mode)
2. Mac'in firewall'ını kontrol et
3. Simülatör log'larını kontrol et

### Modbus hataları
```bash
# Home Assistant loglarını kontrol et
tail -f /config/home-assistant.log | grep modbus
```

## 📚 Ek Kaynaklar

- [Modbus Simulation Plan](modbus-simulation-plan.md) - Detaylı register map
- [Automation readme](../Automation/readme.md) - Tüm otomasyon senaryoları
- [Pymodbus Documentation](https://pymodbus.readthedocs.io/)

