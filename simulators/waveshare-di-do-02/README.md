# Waveshare Modbus RTU IO 8CH - Instance 02

220V Finder Kontaktör Kontrol Sistemi simülatörü.

**Wiki:** https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH

## ⚙️ Konfigürasyon

Tüm ayarlar `config.py` dosyasında merkezi olarak yönetiliyor:
- **Cihaz bilgileri:** Device name, type, description
- **Network:** Port 5027, Slave ID, hostname
- **DI/DO tanımları:** Kontaktör bobin kontrol + status mapping
- **Home Assistant:** Hostname ayarları

## 🔧 Finder 22.22.9.024.4000 Kontaktör Mantığı

Bu modül **Finder 22.22.9.024.4000** modüler kontaktörleri kontrol eder.

### Kontaktör Özellikleri:
- **Tip:** Modüler kontaktör (DIN rail)
- **Kontaklar:** 2 NO (normally open), 25A @ 250VAC
- **Bobin:** 24V DC (~70mA, ~1.7W)
- **Kontak Malzemesi:** AgSnO2

### Sistem Mimarisi:

```
Home Assistant
    ↓
DI/DO-02 Modülü
    ↓ DO (HIGH=AÇ, LOW=KAPA) → Kontaktör Bobin Kontrol
    ↑ DI (STATUS)              ← Kontaktör Yardımcı Kontak
    ↓
220V Cihazlar
```

### IO Mapping (1 DO + 1 DI per cihaz):

**Finder-1 (İndüksiyon Ocak, 1800W):**
- DO0: Bobin kontrol (HIGH=AÇ, LOW=KAPA)
- DI0: STATUS (1=Açık, 0=Kapalı)

**Finder-2 (Bulaşık Makinesi, 1700W):**
- DO1: Bobin kontrol
- DI1: STATUS

**Finder-3 (Çamaşır Makinesi, 160W):**
- DO2: Bobin kontrol
- DI2: STATUS

**Finder-4 (Mikrodalga Fırın, 800W):**
- DO3: Bobin kontrol
- DI3: STATUS

**Finder-5 (Rezerv):**
- DO4: Bobin kontrol
- DI4: STATUS

## 🚀 Başlatma

```bash
cd waveshare-di-do-02
source ../venv/bin/activate
python3 simulator.py
```

## 🎮 Kontrol

### Digital Output (Kontaktör Aç/Kapa)

```bash
# Finder-1 (İndüksiyon Ocak) AÇ
python3 kontrol.py do-ac 0        # DO0: HIGH → Kontaktör çeker

# Finder-1 (İndüksiyon Ocak) KAPA
python3 kontrol.py do-kapa 0      # DO0: LOW → Kontaktör düşer

# Finder-2 (Bulaşık Makinesi) AÇ
python3 kontrol.py do-ac 1        # DO1: HIGH

# Finder-4 (Mikrodalga) AÇ
python3 kontrol.py do-ac 3        # DO3: HIGH
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

## 📋 Kontaktör Mapping Tablosu

| Kontaktör | Cihaz | Güç | DO (Bobin) | DI (Status) |
|-----------|-------|-----|------------|-------------|
| Finder-1 | İndüksiyon Ocak | 1800W | DO0 | DI0 |
| Finder-2 | Bulaşık Makinesi | 1700W | DO1 | DI1 |
| Finder-3 | Çamaşır Makinesi | 160W | DO2 | DI2 |
| Finder-4 | Mikrodalga Fırın | 800W | DO3 | DI3 |
| Finder-5 | Rezerv | - | DO4 | DI4 |

**DO5-7, DI5-7:** Rezerv (genişleme için)

## ⚡ Özellikler

- **Basit Kontrol:** DO HIGH = AÇ, DO LOW = KAPA (pulse timing gerekmez)
- **Fail-safe:** Güç kesilirse tüm kontaktörler düşer → 220V cihazlar kapanır
- **Gerçek Durum Feedback:** DI'lar kontaktör yardımcı kontağından durumu okur
- **1:1 Mapping:** Her cihaz 1 DO + 1 DI kullanır
- **Home Assistant Entegrasyonu:** Basit switch entity (SET/RESET karmaşıklığı yok)

## 🔧 Teknik Özellikler

- **DI:** 8 kanal, 5-36V, kontaktör status feedback
- **DO:** 8 kanal, 5-40V, open-drain, 500mA/kanal (kontaktör bobini ~70mA)
- **Protokol:** Modbus TCP
- **Port:** 5027
- **Slave ID:** 1

---

**Not:** Bu simülatör geliştirme ve test amaçlıdır. Gerçek kurulumda Waveshare fiziksel modülü ve Finder 22.22.9.024.4000 kontaktörler kullanılacaktır.
