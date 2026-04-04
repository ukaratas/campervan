# Karavan Geliştirme Planı

Iveco Daily / MAN TGE 18m³ karavan dönüşüm projesi için sıralı iş planı ve malzeme listeleri (BOM).

Her adımda:
- **Bağımlılık**: Hangi adım(lar)dan sonra başlayabilir
- **BOM Tablosu**: Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı

## Outline

| # | İş | Bağımlılık |
|---|----|------------|
| **1 — Hazırlık** | | |
| [1.1](#11--otomasyon-geliştirme) | Otomasyon Geliştirme | — |
| [1.2](#12--alet-ve-atölye-tedariği) | Alet ve Atölye Tedariği | — |
| **2 — Araç** | | |
| [2.1](#21--araç-alımı) | Araç Alımı | — |
| **3 — Karkas İnşaat** | | |
| [3.1](#31--sigma-profil-i̇skelet-mobilya) | Sigma Profil İskelet (mobilya) | 2.1 |
| [3.2](#32--zemin-geliştirme) | Zemin Geliştirme | 2.1, 3.1 |
| [3.3](#33--su-depoları-şasi-altı) | Su Depoları (şasi altı) | 2.1 |
| **4 — Kabuk İşleri** | | |
| [4.1](#41--pencere-kesim-ve-montaj) | Pencere Kesim ve Montaj | 3.1 |
| [4.2](#42--tavan-klima-montajı) | Tavan Klima Montajı | 4.1 |
| [4.3](#43--çatı-ray-sistemi) | Çatı Ray Sistemi (OEM kanal) | 4.2 |
| [4.4](#44--güneş-paneli-montajı) | Güneş Paneli Montajı | 4.3 |
| [4.5](#45--tente-montajı) | Tente Montajı | 4.3 |
| [4.6](#46--kamera-montajı) | Kamera Montajı | 3.1 |
| **5 — İç Hazırlık** | | |
| [5.1](#51--yalıtım) | Yalıtım (duvar + tavan) | 4.1, 4.2 |
| [5.2](#52--elektrik-altyapı-ekipman-montajı--kablo-döşeme) | Elektrik Altyapı (ekipman + kablo + pano şeması) | 5.1 |
| [5.3](#53--su-1-fix-boru-döşeme) | Su 1. Fix (boru döşeme) | 5.1 |
| [5.4](#54--banyo-altyapı-fiber-zemin) | Banyo Altyapı (fiber zemin) | 5.2, 5.3 |
| [5.5](#55--cihaz-yerleştirme-kaplama-öncesi) | Cihaz Yerleştirme (kaplama öncesi) | 5.2, 5.3, 5.4 |
| **6 — İç Kaplama** | | |
| [6.1](#61--i̇ç-kaplama-duvar-tavan-zemin-tavan-dolapları) | İç Kaplama (duvar, tavan, zemin, tavan dolapları) | 3.1, 3.2, 5.2, 5.3, 5.4, 5.5 |
| **7 — Tamamlama** | | |
| [7.1](#71--elektrik-bağlantı-tamamlama) | Elektrik Bağlantı Tamamlama (DI/DO terminasyon) | 5.2, 6.1 |
| [7.2](#72--su-tesisatı-tamamlama) | Su Tesisatı Tamamlama | 3.3, 6.1 |
| [7.3](#73--elektrik-2-fix-priz-aydınlatma-push-button) | Elektrik 2. Fix (priz, ışık, buton + yerleşim tabloları) | 6.1, 7.1 |
| [7.4](#74--mutfak-tezgah-montajı) | Mutfak Tezgah Montajı | 7.2, 7.3 |
| [7.5](#75--banyo-batarya-montajı) | Banyo Batarya Montajı | 7.2, 7.3 |
| **8 — Tescil** | | |
| [8.1](#81--tescil-ve-proje) | Tescil ve Proje | 7.5 |

---

## 1.1 — Otomasyon Geliştirme
> Bağımlılık: Yok

Otomasyon yazılımının ve donanımlarının tedariki. Home Assistant kurulumu, Modbus entegrasyonu, DI/DO testleri, kontrol paneli ekranı entegrasyonu. Araç olmadan evde masaüstünde yapılır.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Ana Bilgisayar Kasası | Waveshare IPCBOX-CM5-A (4x RS485, CAN, 2DI/2DO, dual ETH, 7-36V) | 1 | ~4.400 ₺ | ~4.400 ₺ | [Waveshare](https://www.waveshare.com/ipcbox-cm5-a.htm) | |
| CM5 Modül | Raspberry Pi CM5 8GB Lite (eMMC'siz, BCM2712 2.4GHz) | 1 | ~3.000 ₺ | ~3.000 ₺ | SAMM Market | |
| NVMe SSD | 512GB M.2 2242 NVMe (Kioxia / WD) | 1 | ~1.000 ₺ | ~1.000 ₺ | | |
| DI/DO Modülü | Waveshare Modbus RTU IO 8CH (8DI/8DO, RS485) | 1 | ~1.428 ₺ | ~1.428 ₺ | [SAMM Market](https://market.samm.com/endustriyel-8-kanalli-dijital-giris-ve-cikis-modulu) | |
| Analog Giriş Modülü | Waveshare 8-Ch Analog Acquisition (RS485) | 1 | ~1.555 ₺ | ~1.555 ₺ | SAMM Market | |
| Araç Aküsü Float Şarj / Dev PSU | Victron Blue Smart IP65 12/5A (220V AC→12V DC, 60W) | 1 | ~5.000 ₺ | ~5.000 ₺ | Tekmobil / MarinReyon | |
| Sigortalı Dağıtım Kutusu | 12'li İkaz Işıklı Negatif Barali Sigorta Kutusu | 1 | ~1.225 ₺ | ~1.225 ₺ | karavanicin.com | |
| RS485 Kablo + Konnektör | CAT5e/shielded + terminal bloklar | 1 set | ~500 ₺ | ~500 ₺ | | |
| Kontrol Paneli Ekranı | Waveshare 11.9" HDMI LCD 320×1480 IPS Touch | 1 | ~4.538 ₺ | ~4.538 ₺ | [Waveshare](https://www.waveshare.com/11.9inch-HDMI-LCD.htm) | |
| Network Switch | TP-Link TL-SG105 5-port Gigabit | 1 | ~1.500 ₺ | ~1.500 ₺ | | |
| Access Point | TP-Link EAP225-Outdoor (Wi-Fi 5) | 1 | ~3.500 ₺ | ~3.500 ₺ | | |
| | | | | **~27.646 ₺** | | |

> **Kur:** 1 USD = 44,07 ₺, 1 EUR = 51,21 ₺ (17 Şubat 2026). Fiyatlar ±%15 sapabilir.

### 1.1 Kapsam Açıklama

- **IPCBOX + CM5 + SSD**: Waveshare IPCBOX-CM5-A endüstriyel kutu + RPi CM5 8GB + 512GB NVMe SSD = Home Assistant ana bilgisayar (4x RS485, CAN, 2DI/2DO, 7-36V DC direkt besleme, dual ETH)
- **DI/DO Modülü**: 1x 8DI/8DO → push button (DI), valf / kontaktör bobini (DO); yük anahtarlama Waveshare Modbus röle modülleri (RTU 8CH + POE ETH 16CH)
- **Analog Giriş**: Su tankı seviye sensörleri, sıcaklık okumaları
- **Float Şarj / Dev PSU**: Victron Blue Smart IP65 12/5A (220V AC → 12V DC) — geliştirme sürecinde otomasyon cihazlarının güç kaynağı olarak kullanılır, karavanda EasySolar-II AC OUT 1'den Waveshare relay ile araç aküsü float şarj (shore yokken de inverter üzerinden çalışır)
- **Sigortalı Dağıtım Kutusu**: DC taraf sigorta dağıtımı
- **RS485 Kablo**: Modüller arası RS485 haberleşme kablolaması
- **Kontrol Paneli Ekranı**: Giriş kapısı üstü, HDMI + USB direkt IPCBOX-CM5-A bağlantısı, HA dashboard

---

## 1.2 — Alet ve Atölye Tedariği
> Bağımlılık: Yok (1.1 ile paralel)

Karavan DIY inşaat sürecinde kullanılacak el aletleri ve elektrik aletleri. Tüm akülü aletler Einhell 18V Power X-Change platformunda — tek akü ailesi.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| **Akülü Aletler (Einhell 18V PXC)** | | | | | | |
| Darbeli Matkap | Einhell Te-Cd 18/50 Li-I Bi + 4 Ah Starter Kit | 1 | ~5.490 ₺ | ~5.490 ₺ | | |
| Akü Twinpack | Einhell PXC Twinpack 5.2 Ah (2x 5.2Ah) | 1 | ~5.511 ₺ | ~5.511 ₺ | | |
| Gönye Testere | Einhell TE-MS 18/210 Li (Solo) | 1 | ~6.500 ₺ | ~6.500 ₺ | | |
| Avuç Taşlama | Einhell AXXIO 18/115 (Solo) | 1 | ~4.099 ₺ | ~4.099 ₺ | | |
| Dekupaj Testere | Einhell TE-JS 18 Li (Solo) | 1 | ~2.560 ₺ | ~2.560 ₺ | | |
| Eksantrik Zımpara | Einhell TP-RS 18/32 Li BL (Solo) | 1 | ~3.967 ₺ | ~3.967 ₺ | | |
| Raspalama Makinesi | Einhell TE-MG 18/1 Li (Solo) | 1 | ~2.499 ₺ | ~2.499 ₺ | | |
| Sıcak Hava Tabancası | Einhell TE-HA 18 Li (Solo) | 1 | ~3.960 ₺ | ~3.960 ₺ | | |
| **Elektrik Tesisat Aletleri** | | | | | | |
| Otomatik Kablo Sıyırıcı | Knipex 12 62 (180 mm) | 1 | ~3.352 ₺ | ~3.352 ₺ | | |
| Yüksük Sıkma Pensi | Knipex 97 53 04 (dörtçene) | 1 | ~9.689 ₺ | ~9.689 ₺ | | |
| Kablo Numaratörü | Mykablo Ec-2 "8" Numara (500 adet) | 1 | ~400 ₺ | ~400 ₺ | | |
| **Montaj / Sac Aletleri** | | | | | | |
| Step Drill (Kademeli Panç) | HSS 4-32 mm | 1 | ~999 ₺ | ~999 ₺ | | |
| Perçin Tabancası | Ceta Form Katlanır Kollu (pop-somun perçin) | 1 | ~9.855 ₺ | ~9.855 ₺ | | |
| **Sarf Malzeme** | | | | | | |
| Isı ile Daralan Makaron | Greenbox yapışkanlı 6,4 mm | 1 | ~260 ₺ | ~260 ₺ | | |
| Makaron Seti | Motorobit 150 parça kutulu siyah | 1 | ~389 ₺ | ~389 ₺ | | |
| | | | | **~59.530 ₺** | | |

---

## 2.1 — Araç Alımı
> Bağımlılık: Yok

Iveco Daily veya MAN TGE 18m³ aracın satın alımı.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Araç | Iveco Daily / MAN TGE 18m³ | 1 | ~1.800.000 ₺ | ~1.800.000 ₺ | | |
| | | | | **~1.800.000 ₺** | | |

---

## 3.1 — Sigma Profil İskelet (Mobilya)
> Bağımlılık: 2.1

Araç alımından sonra ilk iş — tüm mobilya iskeletlerinin 20x20 sigma profille yapımı. Karkas, pencere/klima/kablo kesimlerinin referans noktalarını belirler; her şey plana göre oturmalı — 10cm sapma bile pencere yerleşimini bozar.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Sigma Profil | 20x20 alüminyum ekstrüzyon (6 kanal) | 40 m | ~200 ₺/m | ~8.000 ₺ | [cnc-marketi](https://www.cnc-marketi.com/urun/sigma-profil-20x20-6-kanal-sigma-profil) | |
| Köşe bağlantı elemanları | L/T braketi + M6 somun seti (50 adet) | 1 set | ~1.250 ₺ | ~1.250 ₺ | [cnc-marketi](https://www.cnc-marketi.com/kategori/kose-baglanti-fiyatlari) | |
| Ana yatak çerçevesi | 200x180cm — yukarıdaki profillerden imalat | 1 | — | — | | |
| Kanepe-yatak çerçevesi | 200x70cm — yukarıdaki profillerden imalat | 1 | — | — | | |
| Mutfak dolabı iskeleti | Tezgah + alt/üst dolap — profillerden imalat | 1 set | — | — | | |
| Yatak altı çekmeceler | Alray teleskopik ray 50cm | 6 çift | ~170 ₺ | ~1.020 ₺ | [aliakdas](https://aliakdas.myideasoft.com/urun/alray-50cm-teleskopik-cekmece-rayi) | |
| Lagun Masa | 40x80cm, 360° döner mekanizma + tabla | 2 | ~3.700 ₺ | ~7.400 ₺ | [izmirkaravanekipmanlari](https://www.izmirkaravanekipmanlari.com/kategori/karavan-masa-ayaklari) | |
| | | | | **~17.670 ₺** | | |

---

## 3.2 — Zemin Geliştirme
> Bağımlılık: 2.1, 3.1

Zemin katman yapısının oluşturulması — elastomer pad, sigma mesh, XPS dolgu. Mobilya iskelet pozisyonları (3.1) baz alınarak zemin karkas planlanır.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Elastomer pad | Yapışkanlı elastomerik kauçuk 6mm | ~8 m² | ~325 ₺/m² | ~2.600 ₺ | [karavanicin](https://karavanicin.com/product/6-mm-kendinden-yapiskanli-ve-folyolu-elastomerik-kaucuk-kopugu-karavan-isi-izolasyonu/) | |
| Zemin sigma mesh | 20x20 sigma profil zemin karkas | 20 m | ~200 ₺/m | ~4.000 ₺ | [cnc-marketi](https://www.cnc-marketi.com/urun/sigma-profil-20x20-6-kanal-sigma-profil) | |
| XPS levha (zemin) | Bonuspan 20mm | ~8 m² | ~105 ₺/m² | ~840 ₺ | [flextab](https://www.flextab.com.tr/urun/xps-isi-yalitim-levhasi-20mm-20-adet-14-40-m2-0-288m3) | |
| | | | | **~7.440 ₺** | | |

### Zemin Katman Yapısı (alttan üste)

| Katman | Malzeme | Kalınlık | Adım | İşlev |
|--------|---------|----------|------|-------|
| 1 | Sac (mevcut araç tabanı) | — | — | Taşıyıcı referans yüzey |
| 2 | Elastomer pad | ~3-5mm | 3.2 | Titreşim ve ses yalıtımı |
| 3 | Sigma profil mesh (20x20) | 20mm | 3.2 | Ana yük dağıtıcı karkas |
| 4 | XPS (sigma arası dolgu) | 20mm | 3.2 | Boşluk dolgusu + ısı yalıtımı, sigma ile flush yüzey |
| 5 | Plywood (lip kesimli) | ~12-18mm | 6.1 | Sigma + XPS'i tamamen kapatır, yürünebilir yüzey |

> Sigma 20x20 profiller ve 20mm XPS aynı yükseklikte — zemin düz/flush kalır. Plywood paneller sigma profillerini kapatacak şekilde lip (rabbet) kesimle yerleştirilir; bitmiş zeminde sigma görünmez.

---

## 3.3 — Su Depoları (Şasi Altı)
> Bağımlılık: 2.1

Şasi altına temiz ve gri su depolarının montajı. 3.2 ile koordineli yapılmalı — zemin sigma mesh rivnut pozisyonları depo montaj noktalarıyla çakışmamalı.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Temiz su deposu | Polietilen gıda uyumlu ~180L | 1 | ~3.500 ₺ | ~3.500 ₺ | [plastiksudepolari](https://plastiksudepolari.com.tr/urun/150-litre-kare-plastik-su-deposu/) | |
| Gri su deposu | PSA Polietilen 90L | 1 | ~2.050 ₺ | ~2.050 ₺ | [methuskaravan](https://methuskaravan.com.tr/psa-90lt-atik-su-deposu/) | |
| Temiz su şamandıra | KUS Yakıt/Su Şamandırası 25cm (Ohm 0-190, IP67) | 1 | ~920 ₺ | ~920 ₺ | [agus](https://www.agus.com.tr/karavan--tekne-yakit-ve-su-samandirasi-25-cm) | |
| Gri su şamandıra | KUS Atık Su Şamandırası 25cm (Ohm 0-190, IP67) | 1 | ~1.262 ₺ | ~1.262 ₺ | [agus](https://www.agus.com.tr/karavan--tekne-atik-samandirasi-25-cm) | |
| Temiz su boşaltma vanası | Manuel depo vanası 3/8" | 1 | ~120 ₺ | ~120 ₺ | [roteknik](https://roteknik.com.tr/su-aritma/su-aritma-yedek-parcalari/vana/depo-vanasi-3-8/) | |
| Gri su boşaltma vanası | Manuel depo vanası 3/8" | 1 | ~120 ₺ | ~120 ₺ | [roteknik](https://roteknik.com.tr/su-aritma/su-aritma-yedek-parcalari/vana/depo-vanasi-3-8/) | |
| | | | | **~7.972 ₺** | | |

> Not: Depo boyutları aracın şasi ölçülerine göre belirlenecek. Sigma zemin iskeletiyle birlikte planlanır.

---

## 4.1 — Pencere Kesim ve Montaj
> Bağımlılık: 3.1

Karkas referans noktalarına göre yan panel ve tavan kesimi, pencere ve heki montajı. Kesim pozisyonları iç mobilya iskeletine göre belirlenir.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Heki (tavan pencere) | Dometic Midi Heki Style 70x50cm çevirme kollu | 1 | ~30.800 ₺ | ~30.800 ₺ | [karavanaksesuar](https://www.karavanaksesuar.com/urun/dometic-midi-heki-style-50x70-beyaz-karavan-tavan-havalandirma-heki-cevirme-kollu-kopya) | |
| Yan pencere büyük | Jarup JR50120FW 50x120cm beyaz pervazlı | 2 | ~11.050 ₺ | ~22.100 ₺ | [tekneyat](https://www.tekneyataksesuarlari.com/urun/beyaz-pervazli-karavan-penceresi-50x120) | |
| Yan pencere yatak yanı | Jarup JR45110FW 45x110cm beyaz pervazlı | 2 | ~14.692 ₺ | ~29.384 ₺ | [karavanmarket](https://karavanmarket.com.tr/arama-sayfasi?limit=25&order=ASC&page=5&sort=rating&tag=) | |
| Banyo Penceresi | Jarup JR3050FW 30x50cm beyaz pervazlı | 1 | ~6.106 ₺ | ~6.106 ₺ | [karavanmarket](https://karavanmarket.com.tr/kapilar-pencereler/pistonlu-karavan-pencereleri/beyaz-pervazli-karavan-penceresi-30x50-jr3050fw) | |
| | | | | **~88.390 ₺** | | |

> Not: Pencere ve heki yerleşimi karkas referans noktalarına göre netleştirilir. 10cm bile sapma iç mobilya ile hizalamayı bozar.

---

## 4.2 — Tavan Klima Montajı
> Bağımlılık: 4.1

Tavan klima ünitesinin kesim ve montajı. Heki ve güneş panelleri ile çakışmayacak pozisyonda.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Tavan Klima | Evacool Eva RV 2700 Premium | 1 | ~76.500 ₺ | ~76.500 ₺ | [evacool](https://evacool.com.tr) | |
| | | | | **~76.500 ₺** | | |

---

## 4.3 — Çatı Ray Sistemi
> Bağımlılık: 4.2

OEM çatı ray kanallarına montaj rayı kurulumu. Tavana delik açılmaz — fabrika kanalları kullanılır. Ray sistemi güneş paneli ve tente montaj noktalarını birlikte içerecek şekilde planlanır. Klima ve heki pozisyonlarına göre konumlandırılır.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Çatı Ray Sistemi | OEM kanal uyumlu alüminyum montaj rayı 4m (güneş paneli + tente ortak) | 1 set | ~2.000 ₺ | ~2.000 ₺ | [ekomobilsolar](https://www.ekomobilsolar.com/urun/aluminyum-montaj-rayi-1-metre) | |
| | | | | **~2.000 ₺** | | |

> Not: Ray sistemi güneş panelleri (4.4) ve tente (4.5) için ortak altyapıdır.

---

## 4.4 — Güneş Paneli Montajı
> Bağımlılık: 4.3

4.3'te kurulan çatı ray sistemine güneş panellerinin montajı.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Güneş Paneli | Pantec PNT-205M 200W rigid monokristal | 4 | ~4.410 ₺ | ~17.640 ₺ | [solarkutu](https://www.solarkutu.com/urun/200w-monokristal-gunes-paneli) | |
| MC4 Konnektör + Kablo | Multi-Contact MC4 + solar kablo 4mm² set | 1 set | ~500 ₺ | ~500 ₺ | [solarstok](https://www.solarstok.com/urun/multi-contact-mc4-konnektor-seti-4-6mm-by-staubli/) | |
| | | | | **~18.140 ₺** | | |

> Not: 2S2P konfigürasyon (kısmi gölge dayanıklılığı) önerilir. Solar kablolar 5.2'de EasySolar-II MPPT'ye bağlanır.

---

## 4.5 — Tente Montajı
> Bağımlılık: 4.3

4.3'te kurulan OEM çatı ray sistemine tente montajı. Giriş kapısı tarafı.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Tente | Thule Omnistor 6300 4.0x2.5m kasetli | 1 | ~58.565 ₺ | ~58.565 ₺ | [2kkaravan](https://2kkaravan.com/thule-omnistor-6300-400-x-250-siyah-cati-tipi-karavan-tentesi) | |
| Tente montaj braketi | Thule tavan montaj braketi seti | 1 set | ~15.312 ₺ | ~15.312 ₺ | [2kkaravan](https://2kkaravan.com/thule-omnistor-9200-6300-6200-serisi-tavan-montaj-braketi-) | |
| | | | | **~73.877 ₺** | | |

---

## 4.6 — Kamera Montajı
> Bağımlılık: 3.1

4 kameranın araç üzerine montajı ve aviation kabloların teknik alana indirilmesi. DVR montajı 5.5'te, bağlantı 7.1'de yapılır.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Analog TVI Kamera | Navistar NVS-340-4PIN AHD 1080P, IR, IP67, 4-pin aviation | 4 | ~1.296 ₺ | ~5.184 ₺ | [prostar](https://www.prostarteknoloji.com/u3116/tum-arac-kameralari/ahd-1080p-ve-analog-cvbs-pal-donusturulebilir-gece-goruslu-4-pin-mini-metal-dome-arac-kamerasi.html) | |
| Kamera montaj braketi | Alüminyum vibrasyon dayanıklı | 4 | ~250 ₺ | ~1.000 ₺ | prostar | |
| Kamera aviation kablosu | 4-pin shielded 7m (kamera-teknik alan arası) | 4 | ~410 ₺ | ~1.640 ₺ | [prostar](https://www.prostarteknoloji.com/u3095/arac-kamera-kablolari/4-pin-aviation-hazir-arac-kamera-kablosu-7-metre.html) | |
| Mobile DVR + HDD | HK Vision DS-M5504HM + Seagate 1TB 2.5" | 1 | ~16.807 ₺ | ~16.807 ₺ | [hikvisiontr](https://hikvisiontr.net/ds-m5504hm-t) | |
| | | | | **~24.631 ₺** | | |

> Not: Kamera pozisyonları — ön üst, arka kapı üstü, sol/sağ ayna altı. Ayna altı kablolar A sütunu içinden geçirilir.

---

## 5.1 — Yalıtım
> Bağımlılık: 4.1, 4.2

Kabuk kesimlerden sonra duvar ve tavan ses/ısı yalıtımının tamamlanması. Zemin yalıtımı (elastomer pad) 3.2 zemin adımında yapılır.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Ses yalıtım plakası | Mastercare 2,5mm butil/alüminyum | ~15 m² | ~350 ₺/m² | ~5.250 ₺ | [koctas](https://www.koctas.com.tr/mastercare-25-mm-1-m2-ses-yalitim-levhasi/p/1000169211) | |
| Isı yalıtımı | Folyolu yapışkanlı elastomerik kauçuk 6mm | ~20 m² | ~325 ₺/m² | ~6.500 ₺ | [karavanicin](https://karavanicin.com/product/6-mm-kendinden-yapiskanli-ve-folyolu-elastomerik-kaucuk-kopugu-karavan-isi-izolasyonu/) | |
| | | | | **~11.750 ₺** | | |

---

## 5.2 — Elektrik Altyapı: Ekipman Montajı + Kablo Döşeme
> Bağımlılık: 5.1

Ana yatak altı teknik alana batarya, inverter (EasySolar-II), otomasyon panosu, Orion XS ve dağıtım donanımlarının fiziksel montajı. Ardından tüm elektrik kablolarının duvar/tavan/zemin altına döşenmesi. Güneş paneli kabloları (4.4) bu aşamada EasySolar-II MPPT'ye bağlanır. **İç kaplama yapılmadan ÖNCE tamamlanmalı.**

**Merkezi Ekipman (Teknik Alan)**

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| LiFePO4 Hücre | EVE LF280 3.2V 280Ah prizmatik | 8 | ~5.350 ₺ | ~42.800 ₺ | [dekarenergy](https://www.thedekarenergy.com/urun/eve-lifepo4-3-2v-lfp-280ah-prizmatik-pil-hucresi) | |
| BMS | Daly 8S 25.6V 200A K serisi (BT+RS485+CAN) | 1 | ~13.641 ₺ | ~13.641 ₺ | [elektrodepo](https://www.elektrodepo.com/urun/daly-8s-25-6v-200a-lifepo4-smart-bms-bt-uart-485-canbus-k-series) | |
| İnverter/Şarj/MPPT | Victron EasySolar-II 24/3000/70-32 MPPT 250/70 GX | 1 | ~70.002 ₺ | ~70.002 ₺ | [marinreyon](https://www.marinreyon.com/urun/victron-energy-easysolar-ii-24-3000-70-32-mppt-250-70-gx-pmp242307010) | |
| DC-DC Şarj | Victron Orion XS 12\|12-50A | 1 | ~21.217 ₺ | ~21.217 ₺ | [denizmar](https://www.denizmar.net/urun/victron-energy-orion-xs-12-12-50a-dc-dc-battery-charger) | |
| Relay Modülü (8CH) | Waveshare Modbus RTU Relay (RS485) | 1 | ~2.500 ₺ | ~2.500 ₺ | [SAMM Market](https://market.samm.com) | |
| Relay Modülü (16CH) | Waveshare POE ETH 16CH Relay | 1 | ~4.500 ₺ | ~4.500 ₺ | [SAMM Market](https://market.samm.com) | |
| Blade Fuse Block | 8 pozisyonlu blade sigorta dağıtım bloğu | 2 | ~500 ₺ | ~1.000 ₺ | karavanicin.com | |
| 220V Sigorta Kutusu | Panasonic sıva üstü modüler sigorta kutusu | 1 | ~500 ₺ | ~500 ₺ | | |
| MCB Sigortalar | CHNT C16 otomatik sigorta | 9 | ~80 ₺ | ~720 ₺ | | |
| Kaçak Akım Rölesi | Chint 2P 25A 30mA | 1 | ~720 ₺ | ~720 ₺ | [elektrodijital](https://www.elektrodijital.com/urun/2x25a-30ma-kacak-akim-rolesi) | |
| Ana Sigorta | MTA Megaval 200A | 1 | ~135 ₺ | ~135 ₺ | [adamoto](https://www.adamoto.com.tr/urun/megaval-sigorta-200a-mavi-200-amper-mta) | |
| Akü izleme şantı | Victron SmartShunt 300A (SHU050130050, Bluetooth + VE.Direct, GX uyumlu) | 1 | ~4.607 ₺ | ~4.607 ₺ | [denizmar](https://www.denizmar.net/urun/smartshunt-300a) | |
| Acil Durdurma Butonu | Chint 40mm mantar NC panel montaj | 1 | ~108 ₺ | ~108 ₺ | [elektrodijital](https://www.elektrodijital.com/urun/acil-stop-butonu) | |
| Shore Power Girişi | DEFA MiniPlug besleme kablosu 1m (460901, kompakt gömme — büyük CEE kutusuna göre minik montaj) | 1 | ~2.200 ₺ | ~2.200 ₺ | [Termosa](https://www.termosa.com/urunlerimiz/elektrik-elektronik-enerji-sistemleri/baglanti-kablolari/defa-miniplug-besleme-kablosu-460901) | |
| Ana akım kablosu | Fly 16mm² bakır (batarya-inverter) | ~5m | ~242 ₺/m | ~1.210 ₺ | [adamoto](https://www.adamoto.com.tr/urun/1-metre-16mm-kirmizi-bakir-aku-kablosu-fly) | |
| | | | | **~165.860 ₺** | | |

**Kablolama**

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| AC Kablo | Pamukkale NYAF 4mm² (220V hatlar) | ~100m | ~28 ₺/m | ~2.800 ₺ | [kablocu](https://www.kablocu.com.tr/4-mm-nyaf-pamukkale) | |
| DC Kablo (sinyal/aydınlatma) | Pamukkale NYAF 2.5mm² (24V/12V) | ~150m | ~18 ₺/m | ~2.700 ₺ | [kablocu](https://www.kablocu.com.tr/25-mm-nyaf-pamukkale) | |
| DC Kablo (yüksek akım) | Pamukkale NYAF 4mm² (24V yüksek akım) | ~50m | ~28 ₺/m | ~1.400 ₺ | [kablocu](https://www.kablocu.com.tr/4-mm-nyaf-pamukkale) | |
| Kablo koruyucu | CETEX spiral 25mm yanmaz | ~30m | ~51 ₺/m | ~1.530 ₺ | [hufferelektrik](https://www.hufferelektrik.com/urun/25-lik-kablo-toplama-spirali-gri-1311) | |
| Buat/Junction box | Çetinkaya IP65 ABS sıva üstü | ~20 | ~100 ₺ | ~2.000 ₺ | [elektrikpiyasa](https://www.elektrikpiyasa.com) | |
| RS485 Haberleşme kablosu | CAT5e shielded | ~30m | ~15 ₺/m | ~450 ₺ | | |
| Kablo bağı + klips | Montaj malzemesi seti | 1 set | ~200 ₺ | ~200 ₺ | | |
| | | | | **~11.080 ₺** | | |

> Not: Kablo güzergahları aşağıdaki pano şeması ve kanal haritalarına göre planlanır.

### Elektrik Panosu

![Elektrik Panosu](../Assets/Images/BackPanel.jpg)

### 220V MCB Panel (9x CHINT)

Tüm MCB hatları **8CH Relay CH1 (220V Startup)** üzerinden beslenir. Yüksek güçlü cihazlar ek olarak bireysel relay kontrolündedir.

| # | MCB Etiketi | Bölge | Bireysel Relay Kontrolü |
|---|-------------|-------|------------------------|
| 1 | Victron Blue Smart | Teknik alan | 16CH Relay (float şarj) |
| 2 | Washing Machine | Banyo | 8CH Relay CH6 |
| 3 | Induction Hob | Mutfak | 8CH Relay CH8 |
| 4 | Dishwasher | Mutfak | 16CH Relay (bulaşık makinesi) |
| 5 | Air Condition | Ana Yatak | 8CH Relay CH7 |
| 6 | Bed Outlets | Ana Yatak | Yok — 220V Startup ile aktif |
| 7 | Kitchen Outlets | Mutfak | Yok — 220V Startup ile aktif |
| 8 | Saloon Outlets | Oturma | Yok — 220V Startup ile aktif |
| 9 | Outdoor Outlets | Dış | Yok — 220V Startup ile aktif |

> Yüksek güçlü 220V cihazlar (çamaşır makinesi, indüksiyon ocak, klima, bulaşık makinesi, Victron BlueSmart) bireysel relay kontrolündedir. HA yük yönetimi ile inverter modunda eş zamanlı çalışma önlenir. Outlet hatları sadece MCB korumalı, 220V Startup ile toplu açılır.

### Waveshare Modbus RTU Relay (E) — 8 Kanal

Master startup röleleri ve yüksek güçlü 220V cihaz kontrolü. RS485 üzerinden Modbus ile yönetilir.

| CH | Yük | Tip | Detay |
|----|-----|-----|-------|
| CH1 | 220V Startup | Master | MCB paneli besleme (outlet hatları) |
| CH2 | 24V Startup | Master | 24V dağıtım bloğu |
| CH3 | 12V StartUp | Master | 12V dağıtım bloğu |
| CH4 | Clesana C1 | 12V | Susuz tuvalet (banyo) |
| CH5 | Rezerv | - | Boş |
| CH6 | Washing Machine | 220V | Çamaşır makinesi |
| CH7 | Air Conditioner | 220V | Klima (Evacool RV 2700) |
| CH8 | Induction Hob | 220V | İndüksiyon ocak (Thetford) |

### Waveshare Modbus POE ETH Relay — 16 Kanal

Aydınlatma, DC cihazlar ve ek 220V cihaz kontrolü. POE Ethernet üzerinden Modbus ile yönetilir.

**Blade Fuse Block #1 — Aydınlatma + Macerator (8P, tümü dolu)**

| CH | Blade Fuse Pos | Yük | Voltaj |
|----|---------------|-----|--------|
| CH1 | 1 | Bed Reading Lamp R (okuma lambası sağ) | 24V |
| CH2 | 2 | Bed Light (yatak tavan aydınlatma) | 24V |
| CH3 | 3 | Bathroom Light (banyo aydınlatma) | 24V |
| CH4 | 4 | Saloon Light (oturma aydınlatma) | 24V |
| CH5 | 5 | Bed Reading Lamp L (okuma lambası sol) | 24V |
| CH6 | 6 | Emergency Light (acil aydınlatma) | 24V |
| CH7 | 7 | Kitchen Light (mutfak aydınlatma) | 24V |
| CH8 | 8 | Macerator (macerator pompa) | 24V |

**Blade Fuse Block #2 — DC Cihazlar (8P, 4 dolu + 4 rezerv)**

| CH | Blade Fuse Pos | Yük | Voltaj |
|----|---------------|-----|--------|
| CH9 | 1 | Refrigerator Kitchen (Evacool Eva Berlin, mutfak) | 24V |
| CH10 | 2 | Outdoor Light 2 (dış aydınlatma 2) | 24V |
| CH11 | 3 | Refrigerator Drawer (Evacool D31 R, kanepe altı) | 24V |
| CH12 | 4 | Outdoor Light 1 (dış aydınlatma 1) | 24V |
| - | 5-8 | Rezerv | - |

**220V Doğrudan Kontrol (Blade Fuse Block dışı)**

| CH | Yük | Detay |
|----|-----|-------|
| CH15 | Dishwasher | Bulaşık makinesi (Electrolux), 220V |
| CH16 | Victron BlueSmart | Float şarj (Victron Blue Smart IP65), 220V |

> CH13-CH14: Rezerv (Block #2 boş slotlarına bağlanabilir).

### 24V Startup Dağıtım

8CH Relay CH2 (24V Startup) aktif olduğunda aşağıdaki çıkışlar beslenir:

| Çıkış | Detay |
|--------|-------|
| Water Pump | 24V su pompası |
| Bed USB | Ana yatak USB-C soketleri |
| Kitchen USB | Mutfak USB-C soketleri |
| Saloon USB | Oturma USB-C soketi |
| Lounge USB | Kanepe USB-C soketi |
| Strip LEDs | Shelly RGBW PM besleme (LED strip) |

### 12V Startup Dağıtım

8CH Relay CH3 (12V StartUp) aktif olduğunda aşağıdaki çıkışlar beslenir:

| Çıkış | Detay |
|--------|-------|
| Truma Combi 4D | Isıtma + sıcak su sistemi (12V kontrol) |
| Kitchen Outlet | Mutfak 12V priz |

> Clesana C1 ayrıca 8CH Relay CH4 üzerinden bireysel kontrollüdür, 12V Startup'a bağlı değildir.

### Kanal Özeti

| Kaynak | Toplam | Kullanılan | Rezerv |
|--------|--------|------------|--------|
| 8CH RTU Relay | 8 | 7 | 1 |
| 16CH POE ETH Relay | 16 | 14 | 2 |
| Blade Fuse Block #1 (8P) | 8 | 8 | 0 |
| Blade Fuse Block #2 (8P) | 8 | 4 | 4 |

---

## 5.3 — Su 1. Fix: Boru Döşeme
> Bağımlılık: 5.1

PEX boruların duvar/zemin altına döşenmesi. **İç kaplama yapılmadan ÖNCE tamamlanmalı.**

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| PEX Boru (soğuk su) | Vesbo PEX-A 16x2mm | ~20m | ~28 ₺/m | ~560 ₺ | [yerdenisitma](https://www.yerdenisitma.com.tr/urun/vesbo-yerden-isitma-borusu-pex-a-16x2-600-metre) | |
| PEX Boru (sıcak su) | Vesbo PEX-A 16x2mm (izoleli) | ~15m | ~35 ₺/m | ~525 ₺ | yerdenisitma.com | |
| Gri su borusu | Esnek hortum 32mm | ~10m | ~46 ₺/m | ~460 ₺ | [edukkanim](https://www.edukkanim.com.tr/gri-toz-emis-hortumu-1-1-4-inch-32-mm-50-metre) | |
| Bağlantı elemanları | PEX press fitting set (~20 adet) | 1 set | ~600 ₺ | ~600 ₺ | vipiri.com | |
| | | | | **~2.145 ₺** | | |

---

## 5.4 — Banyo Altyapı: Fiber Zemin
> Bağımlılık: 5.2, 5.3

Banyo (70x180cm dik tam genişlik) ve su alanı için fiber kompozit zemin yapımı.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Fiber elyaf | HITEX cam elyaf dokuma 100g/m² | ~5 m² | ~115 ₺/m² | ~575 ₺ | [kompozitpazari](https://kompozitpazari.com/urun/cam-elyaf-dokuma-kumas-100-g-m2-plain/) | |
| Epoksi reçine | EpoXs laminasyon epoksi set (reçine + sertleştirici) | ~3 kg | ~467 ₺/1.5kg | ~934 ₺ | [kalipsilikonu](https://www.kalipsilikonu.com/urun/laminasyon-epoksi-set-1-5-kg) | |
| XPS levha | Bonuspan yoğun XPS köpük 20mm | ~3 m² | ~105 ₺/m² | ~315 ₺ | [flextab](https://www.flextab.com.tr/urun/xps-isi-yalitim-levhasi-20mm-20-adet-14-40-m2-0-288m3) | |
| Son kat boya | Polchem PU beyaz mat (su geçirmez) | ~2 lt | ~230 ₺/lt | ~460 ₺ | [alizemarinmarket](https://www.alizemarinmarket.com/urun/polchem-poliuretan-beyaz-mat-son-kat-boya) | |
| | | | | **~2.284 ₺** | | |

---

## 5.5 — Cihaz Yerleştirme (Kaplama Öncesi)
> Bağımlılık: 5.2, 5.3, 5.4

Kaplama firmasından ÖNCE yerleştirilmesi gereken büyük cihazlar. Bunların fiziksel boyutları ve pozisyonları kaplama ölçülerini belirler — mm hassasiyetinde flush noktaları için cihazlar yerinde olmalı.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Buzdolabı 1 | Evacool Marin Berlin 90L 12/24V | 1 | ~27.020 ₺ | ~27.020 ₺ | [denizmar](https://www.denizmar.net/urun/evacool-marin-buzdolabi-90-lt-12-24-v-berlin) | |
| Buzdolabı 2 | Evacool EVA D31 R Çekmeceli 24V | 1 | ~14.500 ₺ | ~14.500 ₺ | [evacool](https://evacool.com.tr/eva-d31-r-cekmeceli-buzdolabi) | |
| Bulaşık Makinesi | Electrolux ESF2400OS kompakt | 1 | ~17.229 ₺ | ~17.229 ₺ | [idefix](https://www.idefix.com/electrolux-esf2400os-kompakt-6-programli-gri-tezgah-ustu-bulasik-makinesi-p-690536) | |
| Clesana C1 | Susuz tuvalet (12V) | 1 | ~73.750 ₺ | ~73.750 ₺ | [reimo](https://www.reimo.com/tr/kamp-malzemeleri/su-tesisati-sanitasyon-karavan-tuvaleti/thetford-dometic-kaset-tuvaleti/42003/clesana-c1-yuvarlak-tabanli-susuz-tuvalet) | |
| | | | | **~132.499 ₺** | | |

> Not: Bu cihazlar sigma iskelet içindeki yerlerine monte edilir. Kaplama firması kapak/panel ölçülerini bu cihazların fiziksel pozisyonlarına göre alır.

---

## 6.1 — İç Kaplama (Duvar, Tavan, Zemin, Tavan Dolapları)
> Bağımlılık: 3.1, 3.2, 5.2, 5.3, 5.4, 5.5

Elektrik ve su 1. fix tamamlandıktan sonra duvar, tavan ve zemin kaplaması; **tavan dolapları** (mutfak/salon üstü depolama, kapak, menteşe, amortisör) aynı mobilya/kaplama işi kapsamında firmaya yaptırılır — bu kalem bütçenin en büyük dilimini oluşturur.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Tavan dolapları | Üst dolap gövdeleri + kapak (lamine/ahşap), mutfak/salon bandı | 1 set | — | ~130.000 ₺ | Firma teklifi (tahmini) | |
| Duvar kaplama | Ahşap panel / lamine, duvar yüzeyleri | ~20 m² | — | ~55.000 ₺ | Firma teklifi (tahmini) | |
| Tavan kaplama | Hafif panel / döşeme (dolap dışı tavan yüzeyi) | ~10 m² | — | ~30.000 ₺ | Firma teklifi (tahmini) | |
| Plywood (zemin) | Lip kesimli, sigma + XPS'i kapatır | ~8 m² | — | ~45.000 ₺ | Firma teklifi (tahmini) | |
| Zemin son kat | Vinil / lamine parke — plywood üzerine | ~8 m² | — | ~40.000 ₺ | Firma teklifi (tahmini) | |
| | | | | **~300.000 ₺** | | |

> Not: Toplam **~300.000 ₺** planlama bütçesidir; özellikle **tavan dolapları** işçilik + malzeme ile tabanı taşır, kesin rakam firma metrajı ve malzeme sınıfına göre değişir. Malzeme seçimleri iç tasarım kararlarına bağlı, araç ölçüldükten sonra netleştirilecek. Zemin katman yapısı bkz. 3.2.

---

## 7.1 — Elektrik Bağlantı Tamamlama
> Bağımlılık: 5.2, 6.1

5.2'de yerleştirilen merkezi ekipman ve döşenen kabloların, iç kaplama (6.1) sonrası uç noktalarına sonlandırılması. Pano içi kablo bağlantıları, sigorta atamaları ve RS485 bus terminasyonlarının tamamlanması.

- [ ] Tüm kablo uçlarının panoya terminasyonu
- [ ] Waveshare relay modüllerinin Modbus konfigürasyonu
- [ ] RS485 bus sonlandırma dirençleri
- [ ] Batarya hücre bağlantıları ve BMS konfigürasyonu
- [ ] EasySolar-II AC/DC bağlantıları
- [ ] Shore power hattı sonlandırma

### DI/DO Kanal Dağılımı (1x Waveshare 8DI/8DO)

**DI Kanalları — Push Button Input**

| DI | Bağlantı | İşlev |
|----|----------|-------|
| DI1 | Mutfak PB | Mutfak aydınlatma toggle |
| DI2 | Oturma PB | Oturma aydınlatma toggle |
| DI3 | Yatak Başı Sol PB 1 | Tavan aydınlatma toggle |
| DI4 | Yatak Başı Sol PB 2 | Sol okuma lambası toggle |
| DI5 | Yatak Başı Sağ PB 1 | Tavan aydınlatma toggle |
| DI6 | Yatak Başı Sağ PB 2 | Sağ okuma lambası toggle |
| DI7 | Banyo PB | Banyo aydınlatma toggle |
| DI8 | Rezerv | - |

**DO Kanalları — Rezerv**

| DO | Bağlantı |
|----|----------|
| DO1-DO8 | Rezerv (gelecek genişleme) |

> Eski mimarideki DO → bistable röle toggle mekanizması kaldırılmıştır. Relay switching artık doğrudan Waveshare relay modülleri üzerinden Modbus ile yapılır. DO kanalları gelecek genişleme için ayrılmıştır.

| Kaynak | Toplam | Kullanılan | Rezerv |
|--------|--------|------------|--------|
| DI (1× DI/DO) | 8 | 7 | 1 |
| DO (1× DI/DO) | 8 | 0 | 8 |

---

## 7.2 — Su Tesisatı Tamamlama
> Bağımlılık: 3.3, 6.1

Su tesisatının cihazlara bağlanması, pompa ve ısıtma sistemi montajı.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Hidrofor (su pompası) | SHURflo 24V 30psi 11L/dk | 1 | ~6.391 ₺ | ~6.391 ₺ | [eckmarine](https://www.eckmarine.com/urun/shurflo-hidrofor-11-lt-dk-30-psi-24-v) | |
| Genleşme kabı | Seaflo 1L basınç tankı | 1 | ~1.445 ₺ | ~1.445 ₺ | [karavanyapimarket](https://karavanyapimarket.com/urun/seaflo-genlesme-tanki-1l) | |
| Macerator pompa | SHURflo 24V Macerator | 1 | ~8.069 ₺ | ~8.069 ₺ | [marinreyon](https://www.marinreyon.com/urun/shurflo-24-v-macerator) | |
| Isıtma + Sıcak Su | Truma Combi D4 (dizel, 12V kontrol) | 1 | ~149.168 ₺ | ~149.168 ₺ | [tekneyat](https://www.tekneyataksesuarlari.com/urun/truma-combi-d4-dizel) | |
| Truma Kontrol | Truma iNet CP plus | 1 | ~17.000 ₺ | ~17.000 ₺ | (tahmini ~330 EUR) | |
| Truma Hava Dağıtım | İzoleli hortum 65mm + menfez + T parça kiti | 1 set | ~5.000 ₺ | ~5.000 ₺ | [karavanaksesuar](https://www.karavanaksesuar.com) | |
| Truma Yakıt Kiti | Yakıt pompası, filtre, dizel hat seti | 1 set | ~6.930 ₺ | ~6.930 ₺ | (tahmini ~135 EUR) | |
| Sıcak su dağıtım kollektörü | Pirinç 4 çıkışlı | 1 | ~1.500 ₺ | ~1.500 ₺ | | |
| Soğuk su dağıtım kollektörü | Pirinç 4 çıkışlı | 1 | ~1.500 ₺ | ~1.500 ₺ | | |
| Actuator valf | 24V motorlu küresel vana DN15 (donma koruması) | 1 | ~2.500 ₺ | ~2.500 ₺ | | |
| Çamaşır Makinesi | FIX Mini Me 3kg | 1 | ~45.999 ₺ | ~45.999 ₺ | [yavuzerkaravan](https://www.yavuzerkaravan.com/fix-mini-me-camasir-makinesi-karavan-ve-tekne-camasir-makinesi) | |
| | | | | **~245.502 ₺** | | |

---

## 7.3 — Elektrik 2. Fix: Priz, Aydınlatma, Push Button
> Bağımlılık: 6.1, 7.1

Kabloları daha önce döşedik (5.2). Şimdi uç cihazların montajı.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| 220V Priz | Westacc kapaklı sıva üstü karavan tipi | 8 | ~278 ₺ | ~2.224 ₺ | [tekneyat](https://www.tekneyataksesuarlari.com/urun/220v-priz-kopya) | |
| 12V Priz | TYA çakmak tipi panel montaj | 1 | ~70 ₺ | ~70 ₺ | [tekneyat](https://www.tekneyataksesuarlari.com/urun/cakmak-12v) | |
| USB-C Soket | Powerway Bullet 100W PD panel montaj (12-24V) | 8 | ~641 ₺ | ~5.128 ₺ | [erdenteknoloji](https://www.erdenteknoloji.com.tr/urun/powerway-bullet-100w-arac-cakmaklik-sarj-cihazi-type-c-ve-usb-cikisli-profesyonel-turbo-hizli-sarj) | |
| Push Button | 22mm LED'li anlık buton NO | 7 | ~187 ₺ | ~1.309 ₺ | [elektronikaled](https://elektronikaled.com/urun/22-mm-yayli-ve-ledli-buton-power-simge/) | |
| LED Spot | 24V LED downlight karavan armatür | 10 | ~250 ₺ | ~2.500 ₺ | | |
| LED Şerit | 24V RGB LED şerit IP65 (Ana yatak tavan) | 5 m | ~135 ₺/m | ~675 ₺ | [ledurunleri](https://www.ledurunleri.com/24v-rgb-serit-led-dis-mekan-silikonlu-ip65-5-metre) | |
| LED Şerit | 24V RGB LED şerit IP65 (Oturma ambient) | 5 m | ~135 ₺/m | ~675 ₺ | [ledurunleri](https://www.ledurunleri.com/24v-rgb-serit-led-dis-mekan-silikonlu-ip65-5-metre) | |
| Shelly Plus RGBW PM | Wi-Fi dimmer + renk, 24V | 2 | ~2.450 ₺ | ~4.900 ₺ | | |
| | | | | **~17.481 ₺** | | |

### Priz ve Soket Yerleşimi

| Bölge | Konum | 220V | 12V | USB-C (100W PD) | Toplam |
|-------|-------|------|-----|------------------|--------|
| **Ana Yatak** | Yatak Başı Sol (Mutfak tarafı) | 1 | - | 2 | 3 |
| **Ana Yatak** | Yatak Başı Sağ (Banyo tarafı) | 1 | - | 2 | 3 |
| **Ana Yatak** | Yatak Ayak Ucu (Banyo tarafı) | 1 | - | - | 1 |
| **Mutfak** | Tezgah üstü | 2 | 1 | 2 | 5 |
| **Oturma/Yatak** | Kanepe karkası altı (sol+sağ) | 2 | - | 2 | 4 |
| **Banyo** | Lavabo / duvar | 1 | - | - | 1 |
| **TOPLAM** | | **8** | **1** | **8** | **17** |

### Push Button Yerleşimi

| Bölge | Konum | Adet | İşlev | Bağlantı |
|-------|-------|------|-------|----------|
| **Mutfak** | Tezgah üstü / dolap | 1 | Mutfak aydınlatma | DI → HA → 16CH Relay |
| **Oturma/Yatak** | Duvar | 1 | Oturma aydınlatma | DI → HA → 16CH Relay |
| **Ana Yatak** | Yatak Başı Sol | 2 | Tavan aydınlatma, sol okuma lambası | DI → HA → 16CH Relay |
| **Ana Yatak** | Yatak Başı Sağ | 2 | Tavan aydınlatma, sağ okuma lambası | DI → HA → 16CH Relay |
| **Banyo** | Lavabo / duvar | 1 | Banyo aydınlatma | DI → HA → 16CH Relay |
| **TOPLAM** | | **7** | | |

> Push buttonlar Waveshare DI modülüne bağlıdır. HA butona basışı algılar ve ilgili Waveshare relay kanalını Modbus üzerinden doğrudan toggle eder.

### Aydınlatma Noktaları

| Bölge | Tip | Voltaj | Kontrol | Push Button |
|-------|-----|--------|---------|-------------|
| **Ana Yatak** | Tavan LED (Bed Light) | 24V | 16CH Relay + Shelly RGBW PM (dimmer+renk) | Yatak başı sol + sağ PB |
| **Ana Yatak** | Okuma lambası sol (Reading Lamp L) | 24V | 16CH Relay | Yatak başı sol PB |
| **Ana Yatak** | Okuma lambası sağ (Reading Lamp R) | 24V | 16CH Relay | Yatak başı sağ PB |
| **Ana Yatak** | Acil aydınlatma (Emergency Light) | 24V | 16CH Relay | HA otomasyon |
| **Mutfak** | Mutfak aydınlatma (Kitchen Light) | 24V | 16CH Relay | Mutfak PB |
| **Oturma/Yatak** | Oturma aydınlatma (Saloon Light) | 24V | 16CH Relay | Oturma PB |
| **Oturma/Yatak** | Ambient aydınlatma | 24V | Shelly Plus RGBW PM (dimmer+renk) | HA / Shelly |
| **Banyo** | Banyo aydınlatma (Bathroom Light) | 24V | 16CH Relay | Banyo PB |
| **Dış** | Dış aydınlatma 1 (Outdoor Light 1) | 24V | 16CH Relay | HA otomasyon |
| **Dış** | Dış aydınlatma 2 (Outdoor Light 2) | 24V | 16CH Relay | HA otomasyon |

### Shelly Plus RGBW PM (Wi-Fi, 2 adet)

24V Startup rail'den beslenir. LED strip dimmer + renk kontrolü.

| # | Konum | İşlev | Besleme |
|---|-------|-------|---------|
| 1 | Ana Yatak | Tavan LED — dimmer + renk (16CH Relay CH2 Bed Light downstream) | 24V via Blade Fuse #1 pos 2 |
| 2 | Oturma/Yatak | Ambient aydınlatma — dimmer + renk | 24V Startup rail (doğrudan) |

### Genel Sayılar

| Kategori | Adet |
|----------|------|
| 220V priz | 8 |
| 12V priz | 1 |
| Otomotiv USB-C soket (100W PD) | 8 |
| Push button | 7 |
| Aydınlatma noktası (iç + dış) | 10 |
| 220V MCB devresi | 9 |
| 220V relay kontrollü cihaz | 5 |
| Shelly Plus RGBW PM | 2 |

---

## 7.4 — Mutfak Tezgah Montajı
> Bağımlılık: 7.2, 7.3

Bitmiş tezgah yüzeyine kesim ve montaj.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| İndüksiyon Ocak | Thetford Induction Hob (tezgah kesimi) | 1 | ~12.000 ₺ | ~12.000 ₺ | thetford.com (tahmini ~230 EUR) | |
| Eviye | Thetford Argent Sink 63x47cm TFSSK1055-SP | 1 | ~15.048 ₺ | ~15.048 ₺ | [marinreyon](https://www.marinreyon.com/urun/dikdortgen-eviye) | |
| Mutfak Musluk | Karavan termostatik eviye bataryası | 1 | ~4.000 ₺ | ~4.000 ₺ | | |
| | | | | **~31.048 ₺** | | |

---

## 7.5 — Banyo Batarya Montajı
> Bağımlılık: 7.2, 7.3

Bitmiş banyo duvar/zemin yüzeyine montaj.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Lavabo | Cerastyle Sharp 40x30cm etajerli | 1 | ~2.031 ₺ | ~2.031 ₺ | [banyocu](https://banyocu.com.tr/magaza/cerastyle-sharp-etajerli-lavabo-40x30-cm/) | |
| Banyo Batarya | Comet spiralli karavan banyo musluğu | 1 | ~7.020 ₺ | ~7.020 ₺ | [agus](https://www.agus.com.tr/comet-spiralli-karavan-banyo-muslugu) | |
| Duş Batarya | Fause termostatik duş bataryası KTB102 | 1 | ~3.100 ₺ | ~3.100 ₺ | [yapimanya](https://www.yapimanya.com/urun/fause-termostatik-dus-bataryasi-ktb102) | |
| | | | | **~12.151 ₺** | | |

---

## 8.1 — Tescil ve Proje
> Bağımlılık: 7.5

Karavan dönüşüm sonrası resmi tescil, proje onayı ve vergi işlemleri.

| Ürün | Model | Adet | Fiyat | Toplam | Kaynak | Alındı |
|------|-------|------|-------|--------|--------|--------|
| Dönüşüm Vergisi | Motorlu Taşıtlar Dönüşüm Vergisi | 1 | ~600.000 ₺ | ~600.000 ₺ | | |
| Tescil ve Proje Hizmeti | Mühendislik proje + tescil işlemleri | 1 | ~30.000 ₺ | ~30.000 ₺ | | |
| | | | | **~630.000 ₺** | | |

---

## Proje Bütçe Özeti

| Faz | Adım | Toplam |
|-----|------|--------|
| **1 — Hazırlık** | | |
| | 1.1 Otomasyon Geliştirme | ~27.646 ₺ |
| | 1.2 Alet ve Atölye Tedariği | ~59.530 ₺ |
| **2 — Araç** | | |
| | 2.1 Araç Alımı | ~1.800.000 ₺ |
| **3 — Karkas İnşaat** | | |
| | 3.1 Sigma Profil İskelet (mobilya) | ~17.670 ₺ |
| | 3.2 Zemin Geliştirme | ~7.440 ₺ |
| | 3.3 Su Depoları (şasi altı) | ~7.972 ₺ |
| **4 — Kabuk İşleri** | | |
| | 4.1 Pencere (Jarup + Dometic) | ~88.390 ₺ |
| | 4.2 Tavan Klima (Evacool) | ~76.500 ₺ |
| | 4.3 Çatı Ray Sistemi | ~2.000 ₺ |
| | 4.4 Güneş Paneli (Pantec) | ~18.140 ₺ |
| | 4.5 Tente (Thule 6300) | ~73.877 ₺ |
| | 4.6 Kamera Montajı | ~24.631 ₺ |
| **5 — İç Hazırlık** | | |
| | 5.1 Yalıtım | ~11.750 ₺ |
| | 5.2 Elektrik Altyapı (ekipman) | ~165.860 ₺ |
| | 5.2 Elektrik Altyapı (kablolama) | ~11.080 ₺ |
| | 5.3 Su 1. Fix (boru döşeme) | ~2.145 ₺ |
| | 5.4 Banyo Altyapı | ~2.284 ₺ |
| | 5.5 Cihaz Yerleştirme | ~132.499 ₺ |
| **6 — İç Kaplama** | | |
| | 6.1 İç Kaplama (tavan dolapları dahil) | ~300.000 ₺ |
| **7 — Tamamlama** | | |
| | 7.1 Elektrik Bağlantı Tamamlama | — |
| | 7.2 Su Tesisatı Tamamlama | ~245.502 ₺ |
| | 7.3 Elektrik 2. Fix | ~17.481 ₺ |
| | 7.4 Mutfak Tezgah Montajı | ~31.048 ₺ |
| | 7.5 Banyo Batarya Montajı | ~12.151 ₺ |
| **8 — Tescil** | | |
| | 8.1 Tescil ve Proje | ~630.000 ₺ |
| | | |
| **GENEL TOPLAM** | **(tahmini, 6.1 ~300k dahil)** | **~3.765.596 ₺** |

> **Kur:** 1 USD ≈ 44 ₺, 1 EUR ≈ 51 ₺ (Şubat 2026). Fiyatlar ±%15 sapabilir. 6.1 iç kaplama **~300.000 ₺** plan bütçesiyle dağıtılmıştır; kesin tutar firmadan teklif alındıkça güncellenir.

---

*Bu plan yaşayan bir dokümandır. Her adım tamamlandıkça güncellenir.*
