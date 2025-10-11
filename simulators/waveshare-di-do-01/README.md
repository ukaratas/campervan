# Waveshare Modbus RTU IO 8CH - Instance 01

8 DI (Digital Input) + 8 DO (Digital Output) modülü simülatörü.

**Wiki:** https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH

## ⚙️ Konfigürasyon

Tüm ayarlar `config.py` dosyasında merkezi olarak yönetiliyor:
- **Cihaz bilgileri:** Device name, type, description
- **Network:** Port, Slave ID, hostname
- **DI/DO tanımları:** Digital Input ve Output etiketleri
- **Home Assistant:** Hostname ayarları

## 🚀 Başlatma

```bash
cd waveshare-di-do-01
source ../venv/bin/activate
python3 simulator.py
```

## 🎮 Kontrol

### Digital Output (DO) Kontrolü

```bash
# DO aç/kapat
python3 kontrol.py do-ac 2        # DO2: Su Pompası AÇ
python3 kontrol.py do-kapat 2     # DO2: Su Pompası KAPAT
python3 kontrol.py do-toggle 0    # DO0: Alarm TOGGLE

# Tümünü kapat
python3 kontrol.py do-tumunu-kapat
```

### Digital Input (DI) Okuma

```bash
# Tek bir DI oku
python3 kontrol.py di-oku 0       # DI0: Kapı Sensörü oku

# Tüm DI'ları oku
python3 kontrol.py di-tumunu-oku
```

### Genel Durum

```bash
# Hem DI hem DO durumlarını göster
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

### Button Press Detection

Simülatör **gerçekçi push button davranışı** simüle eder:
- **Short Press:** 0.1-0.3 saniye basma (%70 olasılık)
- **Long Press:** 1.0-2.0 saniye basma (%20 olasılık)
- **Double Press:** 2x kısa basma, 0.2s aralıkla (%10 olasılık)

Home Assistant automations bu pattern'leri algılar ve uygun aksiyonları tetikler.

**Detaylı bilgi:** `../../Automation/ha-configs/README.md`

### Dinamik IP Çözümü
Simülatör Mac'in IP adresi değişse bile çalışır:
- `config.py` içinde `HA_HOSTNAME = "ugurs-macbook-m4-pro.local"` (mDNS)
- Home Assistant `.local` hostname üzerinden bağlanır
- IP değişikliği umursanmaz

### Troubleshooting

**Sorun:** `[Errno 48] address already in use`
- **Çözüm:** Simülatör zaten çalışıyor. `pkill -f "waveshare-di-do-01.*simulator.py"` ile durdur.

**Sorun:** Home Assistant bağlanamıyor
- **Kontrol 1:** Simülatör çalışıyor mu? (`ps aux | grep "di-do.*simulator"`)
- **Kontrol 2:** Port açık mı? (`nc -zv ugurs-macbook-m4-pro.local 5024`)
- **Kontrol 3:** Hostname çözülüyor mu? (`ping ugurs-macbook-m4-pro.local`)

**Sorun:** Binary sensor değişmiyor ama simülatör log atıyor
- **Çözüm 1:** Home Assistant'ta Modbus reconnect: Configuration → Integrations → Modbus → Reload
- **Çözüm 2:** `scan_interval: 1` değerini düşür (örn: 0.5 saniye)

## 📋 Kanal Haritası

### 📥 Digital Inputs (Push Buttons)

| DI  | Buton Adı               | Short Press              | Long Press              | Double Press           |
|-----|-------------------------|--------------------------|-------------------------|------------------------|
| DI0 | Sağ Yatak              | Yatak alanı aç/kapa      | Sağ okuma lambası       | Tüm aydınlatma kapat   |
| DI1 | Sol Yatak              | Yatak alanı aç/kapa      | Sol okuma lambası       | Tüm aydınlatma kapat   |
| DI2 | Popup Yatak            | Popup aydınlatma aç/kapa | Popup ambiyans          | Tüm aydınlatma kapat   |
| DI3 | Dış Aydınlatma         | Tente altı aç/kapa       | Tente ambiyans          | Tüm aydınlatma kapat   |
| DI4 | Otomatik Basamak       | Basamak aç/kapa          | -                       | -                      |
| DI5 | Mutfak                 | Mutfak lambası           | Tezgâh lambası          | -                      |
| DI6 | Orta Alan              | Orta alan aydınlatma     | Ambiyans aydınlatma     | Tüm aydınlatma kapat   |
| DI7 | Banyo                  | Banyo aydınlatma         | Banyo ayna lambası      | -                      |

### 📤 Digital Outputs (Kontrol)

| DO  | Açıklama          | Kullanım              |
|-----|-------------------|-----------------------|
| DO0 | Alarm Siren       | Ses/ışık alarm        |
| DO1 | Havalandırma Fan  | Fan kontrolü          |
| DO2 | Su Pompası        | Pompa on/off          |
| DO3 | Isıtıcı           | Isıtıcı kontrolü      |
| DO4 | Soğutucu          | Soğutucu kontrolü     |
| DO5 | Valf 1            | Elektrovalf kontrolü  |
| DO6 | Valf 2            | Elektrovalf kontrolü  |
| DO7 | Uyarı Lambası     | LED/lamba kontrolü    |

## 🔧 Teknik Özellikler

- **DI:** 8 kanal, 5-36V, passive/active input
- **DO:** 8 kanal, 5-40V, open-drain, 500mA/kanal
- **Protokol:** Modbus RTU
- **Port:** 5024 (varsayılan)
- **Slave ID:** 1 (varsayılan)

## 💡 Özellikler

- DI'lar otomatik simüle edilir (sensör değişimleri)
- DO'lar Modbus ile kontrol edilir
- Gerçek zamanlı izleme ve loglama
- Home Assistant entegrasyonu

