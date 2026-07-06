# CamperGaraj — FAZ 1

## Proje Bağlamı

- **Araç:** MAN TGE L5H4 18.4 m³ (~7.4 m gövde, önden çekişli)
- **Ses / ısı yalıtımı:** Kısmen tamamlandı, kalanı devam edecek
- **Bu doküman:** Faz 1 kapsamındaki temin + montaj kalemlerinin teknik tarifi

---

## 1) Alınacak + CamperGaraj Montajlayacak

> Bu bölümdeki kalemler hem temin edilip hem de CamperGaraj tarafından araca kurulması planlanıyor.

| # | Ürün / Malzeme | Adet | Not |
|---|----------------|:----:|-----|
| 1 | **Pervazlı pistonlu karavan penceresi — 60×35 cm** (çift katlı akrilik, EPDM contalı sıkıştırma montaj) | 2 | Arka yatak sağ + sol yan duvar. Marka: Jarup / Berhimi / SUGA / Carbest veya eşdeğer. |
| 2 | **Pervazlı pistonlu karavan penceresi — 50×30 cm** (çift katlı akrilik, EPDM contalı sıkıştırma montaj) | 1 | WC / banyo. Mahremiyet için koyu / buzlu cam tercih edilebilir. Marka: Jarup / Berhimi / SUGA / Carbest veya eşdeğer. |
| 3 | **Pervazlı pistonlu karavan penceresi — 50×120 cm veya 45×110 cm** (çift katlı akrilik, EPDM contalı sıkıştırma montaj) | 2 | Kanepe alanı + giriş kapısı üst bölgesi. Salon yerleşimine uygun olan ölçüyü firmanın seçmesi rica edilir (her iki boy da uygun aralıkta). Marka: Jarup / Berhimi / SUGA / Carbest veya eşdeğer. |
| 4 | **24V DC Tavan Kliması — ✅ ALINDI & TAKILDI** (çift fanlı + fırçasız DC motor) | 1 | **Haier Elektrikli Park Kliması 24V — 6. Nesil** (Coolman dağıtım). Onaylı spec: çift fanlı, fırçasız, **24V hermetik** kompresör, bakır petek evaporatör, **800 W nominal / 2800 W max soğutma / 9550 BTU**, soğutma aralığı 1000–2800 W, **COP ≥ 3.5**, nominal 14–26 A, **kalkış 43 A**, hava debisi 360/480 m³/h, 48 dB, gaz HFC-134a 450 g, **34 kg**, dış ölçü 840×880×220 mm, montaj kesimi 450×400 – 650×550 mm, performans limiti 45 °C. **24V DC — 220V/inverter sistemine bağlı değildir.** |
| 5 | **800 W ETFE Esnek Güneş Paneli Seti — son nesil** (hücre verimi ≥ %23, IBC veya Maxeon arka temas hücreli) | 1 set | Tavana yapıştırma ile monte edilmesi, panel çıkışlarının seri bağlanarak harici **SmartSolar MPPT 150/45** (Victron Cihazlar RFP — Kalem #2; MultiPlus-II GX'e VE.Direct ile) girişine inmesi planlanıyor. **Dikkat:** 150/45 Voc tavanı 145 V → string voltajı 145 V altında kalmalı (bkz. aşağıda MPPT uyumu). Önerilen ürünler (son nesil ETFE laminasyonlu): **TommaTech 170 Wp Esnek Panel** (TR üretimi, IBC + ETFE, 2 yıl garanti — 5 adet seri ≈ 850 W) veya **SunPower Maxeon hücreli ETFE 200 W** modeller (≥%23 verim, 4 adet seri = 800 W). **Tercih edilmeyen ürünler:** PET/PVF arka kaplamalı eski nesil esnek paneller, hücre verimi %20 altı modeller, ETFE laminasyonsuz "semi-flex" panel klonları. |
| 6 | **Şasi altı (underslung) su depoları — özel imalat** (1× 180 L temiz su + 1× 90 L gri su) | 2 | TR pazarında MAN TGE L5 (LWB/XLWB) için hazır underslung su deposu bulunmuyor; depoların özel olarak yaptırılması gerekiyor. Referans olarak UK üreticisinin (onlinetankstore.co.uk) MAN Crafter / VW Crafter LWB+XLWB için 180 L ve 90 L underslung tankları kullanılabilir. |
| 7 | **Roof-mount (tavan üstü) kasetli kollu tente — 4.5 m** | 1 | MAN TGE L5H4 (~7.4 m gövde) için 4.5 m tavan üstü montajlı kasetli tente.  **Fiamma F80s 450** (yeni nesil aerodinamik alüminyum kasa, F65s'e göre %20 ince kesit) veya **Dometic PerfectRoof PR2500 4500 mm**. Manuel kollu , beyaz kasa, koyu kumaş (UV + leke). Ayrıca tente altı aydınlatma için dış mekan led şerit kullanımı hedefleniyor. Serit montajı için tente ile uyumlu aydınlatma profilininde montajı gerekiyor.|

---

## Tablo 1 — Teknik Notlar

### Pencere montaj tipi (Kalemler #1–3)

Pencerelerin tamamının **pervazlı (framed) sıkıştırma montaj** tipinde olması tercih ediliyor — alüminyum dış pervaz ve iç pervaz sac duvarını EPDM lastik conta ile sıkıştırarak tutar. Tercih edilmeyen montaj tipleri:

- **Yapıştırma camlı pencere** (bonded window — yapısal sealant ile cam-to-body, Sprinter fabrika konversiyonu tipi) — bu projede uygun değil
- **Kauçuk fitilli "RubberVision" tipi** (Jarup'un JRxxxxRFG kodlu kauçuk çerçeveli serisi — alüminyum pervazsız, otomotiv cam fitili benzeri) 

Klasik pervazlı sıkıştırma tipi tamir / değişim açısından daha esnek ve çift katlı akrilik arası hava boşluğu ısı izolasyonu sağlıyor. Dahili sineklik + karartma perdesinin bulunması beklenir. UV dayanımlı PMMA akrilik tercih ediliyor.

### Klima nesil seçim kriteri (Kalem #4)

Çin tabanlı karavan klima pazarı yıllık iterasyonla yenileniyor; üretici / distribütör modelleri **"5.Nesil / 4.Nesil"** veya **"Gen X"** şeklinde etiketliyor (örn. Haier 5.NESİL = son sürüm). Mümkün olan en son nesil modelin seçilmesi rica ediliyor; eski jenerasyonlardan uzak durulması iyi olur. Üreticiden / tedarikçiden **production date / model year** yazılı olarak sorulup teyit alınması faydalı olur; üretim tarihi 6 aydan eski modellerin tercih edilmemesi öneriliyor.

Aranan özellikler:

- **Çift fan** (evaporatör + kondenser)
- **Fırçasız (brushless) DC motor**
- **Hermetik veya inverter kompresör** (sabit hızlı non-inverter tercih edilmiyor)
- **COP ≥ 3.0**
- Hava debisi ≥ 400 m³/h

### Klima taşıyıcı çerçeve (Kalem #4 — montaj)

Aracın dış tavanı GRP fiber glass olduğu için yapısal taşıma kapasitesi düşük; klima (~34 kg) tek başına tavandan asılırsa zamanla yorulma yaratabilir. Bu nedenle aşağıdaki şekilde monte edilmesi rica ediliyor:

- Araç iç tavanındaki MAN TGE fabrika M8 dişli montaj noktalarından destek alan **alüminyum veya çelik profil çerçeve** kurulması — yük yayıcı / taşıyıcı görevini bu çerçevenin üstlenmesi hedefleniyor.
- Klima ünitesinin bu iç çerçeveye sabitlenmesi; dış GRP tavanın yalnızca klima geçişi için kesilmesi, taşıma fonksiyonu üstlenmemesi.
- Tavan kesim çevresinde sızdırmazlığın klimanın orijinal contası + butyl bant ile sağlanması.

Bu yaklaşım GRP tavanın uzun vadeli yorulmasını ve klima oturma yüzeyinin ezilmesini engelliyor; klimanın ağırlık ve titreşim yükü çerçeve üzerinden M8 noktaları aracılığıyla araç gövde / şasi yapısına aktarılıyor.

### Güneş paneli — Inverter (MPPT) uyumu (Kalem #5)

800 W ETFE panel seti, **harici Victron SmartSolar MPPT 150/45-Tr (VE.Direct)** üzerinden 24 V bataryayı besleyecek; MPPT, **MultiPlus-II GX 24/3000**'e VE.Direct ile bağlanır (mimari değişikliği: EasySolar-II TR'ye vergi/ithalat nedeniyle gelmiyor → MultiPlus-II GX + harici MPPT).

**MPPT giriş limitleri (150/45):**

- Maks PV açık devre voltajı (Voc): **145 V** (mutlak tavan — VE.Direct MPPT'lerde en yüksek Voc sınıfı budur)
- Maks şarj akımı: **45 A** (24 V tarafında)
- Maks PV Isc: **50 A**
- 24 V batarya için maks PV array gücü: **1300 W** (800 W rahatça altında, clipping yok)

**Panel:** 4 × **ANTFEA 200 W ETFE esnek** (mono, MC4) — panel başına **Voc 25 V, Vmp 20 V, Isc 10.6 A, Imp 10 A** (1570×700×2 mm, 3.7 kg). Toplam 800 W.

**Uygun seri konfigürasyonlar (ikisi de 150/45 limitleri içinde):**

| Konfigürasyon | Toplam Güç | Voc (STC → soğuk ~−15 °C) | Isc | Değerlendirme |
|---|---|---|---|---|
| **4S — 4 seri** | 800 W | 4 × 25 = **100 V** → ~113 V | 10.6 A | ✅ Voc'a bol pay (145 V). İnce kablo, düşük kayıp, loş ışıkta erken başlar. Tek panel gölgelenince **tüm string düşer**. |
| **2S2P — 2 seri 2 paralel** | 800 W | 2 × 25 = **50 V** → ~57 V | 2 × 10.6 = **21.2 A** | ✅ **Kısmi gölgeye dayanıklı** (bir string gölgede kalsa diğeri üretir). ~21 A → biraz kalın kablo + Y-konektör; 2 paralelde sigorta genelde gerekmez. |

Her ikisi de sınırların rahat içinde (Voc < 145 V, Isc < 50 A, güç < 1300 W; çıkış ~28 A < 45 A). 150/45 **tek-tracker** olduğundan seçim gölgeye göre yapılır: karavan tavanında kısmi gölge muhtemelse **2S2P**, gölge minimal/homojense **4S** (en verimli ve en basit). Montajda tavandaki gerçek gölge paternine göre karar verilir. MC4 konnektör; 4S için 4–6 mm², 2S2P için 6 mm² UV dayanımlı solar kablo.

### Güneş paneli — Tavana yapıştırma (Kalem #5 — montaj)

ETFE esnek panellerin GRP fiber glass tavan üzerine yapıştırma ile monte edilmesi planlanıyor. Tam kapama yapıştırma yerine panel altında hava boşluğu kalacak şekilde uygulama tercih ediliyor (sıcaklıkla verim kaybını ve laminasyon yorulmasını azaltmak için).

**Önerilen yapıştırma yöntemi:**

- Yapıştırıcının zigzag (S-dalgası) deseninde sık sürülmesi; tam yüzey kaplaması yapılmaması
- Panel kenarları ve köşelerinin sızdırmaz şekilde tutturulması, ancak yüzey ortasında zigzag çizgiler arasında hava kanallarının kalması (~5–10 mm boşluk)
- Bu hava kanalları sayesinde panel altında ısınma ile oluşan basınç dışarı atılıyor, panel sıcaklığı ~5–10 °C düşürülüyor
- Yapıştırıcı: **Sikaflex 252i** veya eşdeğer (UV dayanımlı, esnek poliüretan, GRP + ETFE ile uyumlu)

Tam kapama yapıştırma uygulanırsa panel altında ısı birikiyor → verim %15–20 düşüyor, ETFE laminasyon zamanla yoruluyor, panel kabarabiliyor. Zigzag yöntem standart RV/karavan ETFE montajı olarak biliniyor.

### Güneş paneli — Kablo sonlandırma (Kalem #5 — kritik güvenlik)

Solar panel kabloları tavandan araç içine indirildikten sonra **uçlarının açık / boşta bırakılmaması** önem taşıyor. Paneller gün ışığında sürekli üretim yapıyor; string ucunda **daima yüksek Voc bulunuyor** (4S ~100 V / soğukta ~113 V, 2S2P ~50 V) — açık uç montaj sırasında elektrik şok ve boşta sallanan iletkenlerle kısa devre / yangın riski yaratabiliyor.

**Önerilen çözüm:**

- Tavandan inen solar kablonun, araç içinde teknik alan girişinde **Anderson tarzı kapalı çift kutuplu yüksek akım DC soket** ile sonlandırılması — örnek: **Anderson SB50** (50 A / 600 V) veya **Anderson Powerpole 45 A**
- Soketin dişi tarafının kablo ucunda kalıcı şekilde bağlanmış ve sızdırmaz montajla teslim edilmesi; erkek tarafının sonradan kullanıcı tarafından takılması
- Polaritenin düzgün etiketlenmesi (kırmızı = +, siyah/mavi = −) — yanlış polariteyle bağlantı MPPT'ye zarar verebiliyor
- Kablonun araç içinde askıda kalmaması, yol boyunca klipslerle sabitlenmesi, gerginlik bırakılmaması

### Su depoları — Referans tasarımlar (Kalem #6)

TR pazarda MAN TGE L5 (LWB / XLWB) için hazır underslung su deposu bulunmadığından depoların özel imal edilmesi planlanıyor. Aşağıdaki UK üreticisinin (onlinetankstore.co.uk) MAN Crafter / VW Crafter için hazır ürünleri **ölçü ve yerleşim referansı** olarak kullanılabilir:

**Temiz su (180 L):**

- Ürün sayfası: <https://www.onlinetankstore.co.uk/product/180-litre-underslung-tank-crafter-man/>
- Teknik çizim (GA): <https://gasit.co.uk/wp-content/uploads/2022/12/180-litre-underslung-MAN-Carfter.pdf>

**Gri su (90 L):**

- Ürün sayfası: <https://www.onlinetankstore.co.uk/product/90-litre-underslung-water-tank-crafter-man/>
- Teknik çizim (GA): <https://www.onlinetankstore.co.uk/wp-content/uploads/2022/02/90-Litre-Crafter-MAN-LWB-XLWB-Underslung-Tank-GA-CAN-BE-SHARED-1.pdf>

Malzeme tercihi firmaya bırakılıyor: HDPE (yaygın, gıda uyumlu, hafif), paslanmaz krom, alüminyum veya fiberglass. Temiz su deposunun gıda uyumlu malzeme + iç yüzey kaplaması ile imal edilmesi rica ediliyor.

**Her iki depo için beklenen donatım:**

- **Manuel boşaltma vanası** — her deponun altında, küresel veya küresel kollu, donmaya dayanıklı malzeme (pirinç veya paslanmaz çelik), kolayca el ile açılabilir konumda.
- **Vent (hava çıkış) ağzı — her bağımsız tepe noktasında ayrı ayrı** — Depo iç yapısı dalga kıranlarla bölündüğünde her bölme kendi tepe noktasına sahip oluyor; tek bir vent bu durumda yeterli olmuyor. Her bağımsız üst hacmin kendi vent ağzına sahip olması gerekiyor, aksi takdirde doldurma sırasında hava sıkışıyor → sıvı dolmuyor; boşaltma sırasında vakum oluşuyor → sıvı akmıyor. Tüm vent uçlarına sineklik / böcek tıkayıcı eklenmesi, hattın dış ortama yönlendirilmesi (kabin içine değil) rica ediliyor.
- **Dalga kıran (baffles) panelleri** — depo iç hacminin kabaca 1/3 ve 2/3 bölümlerine yerleştirilen, sıvı hareketini sınırlayan iç bölmeler. Sürüş sırasında suyun çalkalanıp denge / fren etkilemesini engelliyor. Baffle panellerin perfore (delikli) olması — sıvı geçişine izin verirken hareketi azaltır.
- **Seviye sensörü flanşı — 4-20 mA / 0-20 mA akım çıkışlı (current-loop) sensör için** — Waveshare 8CH Analog Acquisition modülü direnç (Ohm) okumuyor, yalnızca akım veya gerilim sinyali okuyor. Bu nedenle otomotiv tipi Ohm-bazlı şamandıralar (örn. KUS Ohm 0-190) bu sistemle uyumlu değil. Endüstriyel level transmitter (hidrostatik / kapasitif / ultrasonik / şamandıra-bazlı current-loop çıkışlı) bağlantısı için standart M16 veya 1" NPT dişli flanş hazırlanması rica ediliyor. Sensörün kendisi otomasyon altyapısı kapsamında ayrıca temin edilecek; firmadan yalnızca flanş hazırlığı bekleniyor.
- **Doldurma ağzı** — temiz su deposunda dış kapaklı, kilitlenebilir; gri su deposunda mantıklı bir noktada (genelde alt akış için doğrudan drenajdan gelir).

### Su depoları — Konumlandırma (Kalem #6 — montaj)

**Önemli not:** Her iki deponun şasi altına (underslung) ve **iki aks arası bölgeye** yerleştirilmesi gerekiyor.

- MAN TGE L5H4 uzun gövdeli (~7.4 m) + önden çekişli (FWD) — yük dağılımı sürüş dinamiği için önemli
- 180 L + 90 L = **270 kg sıvı yükü** (dolu hâlinde) — küçük bir yük değil
- Arka uzun overhang'e yük binerse ön aks yükü hafifliyor → direksiyon hakimiyeti azalıyor, yağmurda / karda traksiyon düşüyor
- İki aks arası konumlandırma → ağırlık merkezi şasi orta hattında kalıyor, sürüş dengeli kalıyor

Depoların şasi alt rayına asılma noktalarının MAN TGE'nin fabrika mounting points'lerinden seçilmesi ve ek kaynak / delme yapılmaması gerekiyor. UK referans tanklarının montaj braketleri / askı kayışları örnek alınabilir.

### Tente montajı (Kalem #7 — önemli)

Tente braketlerinin **dış GRP tavan veya GRP üst kaplamasına monte edilmemesi** gerekiyor. GRP'ye delinmesi durumunda olası sorunlar:

- Kısa vadede yağmur sızıntısı (vida başlarından, conta yorulmasıyla)
- Tente açıkken rüzgar yükü altında braketin gevşemesi / sökülmesi
- Vibrasyonun GRP'yi çatlatması, panel kabarması

**Önerilen yöntem:**

- Tente montaj braketlerinin GRP'nin hemen altındaki orijinal MAN TGE metal sac yapısına (yan duvar üst kenarı / orijinal çatı sac kirişi) tutturulması — yük dış kaplamaya değil, taşıyıcı fabrika sac yapısına aktarılıyor.

Tente markaları kendi montaj kit'lerini sağlıyor (Thule Wall Bracket Kit, Fiamma Wall Mount Adapter); uygun olanın seçilmesi ve sac yapı bağlantısına uyarlanması firmaya bırakılıyor.

Bu yaklaşım Kalem #4 (klima taşıyıcı çerçeve) ile aynı mantıkta — **GRP kaplama yapısal yük taşımıyor, MAN TGE orijinal metal sac yapısı taşıyor.**

