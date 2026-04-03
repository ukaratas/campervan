# Mutfak Modülü (Kitchen)

Karavanın konforlu, fonksiyonel ve otomasyona uygun mutfak alanı. Tüm cihazlar, enerji ve su altyapısı ile entegre çalışır.

## 🎯 Amaç ve Kapsam
- Kompakt ve verimli mutfak alanı
- Sıcak/soğuk su, 24V ve 220V enerji altyapısı
- Otomasyon ve merkezi kontrol
- İki buzdolabı: biri tezgah içinde (Eva Berlin), biri kanepe altında çekmeceli (Evacool D31 R)

## 🛠️ Ürünler ve Teknik Özellikler

| Kategori | Ürün/Model | Özellikler |
|----------|------------|------------|
| **Ocak** | Thetford Induction Hob | Ankastre indüksiyon, 220V besleme |
| **Buzdolabı 1** | Evacool Eva Berlin 90Lt | 24V DC, 418x485x975mm, çift yönlü kapı, mutfak tezgahı içinde |
| **Buzdolabı 2** | Evacool D31 R Çekmeceli | 24V DC, çekmeceli tip, kanepe altında |
| **Evye** | Thetford Argent Sink | 63x47cm, sıcak/soğuk su, termostatik vana ile sabit ılık su |
| **Bulaşık Makinesi** | Electrolux ESF2400O | 220V, ankastre, tezgah içinde |
| **Prizler** | 2x220V, 1x12V | Tezgah üstü, portatif cihazlar için |
| **USB Şarj** | 2x otomotiv USB-C soket | 24V giriş, 100W PD, tezgah üstü |
| **Aydınlatma** | 24V mutfak aydınlatma | Waveshare relay (Modbus) ile kontrol |
| **Push Button** | 1 adet | DI → HA → Waveshare relay (Modbus), mutfak aydınlatma |
| **Üst Dolap** | Modüler, tezgah üstü | Ek depolama |

## 🗺️ Yerleşim ve Fonksiyonel Detaylar
- Tezgah, arka yataktan giriş kapısına kadar yekpare
- Buzdolabı 1 (Eva Berlin 90Lt) mutfak tezgahı içinde
- Buzdolabı 2 (Evacool D31 R Çekmeceli) kanepe altında
- Thetford Argent Sink 63x47cm evye, termostatik vanadan sabitlenmiş sıcak/soğuk su
- Bulaşık makinesi tezgah içinde, ankastre
- Üstte HDMI dokunmatik ekran (Home Assistant arayüzü, IPCBOX-CM5 HDMI çıkışı)
- Üst dolap ve dolap altı spot aydınlatma

## ⚡ Elektrik ve Su Tesisatı
- **Bulaşık makinesi:** 220V enerji, gri su çıkışı
- **Buzdolabı 1 (Eva Berlin):** 24V enerji (mutfak tezgahı içinde)
- **Buzdolabı 2 (Evacool D31 R):** 24V enerji (kanepe altında)
- **Evye:** Thetford Argent Sink 63x47cm, temiz su girişi, gri su çıkışı
- **Ocak:** 220V enerji (Thetford Induction Hob ankastre indüksiyon)
- **Prizler:** 2x220V, 1x12V (tezgah üstü)
- **USB Şarj:** 2x otomotiv USB-C soket (24V giriş, 100W PD)
- **Aydınlatma:** 24V mutfak aydınlatma, push button + Waveshare relay (Modbus) ile kontrol

## 🏠 Otomasyon ve Home Assistant Entegrasyonu
- Push button DI'ya bağlı; akış DI → HA → Waveshare relay (Modbus) ile aydınlatma kontrol edilir
- Röle/kanal durumu Waveshare Modbus modüllerinde yerleşik; ayrı DI feedback gerekmez
- Tüm prizler, aydınlatma ve cihazlar merkezi olarak izlenebilir ve otomasyona açıktır
- Enerji tüketimi ve su kullanımı izlenebilir

### Tipik Otomasyon Senaryoları
- **Aydınlatma:** Push button ile aç/kapat, zamanlayıcı veya ortam sensörüne göre otomatik
- **Enerji Yönetimi:** İndüksiyon ocak (Thetford), bulaşık makinesi ve iki buzdolabı enerji tüketimi izleme
- **Yük Yönetimi:** İndüksiyon ocak + bulaşık makinesi toplam güç > 3000W inverter → eş zamanlı çalışmayı Home Assistant otomasyonu ile önle. Shore modunda serbest.
- **Su Yönetimi:** Evye ve bulaşık makinesi su kullanımı izleme

## 🔧 Kurulum ve Bakım
1. **Modül Montajı:** Tezgah, dolap ve cihazların sabitlenmesi
2. **Elektrik ve Su Bağlantıları:** Priz, cihaz ve aydınlatma hatlarının çekilmesi
3. **Otomasyon Entegrasyonu:** Waveshare relay modüllerinin Home Assistant’a tanımlanması
4. **Test ve Devreye Alma:** Tüm fonksiyonların kontrolü

### Bakım Planı
- **Aylık:** Priz, cihaz ve aydınlatma kontrolü
- **Mevsimlik:** Su ve elektrik bağlantı noktalarının gözden geçirilmesi
- **Yıllık:** Cihaz bakımı ve temizlik

## 💡 Ek Öneriler ve Sistem Entegrasyonları
- Thetford Induction Hob 220V ile çalıştığı için enerji verimliliği yüksek ve hızlı ısınma sağlar
- Gri su çıkış çapı ve bağlantısı, temiz su sistemiyle uyumlu olmalı
- Tüm cihazlar ve prizler Home Assistant ile izlenebilir ve otomasyona uygun olmalı
- Üst dolap ve tezgah altı depolama ileride modüler olarak genişletilebilir

---

*Bu mutfak modülü, iki buzdolabı (Eva Berlin tezgah içi + Evacool D31 R kanepe altı çekmeceli), Thetford evye ve indüksiyon ocak ile karavan yaşamında maksimum konfor, enerji verimliliği ve otomasyon sunar.*



