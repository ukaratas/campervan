# Karavan Geliştirme Planı

Iveco Daily 18m³ karavan dönüşüm projesi için sıralı iş planı ve malzeme listeleri (BOM).

Her adımda:
- **Sorumlu**: DIY veya FİRMA
- **Bağımlılık**: Hangi adım(lar)dan sonra başlayabilir
- **BOM Tablosu**: Ürün, Model, Adet, Tahmini Fiyat, Önden Alınabilir (E/H)

---

## Adım 0 — Otomasyon Geliştirme (Evde)
> **DIY** | Bağımlılık: Yok

Otomasyon yazılımının ve donanımlarının tedariki. Home Assistant kurulumu, Modbus entegrasyonu, DI/DO testleri. Araç olmadan evde masaüstünde yapılır.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| Ana Bilgisayar Kasası | Waveshare IPCBOX-CM5-A | 1 | ~4.400 ₺ | E |
| CM5 Modül | Raspberry Pi CM5 8GB Lite | 1 | ~3.000 ₺ | E |
| NVMe SSD | 512GB M.2 2242 NVMe | 1 | ~1.000 ₺ | E |
| DI/DO Modülü | Waveshare 8DI/8DO (RS485) | 3 | ~4.284 ₺ | E |
| Analog Giriş Modülü | Waveshare 8-Ch Analog (RS485) | 1 | ~1.555 ₺ | E |
| Araç Aküsü Float Şarj | Victron Blue Smart IP65s 12/5A | 1 | ~5.000 ₺ | E |
| Sigortalı Dağıtım Kutusu | 12'li sigorta kutusu | 1 | ~1.225 ₺ | E |
| RS485 Kablo + Konnektör | CAT5e shielded + terminal bloklar | 1 set | ~500 ₺ | E |
| | | | **~20.964 ₺** | |

> Detay: [budget-management.md](budget-management.md) T0 bölümü

---

## Adım 1 — Ön Hazırlık ve Malzeme Tedariği
> **DIY** | Bağımlılık: Yok (Adım 0 ile paralel)

Uzun tedarik süreli ve önden alınabilecek malzemelerin toplu siparişi. Tüm adımlardan "Önden = E" olanlar bu aşamada sipariş edilebilir.

---

## Adım 2 — Araç Alımı
> **DIY** | Bağımlılık: Yok

Iveco Daily 18m³ aracın satın alımı.

---

## Adım 3 — Kabuk Hazırlık (Kesim ve Dış Montaj)
> **FİRMA** | Bağımlılık: Adım 2

Araç kaportasına yapılacak kesim, pencere montajı, tavan klima hazırlığı ve yapısal takviye işleri. Firma tarafından yapılmalı.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| Heki (tavan pencere) | Dometic Midi Heki Style 70x50cm | 1 | TBD | E |
| Arka kapı üstü pencere | Karavan pencere 30x50cm | 2 | TBD | E |
| Yan pencere büyük | Karavan pencere 100x50cm | 1 | TBD | E |
| Yan pencere orta | Karavan pencere 60x50cm | 4 | TBD | E |
| Tavan Klima | Evacool Eva RV 2700 Premium | 1 | ~76.500 ₺ | E |
| Pull-down Yatak | Lippert San Diego (manuel/elektrikli) | 1 | TBD | E |
| Yolcu Koltuğu | 2 kişilik emniyet kemerli | 1 | TBD | H |
| Banyo Penceresi | Açılabilir buzlu cam ~30x40cm | 1 | TBD | E |

> Not: Pencere ve heki kesim ölçüleri firma ile birlikte netleştirilecek.

---

## Adım 4 — Yalıtım
> **DIY** | Bağımlılık: Adım 3

Ses ve ısı yalıtımının tamamlanması. Kabuk hazırlıktan sonra, kablo döşemeden önce.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| Ses yalıtım plakası | CTP/Dinamat ses yalıtım | TBD m² | TBD | E |
| Isı yalıtımı | Folyolu yapışkanlı elastomerik kauçuk | TBD m² | TBD | E |

---

## Adım 5 — Elektrik 1. Fix: Kablo Döşeme
> **DIY** | Bağımlılık: Adım 4

Tüm elektrik kablolarının duvar/tavan/zemin altına döşenmesi. **İç kaplama yapılmadan ÖNCE tamamlanmalı.**

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| AC Kablo | NYAF 4mm² (220V hatlar) | ~100m | TBD | E |
| DC Kablo (sinyal/aydınlatma) | NYAF 2.5mm² (24V/12V) | ~150m | TBD | E |
| DC Kablo (yüksek akım) | NYAF 4mm² (24V yüksek akım) | ~50m | TBD | E |
| Kablo koruyucu | Yanmaz spiral kablo koruyucu | TBD m | TBD | E |
| Buat/Junction box | Elektrik buatları | ~20 | TBD | E |
| RS485 Haberleşme kablosu | CAT5e shielded | ~30m | TBD | E |
| Kablo bağı + klips | Montaj malzemesi | 1 set | TBD | E |

> Not: Kablo güzergahları [donanim-ozet.md](donanim-ozet.md) elektrik noktaları tablosuna göre planlanır.

---

## Adım 6 — Su 1. Fix: Boru Döşeme
> **DIY** | Bağımlılık: Adım 4

PEX boruların duvar/zemin altına döşenmesi. **İç kaplama yapılmadan ÖNCE tamamlanmalı.**

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| PEX Boru (soğuk su) | 16mm PEX-A | ~20m | TBD | E |
| PEX Boru (sıcak su) | 16mm PEX-A (izoleli) | ~15m | TBD | E |
| Gri su borusu | 28-32mm esnek hortum | ~10m | TBD | E |
| Bağlantı elemanları | Press fitting / push-fit set | 1 set | TBD | E |

---

## Adım 7 — Banyo Altyapı: Fiber Zemin
> **DIY** | Bağımlılık: Adım 5, Adım 6

Banyo (60cm) ve su alanı için fiber kompozit zemin yapımı.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| Fiber elyaf | Cam elyaf kumaş | TBD m² | TBD | E |
| Epoksi reçine | Laminasyon epoksi + sertleştirici | TBD kg | TBD | E |
| XPS levha | Yoğun XPS köpük | TBD m² | TBD | E |
| Son kat boya | PU beyaz boya (su geçirmez) | TBD lt | TBD | E |

---

## Adım 8 — Su Depoları (Şasi Altı)
> **FİRMA** | Bağımlılık: Adım 2

Şasi altına temiz ve gri su depolarının montajı. Adım 3 ile paralel yapılabilir.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| Temiz su deposu | Polietilen, gıda uyumlu | 1 (200L) | TBD | H |
| Gri su deposu | Polietilen | 1 (100L) | TBD | H |
| Temiz su şamandıra | Seviye sensörü | 1 | TBD | E |
| Gri su şamandıra | Seviye sensörü | 1 | TBD | E |
| Temiz su boşaltma vanası | Manuel vana | 1 | TBD | E |
| Gri su boşaltma vanası | Manuel vana | 1 | TBD | E |

> Not: Depo boyutları aracın şasi ölçülerine göre belirlenecek.

---

## Adım 9 — İç Kaplama (Duvar, Tavan, Zemin)
> **DIY / FİRMA** | Bağımlılık: Adım 5, Adım 6, Adım 7

Elektrik ve su 1. fix tamamlandıktan sonra duvar, tavan ve zemin kaplaması.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| Duvar kaplama | TBD (ahşap panel / lamine) | TBD m² | TBD | H |
| Tavan kaplama | TBD (hafif panel) | TBD m² | TBD | H |
| Zemin döşeme | TBD (vinil / lamine parke) | TBD m² | TBD | H |

> Not: Malzeme seçimleri iç tasarım kararlarına bağlı, araç ölçüldükten sonra netleştirilecek.

---

## Adım 10 — Elektrik Pano ve Batarya Montajı
> **DIY** | Bağımlılık: Adım 9

Ana yatak altı teknik alana batarya, inverter, dağıtım panosu ve otomasyon donanımlarının montajı.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| LiFePO4 Hücre | EVE 3.2V 280Ah prizmatik | 8 | TBD | E |
| BMS | JBD/Overkill 8S 200A RS485/CAN | 1 | TBD | E |
| İnverter/Şarj/MPPT | Victron EasySolar-II 3kVA MPPT 250/70 GX | 1 | TBD | E |
| DC-DC Şarj | Victron Orion XS 1400 | 1 | TBD | E |
| Master Bistable Röle | CHINT NJMC1 32A 4P | 1 | ~350 ₺ | E |
| Bireysel Bistable Röle | CHINT NJMC1 16A 2P | 19 | ~3.800 ₺ | E |
| Blade Fuse Block | 8 pozisyonlu | 2 | ~500 ₺ | E |
| 220V Sigorta Kutusu | Panasonic modüler sıva üstü | 1 | ~500 ₺ | E |
| MCB Sigortalar | CHNT C16 otomatik | 7 | ~560 ₺ | E |
| Kaçak Akım Rölesi | 30mA, 2P | 1 | TBD | E |
| Ana Sigorta | MEGA/ANL 200A | 1 | TBD | E |
| Ana Kontaktör | 24V DC, 200A | 1 | TBD | E |
| Shore Power Girişi | Marin tip priz IP67, 16A | 1 | TBD | E |
| Ana akım kablosu | 16mm² (batarya-inverter) | ~5m | TBD | E |

> Detay: [budget-management.md](budget-management.md) T2 bölümü, [donanim-ozet.md](donanim-ozet.md) otomasyon donanım özeti

---

## Adım 11 — Su Tesisatı Tamamlama
> **DIY** | Bağımlılık: Adım 8, Adım 9

Su tesisatının cihazlara bağlanması, pompa ve ısıtma sistemi montajı.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| Hidrofor (su pompası) | 24V DC basınçlı pompa | 1 | TBD | E |
| Genleşme kabı | 24V balonlu tip | 1 | TBD | E |
| Macerator pompa | SHURflo 24V | 1 | TBD | E |
| Isıtma + Sıcak Su | Truma Combi 4D (12V, dizel) | 1 | TBD | E |
| Truma Kontrol | Truma iNet CP plus | 1 | TBD | E |
| Truma Hava Dağıtım | İzoleli hortum + menfez kiti | 1 set | TBD | E |
| Truma Yakıt Kiti | Yakıt pompası, filtre, dizel hat | 1 set | TBD | E |
| Sıcak su dağıtım kollektörü | Pirinç kollektör | 1 | TBD | E |
| Soğuk su dağıtım kollektörü | Pirinç kollektör | 1 | TBD | E |
| Actuator valf | 24V otomatik vana (donma koruması) | 1 | TBD | E |

---

## Adım 12 — Mobilya
> **FİRMA** | Bağımlılık: Adım 9

Mutfak dolabı, salon masaları, yatak çerçevesi ve depolama mobilyaları.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| Mutfak dolabı | Özel üretim (tezgah + alt dolap + üst dolap) | 1 set | TBD | H |
| Çalışma masası | Yükseklik ayarlı ~80x60cm | 1 | TBD | H |
| Oturma masası | Koltuk grubu masası | 1 | TBD | H |
| Ana yatak çerçevesi | 200cm x araç iç genişliği | 1 | TBD | H |
| Yatak altı çekmeceler | Teknik alan erişimli | TBD | TBD | H |

---

## Adım 13 — Elektrik 2. Fix: Priz, Aydınlatma, Push Button
> **DIY** | Bağımlılık: Adım 10, Adım 12

Kabloları daha önce döşedik (Adım 5). Şimdi uç cihazların montajı.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| 220V Priz | Sıva üstü karavan tipi | 8 | TBD | E |
| 24V Priz | DC priz | 2 | TBD | E |
| 12V Priz | DC priz | 2 | TBD | E |
| USB-C Soket | Otomotiv 100W PD (24V giriş) | 9 | TBD | E |
| Push Button | Anlık buton (NO) | 8 | TBD | E |
| LED Spot | 24V LED spot armatür | TBD | TBD | E |
| LED Şerit | 24V RGB LED şerit (Ana yatak tavan) | TBD m | TBD | E |
| LED Şerit | 24V RGB LED şerit (Oturma ambient) | TBD m | TBD | E |
| Shelly Plus RGBW PM | Wi-Fi dimmer + renk, 24V | 2 | ~2.450 ₺ | E |
| Gece zemin LED | 24V düşük profil LED | TBD | TBD | E |

> Detay: [donanim-ozet.md](donanim-ozet.md) priz/soket ve aydınlatma tabloları

---

## Adım 14 — Cihaz Montajı
> **DIY** | Bağımlılık: Adım 11, Adım 12, Adım 13

Tüm beyaz eşya, mutfak cihazları, banyo donanımları ve güneş paneli montajı.

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| İndüksiyon Ocak | Omake ankastre 1800W | 1 | TBD | E |
| Bulaşık Makinesi | Electrolux ESF2400O | 1 | TBD | E |
| Buzdolabı | EvaCool Eva Berlin 90L (24V) | 1 | TBD | E |
| Çamaşır Makinesi | FİX Mini 3kg | 1 | TBD | E |
| Eviye | Paslanmaz çelik, tek gözlü | 1 | TBD | E |
| Mutfak Musluk | Sıcak/soğuk termostatik | 1 | TBD | E |
| Clesana C1 | Susuz tuvalet (12V) | 1 | TBD | E |
| Lavabo | Kompakt köşe ~40x30cm | 1 | TBD | E |
| Banyo Batarya | Sıcak/soğuk spiralli | 1 | TBD | E |
| Duş Batarya | Termostatik duş bataryası | 1 | TBD | E |
| Güneş Paneli | 400W esnek/rigid, sabit çatıya montaj | 1 | TBD | E |
| HA Ekranı | HDMI dokunmatik ekran | 1 | TBD | E |

---

## Adım 15 — Test ve Devreye Alma
> **DIY** | Bağımlılık: Tüm adımlar

Tüm sistemlerin entegre testi ve Home Assistant konfigürasyonunun finalize edilmesi.

- [ ] Elektrik: Tüm devre testleri, kaçak akım testi
- [ ] 220V: Shore power, inverter, yük yönetimi testi
- [ ] 24V/12V DC: Batarya, DC-DC şarj, güneş paneli testi
- [ ] Su: Basınç testi, sıcak su, drenaj, kaçak kontrolü
- [ ] Otomasyon: DI/DO, bistable röle toggle, feedback doğrulama
- [ ] Aydınlatma: Tüm LED, Shelly RGBW PM, push button testi
- [ ] Klima: Soğutma/ısıtma performans testi
- [ ] Truma: Isıtma + sıcak su, dizel yakıt sistemi testi
- [ ] Güvenlik: Sigorta, kaçak akım, aşırı yük senaryoları
- [ ] Home Assistant: Tüm otomasyon senaryolarının çalıştırılması
- [ ] İlk seyahat öncesi genel kontrol

---

## Özet Tablo

| Adım | İş | Sorumlu | Bağımlılık |
|------|----|---------|------------|
| 0 | Otomasyon Geliştirme | DIY | - |
| 1 | Ön Hazırlık / Malzeme Tedariği | DIY | - |
| 2 | Araç Alımı | DIY | - |
| 3 | Kabuk Hazırlık (kesim, pencere, klima) | FİRMA | 2 |
| 4 | Yalıtım (ses + ısı) | DIY | 3 |
| 5 | Elektrik 1. Fix (kablo döşeme) | DIY | 4 |
| 6 | Su 1. Fix (boru döşeme) | DIY | 4 |
| 7 | Banyo Altyapı (fiber zemin) | DIY | 5, 6 |
| 8 | Su Depoları (şasi altı) | FİRMA | 2 |
| 9 | İç Kaplama (duvar, tavan, zemin) | DIY/FİRMA | 5, 6, 7 |
| 10 | Elektrik Pano + Batarya | DIY | 9 |
| 11 | Su Tesisatı Tamamlama | DIY | 8, 9 |
| 12 | Mobilya | FİRMA | 9 |
| 13 | Elektrik 2. Fix (priz, ışık, buton) | DIY | 10, 12 |
| 14 | Cihaz Montajı | DIY | 11, 12, 13 |
| 15 | Test ve Devreye Alma | DIY | Tüm |

---

*Bu plan yaşayan bir dokümandır. Her adım tamamlandıkça güncellenir.*
