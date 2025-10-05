# Modbus TCP Simülasyon Planı

Bu doküman, Home Assistant test ortamında kullanılacak Modbus TCP simülasyonlarını içerir.

## 🎯 Simülasyon Stratejisi

### Kullanılacak Araçlar
1. **pymodbus** - Python Modbus kütüphanesi (simülatör oluşturmak için)
2. **ModbusPal** - Java tabanlı GUI Modbus simülatörü
3. **Docker Modbus Simulator** - Konteyner tabanlı çözüm

### Tavsiye: pymodbus ile Docker container
- Her cihaz ayrı container'da çalışır
- Farklı IP:Port kombinasyonları
- Kolay yönetim ve sıfırlama

---

## 📋 Simüle Edilecek Cihazlar

### 1. High Current Relay (4 Kanal) - 30A
**IP:** `192.168.1.101` | **Port:** `502` | **Slave ID:** `1`

| Register Tipi | Adres | Açıklama | Değer Aralığı |
|--------------|-------|----------|---------------|
| Coil | 0 | Röle 1 (Macerator pompa) | 0/1 (OFF/ON) |
| Coil | 1 | Röle 2 (Rezerv) | 0/1 |
| Coil | 2 | Röle 3 (Rezerv) | 0/1 |
| Coil | 3 | Röle 4 (Rezerv) | 0/1 |
| Discrete Input | 0-3 | Röle durumu geri bildirim | 0/1 |
| Input Register | 0-3 | Röle akım tüketimi (simüle) | 0-30000 (0-30A, x1000) |

---

### 2. DI/DO Module (8 Kanal)
**IP:** `192.168.1.102` | **Port:** `502` | **Slave ID:** `1`

#### Digital Outputs (DO - Bistable Relay Tetikleme)
| Register Tipi | Adres | Açıklama | Değer |
|--------------|-------|----------|-------|
| Coil | 0 | DO1 - Buzdolabı tetik | 0/1 |
| Coil | 1 | DO2 - Hidrofor tetik | 0/1 |
| Coil | 2 | DO3 - 24V klima tetik | 0/1 |
| Coil | 3 | DO4 - Truma Combi tetik | 0/1 |
| Coil | 4 | DO5 - USB şarj tetik | 0/1 |
| Coil | 5 | DO6 - 24V çıkışlar tetik | 0/1 |
| Coil | 6 | DO7 - 12V çıkışlar tetik | 0/1 |
| Coil | 7 | DO8 - Rezerv | 0/1 |

#### Digital Inputs (DI - Push Button)
| Register Tipi | Adres | Açıklama | Değer |
|--------------|-------|----------|-------|
| Discrete Input | 0 | DI1 - Sağ yatak push button | 0/1 |
| Discrete Input | 1 | DI2 - Sol yatak push button | 0/1 |
| Discrete Input | 2 | DI3 - Popup yatak push button | 0/1 |
| Discrete Input | 3 | DI4 - Dış aydınlatma push button | 0/1 |
| Discrete Input | 4 | DI5 - Otomatik basamak push button | 0/1 |
| Discrete Input | 5 | DI6 - Mutfak push button | 0/1 |
| Discrete Input | 6 | DI7 - Orta alan push button | 0/1 |
| Discrete Input | 7 | DI8 - Banyo push button | 0/1 |

---

### 3. Low Latching Relay (8 Kanal)
**IP:** `192.168.1.103` | **Port:** `502` | **Slave ID:** `1`

| Register Tipi | Adres | Açıklama | Değer |
|--------------|-------|----------|-------|
| Coil | 0 | R1 - Mutfak aydınlatma | 0/1 |
| Coil | 1 | R2 - Mutfak tezgâh aydınlatma | 0/1 |
| Coil | 2 | R3 - Orta alan aydınlatma | 0/1 |
| Coil | 3 | R4 - Yatak alanı aydınlatma | 0/1 |
| Coil | 4 | R5 - Popup yatak aydınlatma | 0/1 |
| Coil | 5 | R6 - Yatak sol baş okuma | 0/1 |
| Coil | 6 | R7 - Yatak sağ baş okuma | 0/1 |
| Coil | 7 | R8 - Tente altı aydınlatma | 0/1 |
| Discrete Input | 0-7 | Röle durumu geri bildirim | 0/1 |
| Input Register | 0-7 | LED güç tüketimi (W) | 0-20 (simüle) |

---

### 4. Analog Acquisition Module (8 Kanal)
**IP:** `192.168.1.104` | **Port:** `502` | **Slave ID:** `1`

| Register Tipi | Adres | Açıklama | Değer Aralığı | Formül |
|--------------|-------|----------|---------------|--------|
| Input Register | 0 | AI1 - Temiz su tank (%) | 0-1000 | 0-100% (x10) |
| Input Register | 1 | AI2 - Gri su tank (%) | 0-1000 | 0-100% (x10) |
| Input Register | 2 | AI3 - Rezerv | 0-65535 | - |
| Input Register | 3 | AI4 - Rezerv | 0-65535 | - |
| Input Register | 4 | AI5 - Rezerv | 0-65535 | - |
| Input Register | 5 | AI6 - Rezerv | 0-65535 | - |
| Input Register | 6 | AI7 - Rezerv | 0-65535 | - |
| Input Register | 7 | AI8 - Rezerv | 0-65535 | - |

**Özel Registerlar:**
| Register Tipi | Adres | Açıklama | Değer |
|--------------|-------|----------|-------|
| Input Register | 100 | Temiz su hacim (L) | 0-150 |
| Input Register | 101 | Gri su hacim (L) | 0-120 |

---

### 5. RGB Dimmer Module (4 Kanal)
**IP:** `192.168.1.105` | **Port:** `502` | **Slave ID:** `1`

#### Kanal 1: Tente Ambiyans
| Register Tipi | Adres | Açıklama | Değer Aralığı |
|--------------|-------|----------|---------------|
| Coil | 0 | CH1 - Power ON/OFF | 0/1 |
| Holding Register | 0 | CH1 - Parlaklık | 0-255 |
| Holding Register | 1 | CH1 - Kırmızı (R) | 0-255 |
| Holding Register | 2 | CH1 - Yeşil (G) | 0-255 |
| Holding Register | 3 | CH1 - Mavi (B) | 0-255 |

#### Kanal 2: Ortam Ambiyans
| Register Tipi | Adres | Açıklama | Değer Aralığı |
|--------------|-------|----------|---------------|
| Coil | 1 | CH2 - Power ON/OFF | 0/1 |
| Holding Register | 10 | CH2 - Parlaklık | 0-255 |
| Holding Register | 11 | CH2 - Kırmızı (R) | 0-255 |
| Holding Register | 12 | CH2 - Yeşil (G) | 0-255 |
| Holding Register | 13 | CH2 - Mavi (B) | 0-255 |

#### Kanal 3-4: Rezerv
| Register Tipi | Adres | Açıklama |
|--------------|-------|----------|
| Coil | 2-3 | CH3-4 Power | 
| Holding Register | 20-33 | CH3-4 Parametreler |

---

### 6. Victron EasySolar-II (Simüle)
**IP:** `192.168.1.110` | **Port:** `502` | **Slave ID:** `100`

Victron cihazları için özel register map kullanılır. Temel simülasyon:

| Register Tipi | Adres | Açıklama | Değer | Birim |
|--------------|-------|----------|-------|-------|
| Input Register | 840 | Batarya voltajı | 2400-2900 | 0.01V (24.00-29.00V) |
| Input Register | 841 | Batarya akımı | -10000 to 10000 | 0.1A (-100A to 100A) |
| Input Register | 842 | Batarya gücü | 0-3000 | 1W |
| Input Register | 843 | Batarya SOC | 0-100 | 1% |
| Input Register | 850 | AC Çıkış gücü | 0-3000 | 1W (inverter) |
| Input Register | 851 | AC Çıkış voltajı | 220-240 | 1V |
| Input Register | 860 | Shore power | 0/1 | Boolean |
| Input Register | 861 | Shore akım | 0-16 | 1A |
| Input Register | 870 | Solar güç | 0-400 | 1W |
| Input Register | 871 | Solar voltaj | 0-50 | 0.1V |
| Input Register | 872 | Solar akım | 0-20 | 0.1A |

---

## 🐍 Python Simülatör Kodu (Örnek)

### Basit Modbus TCP Simülatör

```python
#!/usr/bin/env python3
"""
Modbus TCP Simülatör - Waveshare DI/DO Module
IP: 192.168.1.102
Port: 502
Slave ID: 1
"""

from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import logging

# Logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def run_server():
    # Data Store oluştur
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*8),  # 8 Digital Input (push buttons)
        co=ModbusSequentialDataBlock(0, [0]*8),  # 8 Coils (DO çıkışları)
        hr=ModbusSequentialDataBlock(0, [0]*100), # Holding registers
        ir=ModbusSequentialDataBlock(0, [0]*100)  # Input registers
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Server başlat
    print("DI/DO Module Simulator başlatılıyor...")
    print("IP: 192.168.1.102, Port: 502, Slave ID: 1")
    StartTcpServer(context=context, address=("0.0.0.0", 502))

if __name__ == "__main__":
    run_server()
```

### Docker Compose ile Tüm Simülatörler

```yaml
version: '3.8'

services:
  # High Current Relay Module
  relay-high:
    build: ./simulators/relay-high
    container_name: modbus-relay-high
    ports:
      - "5021:502"
    networks:
      campervan_net:
        ipv4_address: 192.168.1.101

  # DI/DO Module
  di-do:
    build: ./simulators/di-do
    container_name: modbus-di-do
    ports:
      - "5022:502"
    networks:
      campervan_net:
        ipv4_address: 192.168.1.102

  # Low Latching Relay Module
  relay-low:
    build: ./simulators/relay-low
    container_name: modbus-relay-low
    ports:
      - "5023:502"
    networks:
      campervan_net:
        ipv4_address: 192.168.1.103

  # Analog Module
  analog:
    build: ./simulators/analog
    container_name: modbus-analog
    ports:
      - "5024:502"
    networks:
      campervan_net:
        ipv4_address: 192.168.1.104

  # RGB Dimmer
  dimmer:
    build: ./simulators/dimmer
    container_name: modbus-dimmer
    ports:
      - "5025:502"
    networks:
      campervan_net:
        ipv4_address: 192.168.1.105

  # Victron EasySolar-II Simülatör
  victron:
    build: ./simulators/victron
    container_name: modbus-victron
    ports:
      - "5030:502"
    networks:
      campervan_net:
        ipv4_address: 192.168.1.110

networks:
  campervan_net:
    driver: bridge
    ipam:
      config:
        - subnet: 192.168.1.0/24
```

---

## 📝 Home Assistant Konfigürasyonu

### configuration.yaml

```yaml
# Modbus TCP Entegrasyonu
modbus:
  - name: "Campervan Automation"
    type: tcp
    host: 192.168.1.102  # DI/DO Module
    port: 502
    
    # Digital Inputs (Push Buttons)
    binary_sensors:
      - name: "Sağ Yatak Button"
        slave: 1
        address: 0
        input_type: discrete_input
        
      - name: "Sol Yatak Button"
        slave: 1
        address: 1
        input_type: discrete_input
        
      - name: "Popup Yatak Button"
        slave: 1
        address: 2
        input_type: discrete_input
        
      - name: "Dış Aydınlatma Button"
        slave: 1
        address: 3
        input_type: discrete_input
        
      - name: "Basamak Button"
        slave: 1
        address: 4
        input_type: discrete_input
        
      - name: "Mutfak Button"
        slave: 1
        address: 5
        input_type: discrete_input
        
      - name: "Orta Alan Button"
        slave: 1
        address: 6
        input_type: discrete_input
        
      - name: "Banyo Button"
        slave: 1
        address: 7
        input_type: discrete_input
    
    # Digital Outputs (Bistable Relay Tetikleme)
    switches:
      - name: "Buzdolabı"
        slave: 1
        address: 0
        write_type: coil
        
      - name: "Hidrofor"
        slave: 1
        address: 1
        write_type: coil
        
      - name: "24V Klima"
        slave: 1
        address: 2
        write_type: coil
        
      - name: "Truma Combi"
        slave: 1
        address: 3
        write_type: coil
        
      - name: "USB Şarj"
        slave: 1
        address: 4
        write_type: coil

  # Low Latching Relay (Aydınlatma)
  - name: "Lighting Control"
    type: tcp
    host: 192.168.1.103
    port: 502
    
    lights:
      - name: "Mutfak Işık"
        slave: 1
        address: 0
        write_type: coil
        
      - name: "Mutfak Tezgâh Işık"
        slave: 1
        address: 1
        write_type: coil
        
      - name: "Orta Alan Işık"
        slave: 1
        address: 2
        write_type: coil
        
      - name: "Yatak Alanı Işık"
        slave: 1
        address: 3
        write_type: coil
        
      - name: "Popup Yatak Işık"
        slave: 1
        address: 4
        write_type: coil
        
      - name: "Sol Okuma Işık"
        slave: 1
        address: 5
        write_type: coil
        
      - name: "Sağ Okuma Işık"
        slave: 1
        address: 6
        write_type: coil
        
      - name: "Tente Işık"
        slave: 1
        address: 7
        write_type: coil

  # Analog Module (Su Tankları)
  - name: "Water Tanks"
    type: tcp
    host: 192.168.1.104
    port: 502
    
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
        
      - name: "Gri Su Seviyesi"
        slave: 1
        address: 1
        input_type: input
        data_type: uint16
        scale: 0.1
        precision: 1
        unit_of_measurement: "%"
        
      - name: "Gri Su Hacim"
        slave: 1
        address: 101
        input_type: input
        data_type: uint16
        unit_of_measurement: "L"

  # Victron EasySolar-II
  - name: "Victron Energy"
    type: tcp
    host: 192.168.1.110
    port: 502
    
    sensors:
      - name: "Batarya Voltaj"
        slave: 100
        address: 840
        input_type: input
        data_type: uint16
        scale: 0.01
        precision: 2
        unit_of_measurement: "V"
        device_class: voltage
        
      - name: "Batarya Akım"
        slave: 100
        address: 841
        input_type: input
        data_type: int16
        scale: 0.1
        precision: 1
        unit_of_measurement: "A"
        device_class: current
        
      - name: "Batarya SOC"
        slave: 100
        address: 843
        input_type: input
        data_type: uint16
        unit_of_measurement: "%"
        device_class: battery
        
      - name: "AC Çıkış Gücü"
        slave: 100
        address: 850
        input_type: input
        data_type: uint16
        unit_of_measurement: "W"
        device_class: power
        
      - name: "Solar Güç"
        slave: 100
        address: 870
        input_type: input
        data_type: uint16
        unit_of_measurement: "W"
        device_class: power
    
    binary_sensors:
      - name: "Shore Power"
        slave: 100
        address: 860
        input_type: input
```

---

## 🚀 Başlangıç Adımları

### 1. Python Environment Hazırlığı
```bash
cd "/Users/ugurkaratas/Local Projects/campervan"
mkdir -p simulators/{relay-high,relay-low,di-do,analog,dimmer,victron}

# Python sanal ortamı
python3 -m venv venv
source venv/bin/activate
pip install pymodbus Flask

# Her simülatör için requirements.txt
echo "pymodbus==3.5.4" > simulators/requirements.txt
```

### 2. İlk Simülatör Testi (DI/DO)
```bash
# Basit test simülatörü çalıştır
python3 simulators/di-do/server.py
```

### 3. Home Assistant Test
```bash
# HA configuration.yaml'a modbus ekle
# Developer Tools > YAML > Check Configuration
# Restart Home Assistant
```

---

## 📚 Kaynaklar

### Pymodbus Dökümantasyonu
- https://pymodbus.readthedocs.io/

### Modbus Register Tipleri
- **Coil (0x):** Read/Write Boolean (ON/OFF kontrol)
- **Discrete Input (1x):** Read-only Boolean (sensör durumu)
- **Input Register (3x):** Read-only 16-bit (sensor değeri)
- **Holding Register (4x):** Read/Write 16-bit (ayarlar)

### Waveshare Modbus Protokol Detayları
- Her cihaz için gerçek register map'i ürün datasheet'inden alınmalı
- Bu simülasyon genel prensiplere göre hazırlanmıştır

---

## 🎯 Sıradaki Adımlar

1. ✅ İlk simülatör çalıştır (DI/DO)
2. ✅ Home Assistant'a bağlan
3. ✅ Push button simülasyonu test et
4. ✅ Basit otomasyon yaz (button → light)
5. ✅ Tüm cihazları simüle et
6. ✅ Karmaşık senaryolar test et (yük yönetimi)
7. ✅ Dashboard oluştur


