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
| **DI/DO Modülleri** | Waveshare 8DI/8DO (RS485) × 3 | Bistable röle toggle (DO) + durum feedback (DI) |
| **Master Röle** | CHINT NJMC1 32A 4P (Camper ON/OFF) | 220V + 24V + 12V rail anahtarlama |
| **Bireysel Röleler** | CHINT NJMC1 16A 2P bistable × 19 | AC + DC yükler (1P high-side switch, 1P DI feedback) |
| **Analog Giriş** | Industrial 8-Ch Analog Acquisition Module | 12-bit hassasiyet, voltaj/akım okuma, RS485 |

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
- **Kontrol:** NJMC1 16A 2P bistable röle + DI/DO (HA otomasyon)
- **Senaryo:** Kapı açıldığında otomatik aydınlatma, uzaktan kontrol

## ⚡ Elektrik ve Su Tesisatı

- **Enerji:** 24V DC ana hat (IPCBOX-CM5-A 7-36V direkt besleme, modüller, röleler)
- **İletişim:** RS485/Modbus, dijital/analog giriş-çıkışlar
- **Harici Aydınlatma:** 24V LED şeritler (yan taraf + awning/tente)
- **Otomasyon:** Röle, sensör, aktüatör, push button, Home Assistant entegrasyonu
- **Su:** Doğrudan bağlantı yok, ancak su ve nem sensörleriyle izleme yapılabilir

---

*Bu altyapı, karavanın tüm sistemlerinin akıllı, güvenli ve merkezi olarak yönetilmesini sağlar.*
