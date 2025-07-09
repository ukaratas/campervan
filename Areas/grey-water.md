# Gri Su Sistemi (Grey Water)

Karavanın mutfak evyesi, duş ve lavabo gibi kaynaklardan gelen atık suyu toplayan, depolayan ve kontrollü şekilde boşaltan sistem.

## 🎯 Hedefler

### Birincil Hedefler
* **Atık Su Toplama**: Evye, duş, lavabo gri suyunu güvenli şekilde toplama
* **Depolama ve İzleme**: Yeterli kapasitede tank ve seviye izleme
* **Kontrollü Boşaltma**: Manuel ve otomatik boşaltma seçenekleri
* **Hijyen ve Güvenlik**: Koku, sızıntı ve donma koruması

### İkincil Hedefler
* **Otomasyon**: Home Assistant ile seviye izleme ve otomatik boşaltma
* **Donma Koruması**: Kış koşullarında sistem koruması
* **Uzaktan İzleme**: Tank doluluk seviyesi ve sistem durumu izleme

## 🔄 Sistem Kavramsal Yapısı

- **Toplama**: Evye, duş, lavabo gri suyu tek bir ana hatta toplanır
- **Depolama**: 100-120L gri su tankı (temiz su tankından daha küçük)
- **Seviye İzleme**: Analog veya dijital seviye sensörü
- **Boşaltma**: Elektrikli pompa ile kontrollü boşaltma
- **Havalandırma**: Tank havalandırma vanası ile koku ve basınç kontrolü

## 🛠️ Ürün Listesi

| Kategori | Ürün | Model/Özellik | Kapasite/Güç | Fiyat Tahmini |
|----------|------|---------------|--------------|---------------|
| **Gri Su Tankı** | Polietilen Atık Su Tankı | 100-120L, koku dirençli | 100-120L | €150-200 |
| **Boşaltma Pompası** | 24V DC Atık Su Pompası | Yüksek debili, katı parçacık geçişli | 24V, 10-15A | €80-150 |
| **Seviye Sensörü** | Analog/Digital Seviye Sensörü | Korozyona dayanıklı, Home Assistant uyumlu | - | €30-60 |
| **Boşaltma Vanası** | Elektrikli/Manuel Vana | Acil boşaltma için, 24V aktüatör | 24V | €50-100 |
| **Havalandırma** | Tank Havalandırma Vanası | Koku ve basınç kontrolü | - | €20-40 |
| **Koku Filtresi** | Karbon Filtre | Havalandırma hattına | - | €15-30 |

## 🏠 Home Assistant Entegrasyonu

### İzleme Noktaları
- **Tank Seviyesi**: Anlık doluluk yüzdesi ve hacim
- **Pompa Durumu**: Çalışma durumu ve akım tüketimi
- **Vana Durumu**: Açık/kapalı durumu

### Otomasyon Senaryoları
- **Yüksek Seviye Uyarısı**: Tank %80 dolduğunda bildirim
- **Otomatik Boşaltma**: Tank %90 dolduğunda pompa çalıştır
- **Donma Koruması**: Dış sıcaklık 2°C altına inerse tankı boşalt
- **Pompa Koruması**: Uzun süreli çalışmada aşırı ısınma koruması

### Entegrasyon Yöntemleri
- **Analog Sensör**: Waveshare analog giriş modülü ile
- **Dijital Sensör**: RS485 üzerinden direkt okuma
- **Pompa Kontrolü**: Röle modülü ile 24V pompa kontrolü

## 🔧 Kurulum ve Bakım

### Kurulum Aşamaları
1. **Tank Montajı**: Araç altında, donma korumalı bölgeye yerleştirme
2. **Pompa ve Vana**: Tank çıkışına pompa ve vana montajı
3. **Seviye Sensörü**: Tank içine veya dışına sensör yerleştirme
4. **Kablolama**: 24V güç ve sinyal hatları
5. **Home Assistant Entegrasyonu**: Sensör ve pompa tanımlamaları

### Bakım Planı
* **Haftalık**: Seviye kontrolü ve pompa testi
* **Aylık**: Tank ve bağlantı kontrolü
* **Mevsimlik**: Donma koruması ve havalandırma testi
* **Yıllık**: Tank temizliği ve sistem genel bakımı

## 📈 Sistem Performansı

* **Tank Kapasitesi**: 100-120L
* **Pompa Debisi**: 20-30L/dk
* **Boşaltma Süresi**: 4-6 dakika (tam tank)
* **Enerji Tüketimi**: 24V 10-15A (çalışma sırasında)

## 💡 Ek Görüşler ve Öneriler

- **Tank Yerleşimi**: Şasi altında, donma korumalı ve kolay erişilebilir
- **Filtre Sistemi**: Evye çıkışında yağ tutucu filtre önerilir
- **Acil Boşaltma**: Manuel vana ile elektriksiz boşaltma imkanı
- **Koku Kontrolü**: Düzenli temizlik ve havalandırma önemli
- **Yasal Gereksinimler**: Boşaltma sadece uygun alanlarda yapılmalı

## ⚡ Elektrik ve Su Tesisatı

- **Enerji**: 24V DC ana hat (pompa, vana, sensörler)
- **Su Hatları**: Gri su toplama, boşaltma, havalandırma
- **Otomasyon**: Seviye sensörü, pompa ve vana Home Assistant entegrasyonu
- **Sensörler**: Seviye, sıcaklık, kaçak sensörleri önerilir

---

*Bu sistem, karavan hijyeni ve konfor için güvenli, otomasyona uygun gri su yönetimi sunar.* 