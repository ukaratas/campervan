# Donanım Özet

Tüm bölgelerdeki elektrik noktaları (prizler, soketler, push buttonlar, aydınlatma) ve otomasyon donanımlarının (DI/DO, MOSFET, kontaktör, röle) konsolide özeti.

---

## 📊 Prizler ve Soketler

| Bölge | Konum | 220V | 24V | 12V | USB-C (100W PD) | Toplam Nokta |
|-------|-------|------|-----|-----|------------------|--------------|
| **Ana Yatak** | Yatak Başı Sol (Mutfak tarafı) | 1 | - | - | 2 | 3 |
| **Ana Yatak** | Yatak Başı Sağ (Banyo tarafı) | 1 | - | - | 2 | 3 |
| **Ana Yatak** | Yatak Ayak Ucu (Banyo tarafı) | 1 | 1 | - | - | 2 |
| **Mutfak** | Tezgah üstü | 2 | - | 1 | 2 | 5 |
| **Oturma/Çalışma** | Masa / duvar | 2 | 2 | 1 | 2 | 7 |
| **Popup Yatak** | Popup roof içi | - | - | - | 1 | 1 |
| **Banyo** | Lavabo / duvar | 1 | - | - | - | 1 |
| **TOPLAM** | | **8** | **3** | **2** | **9** | **22** |

---

## 🔘 Push Buttonlar ve Anahtarlar

| Bölge | Konum | Tip | Adet | İşlev | Bağlantı |
|-------|-------|-----|------|-------|----------|
| **Mutfak** | Tezgah üstü / dolap | Push button | 2 | Aydınlatma (spot, şerit) | Waveshare DI |
| **Oturma/Çalışma** | Masa / duvar | Push button | 1 | Çalışma aydınlatması | Waveshare DI |
| **Ana Yatak** | Yatak Başı Sol | Push button | 2 | Genel yatak aydınlatması, sol okuma lambası | Waveshare DI |
| **Ana Yatak** | Yatak Başı Sağ | Push button | 2 | Genel yatak aydınlatması, sağ okuma lambası | Waveshare DI |
| **Popup Yatak** | Popup roof içi | Push button | 1 | İç spot aydınlatma | Waveshare DI |
| **Banyo** | Lavabo / duvar | Push button | 1 | Genel spot aydınlatma | Waveshare DI |
| **TOPLAM** | | | **9** | | |

---

## 💡 Aydınlatma Noktaları

| Bölge | Tip | Voltaj | Kontrol | Push Button |
|-------|-----|--------|---------|-------------|
| **Ana Yatak** | Tavan LED (genel) | 24V | Shelly Plus RGBW PM (dimmer + renk) | Yatak başı sol + sağ |
| **Ana Yatak** | Okuma lambası sol | 24V | MOSFET | Yatak başı sol |
| **Ana Yatak** | Okuma lambası sağ | 24V | MOSFET | Yatak başı sağ |
| **Ana Yatak** | Gece zemin aydınlatması | 24V | MOSFET | Yatak başı sol + sağ |
| **Mutfak** | Dolap altı spot | 24V | MOSFET | Mutfak push button |
| **Mutfak** | LED şerit | 24V | MOSFET | Mutfak push button |
| **Oturma/Çalışma** | Çalışma aydınlatması | 24V | MOSFET | Oturma push button |
| **Oturma/Çalışma** | Ambient aydınlatma | 24V | Shelly Plus RGBW PM (dimmer + renk) | - |
| **Popup Yatak** | İç spot aydınlatma | 24V | MOSFET | Popup push button |
| **Banyo** | Genel spot | 24V | MOSFET | Push button |

---

## 🔌 220V Kontrollü Çıkışlar (Sigorta + Finder Kontaktör)

| # | Çıkış | Bölge | Güç / Detay | Kontrol |
|---|-------|-------|-------------|---------|
| 1 | İndüksiyon ocak | Mutfak | 1800W | Sigorta + Finder 22.22.9.024.4000 + DI/DO |
| 2 | Bulaşık makinesi | Mutfak | 1700W | Sigorta + Finder 22.22.9.024.4000 + DI/DO |
| 3 | Klima (Evacool Eva RV 2700) | Ana Yatak | 900-1100W | Sigorta + Finder 22.22.9.024.4000 + DI/DO |
| 4 | Çamaşır makinesi | Banyo | 160W | Sigorta + Finder 22.22.9.024.4000 + DI/DO |
| 5 | Mutfak prizleri (2x) | Mutfak | 2x 220V priz | Sigorta + Finder 22.22.9.024.4000 + DI/DO |
| 6 | Yatak + Banyo prizleri (4x) | Ana Yatak / Banyo | 3x yatak + 1x banyo | Sigorta + Finder 22.22.9.024.4000 + DI/DO |
| 7 | Oturma prizleri (2x) | Oturma/Çalışma | 2x 220V priz | Sigorta + Finder 22.22.9.024.4000 + DI/DO |
| 8 | Rezerv | - | - | Sigorta + Finder 22.22.9.024.4000 + DI/DO |

---

## 📈 Genel Sayılar

| Kategori | Adet |
|----------|------|
| 220V priz | 8 |
| 24V priz | 3 |
| 12V priz | 2 |
| Otomotiv USB-C soket (100W PD, ayrı hat) | 9 |
| Push button | 9 |
| Aydınlatma noktası | 10 |
| 220V kontaktör kontrollü çıkış | 8 |
| **Toplam elektrik noktası** | **49** |

---

## 🤖 Otomasyon Donanım Bütçesi

### Donanım Listesi

| # | Cihaz | Model | Adet | Yönettiği Grup |
|---|-------|-------|------|----------------|
| 1 | Ana Kontrolcü | Waveshare CM4 Industrial IoT | 1 | HA, Modbus master, RS485 hub |
| 2 | DI/DO Modülü | Waveshare 8DI/8DO (RS485) | 3 | Kontaktör + MOSFET + push button |
| 3 | MOSFET Kartı (8 kanal) | devremarketi modüler, 4A/kanal | 2 | DC yük anahtarlama (16 kanal) |
| 4 | Finder Kontaktör | Finder 22.22.9.024.4000 (25A, 24V DC bobin) | 8 | 220V AC aç/kapa |
| 5 | Shelly Plus RGBW PM | Shelly (Wi-Fi, HA entegre) | 2 | Dimmer + renk LED aydınlatma |
| 6 | High Current Relay | Modbus RTU 4-ch 30A | 1 | Yüksek akım DC yükler |
| 7 | Analog Modülü | Waveshare 8-ch Analog (RS485) | 1 | Su tankı seviye, sıcaklık sensörleri |
| 8 | Gaz Dedektörü | Waveshare RS485 Gas Detector | 1 | Genel gaz algılama (mutfak bölgesi) |
| 9 | Hava İstasyonu | Waveshare Environmental RS485 | 1 | Sıcaklık, nem, CO2, PM2.5 |

### DI/DO Kanal Dağılımı

**DI/DO #1 — 220V Kontaktör Kontrolü**

| Yön | Kanal | Bağlantı |
|-----|-------|----------|
| DO1 | İndüksiyon ocak | Finder kontaktör |
| DO2 | Bulaşık makinesi | Finder kontaktör |
| DO3 | Klima | Finder kontaktör |
| DO4 | Çamaşır makinesi | Finder kontaktör |
| DO5 | Mutfak prizleri (2x) | Finder kontaktör |
| DO6 | Yatak + Banyo prizleri (4x) | Finder kontaktör |
| DO7 | Oturma prizleri (2x) | Finder kontaktör |
| DO8 | Rezerv | Finder kontaktör |
| DI1-8 | Rezerv | Kontaktör feedback / gelecek genişleme |

**DI/DO #2 — Aydınlatma MOSFET + Push Buttonlar**

| Yön | Kanal | Bağlantı |
|-----|-------|----------|
| DO1 | Okuma lambası sol | MOSFET Kartı #1 Ch1 |
| DO2 | Okuma lambası sağ | MOSFET Kartı #1 Ch2 |
| DO3 | Gece zemin aydınlatması | MOSFET Kartı #1 Ch3 |
| DO4 | Dolap altı spot | MOSFET Kartı #1 Ch4 |
| DO5 | LED şerit (mutfak) | MOSFET Kartı #1 Ch5 |
| DO6 | Çalışma aydınlatması | MOSFET Kartı #1 Ch6 |
| DO7 | Popup iç spot | MOSFET Kartı #1 Ch7 |
| DO8 | Banyo genel spot | MOSFET Kartı #1 Ch8 |
| DI1 | Mutfak PB #1 | Dolap altı spot |
| DI2 | Mutfak PB #2 | LED şerit |
| DI3 | Oturma PB | Çalışma aydınlatması |
| DI4 | Yatak Sol PB #1 | Genel aydınlatma |
| DI5 | Yatak Sol PB #2 | Sol okuma lambası |
| DI6 | Yatak Sağ PB #1 | Genel aydınlatma |
| DI7 | Yatak Sağ PB #2 | Sağ okuma lambası |
| DI8 | Popup PB | İç spot aydınlatma |

**DI/DO #3 — USB-C MOSFET**

| Yön | Kanal | Bağlantı |
|-----|-------|----------|
| DO1 | Ana Yatak Sol USB-C #1 | MOSFET Kartı #2 Ch1 |
| DO2 | Ana Yatak Sol USB-C #2 | MOSFET Kartı #2 Ch2 |
| DO3 | Ana Yatak Sağ USB-C #1 | MOSFET Kartı #2 Ch3 |
| DO4 | Ana Yatak Sağ USB-C #2 | MOSFET Kartı #2 Ch4 |
| DO5 | Mutfak USB-C #1 | MOSFET Kartı #2 Ch5 |
| DO6 | Mutfak USB-C #2 | MOSFET Kartı #2 Ch6 |
| DO7 | Oturma USB-C #1 | MOSFET Kartı #2 Ch7 |
| DO8 | Oturma USB-C #2 | MOSFET Kartı #2 Ch8 |
| DI1 | Banyo PB | Genel spot aydınlatma |
| DI2-8 | Rezerv | Gelecek genişleme |

> **Not:** Popup USB-C (1x) always-on olarak 24V hattan beslenir (popup kullanımdayken zaten enerji aktif). Bireysel kontrol istenirse 4. DI/DO modülü ile genişletilebilir.

### High Current Relay Kanal Dağılımı (Modbus RTU, 4-ch 30A)

| Kanal | Cihaz | Akım |
|-------|-------|------|
| CH1 | Macerator pompa (SHURflo) | ~8A max |
| CH2 | Hydrofor pompa | ~3-4A |
| CH3 | Buzdolabı (EvaCool 24V) | ~2-3A |
| CH4 | Rezerv | - |

### Shelly Plus RGBW PM (Wi-Fi, 2 adet)

| # | Konum | İşlev |
|---|-------|-------|
| 1 | Ana Yatak | Tavan LED — dimmer + renk kontrolü |
| 2 | Oturma/Çalışma | Ambient aydınlatma — dimmer + renk kontrolü |

### Kanal Özeti

| Kaynak | Toplam | Kullanılan | Rezerv |
|--------|--------|------------|--------|
| DO (3x DI/DO) | 24 | 24 | 0 |
| DI (3x DI/DO) | 24 | 9 | 15 |
| MOSFET kanal (2x 8ch) | 16 | 16 | 0 |
| High Current Relay | 4 | 3 | 1 |
| Finder Kontaktör | 8 | 7 | 1 |

---

*Bu tablo, tüm Area dosyalarından derlenen elektrik noktalarının konsolide özetidir. Değişiklik yapıldığında ilgili Area dosyası ve bu tablo birlikte güncellenmelidir.*
