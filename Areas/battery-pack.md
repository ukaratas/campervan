# Batarya Grubu (Battery Pack)

Karavanın tüm elektrik ihtiyacını karşılayacak ana enerji kaynağıdır. Yüksek kapasiteli LiFePO4 prizmatik hücreler ve akıllı BMS ile, güvenli, uzun ömürlü ve otomasyona uygun bir enerji altyapısı sağlar.

## 🎯 Hedefler

### Birincil Hedefler
* **24V Sistem**: Tüm karavan altyapısı için 24V DC baz voltaj kullanılır. Bu, daha düşük akım, daha az kablo kaybı ve daha yüksek güvenlik sağlar.
* **Yüksek Kapasite**: 8 adet 3.2V 280Ah EVE prizmatik hücre ile toplamda 24V 280Ah (yaklaşık 7kWh) kapasite hedeflenir.
* **Akıllı BMS**: Yüksek akım destekli, RS485/CanBus haberleşmeli, uzaktan izlenebilir ve kontrol edilebilir BMS kullanılır. BMS, 3000W inverter ve yüksek anlık akım çekişlerini destekler.

### İkincil Hedefler
* **Tükenme Koruması**: Batarya %5 SOC altına düştüğünde sistemi otomatik olarak kapatacak otomasyon
* **Otomasyon ve İzleme**: Home Assistant ile tam entegre, kullanıcı müdahalesi olmadan güvenli ve verimli çalışma
* **Genişletilebilirlik**: İleride kapasite artırımı veya paralel batarya eklenmesine uygun altyapı

## 🔄 Sistem Kavramsal Yapısı ve Güvenlik

- **LiFePO4 prizmatik hücreler** yüksek çevrim ömrü ve termal güvenlik sunar.
- **BMS (Battery Management System)** hücre dengeleme, aşırı akım/gerilim/ısı koruması ve iletişim sağlar.
- **24V altyapı** ile karavanın tüm DC yükleri ve enerji yönetimi doğrudan beslenir.
- **Ana sigorta ve kontaktör** ile acil durumda tüm sistemi izole etmek mümkündür.
- **BMS üzerinden RS485/CanBus ile Home Assistant’a veri aktarımı ve otomasyon tetikleme** mümkündür.
- **Güneş paneli çıkışı doğrudan EasySolar-II'nin entegre MPPT girişine bağlanır.**

## 🛠️ Ürün Listesi

| Kategori | Ürün | Model/Özellik | Kapasite/Güç | Fiyat Tahmini |
|----------|------|---------------|--------------|---------------|
| **Hücre** | EVE LiFePO4 Prizmatik | 3.2V 280Ah | 8 adet | $800-1000 |
| **BMS** | JBD/Overkill Solar Akıllı BMS | 8S 24V, 200A, RS485/CanBus, Bluetooth | 24V, 200A | $120-200 |
| **Ana Sigorta** | MEGA/ANL Sigorta | 200A | 1 adet | $10-20 |
| **Kontaktör** | 24V DC Ana Kontaktör | Uzaktan açma/kapama | 200A | $30-50 |
| **Sensörler** | Akım/gerilim/sıcaklık sensörleri | Hall effect/NTC/PT100 | - | $20-40 |

## 🏠 Home Assistant Entegrasyonu

### İzleme Noktaları
- **BMS RS485/CanBus**: Hücre voltajları, toplam voltaj, akım, sıcaklık, SOC, hata durumları
- **Ana Sigorta/Kontaktör**: Açık/kapalı durumu, otomatik izole
- **EasySolar-II GX**: Tüm AC ve güneş enerjisi akışı tek cihazdan izlenir

### Otomasyon Senaryoları
- **Düşük SOC Otomasyonu**: Batarya %5 altına inerse kritik yükleri kapat, kullanıcıya uyarı gönder
- **Aşırı Akım/Sıcaklık**: BMS hata durumunda sistemi izole et, alarm tetikle
- **Uzaktan İzleme**: Home Assistant arayüzünden tüm değerleri canlı izle, geçmiş verileri kaydet
- **Enerji Optimizasyonu**: Güneş enerjisiyle şarj önceliği, şebeke/şarj cihazı otomasyonu

### Entegrasyon Yöntemleri
- **Modbus/RS485**: ESPHome veya USB-RS485 dönüştürücü ile Home Assistant’a veri aktarımı
- **Grafana/InfluxDB**: Geçmiş veri kaydı ve görsel analiz

## 🔧 Kurulum ve Bakım

### Kurulum Aşamaları
1. **Hücrelerin Dizilimi**: 8S seri bağlantı, mekanik sabitleme ve izole
2. **BMS Montajı**: Tüm hücrelere balans kabloları ve ana akım bağlantısı
3. **Sigorta ve Kontaktör**: Ana hatta sigorta ve kontaktör montajı
4. **Sensör ve Haberleşme**: RS485/CanBus/MQTT entegrasyonu
5. **Güneş Paneli Bağlantısı**: Esnek 400W panel doğrudan EasySolar-II MPPT girişine bağlanır
6. **Home Assistant Konfigürasyonu**: Sensörlerin ve otomasyonların tanımlanması

### Bakım Planı
* **Aylık**: Hücre voltajı ve bağlantı kontrolü
* **Mevsimlik**: BMS ve bağlantı noktalarının gözden geçirilmesi
* **Yıllık**: Kapasite testi ve sistem genel bakımı

## 📈 Sistem Performansı

* **Kapasite**: 24V 280Ah (yaklaşık 7kWh)
* **Maksimum Sürekli Akım**: 200A (4.8kW)
* **Beklenen Ömür**: 3000+ çevrim (10 yıl+)
* **Şarj/Deşarj Verimliliği**: %95+
* **Güvenlik**: Aşırı akım, aşırı sıcaklık, düşük voltaj korumaları

## 💡 Ek Görüşler ve Öneriler
- **Yedekleme**: Kritik yükler için ayrı bir DC-DC yedek besleme hattı planlanabilir
- **Genişleme**: Paralel batarya eklenmesi için BMS ve kablolama uygun seçilmeli
- **Yangın Güvenliği**: Batarya bölmesinde duman dedektörü ve havalandırma önerilir
- **Acil İzolasyon**: Ana kontaktör Home Assistant veya acil buton ile uzaktan kapatılabilir
- **Kablo Kesiti**: Yüksek akım hatlarında uygun kalınlıkta kablo ve kaliteli bağlantı elemanları kullanılmalı

---

*Bu sistem, EasySolar-II ile tüm AC ve güneş enerjisi altyapısını tek cihazda birleştirerek, güvenli, akıllı ve ölçeklenebilir bir batarya çözümü sunar.*