# Batarya Paketi

> Bu belge, akü paketi için farklı üreticilerden teklif alınması amacıyla hazırlanmıştır. Aşağıdaki spesifikasyon, tedarik şartları ve teslim testleri bağlayıcıdır.

| # | Ürün / Malzeme | Adet | Not |
|---|----------------|:----:|-----|
| 1 | **24 V / 314 Ah LiFePO4 Akü Paketi** — akücüye yaptırılacak (detay aşağıda § _Akü Paketi Spesifikasyonu_) | 1 | **Hücreler:** 8× prismatik 3.2 V / 314 Ah A-Class — tercih EVE MB31, alt seçenek Gotion LF314 (her ikisi de aynı batch'ten). **BMS:** Daly Smart Active Balance 8S 24V **400 A** (BT + RS485 + CAN, 1 A active balance). Toplam nominal: **24 V / 314 Ah / ~7.5 kWh**. |

---

## Akü Paketi Spesifikasyonu

> ⚠️ **KRİTİK — Haberleşme Çıkışları:** BMS'in **RS485 ve CANbus çıkışları akü kasasının dışında, erişilebilir bir konnektörde** bulunmalıdır. Anlık değerler (gerilim, akım, SoC, hücre voltajları, sıcaklık) **RS485 üzerinden Home Assistant tarafına gerçek zamanlı aktarılacak ve izlenecektir.** Bu nedenle RS485 hattı kalıcı olarak bağlı kalacak şekilde erişilebilir olmalıdır.

### Hücre Tedarik Şartları

- **A-Class grade** — fabrika kalite damgası ve QR kod / seri numarasının her hücrede okunabilir olması
- **Aynı batch (üretim partisi)** — 8 hücrenin tamamının tek seferde, aynı parti numarasından gelmesi
- **Garanti** — en az 24 ay; kapasite kaybı %20'yi geçerse değişim
- **Terminal** — M6 veya M8 vidalı
- **Ambalaj** — hücreler bağımsız ambalajda, transport hasar belgesi açılırken kontrol edilebilir

### Kasa / Mekanik

- **Boyut & ağırlık limiti** — kasa, aracın akü bölmesine sığacak şekilde boyutlandırılmalı; olası ölçüler teklif öncesinde paylaşılacaktır
- **Hücre sıkıştırma fikstürü (compression)** — 8 prismatik hücre, sabit basınçlı fikstür ile sıkıştırılmalı; şişmeyi önlemek ve hücre ömrünü korumak için zorunludur
- **IP koruma & titreşim** — kasa en az **IP54** sınıfında, araç ortamına uygun titreşim/şoka dayanıklı montajla sabitlenmiş olmalı
- **Busbar** — hücre bağlantıları nikel kaplı bakır busbar ile; terminal tork değerleri belgelenmeli

### Teslim Anında Test (bağlamadan önce)

| Test | Hedef | Açıklama |
|---|---|---|
| Açık devre voltajı (OCV) | 8 hücre arası ΔV ≤ **20 mV** | Multimetre ile tek tek ölçüm; teslimden önce hücreler dinlenmiş olmalı (≥ 4 saat) |
| AC iç direnç (1 kHz) | EVE: ≤ **0.25 mΩ**, Gotion: ≤ **0.5 mΩ** | YR1035 / RC3563 tipi IR meter ile; 8 hücre arası fark ≤ %10 |
| 50 A deşarj — gerilim çökmesi (sag) testi (60 sn) | Voltaj düşüşü 8 hücre arası fark ≤ **30 mV** | DC elektronik yük veya kalibre edilmiş şarjlı çıkış; aşırı gerilim çökmesi olan hücre defolu sayılır |

Testlerden herhangi birinde uyumsuzluk görülen hücre kabul edilmeyecek; değişimi veya iadesi görüşülecektir.

### Bağlama Öncesi Top-Balance

8 hücre paralel bağlanır (paketin nominal voltajında değil), CC-CV ile 3.65 V'a kadar şarj edilir (≤ 0.1C akım). Tüm hücreler 3.65 V'a ulaştığında akım düşmeye başlar; bu, top-balance'ın tamamlandığını gösterir. İşlem 12-24 saat sürebilir. Aktif dengeleyici devreye girmeden önce tüm hücrelerin aynı SoC seviyesinde olması beklenmektedir.

### BMS Boyutlandırma Hesabı (Neden 400 A?)

24 V tarafındaki yük analizi:

| Yük | Sürekli akım | Peak akım (kısa süre) |
|---|---|---|
| EasySolar-II inverter (3000 VA) | ~100 A (3000 W / 24 V) | **~250 A** (6000 W overload, 5 sn datasheet) |
| Klima Evacool RV 2700 (AC tarafta ~1100 W) | ~48 A (inverter girişi) | +~50–80 A (kompresör LRA startup geçici overlap) |
| Orion 24/12-80 DC-DC (12V çıkışta peak yüklerde) | ~40 A (960 W) | ~45 A |
| Buzdolapları (Evacool Berlin 90 L + D31 R) | ~8–10 A | — |
| Aydınlatma + kontrol + diğer küçük yükler | ~5–10 A | — |
| **TOPLAM (gerçekçi worst-case eşzamanlı)** | **~110 A sürekli** | **~300–330 A peak** |
