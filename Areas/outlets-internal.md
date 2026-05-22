# İç Prizler ve Anahtarlar

Tüm düğme ve prizler **Viko Thea Modüler** serisi üzerinden geliştirilecektir. USB prizler 24V destekli tekne/kamper yuvarlak prizler olacaktır. Montaj için Viko Thea Serisinde 2M genişliğinden boş kapak kullanılacak; USB priz montajı ona yapılacaktır. Benzer şekilde çakmak soketleri de kapak ile montajlanacaktır.

---

## Kasa Dağılımı

### Garaj (Ağır Cihazlar Alanı)
**7M Kasa:**
- 2M: 220V kapaklı/topraklı priz
- 2M: Boş kapak — USB soket (24V)
- 2M: Boş kapak — 24V çakmak soketi
- 1M: Boş (otomasyon gerekçesi ile hazır tutulur)

**2M Kasa (Truma Combi / Wave 40):**
- 2M: 220V topraklı priz

**2M Kasa (Çamaşır Makinesi):**
- 2M: 220V topraklı priz

### Mutfak — Tezgah Üstü (Ön Alan)
**7M Kasa:**
- 2M: 220V topraklı priz
- 2M: 220V topraklı priz
- 2M: Boş kapak — 24V çakmak soketi
- 1M: Boş (otomasyon gerekçesi ile hazır tutulur)

**4M Kasa:**
- 2M: Boş kapak — USB soket (24V)
- 1M: Push button — Mutfak tezgah aydınlatması
- 1M: Push button — Banyo aydınlatması

### Mutfak — Tezgah Altı (Alet Kasası)
**2M Kasa (Bulaşık Makinası):**
- 2M: 220V topraklı priz

**2M Kasa (İndüksiyon Ocak):**
- 2M: 220V topraklı priz

### Yatak — Başı Sol (Mutfak Tarafı)
**7M Kasa:**
- 2M: 220V topraklı priz
- 2M: Boş kapak — USB soket (24V)
- 1M: Push button — Okuma lambası (sol)
- 2M: Push button — Yatak genel aydınlatması

### Yatak — Başı Sağ (Banyo Tarafı)
**7M Kasa:**
- 2M: 220V topraklı priz
- 2M: Boş kapak — USB soket (24V)
- 1M: Push button — Okuma lambası (sağ)
- 2M: Push button — Yatak genel aydınlatması

### Yatak — Ayak Ucu (Ayakkabı/Çanta)
**2M Kasa:**
- 2M: 220V topraklı priz

### Giriş Üstü (Surgu Kapı)
**4M Kasa:**
- 2M: Boş kapak — USB soket (24V)
- 1M: Push button — Salon aydınlatması
- 1M: Push button — Dış aydınlatması

### Oturma — Kanepe Sol
**4M Kasa:**
- 2M: 220V topraklı priz
- 2M: Boş kapak — USB soket (24V)

### Oturma — Kanepe Sağ
**4M Kasa:**
- 2M: 220V topraklı priz
- 2M: Boş kapak — USB soket (24V)

### Banyo
**2M Kasa:**
- 2M: 220V topraklı priz (traş makinesi, küçük cihazlar)

---

## Özet — Alışveriş Listesi

| Kategorı | Adet | Konum/Not |
|----------|------|-----------|
| **220V Topraklı Priz** | 11 | Garaj 3 (kapaklı + Truma + çamaşır), Yatak başı sol 1, Yatak başı sağ 1, Yatak ayak ucu 1, Mutfak tezgah üstü 2, Mutfak tezgah altı 2, Kanepe sol 1, Kanepe sağ 1, Banyo 1 |
| **220V Kapaklı Priz** | 1 | Garaj (ağır cihaz alanı) |
| **USB Soket (24V)** | 7 | Garaj 1, Yatak başı sol 1, Yatak başı sağ 1, Mutfak tezgah üstü 1, Giriş üstü 1, Kanepe sol 1, Kanepe sağ 1 |
| **24V Çakmak Soketi** | 2 | Garaj 1, Mutfak tezgah üstü 1 |
| **Push Button — Aydınlatma** | 6 | Yatak sol 1, Yatak sağ 1, Mutfak tezgah 1, Banyo 1, Giriş salon 1, Giriş dış 1 — **toplam 6** |
| **Push Button — Okuma Lambası** | 2 | Yatak sol 1, Yatak sağ 1 |
| **Spare DI** | 1 | Boş — gelecek genişleme için |
| **Viko Thea Modüler Kasa** | | 7M (7 adet), 4M (4 adet), 2M (10 adet) — **toplam ~21 modül** |
| **Viko Thea Boş Kapak (2M)** | ~8 | USB ve çakmak soketleri için ön kapak |

**Not:** Tüm 220V prizler topraklı, sıva üstü tip, Viko Thea modüler serisinde. Push buttonlar DI/DO modülüne bağlanır. USB soketler 24V giriş, 100W PD Powerway Bullet tipi.

---

## Otomasyon ve Kontrol

- **Push Button DI:** Waveshare 8DI/8DO Modbus modülüne bağlı — Home Assistant otomasyonu için
- **220V Kontrol:** Waveshare POE ETH 16CH Relay ile MCB panel üzerinden anahtarlama
- **Aydınlatma:** Dimmer kontrol — Shelly Plus RGBW PM ile RGB/whitelight seçeneği
- **Kamera/Hareket:** Güvenlik sensörleri gece aydınlatması otomatik tetikler

---

## Cross-Reference

| Belge | İlişkili Bölüm | Durum |
|-------|-----------------|-------|
| `main-bed.md` | Yatak başı prizler, USB soketler | ✅ Senkronize (1x USB per başı) |
| `seating.md` | Kanepe sol/sağ prizler | ✅ Senkronize (1x 220V + 1x USB per taraf) |
| `kitchen.md` | Mutfak tezgah prizleri | ✅ Senkronize |
| `banyo.md` | Banyo priz (traş) | ✅ Senkronize |
| `plan.md` | BOM: 220V priz (8), USB-C soket (8), 12V priz (1) | ⚠️ Güncelleme gerekebilir — USB soket sayısı 8 → 7 olarak netleşti |

