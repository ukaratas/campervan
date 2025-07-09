# DC-DC Alternatör Şarj Sistemi

Araç çalışırken alternatörden yaşam aküsüne (24V LiFePO4) güvenli ve kontrollü şarj sağlamak için tasarlanmış sistemdir. Aynı zamanda, ihtiyaç halinde yaşam aküsünden araç marş aküsüne destek şarjı da planlanmaktadır.

## 🎯 Hedefler

### Birincil Hedefler
* **Alternatör ile Şarj**: Araç çalışırken alternatörden, DC-DC şarj cihazı ile yaşam aküsünü (24V LiFePO4) güvenli şekilde şarj etmek
* **Akü Tipi Uyumluluğu**: 12V kurşun araç aküsü ve 24V LiFePO4 yaşam aküsü arasında tam uyum
* **Otomatik Kontrol**: Şarj işleminin voltaj ve akım limitleriyle otomatik yönetilmesi

### İkincil Hedefler
* **Marş Aküsüne Destek**: Araç aküsü belirli bir voltajın altına düştüğünde, yaşam aküsünden marş aküsüne destek şarjı (manuel veya otomatik)
* **Otomasyon ve İzleme**: Home Assistant ile şarj durumu, akım, voltaj ve hata izleme
* **Güvenlik**: Aşırı akım, aşırı sıcaklık ve ters akım koruması

## 🔄 Sistem Kavramsal Yapısı ve Güvenlik

- **DC-DC Şarj Cihazı**: Alternatör çıkışından alınan 12V DC, Victron Orion XS 12/24-50 gibi bir DC-DC şarj cihazı ile 24V LiFePO4 aküye uygun voltaj ve akımda şarj edilir.
- **Akü Tipi Uyumluluğu**: Araç aküsü 12V kurşun, yaşam aküsü 24V LiFePO4’tur. DC-DC şarj cihazı bu dönüşümü güvenli şekilde sağlar.
- **Bidirectional (Çift Yönlü) Şarj**: Victron Orion XS serisinde çift yönlü şarj özelliği yoktur. Marş aküsüne destek için ek bir cihaz veya manuel anahtarlama gerekir.
- **Otomasyon**: Home Assistant ile şarj işlemi, voltaj eşikleri ve hata durumları izlenebilir ve otomasyon tetiklenebilir.

## 🛠️ Ürün Listesi

| Kategori | Ürün | Model/Özellik | Kapasite/Güç | Fiyat Tahmini |
|----------|------|---------------|--------------|---------------|
| **DC-DC Şarj Cihazı** | Victron Orion XS 12/24-50 | 12V→24V, 50A, LiFePO4 uyumlu, izlenebilir | 1200W | €350-450 |
| **Kablo ve Sigorta** | H07RN-F, ANL Sigorta | 16mm², 60A | - | €50-80 |
| **Akü İzleme** | Victron SmartShunt veya BMV | Bluetooth, Home Assistant uyumlu | - | €100-150 |
| **Yedek Şarj Cihazı** | (Opsiyonel) | Yaşam aküsünden marş aküsüne DC-DC charger | 12V, 10-20A | €80-150 |

## 🏠 Home Assistant Entegrasyonu

### İzleme Noktaları
- **DC-DC Şarj Durumu**: Akım, voltaj, sıcaklık, hata durumu (Orion XS Bluetooth veya Modbus ile)
- **Akü Voltajları**: Araç ve yaşam aküsü voltajı
- **Şarj Akımı**: Anlık ve toplam şarj miktarı

### Otomasyon Senaryoları
- **Şarj Başlatma**: Araç çalıştığında (D+ sinyali veya voltaj eşiği ile) DC-DC şarjı başlat
- **Marş Aküsü Desteği**: Araç aküsü 12.4V altına düştüğünde, yaşam aküsünden destek şarjı başlat (manuel veya otomatik anahtarlama ile)
- **Aşırı Sıcaklık/Akım**: Hata durumunda şarjı otomatik durdur ve uyarı gönder

### Entegrasyon Yöntemleri
- **Bluetooth**: Victron Connect ile izleme ve temel otomasyon
- **Modbus/MQTT**: Home Assistant ile gelişmiş izleme ve otomasyon (Orion XS destekliyorsa)
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

* **Şarj Akımı**: 50A (maksimum, ayarlanabilir)
* **Şarj Gücü**: 1200W (maksimum)
* **Verimlilik**: %95+
* **Güvenlik**: Aşırı akım, aşırı sıcaklık, ters akım korumaları

## 💡 Ek Görüşler ve Öneriler
- **Bidirectional Şarj**: Victron Orion XS serisinde çift yönlü şarj yoktur. Marş aküsüne destek için ayrı bir DC-DC charger veya manuel anahtarlama gerekir.
- **D+ Sinyali**: Şarj işlemini sadece motor çalışırken başlatmak için D+ sinyali veya voltaj algılayıcı kullanılabilir.
- **Akü Tipi Uyumu**: Lityum ve kurşun akü kombinasyonlarında şarj voltajı ve akım limitlerine dikkat edilmeli
- **Kablo Kesiti**: Yüksek akım hatlarında uygun kalınlıkta kablo ve kaliteli bağlantı elemanları kullanılmalı
- **Yedekleme**: Kritik durumlar için manuel bypass veya acil şarj hattı planlanabilir

## ⚡ Elektrik ve Su Tesisatı

- **Enerji:** 12V DC (araç aküsü/alternatör), 24V DC (yaşam aküsü), DC-DC şarj cihazı
- **Kablo ve Sigorta:** Yüksek akım kablosu, ANL sigorta, bağlantı noktaları
- **Otomasyon:** Şarj durumu, voltaj/akım sensörleri, Home Assistant entegrasyonu
- **Su:** Doğrudan bağlantı yok

---

*Bu sistem, karavan alternatöründen yaşam aküsüne güvenli, verimli ve otomasyona uygun şarj çözümü sunar.*