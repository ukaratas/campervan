# Donanım Özet

Tüm bölgelerdeki elektrik noktaları (prizler, soketler, push buttonlar, aydınlatma) ve otomasyon donanımlarının (DI/DO, NJMC1 bistable röle, Shelly) konsolide özeti.

---

## 📊 Prizler ve Soketler

| Bölge | Konum | 220V | 24V | 12V | USB-C (100W PD) | Toplam Nokta |
|-------|-------|------|-----|-----|------------------|--------------|
| **Ana Yatak** | Yatak Başı Sol (Mutfak tarafı) | 1 | - | - | 2 | 3 |
| **Ana Yatak** | Yatak Başı Sağ (Banyo tarafı) | 1 | - | - | 2 | 3 |
| **Ana Yatak** | Yatak Ayak Ucu (Banyo tarafı) | 1 | - | - | - | 1 |
| **Mutfak** | Tezgah üstü | 2 | - | 1 | 2 | 5 |
| **Oturma/Çalışma** | Masa / duvar | 2 | 2 | 1 | 2 | 7 |
| **Pull-down Yatak** | Şoför kabini üstü | - | - | - | 1 | 1 |
| **Banyo** | Lavabo / duvar | 1 | - | - | - | 1 |
| **TOPLAM** | | **8** | **2** | **2** | **9** | **21** |

---

## 🔘 Push Buttonlar

| Bölge | Konum | Tip | Adet | İşlev | Bağlantı |
|-------|-------|-----|------|-------|----------|
| **Mutfak** | Tezgah üstü / dolap | Push button | 1 | Mutfak aydınlatma | Waveshare DI → HA → DO → bistable röle |
| **Oturma/Çalışma** | Masa / duvar | Push button | 1 | Oturma aydınlatma | Waveshare DI → HA → DO → bistable röle |
| **Ana Yatak** | Yatak Başı Sol | Push button | 2 | Tavan aydınlatma, sol okuma lambası | Waveshare DI → HA → DO → bistable röle |
| **Ana Yatak** | Yatak Başı Sağ | Push button | 2 | Tavan aydınlatma, sağ okuma lambası | Waveshare DI → HA → DO → bistable röle |
| **Pull-down Yatak** | Şoför kabini üstü | Push button | 1 | İç spot aydınlatma | Waveshare DI → HA → DO → bistable röle |
| **Banyo** | Lavabo / duvar | Push button | 1 | Genel spot aydınlatma | Waveshare DI → HA → DO → bistable röle |
| **TOPLAM** | | | **8** | | |

---

## 💡 Aydınlatma Noktaları

| Bölge | Tip | Voltaj | Kontrol | Push Button |
|-------|-----|--------|---------|-------------|
| **Ana Yatak** | Tavan LED (genel) | 24V | NJMC1 16A 2P + Shelly RGBW PM (dimmer + renk) | Yatak başı sol + sağ PB |
| **Ana Yatak** | Okuma lambası sol | 24V | NJMC1 16A 2P bistable | Yatak başı sol PB |
| **Ana Yatak** | Okuma lambası sağ | 24V | NJMC1 16A 2P bistable | Yatak başı sağ PB |
| **Ana Yatak** | Gece zemin aydınlatması | 24V | NJMC1 16A 2P bistable | HA otomasyon |
| **Mutfak** | Mutfak aydınlatma | 24V | NJMC1 16A 2P bistable | Mutfak PB |
| **Oturma/Çalışma** | Oturma aydınlatma | 24V | NJMC1 16A 2P bistable | Oturma PB |
| **Oturma/Çalışma** | Ambient aydınlatma | 24V | Shelly Plus RGBW PM (dimmer + renk) | HA / Shelly |
| **Pull-down Yatak** | İç spot aydınlatma | 24V | NJMC1 16A 2P bistable | Pull-down PB |
| **Banyo** | Genel spot | 24V | NJMC1 16A 2P bistable | Banyo PB |
| **Dış** | Dış aydınlatma 1 | 24V | NJMC1 16A 2P bistable | HA otomasyon |
| **Dış** | Dış aydınlatma 2 | 24V | NJMC1 16A 2P bistable | HA otomasyon |

---

## 🔌 220V Kontrollü Çıkışlar (Sigorta + NJMC1 Bistable Röle)

220V inverter çıkışı **AC OUT 1** (inverter + shore) → NJMC1 32A 4P master röle P1 ile etkinleşir. Her çıkış bireysel NJMC1 16A 2P bistable röle + sigorta ile kontrol edilir. HA yük yönetimi ile inverter modunda çakışma önlenir.

| # | Çıkış | Bölge | Güç / Detay | Kontrol |
|---|-------|-------|-------------|---------|
| 1 | Çamaşır makinesi | Banyo | 160W | Sigorta + NJMC1 16A 2P bistable + DI/DO |
| 2 | İndüksiyon ocak | Mutfak | 1800W | Sigorta + NJMC1 16A 2P bistable + DI/DO |
| 3 | Bulaşık makinesi | Mutfak | 1700W | Sigorta + NJMC1 16A 2P bistable + DI/DO |
| 4 | Klima (Evacool Eva RV 2700) | Ana Yatak | 900-1100W | Sigorta + NJMC1 16A 2P bistable + DI/DO |
| 5 | Yatak + Banyo prizleri (4x) | Ana Yatak / Banyo | 3x yatak + 1x banyo | Sigorta + NJMC1 16A 2P bistable + DI/DO |
| 6 | Mutfak prizleri (2x) | Mutfak | 2x 220V priz | Sigorta + NJMC1 16A 2P bistable + DI/DO |
| 7 | Oturma prizleri (2x) | Oturma/Çalışma | 2x 220V priz | Sigorta + NJMC1 16A 2P bistable + DI/DO |
| 8 | Araç aküsü float şarj (Blue Smart IP65) | Teknik alan | 60W | Sigorta + NJMC1 16A 2P bistable + DI/DO |

> AC OUT 1 üzerinden beslenir. Shore yokken de HA otomasyonu ile açılabilir (inverter üzerinden). HA yük yönetimi ile gereksiz durumlarda kapatılır.

---

## 📈 Genel Sayılar

| Kategori | Adet |
|----------|------|
| 220V priz | 8 |
| 24V priz | 2 |
| 12V priz | 2 |
| Otomotiv USB-C soket (100W PD) | 9 |
| Push button | 8 |
| Aydınlatma noktası (iç + dış) | 11 |
| 220V bistable röle kontrollü çıkış | 8 |
| **Toplam elektrik noktası** | **47** |

---

## 🤖 Otomasyon Donanım Özeti

### Donanım Listesi

| # | Cihaz | Model | Adet | Yönettiği Grup |
|---|-------|-------|------|----------------|
| 1 | Ana Kontrolcü | Waveshare IPCBOX-CM5-A + RPi CM5 8GB Lite + 512GB NVMe SSD | 1 | HA, Modbus master, 4x RS485, CAN, 2DI/2DO, dual ETH, 7-36V DC |
| 2 | DI/DO Modülü | Waveshare 8DI/8DO (RS485) | 3 | Bistable röle toggle (DO) + durum feedback (DI) |
| 3 | Master Röle | CHINT NJMC1 32A 4P (Camper ON/OFF) | 1 | 220V + 24V + 12V rail anahtarlama, DI feedback |
| 4 | Bireysel Bistable Röle | CHINT NJMC1 16A 2P | 20 | AC + DC yükler (1P high-side switch, 1P DI feedback) |
| 5 | Shelly Plus RGBW PM | Shelly (Wi-Fi, HA entegre, 24V) | 2 | Dimmer + renk LED aydınlatma (Camper ON ile aktif) |
| 6 | Analog Modülü | Waveshare 8-ch Analog (RS485) | 1 | Su tankı seviye, sıcaklık sensörleri |
| 7 | Kontrol Paneli | Waveshare 11.9" HDMI LCD 320×1480 IPS Touch | 1 | Giriş kapısı üstü, HDMI+USB direkt HA bağlantısı |

---

### Camper ON/OFF Master Röle (CHINT NJMC1 32A 4P)

Karavan modu açma/kapama. Tek darbe ile tüm enerji hatlarını etkinleştirir.

| Pol | Rail | Yükler | Koruma |
|-----|------|--------|--------|
| P1 | 220V | 220V ana rail → bireysel NJMC1 16A 2P röleler ile cihaz/priz kontrolü | Ana sigorta |
| P2 | 12V | Clesana C1 tuvalet, Truma Combi 4D, Mutfak 12V priz | Blade fuse |
| P3 | 24V | USB-C soketler (9x), su pompası, Shelly RGBW PM (2x), 24V prizler (2x oturma) | Blade fuse |
| P4 | DI | Açık/kapalı durum geri bildirimi | Waveshare DI |

---

### 220V Bireysel Bistable Röleler (NJMC1 16A 2P × 8)

| # | Yük | 1P High-Side | 1P Feedback |
|---|-----|-------------|-------------|
| 1 | Çamaşır makinesi | 220V L hat | Waveshare DI |
| 2 | İndüksiyon ocak | 220V L hat | Waveshare DI |
| 3 | Bulaşık makinesi | 220V L hat | Waveshare DI |
| 4 | Klima (Evacool Eva RV 2700) | 220V L hat | Waveshare DI |
| 5 | Yatak + Banyo prizleri (4x) | 220V L hat | Waveshare DI |
| 6 | Mutfak prizleri (2x) | 220V L hat | Waveshare DI |
| 7 | Oturma prizleri (2x) | 220V L hat | Waveshare DI |
| 8 | Blue Smart IP65 float şarj | 220V L hat | Waveshare DI |

### DC Bireysel Bistable Röleler (NJMC1 16A 2P × 12)

**Blade Fuse Block #1 — Aydınlatma (8P, tümü dolu)**

| # | Yük | Voltaj | Push Button |
|---|-----|--------|-------------|
| 1 | Okuma lambası sağ | 24V | Yatak sağ PB |
| 2 | Tavan aydınlatma (Bed Light) | 24V | Yatak sol + sağ PB |
| 3 | Banyo aydınlatma | 24V | Banyo PB |
| 4 | Oturma aydınlatma (Saloon Light) | 24V | Oturma PB |
| 5 | Okuma lambası sol | 24V | Yatak sol PB |
| 6 | Gece zemin aydınlatması | 24V | HA otomasyon |
| 7 | Mutfak aydınlatma | 24V | Mutfak PB |
| 8 | Pull-down yatak aydınlatma | 24V | Pull-down PB |

**Blade Fuse Block #2 — Diğer DC (8P, 4 dolu + 4 rezerv)**

| # | Yük | Voltaj | Detay |
|---|-----|--------|-------|
| 1 | Buzdolabı (EvaCool 24V) | 24V | ~2-3A |
| 2 | Dış aydınlatma 1 | 24V | HA otomasyon |
| 3 | Dış aydınlatma 2 | 24V | HA otomasyon |
| 4 | Macerator pompa (SHURflo) | 24V | ~8A max |
| 5-8 | Rezerv | - | Gelecek genişleme |

> Her DC bistable röle: 1P = 24V+ high-side switch, 1P = DI feedback. Push buttonlar Waveshare DI'ya bağlıdır; HA butona basışı algılar ve ilgili DO kanalı üzerinden bistable röleyi toggle eder.

---

### Shelly Plus RGBW PM (Wi-Fi, 2 adet)

24V master rail'den beslenir (Camper ON ile aktif). LED strip dimmer + renk kontrolü.

| # | Konum | İşlev | Besleme |
|---|-------|-------|---------|
| 1 | Ana Yatak | Tavan LED — dimmer + renk (bistable röle downstream) | 24V via Blade Fuse #1 pos 2 |
| 2 | Oturma/Çalışma | Ambient aydınlatma — dimmer + renk | 24V master rail (doğrudan) |

---

### DI/DO Kanal Dağılımı

**DI/DO #1 — 220V Bistable + Master Röle**

| Yön | Kanal | Bağlantı |
|-----|-------|----------|
| DO1 | Çamaşır makinesi | NJMC1 16A 2P toggle |
| DO2 | İndüksiyon ocak | NJMC1 16A 2P toggle |
| DO3 | Bulaşık makinesi | NJMC1 16A 2P toggle |
| DO4 | Klima | NJMC1 16A 2P toggle |
| DO5 | Yatak + Banyo prizleri | NJMC1 16A 2P toggle |
| DO6 | Mutfak prizleri | NJMC1 16A 2P toggle |
| DO7 | Oturma prizleri | NJMC1 16A 2P toggle |
| DO8 | Camper ON/OFF master | NJMC1 32A 4P toggle |
| DI1 | Çamaşır makinesi | Feedback (2. pol) |
| DI2 | İndüksiyon ocak | Feedback (2. pol) |
| DI3 | Bulaşık makinesi | Feedback (2. pol) |
| DI4 | Klima | Feedback (2. pol) |
| DI5 | Yatak + Banyo prizleri | Feedback (2. pol) |
| DI6 | Mutfak prizleri | Feedback (2. pol) |
| DI7 | Oturma prizleri | Feedback (2. pol) |
| DI8 | Camper ON/OFF master | Feedback (4. pol) |

**DI/DO #2 — Aydınlatma Bistable (Blade Fuse Block #1)**

| Yön | Kanal | Bağlantı |
|-----|-------|----------|
| DO1 | Okuma lambası sağ | NJMC1 16A 2P toggle |
| DO2 | Tavan aydınlatma | NJMC1 16A 2P toggle |
| DO3 | Banyo aydınlatma | NJMC1 16A 2P toggle |
| DO4 | Oturma aydınlatma | NJMC1 16A 2P toggle |
| DO5 | Okuma lambası sol | NJMC1 16A 2P toggle |
| DO6 | Gece zemin aydınlatması | NJMC1 16A 2P toggle |
| DO7 | Mutfak aydınlatma | NJMC1 16A 2P toggle |
| DO8 | Pull-down yatak aydınlatma | NJMC1 16A 2P toggle |
| DI1 | Okuma lambası sağ | Feedback (2. pol) |
| DI2 | Tavan aydınlatma | Feedback (2. pol) |
| DI3 | Banyo aydınlatma | Feedback (2. pol) |
| DI4 | Oturma aydınlatma | Feedback (2. pol) |
| DI5 | Okuma lambası sol | Feedback (2. pol) |
| DI6 | Gece zemin | Feedback (2. pol) |
| DI7 | Mutfak aydınlatma | Feedback (2. pol) |
| DI8 | Pull-down yatak | Feedback (2. pol) |

**DI/DO #3 — Diğer DC + AC Bistable**

| Yön | Kanal | Bağlantı |
|-----|-------|----------|
| DO1 | Buzdolabı | NJMC1 16A 2P toggle |
| DO2 | Dış aydınlatma 1 | NJMC1 16A 2P toggle |
| DO3 | Dış aydınlatma 2 | NJMC1 16A 2P toggle |
| DO4 | Macerator pompa | NJMC1 16A 2P toggle |
| DO5 | Blue Smart IP65 float şarj | NJMC1 16A 2P toggle (220V) |
| DO6-8 | Rezerv | Gelecek genişleme |
| DI1 | Buzdolabı | Feedback (2. pol) |
| DI2 | Dış aydınlatma 1 | Feedback (2. pol) |
| DI3 | Dış aydınlatma 2 | Feedback (2. pol) |
| DI4 | Macerator pompa | Feedback (2. pol) |
| DI5 | Blue Smart IP65 float şarj | Feedback (2. pol) |
| DI6-8 | Rezerv | Gelecek genişleme |

---

### Kanal Özeti

| Kaynak | Toplam | Kullanılan | Rezerv |
|--------|--------|------------|--------|
| DO (3× DI/DO) | 24 | 21 | 3 |
| DI (3× DI/DO) | 24 | 21 | 3 |
| IPCBOX-CM5 dahili DI/DO | 2+2 | 0 | 2+2 |
| NJMC1 32A 4P (master) | 1 | 1 | 0 |
| NJMC1 16A 2P (bireysel) | 20 | 20 | 0 |
| Shelly RGBW PM | 2 | 2 | 0 |
| Blade Fuse Block 8P slot | 16 | 12 | 4 |

---

*Bu tablo, tüm Area dosyalarından derlenen elektrik noktalarının ve otomasyon donanımlarının konsolide özetidir. Değişiklik yapıldığında ilgili Area dosyası ve bu tablo birlikte güncellenmelidir.*
