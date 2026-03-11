# Bütçe Yönetimi

Karavan otomasyon ve elektrik altyapısı için aşamalı satın alma planı.

---

## T0 — İlk Alım (Otomasyon Altyapısı — Evde Geliştirme)

Karavan inşaatına başlamadan önce temin edilmesi gereken otomasyon ve kontrol donanımları. Evde masaüstünde HA kurulumu, Modbus entegrasyonu ve otomasyon geliştirmesi yapılacak.

| # | Ürün | Model | Adet | Birim Fiyat | Toplam | Kaynak |
|---|------|-------|------|-------------|--------|--------|
| 1 | Ana Bilgisayar Kasası | Waveshare IPCBOX-CM5-A (4x RS485, CAN, 2DI/2DO, dual ETH, 7-36V) | 1 | ~4.400 ₺ | ~4.400 ₺ | [Waveshare](https://www.waveshare.com/ipcbox-cm5-a.htm) |
| 2 | CM5 Modül | Raspberry Pi CM5 8GB Lite (eMMC'siz, BCM2712 2.4GHz) | 1 | ~3.000 ₺ | ~3.000 ₺ | SAMM Market |
| 3 | NVMe SSD | 512GB M.2 2242 NVMe SSD (Kioxia / WD) | 1 | ~1.000 ₺ | ~1.000 ₺ | Genel |
| 4 | DI/DO Modülü | Waveshare Modbus RTU IO 8CH (8DI/8DO, RS485) | 3 | ~1.428 ₺ | ~4.284 ₺ | [SAMM Market](https://market.samm.com/endustriyel-8-kanalli-dijital-giris-ve-cikis-modulu) |
| 5 | Analog Giriş Modülü | Waveshare 8-Ch Analog Acquisition (RS485) | 1 | ~1.555 ₺ | ~1.555 ₺ | SAMM Market |
| 6 | Araç Aküsü Float Şarj | Victron Blue Smart IP65s 12/5A + DC connector | 1 | ~5.000 ₺ | ~5.000 ₺ | Tekmobil / MarinReyon |
| 7 | Sigortalı Dağıtım Kutusu | 12'li İkaz Işıklı Negatif Barali Sigorta Kutusu | 1 | ~€24 (~1.225 ₺) | ~1.225 ₺ | karavanicin.com |
| 8 | RS485 Kablo + Konnektör | CAT5e/shielded + terminal bloklar | 1 set | ~500 ₺ | ~500 ₺ | Genel |
| 9 | Kontrol Paneli Ekranı | Waveshare 11.9" HDMI LCD 320×1480 IPS Touch (Capacitive, Toughened Glass) | 1 | ~$103 (~4.538 ₺) | ~4.538 ₺ | [Waveshare](https://www.waveshare.com/11.9inch-HDMI-LCD.htm) |
| | | | | **T0 TOPLAM** | **~25.502 ₺** | |

> **Kur:** 1 USD = 44,07 ₺, 1 EUR = 51,21 ₺ (17 Şubat 2026)
>
> **Not:** Fiyatlar araştırma tarihindeki güncel web fiyatlarıdır, stok ve kur değişimlerine göre ±%15 sapma olabilir.

### T0 Kapsamı Açıklama

- **#1-3**: Waveshare IPCBOX-CM5-A endüstriyel kutu + RPi CM5 8GB + 512GB NVMe SSD = Home Assistant ana bilgisayar (4x RS485, CAN, 2DI/2DO, 7-36V DC direkt besleme, dual ETH)
- **#4**: 3x 8DI/8DO → bistable röle toggle (DO) + durum feedback (DI)
- **#5**: Su tankı seviye sensörleri, sıcaklık okumaları
- **#6**: Araç aküsü float şarj (EasySolar-II AC OUT 2'den beslenir)
- **#7**: DC taraf sigorta dağıtımı
- **#8**: Modüller arası RS485 haberleşme kablolaması
- **#9**: Kontrol paneli ekranı — giriş kapısı üstü, HDMI + USB direkt IPCBOX-CM5-A bağlantısı, HA dashboard

---

## T2 — Karavan Cihaz Donanımları

Karavan montajı aşamasında alınacak, fiziksel kurulum gerektiren kalemler.

| # | Ürün | Model | Adet | Birim Fiyat | Toplam | Kaynak |
|---|------|-------|------|-------------|--------|--------|
| 1 | Master Bistable Röle | CHINT NJMC1 32A 4P (Camper ON/OFF) | 1 | ~350 ₺ | ~350 ₺ | Elektrik market |
| 2 | Bireysel Bistable Röle | CHINT NJMC1 16A 2P | 19 | ~200 ₺ | ~3.800 ₺ | Elektrik market |
| 3 | Shelly Plus RGBW PM | Shelly (Wi-Fi, dimmer + renk, 24V) | 2 | ~€24 (~1.225 ₺) | ~2.450 ₺ | Shelly / Bosteknik |
| 4 | Blade Fuse Block 8P | 8 pozisyonlu blade sigorta dağıtım bloğu | 2 | ~250 ₺ | ~500 ₺ | karavanicin.com |
| 5 | Panasonic Sigorta Kutusu | Sıva üstü modüler sigorta kutusu (220V panel) | 1 | ~500 ₺ | ~500 ₺ | Elektrik market |
| 6 | MCB Sigortalar | CHNT C16 otomatik sigorta (220V devreler) | 7 | ~80 ₺ | ~560 ₺ | Elektrik market |
| | | | | **T2 TOPLAM** | **~8.160 ₺** | |

### T2 Kapsamı Açıklama

- **#1**: 1x master 32A 4P → Camper ON/OFF (220V + 24V + 12V rail anahtarlama)
- **#2**: 19x bireysel 16A 2P → 7 AC çıkış + 8 aydınlatma + 4 DC yük (1P switch + 1P feedback)
- **#3**: 2x Shelly → ana yatak tavan LED + oturma ambient (dimmer + renk)
- **#4**: 2x blade fuse block → DC yük dağıtımı (aydınlatma + diğer)
- **#5-6**: 220V panel koruma (modüler sigorta kutusu + 7x MCB sigorta)

---

## T1+ — Sonraki Alımlar (Planlanacak)

Karavan inşaat sürecinde ihtiyaç duyuldukça temin edilecek kalemler:

- EasySolar-II 3kVA MPPT 250/70 GX
- LiFePO4 batarya paketi (8S 280Ah)
- Victron Orion XS 1400 DC-DC şarj
- Evacool Eva RV 2700 Premium Klima
- Güneş paneli (400W, sabit çatıya montaj)
- Shore power girişi + kablolama
- AC dağıtım panosu + sigortalar + kaçak akım rölesi
- Cihazlar (indüksiyon ocak, bulaşık makinesi, çamaşır makinesi, buzdolabı)
- Clesana C1 tuvalet (12V)
- Truma Combi 4D (12V, hava + su ısıtma)
- Push buttonlar, prizler, USB-C soketler
- NYAF kablolama (4mm² + 2.5mm²)
- Aydınlatma armatürleri (LED spot, şerit)
- SHURflo macerator pompa, hydrofor

---

*Bu bütçe yaşayan bir dokümandır. Her alım sonrası gerçekleşen fiyatlar ile güncellenir.*
