# Waveshare Latching Relay Instance 03

8 kanallı yüksek tüketim cihazları kontrol modülü simülatörü.

## ⚙️ Konfigürasyon

Tüm ayarlar `config.py` dosyasında merkezi olarak yönetiliyor:
- **Cihaz bilgileri:** Device name, type, description
- **Network:** Port 5026, Slave ID, hostname
- **Röle tanımları:** Labels, power consumption
- **Home Assistant:** Hostname ayarları

## 🚀 Başlatma

```bash
cd waveshare-latching-relay-03
source ../venv/bin/activate
python3 simulator.py
```

## 🎮 Kontrol

```bash
# Röle aç/kapat
python3 kontrol.py ac 0        # R0: Buzdolabı AÇ
python3 kontrol.py kapat 1     # R1: USB Mutfak KAPAT
python3 kontrol.py toggle 5    # R5: Truma TOGGLE

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
- **Çözüm:** Simülatör zaten çalışıyor. `pkill -f "relay-03.*simulator.py"` ile durdur.

**Sorun:** Home Assistant bağlanamıyor
- **Kontrol 1:** Simülatör çalışıyor mu? (`ps aux | grep "relay-03"`)
- **Kontrol 2:** Port açık mı? (`nc -zv ugurs-macbook-m4-pro.local 5026`)
- **Kontrol 3:** Hostname çözülüyor mu? (`ping ugurs-macbook-m4-pro.local`)

**Sorun:** Loglar dosyaya yazılmıyor
- **Çözüm:** `simulator.log` dosyası otomatik oluşturulur, klasör yazılabilir olmalı.

## 📋 Röle Haritası

| Coil | Röle | Açıklama | Güç | Akım |
|------|------|----------|-----|------|
| 0 | R0 | Buzdolabı | 65W | 2.7A |
| 1 | R1 | USB Kutusu #1 (Mutfak) | 200W | 8A |
| 2 | R2 | USB Kutusu #2 (Yatak) | 200W | 8A |
| 3 | R3 | USB Kutusu #3 (Banyo) | 200W | 8A |
| 4 | R4 | USB Kutusu #4 (Popup) | 200W | 8A |
| 5 | R5 | Truma Combi D4 | 50W | 2A |
| 6 | R6 | Gri Su Pompası | 120W | 5A |
| 7 | R7 | Rezerv | - | - |

**Toplam Güç:** ~1035W (tüm aktif röleler)  
**Port:** 5026  
**Modbus TCP Slave ID:** 1

**⚠️ Notlar:**
- USB kutuları aynı anda tam yükte çalışmayacak (gerçek senaryoda daha düşük tüketim)
- Buzdolabı sürekli çalışır (30-50W ortalama)
- Truma sadece çalışırken güç çeker (aralıklı)

