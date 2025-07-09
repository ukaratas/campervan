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
| **Ocak** | Wallas 1200D | Dizel, cam üst, 12V besleme |
| **Buzdolabı** | EvaCool Eva Berlin 90Lt | 24V DC, 418x485x975mm, çift yönlü kapı |
| **Evye** | Paslanmaz çelik, tek musluk | Sıcak/soğuk su, termostatik vana ile sabit ılık su |
| **Bulaşık Makinesi** | Elektrolux ESF2400O | 220V, ankastre, tezgah altı |
| **Prizler** | 2x220V, 2x24V, 1x12V | Tezgah üstü, portatif cihazlar için |
| **Aydınlatma** | 24V spot ve LED şerit | Dolap altı ve oturma grubu dahil |
| **Push Button** | 3 adet, Waveshare DI | Aydınlatma otomasyonu için |
| **Üst Dolap** | Modüler, tezgah üstü | Ek depolama |

## 🗺️ Yerleşim ve Fonksiyonel Detaylar
- Tezgah, arka yataktan giriş kapısına kadar yekpare
- Buzdolabı tezgah altında, kapısı hem içe hem dışa açılır (kayarlı kapı yanında)
- Evye tek musluklu, sıcak/soğuk su termostatik vanadan sabitlenmiş
- Bulaşık makinesi tezgah altında, ankastre
- Üstte dokunmatik Raspberry Pi ekranı (Home Assistant arayüzü)
- Üst dolap ve dolap altı spot aydınlatma

## ⚡ Elektrik ve Su Tesisatı
- **Bulaşık makinesi:** 220V enerji, gri su çıkışı
- **Buzdolabı:** 24V enerji
- **Evye:** Temiz su girişi, gri su çıkışı
- **Ocak:** 12V enerji (24V to 12V DC konvertör ile, 20-30A kapasiteli; detay battery-pack dosyasında)
- **Prizler:** 2x220V, 2x24V, 1x12V (tezgah üstü)
- **Aydınlatma:** 24V spot ve LED şerit, push button ile otomasyon

## 🏠 Otomasyon ve Home Assistant Entegrasyonu
- Push button’lar Waveshare DI ile Home Assistant’a bağlı, aydınlatma röleleri üzerinden kontrol
- Tüm prizler, aydınlatma ve cihazlar merkezi olarak izlenebilir ve otomasyona açıktır
- Enerji tüketimi ve su kullanımı izlenebilir

### Tipik Otomasyon Senaryoları
- **Aydınlatma:** Push button ile aç/kapat, zamanlayıcı veya ortam sensörüne göre otomatik
- **Enerji Yönetimi:** Bulaşık makinesi ve buzdolabı enerji tüketimi izleme
- **Su Yönetimi:** Evye ve bulaşık makinesi su kullanımı izleme

## 🔧 Kurulum ve Bakım
1. **Modül Montajı:** Tezgah, dolap ve cihazların sabitlenmesi
2. **Elektrik ve Su Bağlantıları:** Priz, cihaz ve aydınlatma hatlarının çekilmesi
3. **Otomasyon Entegrasyonu:** Push button ve rölelerin Home Assistant’a tanımlanması
4. **Test ve Devreye Alma:** Tüm fonksiyonların kontrolü

### Bakım Planı
- **Aylık:** Priz, cihaz ve aydınlatma kontrolü
- **Mevsimlik:** Su ve elektrik bağlantı noktalarının gözden geçirilmesi
- **Yıllık:** Cihaz bakımı ve temizlik

## 💡 Ek Öneriler ve Sistem Entegrasyonları
- 24V to 12V DC konvertör, battery-pack modülünde detaylandırılmalı
- Gri su çıkış çapı ve bağlantısı, temiz su sistemiyle uyumlu olmalı
- Tüm cihazlar ve prizler Home Assistant ile izlenebilir ve otomasyona uygun olmalı
- Üst dolap ve tezgah altı depolama ileride modüler olarak genişletilebilir

---

*Bu mutfak modülü, karavan yaşamında maksimum konfor, enerji verimliliği ve otomasyon sunar.*



