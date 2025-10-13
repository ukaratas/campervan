# Waveshare Modbus RTU IO 8CH - Instance 02

220V Finder Röle Kontrol Sistemi simülatörü.

**Wiki:** https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH

## ⚙️ Konfigürasyon

Tüm ayarlar `config.py` dosyasında merkezi olarak yönetiliyor:
- **Cihaz bilgileri:** Device name, type, description
- **Network:** Port 5027, Slave ID, hostname
- **DI/DO tanımları:** Finder SET/RESET/STATUS mapping
- **Home Assistant:** Hostname ayarları

## 🔧 Finder Röle Mantığı

Bu modül **Finder 20.22.0.024.0000** rölelerini kontrol eder.

### Sistem Mimarisi:

```
Home Assistant
    ↓
DI/DO-02 Modülü
    ↓ DO (SET/RESET) → Finder Röle Kontrol
    ↑ DI (STATUS)    ← Finder Röle Durum Feedback
    ↓
220V Cihazlar
```

### IO Mapping:

**Finder-1 (İndüksiyon Ocak):**
- DO0: SET (AÇ)
- DO1: RESET (KAPA)
- DI0: STATUS (1=Açık, 0=Kapalı)

**Finder-2 (Bulaşık Makinesi):**
- DO2: SET (AÇ)
- DO3: RESET (KAPA)
- DI1: STATUS

**Finder-3 (Rezerv):**
- DO4: SET (AÇ)
- DO5: RESET (KAPA)
- DI2: STATUS

**Finder-4 (Rezerv):**
- DO6: SET (AÇ)
- DO7: RESET (KAPA)
- DI3: STATUS

## 🚀 Başlatma

```bash
cd waveshare-di-do-02
source ../venv/bin/activate
python3 simulator.py
```

## 🎮 Kontrol

### Digital Output (Finder Kontrol)

```bash
# Finder-1 (İndüksiyon Ocak) AÇ
python3 kontrol.py do-ac 0        # DO0: SET

# Finder-1 (İndüksiyon Ocak) KAPA
python3 kontrol.py do-ac 1        # DO1: RESET

# Finder-2 (Bulaşık Makinesi) AÇ
python3 kontrol.py do-ac 2        # DO2: SET

# Finder-2 (Bulaşık Makinesi) KAPA
python3 kontrol.py do-ac 3        # DO3: RESET
```

### Digital Input (Status Okuma)

```bash
# Finder-1 durumunu oku
python3 kontrol.py di-oku 0       # DI0: Finder-1 Status

# Tüm Finder durumlarını oku
python3 kontrol.py di-tumunu-oku

# Genel durum
python3 kontrol.py durum
```

## 📺 İzleme

```bash
python3 izle.py
```

## 🏠 Home Assistant

`ha-config.yaml` içeriğini Home Assistant `configuration.yaml`'a ekle.

**Otomatik Deployment:**
```bash
cd ../../Automation/ha-configs
python3 deploy.py --auto
```

### Dinamik IP Çözümü
Simülatör Mac'in IP adresi değişse bile çalışır:
- `config.py` içinde `HA_HOSTNAME = "ugurs-macbook-m4-pro.local"` (mDNS)
- Home Assistant `.local` hostname üzerinden bağlanır
- IP değişikliği umursanmaz

### Troubleshooting

**Sorun:** `[Errno 48] address already in use`
- **Çözüm:** Simülatör zaten çalışıyor. `pkill -f "di-do-02.*simulator.py"` ile durdur.

**Sorun:** Home Assistant bağlanamıyor
- **Kontrol 1:** Simülatör çalışıyor mu? (`ps aux | grep "di-do-02"`)
- **Kontrol 2:** Port açık mı? (`nc -zv ugurs-macbook-m4-pro.local 5027`)
- **Kontrol 3:** Hostname çözülüyor mu? (`ping ugurs-macbook-m4-pro.local`)

## 📋 Finder Mapping Tablosu

| Finder | Cihaz | DO SET | DO RESET | DI STATUS |
|--------|-------|--------|----------|-----------|
| Finder-1 | İndüksiyon Ocak (1800W) | DO0 | DO1 | DI0 |
| Finder-2 | Bulaşık Makinesi | DO2 | DO3 | DI1 |
| Finder-3 | 220V Cihaz (Rezerv) | DO4 | DO5 | DI2 |
| Finder-4 | 220V Cihaz (Rezerv) | DO6 | DO7 | DI3 |

**DI4-7:** Rezerv (8 Finder için 2. modül gerekir)

## ⚡ Özellikler

- **Gerçek Durum Feedback:** DI'lar Finder rölelerin gerçek durumunu gösterir
- **2 Kanallı Kontrol:** SET (AÇ) ve RESET (KAPA) ayrı DO'lar
- **Simülasyon Mantığı:** DO SET/RESET komutları otomatik olarak DI'ları günceller
- **Home Assistant Entegrasyonu:** Binary sensor (status) + Switch (kontrol)

## 🔧 Teknik Özellikler

- **DI:** 8 kanal, 5-36V, Finder status feedback
- **DO:** 8 kanal, 5-40V, open-drain, 500mA/kanal
- **Protokol:** Modbus TCP
- **Port:** 5027
- **Slave ID:** 1

## 💡 Finder Röle Avantajları

✅ Home Assistant her zaman gerçek durumu bilir  
✅ Fiziksel buton ile kontrol edilse bile HA senkronize kalır  
✅ Güvenli: 2 kanallı kontrol (SET/RESET)  
✅ Status feedback ile doğrulama  
✅ 220V yüksek güç cihazları için ideal

---

**Not:** Bu simülatör geliştirme ve test amaçlıdır. Gerçek kurulumda Waveshare fiziksel modülü ve Finder 20.22.0.024.0000 röleleri kullanılacaktır.

