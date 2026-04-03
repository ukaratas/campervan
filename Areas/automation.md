# Otomasyon ve Kontrol Altyapısı

Karavanın tüm sistemlerinin merkezi ve akıllı şekilde izlenmesi, kontrolü ve otomasyonu için Home Assistant tabanlı bir altyapı kurulmuştur. Tüm cihazlar, sensörler ve aktüatörler mümkün olduğunca kablolu (RS485/Modbus) olarak entegre edilir.

## 🎯 Amaç ve Kapsam

- Tüm elektrikli cihazların, sensörlerin ve valflerin merkezi olarak izlenmesi ve kontrolü
- Enerji optimizasyonu, güvenlik, konfor ve bakım kolaylığı
- Uzaktan izleme, bildirim ve otomasyon senaryoları

## 🛠️ Kullanılan Donanımlar

| Kategori | Ürün/Modül | Özellikler |
|----------|------------|------------|
| **Ana Kontrolcü** | Waveshare IPCBOX-CM5-A + RPi CM5 8GB Lite + 512GB NVMe SSD | 4x RS485, CAN, 2DI/2DO, dual ETH (1G+2.5G), 7-36V DC, M.2 4G/5G slot, DIN rail, alüminyum kasa |
| **DI/DO Modülü** | Waveshare 8DI/8DO (RS485) × 1 | Push button (DI), valf / kontaktör bobini tetik (DO); yük anahtarlama Waveshare Modbus röle modülleri |
| **Master / camper enable** | Waveshare 8CH RTU Relay (master startup) | Camper ON/OFF — 220V + 24V + 12V rail anahtarlama (Modbus RTU) |
| **Yük röleleri** | Waveshare Modbus relay (RTU 8CH + POE ETH 16CH) | AC + DC yükler; doğrudan Modbus ile HA kontrolü |
| **Analog Giriş** | Industrial 8-Ch Analog Acquisition Module | 12-bit hassasiyet, voltaj/akım okuma, RS485 |
| **Kontrol Paneli** | Waveshare 11.9" HDMI LCD 320×1480 IPS Touch | Giriş kapısı üstü, HDMI + USB direkt bağlantı, HA dashboard |

## 🏠 Home Assistant Entegrasyonu

- Tüm modüller Home Assistant'a Modbus/RS485 ile entegre edilir
- Cihaz ve sensör durumları, enerji tüketimi, su seviyesi, sıcaklık vb. merkezi olarak izlenir
- Otomasyonlar YAML veya görsel arayüz ile tanımlanır

### Tipik Otomasyon Senaryoları
- **Enerji Yönetimi:** Yüksek akım çeken cihazların (pompa, ısıtıcı vb.) otomatik aç/kapatılması
- **Donma Koruması:** Sıcaklık sensörüne göre valf/pompa otomasyonu
- **Su Yönetimi:** Seviye sensörüne göre pompa ve valf kontrolü
- **Güvenlik:** Kaçak akım, aşırı sıcaklık/akım durumunda otomatik müdahale ve alarm

## 🔧 Kurulum ve Bakım

1. **Donanım Montajı:** IPCBOX-CM5-A ve modüllerin pano içine yerleştirilmesi (DIN rail)
2. **Kablolama:** RS485, güç ve sinyal hatlarının çekilmesi
3. **Home Assistant Kurulumu:** CM5 üzerinde Home Assistant OS kurulumu (512GB NVMe SSD)
4. **Modül Entegrasyonu:** Modbus cihazlarının Home Assistant'a tanımlanması
5. **Otomasyonların Tanımlanması:** Senaryoların yazılması ve test edilmesi

## 💡 Genişletilebilirlik ve Öneriler
- Ek modüllerle (röle, analog, dijital giriş/çıkış) sistem kolayca büyütülebilir
- MQTT, Modbus TCP gibi ek protokollerle uzaktan izleme ve entegrasyon
- Endüstriyel modüller sayesinde uzun ömür ve güvenilirlik
- 24V bataryadan direkt besleme (IPCBOX-CM5 7-36V giriş), ihtiyaç halinde harici UPS eklenebilir

## 🔗 Cihaz Detayları

### Harici Aydınlatma Sistemi (2 devre)
- **Dış Aydınlatma 1 + 2:** 24V LED dış aydınlatma
- **Kontrol:** DI → HA → Waveshare relay (Modbus)
- **Senaryo:** Kapı açıldığında otomatik aydınlatma, uzaktan kontrol

## ⚡ Elektrik ve Su Tesisatı

- **Enerji:** 24V DC ana hat (IPCBOX-CM5-A 7-36V direkt besleme, modüller, röleler)
- **İletişim:** RS485/Modbus, dijital/analog giriş-çıkışlar
- **Harici Aydınlatma:** 24V LED şeritler (yan taraf + awning/tente)
- **Otomasyon:** Röle, sensör, aktüatör, push button, Home Assistant entegrasyonu
- **Su:** Doğrudan bağlantı yok, ancak su ve nem sensörleriyle izleme yapılabilir

---

*Bu altyapı, karavanın tüm sistemlerinin akıllı, güvenli ve merkezi olarak yönetilmesini sağlar.*
