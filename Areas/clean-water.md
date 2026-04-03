# Temiz Su Sistemi (Clean Water)

Karavanın tüm temiz su ihtiyacını karşılayan, güvenli, otomasyona uygun ve donmaya karşı korumalı bir altyapı.

## 🎯 Amaç ve Kapsam
- Yeterli hacimde temiz su depolama ve dağıtım
- Su seviyesinin hassas izlenmesi ve otomatik kontrol
- Donma koruması ve otomatik drenaj
- Home Assistant ile merkezi izleme ve otomasyon

## 🛠️ Ürün ve Bileşenler

| Kategori | Ürün/Modül | Özellikler |
|----------|------------|------------|
| **Su Deposu** | Polietilen Temiz Su Tankı | 180L, gıda uyumlu, kolay temizlik |
| **Seviye Sensörü** | RS485 veya analog şamandıra | Hassas seviye ölçümü, Home Assistant entegrasyonu |
| **Pompa** | 24V DC Basınçlı Pompa | Sessiz, yüksek debili, araç içine montaj |
| **Genleşme Kabı** | 24V, balonlu tip | Pompa darbelerini sönümleme, sistem ömrü |
| **Actuator Valf** | 24V otomatik vana | Donma koruması ve otomatik drenaj |

## 🔄 Sistem Kavramsal Yapısı
- 180L temiz su deposu, araç içinde veya izole bölmede
- Seviye sensörü ile anlık su miktarı izlenir
- 24V pompa ve genleşme kabı ile tüm musluklara basınçlı su dağıtımı
- Donma riski durumunda actuator valf ile otomatik drenaj
- Tüm bileşenler Home Assistant üzerinden izlenir ve kontrol edilir

## 🏠 Home Assistant Entegrasyonu
- Su seviyesi, pompa durumu ve valfler merkezi olarak izlenir
- Otomasyon: Düşük seviye uyarısı, donma riski otomatik boşaltma, uzaktan pompa/valf kontrolü
- Enerji ve su tüketimi geçmişi kaydı (Grafana/InfluxDB)

### Tipik Otomasyon Senaryoları
- **Düşük Seviye Uyarısı:** Su seviyesi %10 altına inince bildirim
- **Donma Koruması:** Dış sıcaklık 0°C altına inerse otomatik drenaj
- **Uzaktan Kontrol:** Pompa ve valflerin mobil arayüzden aç/kapatılması
- **Kaçak Tespiti:** Beklenmeyen hızlı seviye düşüşünde alarm

## 🔧 Kurulum ve Bakım
1. **Depo ve Pompa Montajı:** Araç içine sabitlenir, titreşim önleyici bağlantı
2. **Seviye Sensörü ve Valf Montajı:** Depoya uygun şekilde yerleştirilir
3. **Kablolama:** 24V güç ve sensör hatları çekilir
4. **Home Assistant Konfigürasyonu:** Sensör ve aktüatörler tanımlanır, otomasyonlar yazılır

### Bakım Planı
- **Aylık:** Su seviyesi ve bağlantı kontrolü
- **Mevsimlik:** Donma koruması ve valf testi
- **Yıllık:** Depo temizliği ve sistem genel bakımı

## 💡 Ek Görüşler ve Öneriler
- Gıda uyumlu hortum ve bağlantı elemanları kullanılmalı
- Donma riski yüksek bölgelerde depo ve hatlar izole edilmeli
- Su kaçağı sensörü ile ek güvenlik sağlanabilir

## ⚡ Elektrik ve Su Tesisatı

- **Enerji:** 24V DC ana hat (pompa, genleşme kabı, actuator valf)
- **Otomasyon:** Seviye sensörü, valf ve pompa Home Assistant ile entegre
- **Su:** Temiz su girişi, basınçlı dağıtım, gri su çıkışı, otomatik drenaj
- **Sensörler:** Seviye, basınç, kaçak sensörleri önerilir

---

*Bu sistem, karavan için güvenli, hijyenik ve otomasyona uygun bir temiz su altyapısı sunar.* 
