# Waveshare Modbus Simülatörleri

Her Waveshare modülü instance bazlı klasörlerde.

## 📁 Yapı

```
simulators/
├── waveshare-latching-relay-01/    ✅ Aydınlatma kontrol (8 röle)
│   ├── simulator.py
│   ├── kontrol.py
│   ├── izle.py
│   ├── ha-config.yaml
│   └── README.md
│
├── waveshare-di-do-01/             ⏳ Gelecek (Push buttons + DO)
│
├── requirements.txt                 Ortak bağımlılıklar
└── venv/                           Python virtual environment
```

## 🚀 Hızlı Başlangıç

### İlk Kurulum
```bash
cd simulators
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Latching Relay Başlat
```bash
cd waveshare-latching-relay-01
source ../venv/bin/activate
python3 simulator.py
```

### Test Et
```bash
# Yeni terminal
cd waveshare-latching-relay-01
source ../venv/bin/activate
python3 kontrol.py toggle 3    # Yatak ışığı
```

## 📖 Detaylar

Her klasörde kendi `README.md` var.

## 🏠 Home Assistant

Her instance klasöründeki `ha-config.yaml` → HA `configuration.yaml`'a ekle.
