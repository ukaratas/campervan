# 🎯 Basit Başlangıç - 1 Button + 1 Lamba

Adım adım, en basit senaryodan başlayalım!

---

## 📋 ADIM 1: Simülatörü Başlat

### Terminal-1: Simülatör

```bash
cd "/Users/ugurkaratas/Local Projects/campervan/simulators"

# İlk defa ise:
python3 -m venv venv
source venv/bin/activate
pip install pymodbus==3.5.4

# Simülatörü başlat
python3 simple-start.py
```

✅ **Göreceksin:**
```
🚀 KARAVAN OTOMASYON - BASİT TEST SİMÜLATÖRÜ
📡 Listening on: 0.0.0.0:5020
```

Bu terminali açık bırak!

---

## 📋 ADIM 2: Mac IP Adresini Bul

### Terminal-2: IP Öğren

```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Çıktı: `inet 192.168.1.100 ...`

**IP'ni not et:** `192.168.1.100`

---

## 📋 ADIM 3: Home Assistant Ayarla

### 3.1 Configuration.yaml Düzenle

UTM Home Assistant → File Editor → `configuration.yaml`

**En alta ekle (IP'ni değiştir!):**

```yaml
modbus:
  - name: "Test"
    type: tcp
    host: 192.168.1.100  # ⚠️ BURAYA KENDİ IP'Nİ YAZ!
    port: 5020
    
    lights:
      - name: "Yatak Işık"
        slave: 1
        address: 0
        write_type: coil
```

### 3.2 Kontrol Et ve Restart

- Developer Tools → YAML → Check Configuration ✅
- Settings → System → Restart

---

## 📋 ADIM 4: İlk Test!

### 4.1 Işığı Home Assistant'tan Kontrol Et

- Overview → Add Card → Entities
- `light.yatak_isik` ekle
- Toggle et (aç/kapa)

**Simülatör terminalinde göreceksin:**
```
💡 [YATAK ALANI IŞIK] → 🟢 AÇILDI
💡 [YATAK ALANI IŞIK] → ⚫ KAPANDI
```

✅ **Çalışıyor!**

---

## 📋 ADIM 5: Manuel Button Simülasyonu

Home Assistant'ta manuel button oluşturacağız:

### 5.1 Helper Oluştur

- Settings → Devices & Services → Helpers
- Create Helper → **Input Button**
- Name: `Test Button`
- Icon: `mdi:gesture-tap-button`
- Create

### 5.2 Otomasyon Ekle

Developer Tools → Automations → Create

```yaml
alias: Test Button Toggle Light
trigger:
  - platform: state
    entity_id: input_button.test_button
action:
  - service: light.toggle
    target:
      entity_id: light.yatak_isik
```

Save!

### 5.3 Test Et

- Overview'a dön
- `input_button.test_button` ekle
- Tile'a bas
- Işığın değiştiğini gör! 💡

---

## 📋 ADIM 6: Short/Long/Double Press (Gelişmiş)

Şimdi gerçek button davranışlarını ekleyelim!

### 6.1 Configuration Güncelle

`configuration.yaml`:

```yaml
modbus:
  - name: "Test"
    type: tcp
    host: 192.168.1.100
    port: 5020
    
    binary_sensors:
      - name: "Sağ Yatak Button"
        slave: 1
        address: 0
        input_type: discrete_input
        scan_interval: 1
    
    lights:
      - name: "Yatak Işık"
        slave: 1
        address: 0
        write_type: coil
      
      - name: "Okuma Işık"
        slave: 1
        address: 1
        write_type: coil

input_number:
  button_press_count:
    name: Button Press Counter
    min: 0
    max: 10
    step: 1

timer:
  button_double_press:
    duration: "00:00:00.5"  # 500ms window

automation:
  # Short Press: Yatak ışığını toggle
  - alias: "Button Short Press"
    trigger:
      - platform: state
        entity_id: binary_sensor.sag_yatak_button
        to: "on"
    action:
      - service: input_number.increment
        target:
          entity_id: input_number.button_press_count
      - service: timer.start
        target:
          entity_id: timer.button_double_press
  
  # Timer bitince press count'a göre karar ver
  - alias: "Button Action Decision"
    trigger:
      - platform: event
        event_type: timer.finished
        event_data:
          entity_id: timer.button_double_press
    action:
      - choose:
          # Double press (2 kez basıldı)
          - conditions:
              - condition: numeric_state
                entity_id: input_number.button_press_count
                above: 1.5
            sequence:
              - service: light.turn_off
                target:
                  entity_id:
                    - light.yatak_isik
                    - light.okuma_isik
              - service: notify.persistent_notification
                data:
                  message: "Double Press - Tüm ışıklar kapandı"
          
          # Single press
          - conditions:
              - condition: numeric_state
                entity_id: input_number.button_press_count
                below: 1.5
            sequence:
              - service: light.toggle
                target:
                  entity_id: light.yatak_isik
      
      # Counter'ı sıfırla
      - service: input_number.set_value
        target:
          entity_id: input_number.button_press_count
        data:
          value: 0
```

---

## 🎯 Özet

✅ **ADIM 1:** Simülatör çalışıyor  
✅ **ADIM 2:** IP öğrendin  
✅ **ADIM 3:** HA'ya bağlandın  
✅ **ADIM 4:** Manuel kontrol çalışıyor  
✅ **ADIM 5:** Button helper test edildi  
✅ **ADIM 6:** Short/Double press mantığı hazır  

---

## 🚀 Sırada Ne Var?

1. **Long Press** ekle (1 saniye+ basılı tutma)
2. **İkinci button** ve **ikinci lamba** ekle
3. **Tüm ışıkları kapat** senaryosu test et
4. **Gerçek Modbus cihaz** simülasyonuna geç

---

## 💡 İpuçları

### Simülatör Durumu Görme

Terminal-2'de (simülatör çalışırken):
```bash
cd "/Users/ugurkaratas/Local Projects/campervan/simulators"
source venv/bin/activate
python3
```

```python
from pymodbus.client import ModbusTcpClient
client = ModbusTcpClient('localhost', port=5020)
client.connect()

# Coil durumu oku (Işık)
result = client.read_coils(0, 1)
print(f"Yatak Işık: {'AÇIK' if result.bits[0] else 'KAPALI'}")

client.close()
```

### Home Assistant Log İzleme

- Settings → System → Logs
- Filter: "modbus"

---

## ❓ Sorun Giderme

### "Connection refused"
- Simülatörün çalıştığından emin ol
- IP adresini doğru girdin mi?
- UTM network ayarı bridge mode'da mı?

### Entity görünmüyor
- Configuration valid mi kontrol et
- Restart sonrası 1-2 dakika bekle
- Settings → Devices & Services → Entities'de ara

### Button çalışmıyor
- `binary_sensor.sag_yatak_button` entity var mı?
- Developer Tools → States'de durumunu gör

---

**Hazır mısın? Hadi başlayalım! 🚀**

Hangi adımda yardım istersen söyle!
