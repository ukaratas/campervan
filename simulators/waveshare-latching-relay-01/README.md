# Waveshare Latching Relay Instance 01

8 kanallı aydınlatma kontrol modülü simülatörü.

## ⚙️ Konfigürasyon

Tüm ayarlar `config.py` dosyasında merkezi olarak yönetiliyor:
- **Cihaz bilgileri:** Device name, type, description
- **Network:** Port, Slave ID, hostname
- **Röle tanımları:** Labels, power consumption
- **Home Assistant:** Hostname ayarları

## 🚀 Başlatma

```bash
cd waveshare-latching-relay-01
source ../venv/bin/activate
python3 simulator.py
```

## 🎮 Kontrol

```bash
# Röle aç/kapat
python3 kontrol.py ac 3        # R3: Yatak Alanı Işık AÇ
python3 kontrol.py kapat 3     # R3: Yatak Alanı Işık KAPAT
python3 kontrol.py toggle 0    # R0: Mutfak Işık TOGGLE

# Durumları göster
python3 kontrol.py durum

# Tümünü kapat
python3 kontrol.py tumunu-kapat
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
- **Çözüm:** Simülatör zaten çalışıyor. `pkill -f simulator.py` ile durdur.

**Sorun:** Home Assistant bağlanamıyor
- **Kontrol 1:** Simülatör çalışıyor mu? (`ps aux | grep simulator.py`)
- **Kontrol 2:** Port açık mı? (`nc -zv ugurs-macbook-m4-pro.local 5023`)
- **Kontrol 3:** Hostname çözülüyor mu? (`ping ugurs-macbook-m4-pro.local`)

**Sorun:** Loglar dosyaya yazılmıyor
- **Çözüm:** `simulator.log` dosyası otomatik oluşturulur, klasör yazılabilir olmalı.

## 📋 Röle Haritası

| Coil | Röle | Açıklama |
|------|------|----------|
| 0 | R0 | Mutfak Işık (8W) |
| 1 | R1 | Mutfak Tezgâh Işık (7W) |
| 2 | R2 | Orta Alan Işık (12W) |
| 3 | R3 | Yatak Alanı Işık (14W) |
| 4 | R4 | Popup Yatak Işık (6W) |
| 5 | R5 | Sol Okuma Işık (4W) |
| 6 | R6 | Sağ Okuma Işık (4W) |
| 7 | R7 | Tente Işık (12W) |

