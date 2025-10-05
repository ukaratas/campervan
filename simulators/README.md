# Waveshare Modbus Simülatörleri

Her Waveshare modülü için ayrı klasör yapısı.

## 📁 Klasör Yapısı

```
simulators/
├── waveshare-latching-relay-01/    # Instance 01
│   ├── simulator.py                # Simülatör
│   ├── kontrol.py                  # Kontrol aracı
│   ├── izle.py                     # İzleme aracı
│   ├── ha-config.yaml              # HA konfigürasyonu
│   └── README.md                   # Kullanım kılavuzu
│
├── waveshare-latching-relay-02/    # Instance 02 (ileride)
├── waveshare-di-do-01/             # Instance 01 (ileride)
│
└── requirements.txt                # Ortak bağımlılıklar
```

## 🚀 Hızlı Başlangıç

### 1. Kurulum (İlk Defa)

```bash
cd simulators
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Latching Relay Başlat

```bash
cd waveshare-latching-relay-01
source ../venv/bin/activate
python3 simulator.py
```

### 3. Kontrol Et (Yeni Terminal)

```bash
cd waveshare-latching-relay-01
source ../venv/bin/activate

python3 kontrol.py toggle 3    # Yatak ışığı aç/kapa
python3 kontrol.py durum       # Tüm durumları göster
```

### 4. İzle (Yeni Terminal)

```bash
cd waveshare-latching-relay-01
source ../venv/bin/activate
python3 izle.py
```

---

## 📋 Mevcut Simülatörler

### ✅ waveshare-latching-relay-01
- **Port:** 5023
- **Tip:** 8-Ch Latching Relay
- **Kullanım:** Aydınlatma kontrol
- **Status:** Hazır ✓

### ⏳ waveshare-di-do-01
- **Port:** 5022
- **Tip:** 8-Ch DI/DO Module
- **Kullanım:** Push buttons + relay triggers
- **Status:** Geliştirilecek

---

## 🏠 Home Assistant

Her klasördeki `ha-config.yaml` dosyasını Home Assistant `configuration.yaml`'a ekle.

---

## 💡 Yeni Instance Eklemek

İkinci latching relay eklemek için:

```bash
cp -r waveshare-latching-relay-01 waveshare-latching-relay-02
```

Sonra `waveshare-latching-relay-02/` içinde:
- Port değiştir (örn: 5024)
- Etiketleri güncelle
