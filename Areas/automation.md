# Otomasyon ve Kontrol Altyapısı

Karavanın tüm sistemlerinin merkezi ve akıllı şekilde izlenmesi, kontrolü ve otomasyonu için Home Assistant tabanlı bir altyapı kurulmuştur. Tüm cihazlar, sensörler ve aktüatörler mümkün olduğunca kablolu (RS485/Modbus) olarak entegre edilir.

## 🎯 Amaç ve Kapsam

- Tüm elektrikli cihazların, sensörlerin ve valflerin merkezi olarak izlenmesi ve kontrolü
- Enerji optimizasyonu, güvenlik, konfor ve bakım kolaylığı
- Uzaktan izleme, bildirim ve otomasyon senaryoları

## 🛠️ Kullanılan Donanımlar

| Kategori | Ürün/Modül | Özellikler |
|----------|------------|------------|
| **Ana Kontrolcü** | Raspberry Pi CM4 + Waveshare Industrial IoT Modül | UPS, M.2 slot, endüstriyel I/O, RS485, genişletilebilir |
| **Röle Modülleri** | Modbus RTU 8-ch Latching Relay (C) | RS485, uzun süre açık kalacak cihazlar için |
| | Modbus RTU 4-ch 30A High Current Relay | RS485, yüksek akım (pompa, motor vb.) için, LED göstergeli |
| **Analog Giriş** | Industrial 8-Ch Analog Acquisition Module | 12-bit hassasiyet, voltaj/akım okuma, RS485 |
| **Gaz Dedektörleri** | Waveshare Industrial RS485 Gas Detector | LPG/Doğalgaz algılama, ön ve arka pozisyon |
| **Hava İstasyonu** | Waveshare Environmental Monitoring RS485 | Nem, sıcaklık, basınç, hava kalitesi (PM2.5, CO2) |
| **GPS Modülü** | Raspberry Pi GPS HAT/USB | Sürekli lokasyon takibi, Home Assistant entegrasyonu |
| **4G Bağlantı** | Raspberry Pi 4G/LTE HAT | Cloud etkileşim, uzaktan erişim, bildirimler |

## 🏠 Home Assistant Entegrasyonu

- Tüm modüller Home Assistant'a Modbus/RS485 ile entegre edilir
- Cihaz ve sensör durumları, enerji tüketimi, su seviyesi, sıcaklık vb. merkezi olarak izlenir
- Otomasyonlar YAML veya görsel arayüz ile tanımlanır

### Tipik Otomasyon Senaryoları
- **Enerji Yönetimi:** Yüksek akım çeken cihazların (pompa, ısıtıcı vb.) otomatik aç/kapatılması
- **Donma Koruması:** Sıcaklık sensörüne göre valf/pompa otomasyonu
- **Su Yönetimi:** Seviye sensörüne göre pompa ve valf kontrolü
- **Gaz Güvenliği:** LPG/doğalgaz algılandığında otomatik valf kapatma ve alarm
- **Hava Kalitesi:** CO2 seviyesi yüksekse otomatik havalandırma
- **Nem Kontrolü:** Yüksek nem algılandığında fan devreye girme
- **GPS Takip:** Sürekli lokasyon izleme ve geofencing uyarıları
- **Uzaktan İzleme:** 4G ile cloud bağlantısı ve mobil bildirimler
- **Güvenlik:** Kaçak akım, aşırı sıcaklık/akım durumunda otomatik müdahale ve alarm

## 🔧 Kurulum ve Bakım

1. **Donanım Montajı:** Raspberry Pi ve modüllerin pano içine yerleştirilmesi
2. **Kablolama:** RS485, güç ve sinyal hatlarının çekilmesi
3. **Home Assistant Kurulumu:** Raspberry Pi üzerinde Home Assistant OS kurulumu
4. **Modül Entegrasyonu:** Modbus cihazlarının Home Assistant'a tanımlanması
5. **Otomasyonların Tanımlanması:** Senaryoların yazılması ve test edilmesi

## 💡 Genişletilebilirlik ve Öneriler
- Ek modüllerle (röle, analog, dijital giriş/çıkış) sistem kolayca büyütülebilir
- MQTT, Modbus TCP gibi ek protokollerle uzaktan izleme ve entegrasyon
- Endüstriyel modüller sayesinde uzun ömür ve güvenilirlik
- Yedekli güç (UPS) ile kesintisiz otomasyon

## 🔗 Sensör ve Cihaz Detayları

### Gaz Dedektörleri (2 adet)
- **Konum:** Ön bölge (mutfak) ve arka bölge (yatak alanı)
- **Algılama:** LPG, doğalgaz, propan
- **İletişim:** RS485/Modbus RTU
- **Alarm:** Sesli uyarı + Home Assistant bildirimi
- **Otomasyon:** Gaz algılandığında otomatik gaz vanası kapatma

### Hava İstasyonu
- **Konum:** İç mekan merkezi (tavan montajı)
- **Metrikler:** Sıcaklık, nem, basınç, hava kalitesi (PM2.5), CO2
- **İletişim:** RS485/Modbus RTU
- **Otomasyon:** Hava kalitesine göre otomatik havalandırma kontrolü

### GPS ve 4G Modülleri
- **GPS:** Sürekli konum takibi, geofencing
- **4G/LTE:** Cloud bağlantısı, uzaktan Home Assistant erişimi
- **Veri Senkronizasyonu:** Sensör verileri cloud'a yedekleme
- **Mobil Bildirimler:** Kritik durumlarda push notification

### Harici Aydınlatma Sistemi
- **LED Şeritler:** 24V LED yan taraf aydınlatması
- **Awning/Tente:** LED şerit entegrasyonu, IP65 koruma
- **Kontrol:** Home Assistant ile otomatik/manuel açma-kapama
- **Senaryo:** Kapı açıldığında otomatik aydınlatma

## ⚡ Elektrik ve Su Tesisatı

- **Enerji:** 24V DC ana hat (Raspberry Pi, modüller, röleler), UPS ile yedekli
- **İletişim:** RS485/Modbus, dijital/analog giriş-çıkışlar, GPS, 4G
- **Sensörler:** Gaz dedektörleri, hava istasyonu, GPS modülü
- **Harici Aydınlatma:** 24V LED şeritler (yan taraf + awning/tente)
- **Otomasyon:** Röle, sensör, aktüatör, push button, Home Assistant entegrasyonu
- **Su:** Doğrudan bağlantı yok, ancak su ve nem sensörleriyle izleme yapılabilir

---

*Bu altyapı, karavanın tüm sistemlerinin akıllı, güvenli ve merkezi olarak yönetilmesini sağlar.*
