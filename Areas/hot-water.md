# Sıcak Su Tesisatı

Karavana gerektiğinde sıcak su sağlamak için kullanılacak tesisatın bütününü kapsar. Bu sistem, konfor ve hijyen açısından kritik öneme sahip olup, farklı enerji kaynaklarından faydalanarak optimize edilmiş bir çözüm sunar.

## 🎯 Hedefler

### Birincil Hedefler
* **Motor Entegrasyonu**: Motor çalışır durumda iken motor radyatör suyunu boiler içindeki heat exchanger'dan geçirerek ısıtma sağlamak
* **Elektriksel Isıtma**: 220V ile isıtma (shore power mevcut ise doğrudan, yoksa inverter üzerinden)
* **Sıcaklık Kontrolü**: Sıcak su çıkışını tüm karavan içinde maksimum belirlenen sıcaklıkta (hedef: 37°C) sağlamak

### İkincil Hedefler
* **Enerji Verimliliği**: Yakıt tüketimini minimize ederek sıcak su üretimi
* **Donma Koruması**: Kış koşullarında sistemin hasar görmesini önleme
* **Otomasyon**: Kullanıcı müdahalesi gerektirmeden optimal çalışma

## 🛠️ Ürün Listesi

| Kategori | Ürün | Model/Özellik | Güç/Kapasite | Fiyat Tahmini |
|----------|------|---------------|---------------|---------------|
| **Ana Boiler** | Quick Nautic Boiler B3 | 20L, Marine Grade | 220V, 1200W | €200-250 |
| **Devirdaim Sistemi** | Basit Su Devirdaim Pompası | Motor radyatör suyu dolaşımı | 24V DC, 3-5A | €30-60 |
| **Sıcaklık Kontrolü** | Termostatik Karıştırma Vanası | Ayarlanabilir çıkış sıcaklığı | 35-60°C | €80-120 |
| **Donma Koruması** | Otomatik Boşaltma Vanası | Elektromanyetik vana | 24V DC | €60-100 |
| **Sensörler** | Su Sıcaklığı Sensörü | PT100/NTC tip | -50°C/+150°C | €25-40 |
| **Kontrol** | Akıllı Röle/Termostat | DI/DO veya RS485 ile kontrol | 24V DC | €100-150 |

## 🏠 Home Assistant Entegrasyonu

### Akıllı Senaryolar

#### 🌡️ **Sıcaklık Yönetimi**
* **Motor Suyu Sensörü**: Motor suyu sıcaklığı eşik değerin üstünde ise (örn: 80°C) devirdaim pompasını çalıştır
* **Hedef Sıcaklık Kontrolü**: Boiler suyu hedef sıcaklığa ulaştığında (37°C) devirdaim pompasını durdur
* **Aşırı Isınma Koruması**: Boiler sıcaklığı 65°C'yi aşarsa acil güvenlik durdurması

#### ❄️ **Donma Koruması**
* **Otomatik Boşaltma**: Dış sıcaklık 0°C'ye düştüğünde donmaya karşı sıcak su hattını boşalt
* **Ön Isıtma**: Dış sıcaklık 5°C'nin altına düştüğünde sistem hazırlık moduna geç
* **Kritik Uyarı**: Donma riski yüksek olduğunda kullanıcıya bildirim gönder

#### ⚡ **Enerji Optimizasyonu**
* **Güç Kaynağı Önceliği**: Shore power mevcut ise elektriksel ısıtmayı tercih et
* **Batarya Koruma**: Batarya seviyesi %30'un altında ise sadece motor çalışırken ısıt
* **Zaman Tabanlı Kontrol**: Kullanım saatlerine göre önceden ısıtma

### 📊 Sensör Altyapısı

#### Donanım Sensörleri
* **OBD Entegrasyonu**: Motor suyu sıcaklığı ve çalışma durumu
* **Dış Hava Sıcaklığı**: Meteoroloji sensörü veya API entegrasyonu
* **Boiler İç Sıcaklığı**: Hassas sıcaklık ölçümü için PT100 sensörü
* **Su Basıncı**: Sistem sağlığı ve sızıntı tespiti
* **Pompa Durum Feedback**: Çalışma durumu ve arıza tespiti

#### Yazılım Entegrasyonu
* **DI/DO veya RS485**: Tüm sensör ve aktüatörler mümkün olduğunda doğrudan kablolu olarak bağlanır
* **Raspberry Pi Üzerinde Home Assistant**: Tüm sistem merkezi olarak Raspberry Pi üzerinde çalışan Home Assistant ile kontrol edilir
* **MQTT/Modbus**: Gerekirse RS485 üzerinden Modbus veya benzeri protokollerle veri iletimi
* **InfluxDB**: Geçmiş veri analizi ve trend takibi
* **Grafana Dashboard**: Görsel izleme ve raporlama

## 🔧 Kurulum ve Bakım

### Kurulum Aşamaları
1. **Mekanik Montaj**: Boiler, pompalar ve vanaların yerleşimi
2. **Hidrolik Bağlantılar**: Su hatlarının bağlanması ve test edilmesi
3. **Elektrik Bağlantıları**: 24V ve 220V güç hatlarının kurulumu
4. **Sensör Montajı**: Tüm ölçüm noktalarının kalibrasyonu
5. **Yazılım Konfigürasyonu**: Home Assistant entegrasyonu ve test

### Bakım Planı
* **Haftalık**: Sistem çalışma kontrolü ve sıcaklık testleri
* **Aylık**: Su kalitesi kontrolü ve filtre değişimi
* **Mevsimlik**: Donma koruması test ve kış hazırlığı
* **Yıllık**: Komple sistem bakımı ve performans optimizasyonu

## 📈 Sistem Performansı

### Beklenen Verimlilik
* **Isıtma Süresi**: 20L su için 15-20 dakika (motor çalışırken)
* **Enerji Tüketimi**: 1.2kW elektrik veya motor atık ısısı
* **Sıcaklık Stabilitesi**: ±2°C hassasiyetle kontrol
* **Donma Koruması**: -20°C'ye kadar güvenli çalışma

## 🔄 Devre Bağımsızlığı ve Güvenlik

Motorun orijinal soğutma devresi (radyatör ve motorun kendi su pompası) ile boyler devresi birbirinden bağımsızdır. Boyler devresi, motordan alınan sıcak suyun ayrı bir hat üzerinden boylerin içindeki ısı eşanjöründen geçirilmesiyle çalışır. 

- **Boyler devirdaim pompası** sadece boyler hattında suyun dolaşmasını sağlar. Bu pompa çalışmazsa, yalnızca boyler hattında su dolaşmaz ve boyler ısınmaz.
- **Motorun ana soğutma devresi** ise, her zaman güvenli şekilde çalışmaya devam eder ve motorun aşırı ısınmasını önler. Boyler devresindeki pompanın durması, motorun ana devresini hiçbir şekilde etkilemez.
- Bu sayede, boyler devresi bakım veya arıza durumunda devre dışı kalsa bile aracın motor soğutma sistemi tam güvenli şekilde çalışır.

## ⚡ Elektrik ve Su Tesisatı

- **Enerji:** 220V AC (boiler), 24V DC (devirdaim pompası, otomatik vana, sensörler)
- **Otomasyon:** Sıcaklık, basınç, seviye sensörleri, Home Assistant entegrasyonu
- **Su:** Temiz su girişi, sıcak su çıkışı, motor suyu hattı, otomatik boşaltma
- **Sensörler:** Sıcaklık, basınç, kaçak sensörleri önerilir

---

*Bu sistem, modern karavan konfor standartlarına uygun, enerji verimli ve tamamen otomatik sıcak su çözümü sunar.*