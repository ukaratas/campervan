# Waveshare Latching Relay Instance 02

8 kanallı banyo aydınlatma ve su sistemi kontrol modülü simülatörü.

## ⚙️ Konfigürasyon

Tüm ayarlar `config.py` dosyasında merkezi olarak yönetiliyor:
- **Cihaz bilgileri:** Device name, type, description
- **Network:** Port 5025, Slave ID, hostname
- **Röle tanımları:** Labels, power consumption
- **Home Assistant:** Hostname ayarları

## 🚀 Başlatma

```bash
cd waveshare-latching-relay-02
source ../venv/bin/activate
python3 simulator.py
```

## 🎮 Kontrol

```bash
# Röle aç/kapat
python3 kontrol.py ac 0        # R0: Banyo Aydınlatma AÇ
python3 kontrol.py kapat 2     # R2: Hidrofor KAPAT
python3 kontrol.py toggle 3    # R3: Macerator TOGGLE

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
- **Çözüm:** Simülatör zaten çalışıyor. `pkill -f "relay-02.*simulator.py"` ile durdur.

**Sorun:** Home Assistant bağlanamıyor
- **Kontrol 1:** Simülatör çalışıyor mu? (`ps aux | grep "relay-02"`)
- **Kontrol 2:** Port açık mı? (`nc -zv ugurs-macbook-m4-pro.local 5025`)
- **Kontrol 3:** Hostname çözülüyor mu? (`ping ugurs-macbook-m4-pro.local`)

**Sorun:** Loglar dosyaya yazılmıyor
- **Çözüm:** `simulator.log` dosyası otomatik oluşturulur, klasör yazılabilir olmalı.

## 📋 Röle Haritası

| Coil | Röle | Açıklama | Güç | Akım |
|------|------|----------|-----|------|
| 0 | R0 | Banyo Aydınlatma | 8W | 0.33A |
| 1 | R1 | Banyo Ayna Aydınlatma | 8W | 0.33A |
| 2 | R2 | Temiz Su Hidrofor | 84W | 3.5A |
| 3 | R3 | Macerator Pompa | 192W | 8A |
| 4 | R4 | Rezerv | - | - |
| 5 | R5 | Rezerv | - | - |
| 6 | R6 | Rezerv | - | - |
| 7 | R7 | Rezerv | - | - |

**Toplam Güç:** ~292W (tüm aktif röleler)  
**Port:** 5025  
**Modbus TCP Slave ID:** 1

