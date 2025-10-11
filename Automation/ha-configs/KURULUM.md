# Home Assistant Kurulum Rehberi
## Push Button Detection & Modbus Integration

Bu rehber, Waveshare DI/DO modülü ve Latching Relay'in Home Assistant'a entegrasyonunu ve push button pattern detection'ı açıklar.

---

## 📋 Dosyalar

Bu klasörde hazırlanmış dosyalar:
- `modbus_combined.yaml` - Modbus cihaz tanımlamaları
- `helpers/` - Helper tanımlamaları (3 dosya)
  - `input_datetime.yaml` - DateTime helpers
  - `input_number.yaml` - Number helpers  
  - `input_boolean.yaml` - Boolean helpers
- `button_press_detection.yaml` - Button detection automationları
- `button_actions.yaml` - Button action automationları

---

## 🚀 Adım 1: Helpers Klasörü Oluştur ve Dosyaları Ekle

Home Assistant File Editor'den helpers klasörü oluştur ve 3 dosyayı ekle:

### 1.1. Klasör Oluştur

Home Assistant'ta File Editor ile:
- Sol menüden **📁 klasör ikonu** → **New folder**
- Klasör adı: `helpers`
- ✅ Oluştur

### 1.2. Helper Dosyalarını Kopyala

**3 dosya kopyalaman gerekiyor:**

#### a) input_datetime.yaml
- `helpers/input_datetime.yaml` dosyasını aç (bu repo'dan)
- **Tüm içeriği kopyala**
- Home Assistant File Editor'de `helpers` klasörüne gir
- **New file** → `input_datetime.yaml`
- İçeriği yapıştır ve **Save**

#### b) input_number.yaml
- `helpers/input_number.yaml` dosyasını aç
- **Tüm içeriği kopyala**
- `helpers` klasöründe **New file** → `input_number.yaml`
- İçeriği yapıştır ve **Save**

#### c) input_boolean.yaml
- `helpers/input_boolean.yaml` dosyasını aç
- **Tüm içeriği kopyala**
- `helpers` klasöründe **New file** → `input_boolean.yaml`
- İçeriği yapıştır ve **Save**

### 1.3. Configuration.yaml'a Include Ekle

`configuration.yaml` dosyasını aç ve **en üste** ekle:

```yaml
# Helpers Include
input_datetime: !include helpers/input_datetime.yaml
input_number: !include helpers/input_number.yaml
input_boolean: !include helpers/input_boolean.yaml
```

**NOT:** Zaten `input_datetime:`, `input_number:` veya `input_boolean:` başlığın varsa, onları kaldır ve yukardaki include satırlarını ekle.

✅ **24 helper otomatik oluşturulacak!** (8 buton × 3 helper)

---

## 🔌 Adım 2: Modbus Config Ekle

Home Assistant'ta `configuration.yaml` dosyasını aç (File Editor addon ile):

**Developer Tools → YAML → Edit Config Files → configuration.yaml**

### Eğer `modbus:` başlığın YOKSA:

`modbus_combined.yaml` dosyasının içeriğini TAMAMEN kopyala ve `configuration.yaml`'ın sonuna yapıştır.

### Eğer `modbus:` başlığın VARSA:

Sadece cihaz tanımlamalarını ekle:

```yaml
modbus:
  # Mevcut cihazların...
  
  # YENİ: Latching Relay
  - name: "Aydinlatma_Kontrol"
    type: tcp
    host: ugurs-macbook-m4-pro.local
    port: 5023
    lights:
      - name: "Mutfak Işık"
        slave: 1
        address: 0
        write_type: coil
        scan_interval: 1
      # ... diğer ışıklar
  
  # YENİ: DI/DO Module
  - name: "DI_DO_Kontrol"
    type: tcp
    host: ugurs-macbook-m4-pro.local
    port: 5024
    binary_sensors:
      - name: "Sağ Yatak Butonu"
        slave: 1
        address: 0
        input_type: discrete_input
        scan_interval: 1
      # ... diğer butonlar
    switches:
      - name: "Alarm Siren"
        slave: 1
        address: 0
        write_type: coil
        scan_interval: 1
      # ... diğer switch'ler
```

**💡 İPUCU:** `modbus_combined.yaml` dosyasındaki tüm içeriği kopyala yapıştır, daha kolay!

---

## 🤖 Adım 3: Automations Ekle

### 3.1. Automations Klasörü Oluştur

Home Assistant File Editor'de:
- Sol menüden **📁 klasör ikonu** → **New folder**
- Klasör adı: `automations`
- ✅ Oluştur

### 3.2. Automation Dosyalarını Kopyala

**2 dosya kopyalaman gerekiyor:**

#### a) button_press_detection.yaml (454 satır)

- `automations/button_press_detection.yaml` dosyasını aç (bu repo'dan)
- **Tüm içeriği kopyala**
- Home Assistant File Editor'de `automations` klasörüne gir
- **New file** → `button_press_detection.yaml`
- İçeriği yapıştır ve **Save**

#### b) button_actions.yaml (242 satır)

- `automations/button_actions.yaml` dosyasını aç (bu repo'dan)
- **Tüm içeriği kopyala**
- `automations` klasöründe **New file** → `button_actions.yaml`
- İçeriği yapıştır ve **Save**

**NOT:** `button_actions.yaml` template'dir, kendi light entity'lerine göre düzenle!

### 3.3. Configuration.yaml'a Include Ekle

`configuration.yaml` dosyasını aç ve ekle:

```yaml
# Automations Include
automation: !include_dir_merge_list automations/
```

Bu şekilde `automations/` klasöründeki **TÜM `.yaml` dosyaları** otomatik yüklenecek!

**TOPLAM:** ~32 automation (16 detection + 16 action)

---

## ✅ Adım 4: Config Check & Restart

### 4.1. Config Kontrolü

Developer Tools → YAML → Check Configuration

Hata varsa düzeltin.

### 4.2. Home Assistant'ı Restart

Settings → System → Restart

---

## 🎮 Adım 5: Test

### Binary Sensor'leri Kontrol Et

Developer Tools → States:
- `binary_sensor.sag_yatak_butonu`
- `binary_sensor.sol_yatak_butonu`
- `binary_sensor.mutfak_butonu`
- ...

### Button Press Test

1. Simulator'den bir butona basın (örnek: `kontrol.py di-oku 0`)
2. Home Assistant'ta binary_sensor değişmeli
3. Automation çalışmalı
4. Event'ler tetiklenmeli

Developer Tools → Events → Listen to Event:
- `sag_yatak_short_press`
- `sag_yatak_long_press`
- `sag_yatak_double_press`

---

## 📝 Adım 6: Light Entity'leri Güncelle

`button_actions.yaml` dosyasında entity_id'leri kendi light'larınıza göre değiştirin:

```yaml
# Örnek:
- service: light.toggle
  target:
    entity_id: light.yatak_alani_isik  # ← Kendi entity'niz
```

---

## 🔧 Button Press Ayarları

### Press Duration Ayarı

`button_press_detection.yaml` içinde:

```yaml
is_long: "{{ press_duration > 0.8 }}"  # 800ms
```

Değiştirmek için:
- Daha hızlı long press: `0.5` (500ms)
- Daha yavaş long press: `1.2` (1200ms)

### Double Press Timeout

```yaml
- delay:
    milliseconds: 400  # ← Bu değeri değiştir
```

- Daha hızlı double: `300ms`
- Daha yavaş double: `600ms`

---

## 📊 Button Mapping

| Button | DI | Short Press | Long Press | Double Press |
|--------|----|-----------|-----------|--------------------|
| Sağ Yatak | DI0 | Yatak alanı toggle | Sağ okuma toggle | Tümünü kapat |
| Sol Yatak | DI1 | Yatak alanı toggle | Sol okuma toggle | Tümünü kapat |
| Popup Yatak | DI2 | Popup toggle | Popup ambiyans | Tümünü kapat |
| Dış Aydınlatma | DI3 | Tente toggle | Tente ambiyans | Tümünü kapat |
| Basamak | DI4 | Basamak toggle | - | - |
| Mutfak | DI5 | Mutfak toggle | Tezgâh toggle | - |
| Orta Alan | DI6 | Orta alan toggle | Ambiyans | Tümünü kapat |
| Banyo | DI7 | Banyo toggle | Ayna lambası toggle | - |

---

## 🐛 Troubleshooting

### Modbus bağlanmıyor

1. Simulator çalışıyor mu?
   ```bash
   cd simulators/waveshare-latching-relay-01
   python3 simulator.py
   ```

2. Hostname çözülüyor mu?
   ```bash
   ping ugurs-macbook-m4-pro.local
   ```

3. Port açık mı?
   ```bash
   nc -zv ugurs-macbook-m4-pro.local 5023
   nc -zv ugurs-macbook-m4-pro.local 5024
   ```

### Binary sensor değişmiyor

1. Developer Tools → States'te kontrol et
2. Modbus integration loglarına bak:
   Settings → System → Logs → Filter: "modbus"

### Automation çalışmıyor

1. Automation enabled mi?
   Settings → Automations → İlgili automation
   
2. Event tetikleniyor mu?
   Developer Tools → Events → Listen: `sag_yatak_short_press`
   
3. Trace'e bak:
   Automation'ı aç → 3 nokta → Traces

### Helper'lar görünmüyor

1. Config check yaptın mı?
2. Restart sonrası:
   Settings → Devices & Services → Helpers
   Listede olmalılar

---

## 🎯 Ekstra Özellikler

### Notification Ekle

Double press'te bildirim gönder:

```yaml
- id: sag_yatak_double_press_action
  trigger:
    - platform: event
      event_type: sag_yatak_double_press
  action:
    - service: notify.mobile_app_your_phone
      data:
        message: "Tüm ışıklar kapatıldı"
    - service: light.turn_off
      target:
        entity_id: all
```

### Condition Ekle

Sadece gece çalışsın:

```yaml
- id: orta_alan_short_press_action
  trigger:
    - platform: event
      event_type: orta_alan_short_press
  condition:
    - condition: time
      after: "18:00:00"
      before: "06:00:00"
  action:
    - service: light.toggle
      target:
        entity_id: light.orta_alan_isik
```

### Scene Kullan

Ambiyans için scene:

```yaml
- id: popup_yatak_long_press_action
  trigger:
    - platform: event
      event_type: popup_yatak_long_press
  action:
    - service: scene.turn_on
      target:
        entity_id: scene.popup_ambient
```

---

## 📞 Destek

Sorun yaşarsan:
1. Logs kontrol et
2. Automation trace'lerine bak
3. Event'leri dinle
4. Binary sensor state'lerini kontrol et

Başarılar! 🚀

