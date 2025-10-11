# Waveshare Modül Simülatörleri

Bu klasörde karavan projesinde kullanılan Waveshare endüstriyel IoT modüllerinin **Modbus TCP simülatörleri** bulunur.

## 🎯 Amaç

Gerçek donanım olmadan:
- ✅ Home Assistant automation'larını geliştir ve test et
- ✅ Modbus TCP iletişimini doğrula
- ✅ Button press detection mantığını test et
- ✅ Light control senaryolarını simüle et
- ✅ Deployment pipeline'ı test et

## 📦 Kurulum

### 1. Python Virtual Environment Oluştur

```bash
cd simulators
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# veya
venv\Scripts\activate     # Windows
```

### 2. Gerekli Paketleri Yükle

```bash
pip install -r requirements.txt
```

**requirements.txt içeriği:**
```
pymodbus==3.5.4
```

## 🚀 Simülatörleri Başlat

### Option 1: Ayrı Terminal'lerde (Önerilen)

**Terminal 1 - Latching Relay 01 (Aydınlatma):**
```bash
cd simulators/waveshare-latching-relay-01
source ../venv/bin/activate
python3 simulator.py
```

**Terminal 2 - DI/DO Module:**
```bash
cd simulators/waveshare-di-do-01
source ../venv/bin/activate
python3 simulator.py
```

**Terminal 3 - Latching Relay 02 (Banyo + Su):**
```bash
cd simulators/waveshare-latching-relay-02
source ../venv/bin/activate
python3 simulator.py
```

**Terminal 4 - Latching Relay 03 (Yüksek Tüketim):**
```bash
cd simulators/waveshare-latching-relay-03
source ../venv/bin/activate
python3 simulator.py
```

### Option 2: Background Process

```bash
cd simulators
source venv/bin/activate

# Latching Relay 01 - Port 5023 (Aydınlatma)
cd waveshare-latching-relay-01
python3 simulator.py > simulator.log 2>&1 &
RELAY01_PID=$!
echo "Latching Relay 01 started (PID: $RELAY01_PID)"

# DI/DO Module - Port 5024
cd ../waveshare-di-do-01
python3 simulator.py > simulator.log 2>&1 &
DIDO_PID=$!
echo "DI/DO Module started (PID: $DIDO_PID)"

# Latching Relay 02 - Port 5025 (Banyo + Su)
cd ../waveshare-latching-relay-02
python3 simulator.py > simulator.log 2>&1 &
RELAY02_PID=$!
echo "Latching Relay 02 started (PID: $RELAY02_PID)"

# Latching Relay 03 - Port 5026 (Yüksek Tüketim)
cd ../waveshare-latching-relay-03
python3 simulator.py > simulator.log 2>&1 &
RELAY03_PID=$!
echo "Latching Relay 03 started (PID: $RELAY03_PID)"

# Tüm simülatörleri durdurmak için:
# kill $RELAY01_PID $DIDO_PID $RELAY02_PID $RELAY03_PID
```

## 📋 Modül Listesi

| Modül | Port | Açıklama | Folder |
|-------|------|----------|--------|
| **Latching Relay 01** | 5023 | 8-kanal bistable röle<br/>Aydınlatma kontrolü | `waveshare-latching-relay-01/` |
| **DI/DO 01** | 5024 | 8 Digital Input (push buttons)<br/>8 Digital Output (switches) | `waveshare-di-do-01/` |
| **Latching Relay 02** | 5025 | 8-kanal bistable röle<br/>Banyo + Su sistemi | `waveshare-latching-relay-02/` |
| **Latching Relay 03** | 5026 | 8-kanal bistable röle<br/>Yüksek tüketim cihazları | `waveshare-latching-relay-03/` |

## 🎮 Kullanım

### Latching Relay Kontrolü

```bash
cd waveshare-latching-relay-01

# Röle aç/kapat
python3 kontrol.py ac 0        # R0: Mutfak Işık AÇ
python3 kontrol.py kapat 3     # R3: Yatak Alanı KAPAT
python3 kontrol.py toggle 5    # R5: Sol Okuma TOGGLE

# Durumları göster
python3 kontrol.py durum

# Tümünü kapat
python3 kontrol.py tumunu-kapat
```

### DI/DO Modül Kontrolü

```bash
cd waveshare-di-do-01

# Digital Output kontrolü
python3 kontrol.py do-ac 2        # DO2: Su Pompası AÇ
python3 kontrol.py do-kapat 2     # DO2: Su Pompası KAPAT
python3 kontrol.py do-toggle 0    # DO0: Alarm TOGGLE

# Digital Input okuma
python3 kontrol.py di-oku 0       # DI0: Sağ Yatak Butonu
python3 kontrol.py di-tumunu-oku  # Tüm DI'ları oku

# Genel durum
python3 kontrol.py durum
```

### Real-Time Monitoring

```bash
# Her modülün kendi klasöründe:
python3 izle.py
```

## 🏠 Home Assistant Entegrasyonu

### 1. Modbus Konfigürasyonu

Her simülatörün `ha-config.yaml` dosyası var. Bu dosyaları Home Assistant'a ekle:

```bash
cd ../Automation/ha-configs

# Otomatik deployment (önerilen)
python3 deploy.py --auto

# Manuel deployment
# modbus_combined.yaml içeriğini Home Assistant configuration.yaml'a ekle
```

### 2. Hostname Kullanımı

Simülatörler **dinamik IP** sorununu çözmek için `.local` hostname kullanır:

```yaml
# ha-config.yaml içinde
host: ugurs-macbook-m4-pro.local  # IP yerine hostname
```

**Avantajları:**
- ✅ IP değişse bile bağlantı kopmaz
- ✅ mDNS (Bonjour) ile otomatik çözümleme
- ✅ Network değiştirme toleransı

### 3. Button Press Detection

DI/DO simülatörü **gerçekçi push button davranışı** simüle eder:

- **Short Press:** 0.1-0.3 saniye (%70)
- **Long Press:** 1.0-2.0 saniye (%20)
- **Double Press:** 2x kısa basma, 0.2s aralık (%10)

Home Assistant automations bu pattern'leri algılar:
- `sag_yatak_short_press` → Yatak alanı ışık toggle
- `sag_yatak_long_press` → Sağ okuma lambası
- `sag_yatak_double_press` → Tüm lambaları kapat

**Detaylı bilgi:** `../Automation/ha-configs/README.md`

## 🔧 Konfigürasyon

Her simülatör klasöründe `config.py` dosyası merkezi konfigürasyon sağlar:

```python
# config.py örneği
DEVICE_NAME = "Relay-01"
PORT = 5023
SLAVE_ID = 1
HOST = "0.0.0.0"  # Tüm interface'lerde dinle
HA_HOSTNAME = "ugurs-macbook-m4-pro.local"  # HA'nın bağlanacağı adres
RELAY_COUNT = 8
START_ADDRESS = 0
RELAY_LABELS = ["R0: Mutfak Işık", "R1: Tezgâh", ...]
```

## 🐛 Troubleshooting

### Sorun: `[Errno 48] address already in use`

**Sebep:** Simülatör zaten çalışıyor

**Çözüm:**
```bash
# Tüm simülatörleri durdur
pkill -f simulator.py

# veya spesifik olarak
pkill -f "waveshare-latching-relay-01.*simulator.py"
pkill -f "waveshare-di-do-01.*simulator.py"
```

### Sorun: `ModuleNotFoundError: No module named 'pymodbus'`

**Sebep:** Virtual environment aktif değil veya pymodbus yüklü değil

**Çözüm:**
```bash
source venv/bin/activate
pip install pymodbus==3.5.4
```

### Sorun: Home Assistant bağlanamıyor

**Kontrol 1:** Simülatör çalışıyor mu?
```bash
ps aux | grep simulator.py
```

**Kontrol 2:** Portlar açık mı?
```bash
nc -zv ugurs-macbook-m4-pro.local 5023  # Relay 01
nc -zv ugurs-macbook-m4-pro.local 5024  # DI/DO
nc -zv ugurs-macbook-m4-pro.local 5025  # Relay 02
nc -zv ugurs-macbook-m4-pro.local 5026  # Relay 03
```

**Kontrol 3:** Hostname çözülüyor mu?
```bash
ping ugurs-macbook-m4-pro.local
```

**Kontrol 4:** Home Assistant log'ları incele
```
Settings → System → Logs → Filter: "modbus"
```

### Sorun: Binary sensor değişmiyor

**Çözüm:**
1. Modbus connection'ı reload et:
   - Configuration → Integrations → Modbus → Reload
2. `scan_interval` değerini düşür (örn: 0.5 saniye)
3. DI/DO simülatörü log'larını kontrol et

## 📊 Log Dosyaları

Her simülatör kendi klasöründe `simulator.log` dosyası oluşturur:

```bash
# Latching Relay log
tail -f waveshare-latching-relay-01/simulator.log

# DI/DO log
tail -f waveshare-di-do-01/simulator.log
```

**Log içeriği:**
- Modbus sunucu başlatma
- Coil/register değişiklikleri
- DI simülasyon event'leri (button presses)
- Hata mesajları

## 🚀 Deployment Workflow

**Tam geliştirme döngüsü:**

```bash
# 1. Simülatörleri başlat
cd simulators
source venv/bin/activate

# Terminal 1
cd waveshare-latching-relay-01 && python3 simulator.py

# Terminal 2
cd waveshare-di-do-01 && python3 simulator.py

# 2. HA config değişikliği yap
cd ../Automation/ha-configs
# helpers/ veya automations/ dosyalarını düzenle

# 3. Deploy et
python3 deploy.py --auto

# 4. Home Assistant'ta test et
# - Developer Tools → States
# - Developer Tools → Events (event trace)
# - Automations → Traces
```

## 📝 Yeni Simülatör Ekleme

Yeni bir Waveshare modülü için simülatör oluşturmak istersen:

1. **Klasör oluştur:**
   ```bash
   mkdir waveshare-yeni-modul-01
   cd waveshare-yeni-modul-01
   ```

2. **Dosyaları kopyala (template olarak):**
   ```bash
   cp ../waveshare-latching-relay-01/config.py .
   cp ../waveshare-latching-relay-01/simulator.py .
   cp ../waveshare-latching-relay-01/kontrol.py .
   cp ../waveshare-latching-relay-01/izle.py .
   ```

3. **config.py'yi düzenle:**
   - `DEVICE_NAME`, `PORT`, `DEVICE_TYPE`
   - Modül spesifik parametreler

4. **simulator.py'yi düzenle:**
   - Modbus register/coil mapping
   - Özel simülasyon mantığı

5. **ha-config.yaml oluştur**

6. **README.md yaz**

## 🔗 İlgili Dokümantasyon

- **Home Assistant Configs:** `../Automation/ha-configs/README.md`
- **Sistem Mimarisi:** `../Automation/readme.md`
- **Latching Relay:** `waveshare-latching-relay-01/README.md`
- **DI/DO Module:** `waveshare-di-do-01/README.md`
- **Ana Proje README:** `../README.md`

---

**Not:** Bu simülatörler geliştirme ve test amaçlıdır. Gerçek donanım kurulumunda Waveshare fiziksel modülleri kullanılacaktır.
