# DC-DC Alternatör Şarj Sistemi

Araç çalışırken alternatörden yaşam aküsüne (24V LiFePO4) güvenli ve kontrollü şarj sağlamak için tasarlanmış sistemdir. Aynı zamanda, ihtiyaç halinde yaşam aküsünden araç marş aküsüne destek şarjı da planlanmaktadır.

## 🎯 Hedefler

### Birincil Hedefler
* **Alternatör ile Şarj**: Araç çalışırken alternatörden, DC-DC şarj cihazı ile yaşam aküsünü (24V LiFePO4) güvenli şekilde şarj etmek
* **Akü Tipi Uyumluluğu**: 12V kurşun araç aküsü ve 24V LiFePO4 yaşam aküsü arasında tam uyum
* **Otomatik Kontrol**: Şarj işleminin voltaj ve akım limitleriyle otomatik yönetilmesi

### İkincil Hedefler
* **Marş Aküsü Float Şarj**: Kampta park halindeyken 220V (inverter veya shore) üzerinden araç aküsünü float tutarak boşalmayı önlemek (araç ECU, merkezi kilit, alarm vb. parasitik yükler). NJMC1 16A 2P bistable röle ile HA kontrolünde
* **Otomasyon ve İzleme**: Home Assistant ile şarj durumu, akım, voltaj ve hata izleme
* **Güvenlik**: Aşırı akım, aşırı sıcaklık ve ters akım koruması

## 🔄 Sistem Kavramsal Yapısı ve Güvenlik

- **DC-DC Şarj Cihazı**: Alternatör çıkışından alınan 12V DC, Victron Orion XS 1400 DC-DC şarj cihazı ile 24V LiFePO4 aküye uygun voltaj ve akımda şarj edilir.
- **Akü Tipi Uyumluluğu**: Araç aküsü 12V kurşun, yaşam aküsü 24V LiFePO4’tur. DC-DC şarj cihazı bu dönüşümü güvenli şekilde sağlar.
- **Araç Aküsü Float Şarj**: Kampta park halindeyken Victron Blue Smart IP65 12/5A şarj aleti, EasySolar-II **AC OUT 1** çıkışından NJMC1 16A 2P bistable röle ile beslenir. HA otomasyonu ile açılıp kapatılır — shore yokken de inverter üzerinden çalıştırılabilir. Parasitik yüklerden (ECU, alarm, merkezi kilit) kaynaklanan boşalmayı önler.
- **Otomasyon**: Home Assistant ile şarj işlemi, voltaj eşikleri ve hata durumları izlenebilir ve otomasyon tetiklenebilir.

## 🛠️ Ürün Listesi

| Kategori | Ürün | Model/Özellik | Kapasite/Güç | Fiyat Tahmini |
|----------|------|---------------|--------------|---------------|
| **DC-DC Şarj Cihazı** | Victron Orion XS 1400 | 9-35V giriş, 10-35V çıkış, 1-50A ayarlanabilir, IP65, fansız, Bluetooth + VE.Direct, 520g | 1400W sürekli | €350-450 |
| **Kablo ve Sigorta** | H07RN-F, ANL Sigorta | 16mm², 60A | - | €50-80 |
| **Akü İzleme** | Victron SmartShunt veya BMV | Bluetooth, Home Assistant uyumlu | - | €100-150 |
| **Araç Aküsü Float Şarj** | Victron Blue Smart IP65 12/5A + DC connector | 220V AC giriş, 12V/5A çıkış, 7 adımlı akıllı şarj, Bluetooth, IP65, float modda <0.5W | 60W max | €80-120 |

## 🏠 Home Assistant Entegrasyonu

### İzleme Noktaları
- **DC-DC Şarj Durumu**: Akım, voltaj, sıcaklık, hata durumu (Orion XS 1400 Bluetooth + VE.Direct ile)
- **Akü Voltajları**: Araç ve yaşam aküsü voltajı
- **Şarj Akımı**: Anlık ve toplam şarj miktarı

### Otomasyon Senaryoları
- **Şarj Başlatma**: Araç çalıştığında (D+ sinyali veya voltaj eşiği ile) DC-DC şarjı başlat
- **Araç Aküsü Float**: HA otomasyonu araç aküsü voltajını izler, düşerse AC OUT 1 üzerinden Blue Smart IP65 bistable rölesini açar → araç aküsünü float modda tutar. Shore yokken de inverter üzerinden çalışır. Akü voltajı düşerse Bluetooth üzerinden uyarı gönder
- **Aşırı Sıcaklık/Akım**: Hata durumunda şarjı otomatik durdur ve uyarı gönder

### Entegrasyon Yöntemleri
- **Bluetooth**: Victron Connect ile izleme ve temel otomasyon
- **VE.Direct / MQTT**: Home Assistant ile gelişmiş izleme ve otomasyon (Orion XS 1400 VE.Direct destekli)
- **Grafana/InfluxDB**: Geçmiş veri kaydı ve görsel analiz

## 🔧 Kurulum ve Bakım

### Kurulum Aşamaları
1. **DC-DC Şarj Cihazı Montajı**: Alternatör çıkışından ve yaşam aküsüne uygun kablo ile bağlantı
2. **Sigorta ve Kablo**: Her iki uçta uygun sigorta ve kalınlıkta kablo kullanımı
3. **Akü İzleme**: SmartShunt veya BMV ile voltaj/akım izleme
4. **Home Assistant Konfigürasyonu**: İzleme ve otomasyonların tanımlanması

### Bakım Planı
* **Aylık**: Kablo ve bağlantı kontrolü, hata kaydı izleme
* **Mevsimlik**: DC-DC cihazı ve sigorta kontrolü
* **Yıllık**: Akü kapasite testi ve sistem genel bakımı

## 📈 Sistem Performansı

* **Şarj Akımı**: 1-50A (ayarlanabilir)
* **Şarj Gücü**: 1400W sürekli (40°C'ye kadar, üstünde %1.5/°C derating)
* **Verimlilik**: %98.5 (maksimum)
* **Koruma Sınıfı**: IP65, fansız tasarım
* **Bağlantı**: Bluetooth Smart + VE.Direct
* **Güvenlik**: Aşırı akım, aşırı sıcaklık, ters akım korumaları, akıllı alternatör desteği (engine shutdown detection)

## 💡 Ek Görüşler ve Öneriler
- **Araç Aküsü Float Şarj**: Victron Blue Smart IP65 12/5A, EasySolar-II AC OUT 1 üzerinden NJMC1 16A 2P bistable röle ile kontrol edilir. HA otomasyonu ile shore veya inverter modunda çalıştırılabilir. Kampta birkaç gün park halinde araç aküsü boşalmaz.
- **D+ Sinyali**: Şarj işlemini sadece motor çalışırken başlatmak için D+ sinyali veya voltaj algılayıcı kullanılabilir.
- **Akü Tipi Uyumu**: Lityum ve kurşun akü kombinasyonlarında şarj voltajı ve akım limitlerine dikkat edilmeli
- **Kablo Kesiti**: Yüksek akım hatlarında uygun kalınlıkta kablo ve kaliteli bağlantı elemanları kullanılmalı
- **Yedekleme**: Kritik durumlar için manuel bypass veya acil şarj hattı planlanabilir

## ⚡ Elektrik ve Su Tesisatı

- **Enerji:** 12V DC (araç aküsü/alternatör), 24V DC (yaşam aküsü), DC-DC şarj cihazı
- **Araç Aküsü Float:** EasySolar-II AC OUT 1 → NJMC1 16A 2P bistable röle → Blue Smart IP65 12/5A → araç 12V aküsü (HA otomasyonu ile aç/kapa)
- **Kablo ve Sigorta:** Yüksek akım kablosu, ANL sigorta, bağlantı noktaları
- **Araç Aküsü Float:** Victron Blue Smart IP65 12/5A + DC connector, 220V AC → 12V araç aküsü float şarj
- **Otomasyon:** Şarj durumu, voltaj/akım sensörleri, Home Assistant entegrasyonu
- **Su:** Doğrudan bağlantı yok

---

*Bu sistem, seyir halinde alternatörden yaşam aküsüne şarj ve park halinde 220V üzerinden araç aküsünü float modda tutma olmak üzere çift yönlü enerji akışı sağlar.*