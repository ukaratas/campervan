# Mutfak Modülü (Kitchen)

Karavanın konforlu, fonksiyonel ve otomasyona uygun mutfak alanı. Tüm cihazlar, enerji ve su altyapısı ile entegre çalışır.

## 🎯 Amaç ve Kapsam
- Kompakt ve verimli mutfak alanı
- Sıcak/soğuk su, 24V ve 220V enerji altyapısı
- Otomasyon ve merkezi kontrol
- Hem araç içinden hem dışından erişilebilen buzdolabı

## 🛠️ Ürünler ve Teknik Özellikler

| Kategori | Ürün/Model | Özellikler |
|----------|------------|------------|
| **Ocak** | Omake Ankastre İndüksiyon | 1800W, ankastre, 220V besleme |
| **Buzdolabı** | EvaCool Eva Berlin 90Lt | 24V DC, 418x485x975mm, çift yönlü kapı |
| **Evye** | Paslanmaz çelik, tek musluk | Sıcak/soğuk su, termostatik vana ile sabit ılık su |
| **Bulaşık Makinesi** | Elektrolux ESF2400O | 220V, ankastre, tezgah altı |
| **Prizler** | 2x220V, 1x12V | Tezgah üstü, portatif cihazlar için |
| **USB Şarj** | 2x otomotiv USB-C soket | 24V giriş, 100W PD, tezgah üstü |
| **Aydınlatma** | 24V mutfak aydınlatma | NJMC1 16A 2P bistable röle ile kontrol |
| **Push Button** | 1 adet | Waveshare DI → HA → DO → bistable röle, mutfak aydınlatma |
| **Üst Dolap** | Modüler, tezgah üstü | Ek depolama |

## 🗺️ Yerleşim ve Fonksiyonel Detaylar
- Tezgah, arka yataktan giriş kapısına kadar yekpare
- Buzdolabı tezgah altında, kapısı hem içe hem dışa açılır (kayarlı kapı yanında)
- Evye tek musluklu, sıcak/soğuk su termostatik vanadan sabitlenmiş
- Bulaşık makinesi tezgah altında, ankastre
- Üstte HDMI dokunmatik ekran (Home Assistant arayüzü, IPCBOX-CM5 HDMI çıkışı)
- Üst dolap ve dolap altı spot aydınlatma

## ⚡ Elektrik ve Su Tesisatı
- **Bulaşık makinesi:** 220V enerji, gri su çıkışı
- **Buzdolabı:** 24V enerji
- **Evye:** Temiz su girişi, gri su çıkışı
- **Ocak:** 220V enerji (1800W Omake ankastre indüksiyon ocak)
- **Prizler:** 2x220V, 1x12V (tezgah üstü)
- **USB Şarj:** 2x otomotiv USB-C soket (24V giriş, 100W PD)
- **Aydınlatma:** 24V mutfak aydınlatma, push button + NJMC1 bistable röle ile kontrol

## 🏠 Otomasyon ve Home Assistant Entegrasyonu
- Push button Waveshare DI'ya bağlı, HA algılar ve DO üzerinden bistable röleyi toggle eder
- Röle durum feedback: Waveshare DI ile Home Assistant entegrasyonu
- Tüm prizler, aydınlatma ve cihazlar merkezi olarak izlenebilir ve otomasyona açıktır
- Enerji tüketimi ve su kullanımı izlenebilir

### Tipik Otomasyon Senaryoları
- **Aydınlatma:** Push button ile aç/kapat, zamanlayıcı veya ortam sensörüne göre otomatik
- **Enerji Yönetimi:** İndüksiyon ocak (1800W), bulaşık makinesi ve buzdolabı enerji tüketimi izleme
- **Yük Yönetimi:** İndüksiyon ocak (1800W) + bulaşık makinesi (1700W) = 3500W > 3000W inverter → eş zamanlı çalışmayı Home Assistant otomasyonu ile önle. Shore modunda serbest.
- **Su Yönetimi:** Evye ve bulaşık makinesi su kullanımı izleme

## 🔧 Kurulum ve Bakım
1. **Modül Montajı:** Tezgah, dolap ve cihazların sabitlenmesi
2. **Elektrik ve Su Bağlantıları:** Priz, cihaz ve aydınlatma hatlarının çekilmesi
3. **Otomasyon Entegrasyonu:** Bistable röle ve DI/DO modüllerinin Home Assistant’a tanımlanması
4. **Test ve Devreye Alma:** Tüm fonksiyonların kontrolü

### Bakım Planı
- **Aylık:** Priz, cihaz ve aydınlatma kontrolü
- **Mevsimlik:** Su ve elektrik bağlantı noktalarının gözden geçirilmesi
- **Yıllık:** Cihaz bakımı ve temizlik

## 💡 Ek Öneriler ve Sistem Entegrasyonları
- İndüksiyon ocak 220V ile çalıştığı için enerji verimliliği yüksek ve hızlı ısınma sağlar
- Gri su çıkış çapı ve bağlantısı, temiz su sistemiyle uyumlu olmalı
- Tüm cihazlar ve prizler Home Assistant ile izlenebilir ve otomasyona uygun olmalı
- Üst dolap ve tezgah altı depolama ileride modüler olarak genişletilebilir

---

*Bu mutfak modülü, karavan yaşamında maksimum konfor, enerji verimliliği ve otomasyon sunar.*



