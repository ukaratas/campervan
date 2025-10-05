# 🔌 Waveshare Modbus Simülatörleri

Gerçek Waveshare ürünlerinin davranışını simüle eden Modbus TCP sunucuları.

## 📋 Simülatörler

### 1. `waveshare-di-do.py` - DI/DO Module
[Waveshare Modbus RTU IO 8CH](https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH)

- **8x Digital Input (DI):** Push button girişleri
- **8x Digital Output (DO):** Bistable relay tetikleme
- **Port:** 5022 (varsayılan)

### 2. `waveshare-latching-relay.py` - Latching Relay
[Waveshare Modbus RTU Relay (C)](https://www.waveshare.com/wiki/Modbus_RTU_Relay_(C))

- **8x Latching Relay:** Aydınlatma kontrol
- **READ + WRITE:** Durum okunabilir ve yazılabilir
- **Port:** 5023 (varsayılan)

---

## 🚀 Basit Başlangıç

### Terminal 1: DI/DO Module
```bash
cd "/Users/ugurkaratas/Local Projects/campervan/simulators"
source venv/bin/activate
python3 waveshare-di-do.py
```

### Terminal 2: Latching Relay
```bash
cd "/Users/ugurkaratas/Local Projects/campervan/simulators"
source venv/bin/activate
python3 waveshare-latching-relay.py
```

---

## 🎮 Multi-Instance Kullanımı

### Örnek 1: İki Latching Relay Modülü
```bash
# Terminal 1: İlk modül (Aydınlatma)
python3 waveshare-latching-relay.py --port 5023 --name Relay-Lighting

# Terminal 2: İkinci modül (Diğer yükler)
python3 waveshare-latching-relay.py --port 5024 --name Relay-Misc
```

### Örnek 2: İki DI/DO Modülü
```bash
# Terminal 1: İlk DI/DO (Ana push buttonlar)
python3 waveshare-di-do.py --port 5022 --name DI/DO-Main

# Terminal 2: İkinci DI/DO (Ek sensörler)
python3 waveshare-di-do.py --port 5025 --name DI/DO-Extra
```

---

## 🎮 Kontrol Komutları

### DI/DO Module (Push Button Simülasyonu)

Simülatör çalışırken Python console'dan:

```python
# Simülatör terminalinde Ctrl+Z -> fg ile pause/resume
# Veya Python interactive modda başlat:
# python3 -i waveshare-di-do.py

# Push button simülasyonu
simulator.press_button(0)           # DI0: Sağ yatak button (300ms)
simulator.press_button(0, 1.0)      # DI0: Long press (1 saniye)
simulator.press_button(1)           # DI1: Sol yatak button
simulator.show_status()             # Tüm DI/DO durumu
```

### Latching Relay (Manuel Röle Kontrolü)

```python
# Simülatör terminalinde
simulator.set_relay(3, True)        # R3: Yatak ışık AÇ
simulator.set_relay(3, False)       # R3: Yatak ışık KAPAT
simulator.show_status()             # Tüm röle durumları
```

---

## 📊 Home Assistant Konfigürasyonu

### DI/DO Module (Port 5022)

```yaml
modbus:
  - name: "DI_DO_Module"
    type: tcp
    host: 192.168.1.45
    port: 5022
    
    # Push Buttons (Discrete Inputs)
    binary_sensors:
      - name: "Sağ Yatak Button"
        slave: 1
        address: 0
        input_type: discrete_input
        scan_interval: 1
      
      - name: "Sol Yatak Button"
        slave: 1
        address: 1
        input_type: discrete_input
        scan_interval: 1
      
      - name: "Popup Yatak Button"
        slave: 1
        address: 2
        input_type: discrete_input
        scan_interval: 1
    
    # Bistable Relay Triggers (Coils)
    switches:
      - name: "Buzdolabı Tetik"
        slave: 1
        address: 0
        write_type: coil
      
      - name: "24V Klima Tetik"
        slave: 1
        address: 2
        write_type: coil
```

### Latching Relay Module (Port 5023)

```yaml
modbus:
  - name: "Lighting_Control"
    type: tcp
    host: 192.168.1.45
    port: 5023
    
    # Işıklar (Latching Relay - hem READ hem WRITE)
    lights:
      - name: "Mutfak Işık"
        slave: 1
        address: 0
        write_type: coil
        scan_interval: 1
      
      - name: "Yatak Alanı Işık"
        slave: 1
        address: 3
        write_type: coil
        scan_interval: 1
      
      - name: "Sol Okuma Işık"
        slave: 1
        address: 5
        write_type: coil
        scan_interval: 1
      
      - name: "Sağ Okuma Işık"
        slave: 1
        address: 6
        write_type: coil
        scan_interval: 1
```

### Otomasyon Örneği

```yaml
automation:
  # Sağ yatak button → Yatak alanı ışık
  - alias: "Sağ Yatak Button - Short Press"
    trigger:
      - platform: state
        entity_id: binary_sensor.sag_yatak_button
        to: 'on'
    action:
      - service: light.toggle
        target:
          entity_id: light.yatak_alani_isik
```

---

## 🎯 Port Listesi

| Port | Modül | Instance | Açıklama |
|------|-------|----------|----------|
| 5022 | DI/DO | #1 | Ana push buttonlar |
| 5023 | Latching Relay | #1 | Aydınlatma röleleri |
| 5024 | Latching Relay | #2 (opsiyonel) | İkinci modül |
| 5025 | DI/DO | #2 (opsiyonel) | İkinci DI/DO |

---

## 🧪 Test Senaryosu

### 1. İki Modülü Başlat

**Terminal 1:**
```bash
cd "/Users/ugurkaratas/Local Projects/campervan/simulators"
source venv/bin/activate
python3 waveshare-di-do.py
```

**Terminal 2:**
```bash
cd "/Users/ugurkaratas/Local Projects/campervan/simulators"
source venv/bin/activate
python3 waveshare-latching-relay.py
```

### 2. Home Assistant'a Konfigürasyon Ekle

Yukarıdaki YAML konfigürasyonunu `configuration.yaml`'a ekle.

### 3. Test

**Home Assistant'tan:**
- `light.yatak_alani_isik` toggle et
- **Latching Relay terminalinde** göreceksin: `💡 R3: Yatak Alanı Işık → 🟢 AÇILDI`

**Push Button Simülasyonu (Terminal 3):**
```bash
cd "/Users/ugurkaratas/Local Projects/campervan/simulators"
source venv/bin/activate
python3
```

```python
from pymodbus.client import ModbusTcpClient
client = ModbusTcpClient('localhost', port=5022)
client.connect()

# DI0'ı tetikle (Sağ yatak button)
client.write_coil(100, 0)  # Trigger button press
# NOT: Bu özel bir komut, gerçek cihazda olmaz
# Gerçekte push_button() fonksiyonunu kullanmalısın
```

**Veya simülatör terminalinden:**
```python
simulator.press_button(0)  # Sağ yatak button
```

---

## 📖 Register Map Özeti

### DI/DO Module
| Register Type | Address | Açıklama | R/W |
|--------------|---------|----------|-----|
| Discrete Input | 0-7 | DI1-DI8 (push buttons) | R |
| Coil | 0-7 | DO1-DO8 (relay triggers) | R/W |
| Input Register | 0-7 | DI status (register format) | R |

### Latching Relay
| Register Type | Address | Açıklama | R/W |
|--------------|---------|----------|-----|
| Coil | 0-7 | R1-R8 relay status | R/W |
| Holding Register | 0-7 | R1-R8 status (register) | R/W |

---

## ✅ Hazır!

Artık gerçek Waveshare cihazlarının davranışını simüle edebilirsin!

**Hangi konfigürasyonla başlamak istersin?**
1. Basit (1 DI/DO + 1 Relay)
2. İki Latching Relay
3. Tam sistem (4 modül)

