
# Otomasyon Sistemi - Tam Teknik Doküman

Bu doküman, karavanın tüm otomasyon altyapısını, IO haritalarını, elektrik tüketicilerini ve sistem mimarisini kapsamlı şekilde özetler. Diğer dosyalara dokunmadan bu sayfa referans alınabilir.

## 🎯 Sistem Genel Bakış

Karavanın tüm elektrik ve elektronik sistemleri **Raspberry Pi CM4** üzerinde çalışan **Home Assistant** ile merkezi olarak kontrol edilir.

### Temel Prensipler
* **Merkezi Kontrol:** Tüm cihazlar, sensörler ve yükler Home Assistant üzerinden izlenir ve kontrol edilir
* **Modbus over TCP:** RS485 cihazlar Ethernet çeviricisi ile TCP/IP üzerinden Home Assistant'a bağlanır
* **24V DC Ana Sistem:** Tüm karavan elektriği 24V DC tabanlıdır, 12V ve 220V ihtiyaçlar dönüştürücülerle sağlanır
* **Otomasyonlu Yük Yönetimi:** Kritik yüklerin enerji verimliliği ve güvenlik için otomatik kontrolü

---

## 🏗️ Donanım Mimarisi

### Ana Kontrolcü
**Raspberry Pi CM4 + Waveshare 7″ Touch Screen All-In-One Kit**
* 5MP kamera, alüminyum kasa
* Home Assistant OS
* 7" dokunmatik kontrol paneli
* UPS desteği (kesintisiz çalışma)

### Ağ Altyapısı
**Industrial 5P Gigabit Ethernet Switch**
* Full-Duplex 10/100/1000M
* DIN Rail montaj
* Tüm Modbus cihazları için merkezi hub

**2-Ch RS485 to RJ45 Ethernet Serial Server**
* Dual RS485 kanalı bağımsız çalışma
* Modbus RTU → Modbus TCP dönüşümü
* Dual Ethernet portları

### Modbus RTU Cihazlar (RS485)

#### 1. High Current Relay Module
* **Model:** Industrial Modbus RTU 4-ch Relay Module
* **Özellikler:** 30A yüksek akım, LED göstergeler, çoklu izolasyon koruması
* **Kullanım:** Kısa süreli yüksek yük (pompalar, macerator)

#### 2. High Power Latching Relay (Bistable)
* **Tetikleyici:** Waveshare Industrial 8-Ch Digital Input & Output Module (DO çıkışları)
* **Röle:** Finder Bistable Relay (80A/250VAC, 50A/30VDC)
* **Kullanım:** Uzun süreli yüksek güç yükleri (klima, buzdolabı, hidrofor)

#### 3. Low Power Latching Relay Module
* **Model:** Modbus RTU 8-ch Latching Relay Module (C)
* **Özellikler:** RS485, çoklu izolasyon, ray montaj
* **Kullanım:** Uzun süreli düşük güç yükleri (aydınlatma)

#### 4. DI/DO Module
* **Model:** Industrial 8-Ch Digital Input & Output Module
* **Özellikler:** DC 7~36V, Modbus RTU
* **Kullanım:** Push button girişleri, bistable röle tetikleme

#### 5. Analog Acquisition Module
* **Model:** Industrial 8-Ch Analog Acquisition Module
* **Özellikler:** 12-bit hassasiyet, voltaj/akım okuma
* **Kullanım:** Su tank seviye sensörleri (temiz su, gri su)

#### 6. RGB Dimmer — Shelly Plus RGBW PM (x2)
* **Model:** Shelly Plus RGBW PM (SNDC-0D4P10WW) — 2 adet
* **Özellikler:** 4 kanal PWM dimming (kanal başı 4A, toplam 10A), 12/24V DC, Wi-Fi + Bluetooth, güç ölçümü, scripting desteği
* **Bağlantı:** Wi-Fi üzerinden Home Assistant entegrasyonu (Modbus gerektirmez)
* **Kullanım:**
  - **Shelly #1:** Tente ambiyans (RGBW LED şerit)
  - **Shelly #2:** Ortam ambiyans (RGBW LED şerit)
* **Detay:** https://www.shelly.com/products/shelly-plus-rgbw-pm

### Ethernet Üzerinden Bağlanan Cihazlar
* **Victron EasySolar-II 3kVA MPPT 250/70 GX** — Inverter/şarj/MPPT kombine, VE.Bus/Modbus TCP
* **RS485 to Ethernet Serial Server** — Modbus RTU → TCP gateway

---

## 📊 Elektrik Tüketicileri - Detaylı Liste

### 24V DC Tüketiciler

#### Yüksek Güç (>100W)
| Cihaz | Güç | Akım | Kontrol | Notlar |
|-------|-----|------|---------|--------|
| 24V Klima (Eva Cool Eva 24V 20T Premium) | 720-960W | 30-40A | Kontaktör + DI/DO | Ana yatak soğutma |
| Macerator pompa (gri su boşaltma) | ~192W | 8A | Low Latching Relay | WC atık su boşaltma |
| Temiz su hidrofor pompası | 72-96W | 3-4A (5A sigorta) | Low Latching Relay | Basınçlı su sistemi |

#### Orta Güç (10-100W)
| Cihaz | Güç | Akım | Kontrol | Notlar |
|-------|-----|------|---------|--------|
| Buzdolabı (EvaCool Eva Berlin 90L) | 50-80W | 2-3A | High Latching Relay | Sürekli çalışma |
| USB Şarj Kutusu #1 (Mutfak) | ~200W | 8A | High Latching Relay | Bağımsız kutu |
| USB Şarj Kutusu #2 (Yatak) | ~200W | 8A | High Latching Relay | Bağımsız kutu |
| USB Şarj Kutusu #3 (Popup) | ~200W | 8A | High Latching Relay | Bağımsız kutu |
| USB Şarj Kutusu #4 (Salon) | ~200W | 8A | High Latching Relay | Bağımsız kutu |
| 24V genel prizler | Değişken | Değişken | High Latching Relay | Portatif cihazlar |

#### Düşük Güç (<10W)
| Cihaz | Güç | Kontrol | Notlar |
|-------|-----|---------|--------|
| Mutfak aydınlatma | 5-10W | Low Latching Relay | LED spot |
| Mutfak tezgâh aydınlatma | 5-10W | Low Latching Relay | Dolap altı LED |
| Orta alan aydınlatma | 10-15W | Low Latching Relay | Genel aydınlatma |
| Yatak alanı aydınlatma | 10-15W | Low Latching Relay | Ana yatak |
| Popup yatak aydınlatma | 5-10W | Low Latching Relay | Popup roof içi |
| Yatak sol baş okuma ışık | 3-5W | Low Latching Relay | Okuma lambası |
| Yatak sağ baş okuma ışık | 3-5W | Low Latching Relay | Okuma lambası |
| Tente altı aydınlatma | 10-15W | Low Latching Relay | Dış aydınlatma |
| Banyo aydınlatma | 5-10W | Low Latching Relay | Genel banyo |
| Banyo ayna aydınlatması | 5-10W | Low Latching Relay | Ayna LED |
| Tente ambiyans (RGBW) | 10-20W | Shelly Plus RGBW PM #1 | RGBW LED şerit, Wi-Fi kontrol |
| Ortam ambiyans (RGBW) | 10-20W | Shelly Plus RGBW PM #2 | RGBW LED şerit, Wi-Fi kontrol |

#### Sensörler ve Valfler
| Cihaz | Güç | Akım | Kontrol | Notlar |
|-------|-----|------|---------|--------|
| Su seviye sensörleri | <1W | <0.1A | Analog Module | Temiz/gri su tankları |
| Elektrikli actuator valf (temiz su) | 2.4W | 0.1A | DI/DO Module (DO1) | Donma koruması boşaltma |
| Hareket sensörleri | <1W | <0.1A | DI Module | Otomatik aydınlatma |
| Nem sensörleri | <1W | <0.1A | Analog Module | Hava kalitesi |
| Popup roof fanı (opsiyonel) | 10-20W | <1A | Home Assistant | Havalandırma |
| Banyo fanı (opsiyonel) | 10-20W | <1A | Home Assistant | Nem kontrolü |

### 12V DC Tüketiciler (24V'dan Konvertör ile)
| Cihaz | Güç | Akım | Kontrol | Notlar |
|-------|-----|------|---------|--------|
| Truma Combi D4 inet | 24-96W | 2-8A | Truma inet / HA | Dizel kombi |
| Clesana C1 susuz tuvalet | 0.6W standby / 6.6W flush | 0.05A / 0.55A | Home Assistant | Susuz tuvalet |
| 12V genel prizler | 24-60W | 2-5A | High Latching Relay | Portatif cihazlar |

**24V to 12V DC Konvertör:** 15-20A (180-240W) kapasite

### 220V AC Tüketiciler (EasySolar-II İnverter)

#### Yüksek Güç (>1000W)
| Cihaz | Güç | Kontrol | Notlar |
|-------|-----|---------|--------|
| Omake ankastre indüksiyon ocak | 1800W | Finder 22.22 kontaktör + DI/DO-02 | Yük yönetimi gerekli |
| Electrolux bulaşık makinesi (ESF2400O) | 1500W (ısıtıcı) + 200W (pompa) | Finder 22.22 kontaktör + DI/DO-02 | Yük yönetimi gerekli |
| Profilo FRIAT9AN mikrodalga fırın | 800W | Finder 22.22 kontaktör + DI/DO-02 | 20L kapasite |

#### Orta Güç (100-1000W)
| Cihaz | Güç | Kontrol | Notlar |
|-------|-----|---------|--------|
| Samsung 32" Smart Monitor M8 4K | 50-100W | 220V priz | Çalışma/TV modu |
| 220V genel prizler | Değişken | EasySolar-II | Şarj cihazları |

#### Düşük Güç (<100W)
| Cihaz | Güç | Kontrol | Notlar |
|-------|-----|---------|--------|
| Banyo 220V prizi | <100W | 220V priz | Traş, saç kurutma |

### Otomasyon ve Kontrol Sistemleri
| Cihaz | Güç | Notlar |
|-------|-----|--------|
| Raspberry Pi CM4 + 7" Touch Screen | 10-20W | Ana kontrolcü |
| Industrial Ethernet Switch | 5-10W | Ağ altyapısı |
| RS485 to Ethernet Converter | 2-5W | Modbus gateway |
| Modbus röle modülleri | 1-2W/adet | 4 adet modül |
| DI/DO modülleri | 2-5W | Push button + DO |
| Analog modüller | 2-5W | Tank sensörleri |
| Shelly Plus RGBW PM (x2) | <1.2W/adet | RGB ambiyans, Wi-Fi |

### Şarj ve Enerji Yönetimi
| Cihaz | Kapasite | Notlar |
|-------|----------|--------|
| Victron EasySolar-II 3kVA MPPT 250/70 GX | 3000W inverter, 70A MPPT | Kombine sistem |
| Victron Orion XS 12/24-50 | 1200W max | Alternatör şarj |
| BMS (Battery Management System) | 2-5W sürekli | Akü yönetimi |

### Toplam Güç Analizi
* **24V DC Toplam:** ~1500-2000W maksimum eş zamanlı
* **12V DC Toplam:** ~150-200W maksimum (konvertör üzerinden)
* **220V AC Toplam:** ~3000W maksimum (inverter limiti)
* **Kritik Yük Yönetimi:** 
  - İndüksiyon ocak (1800W) + bulaşık makinesi (1700W) = 3500W > 3000W
  - İndüksiyon ocak (1800W) + mikrodalga (800W) = 2600W < 3000W ✓
  - Bulaşık makinesi (1700W) + mikrodalga (800W) = 2500W < 3000W ✓
  - **Otomasyon:** Home Assistant sadece ocak + bulaşık makinesi eş zamanlı çalışmasını engeller

### Enerji Üretimi ve Şarj
* **Güneş Paneli:** 400W esnek panel (popup roof üstü) → EasySolar-II MPPT
* **Alternatör Şarj:** 50A @ 24V (1200W max) → Victron Orion XS
* **Shore Power:** 16A @ 220V (3520W max) → EasySolar-II

---

## 📦 Latching Relay Detaylı Liste

Karavanda toplam **3 adet Latching Relay** modülü kullanılacak:

### ✅ LOW Latching Relay #1 (8 Kanal) - MEVCUT
**Kullanım:** Aydınlatma sistemleri (düşük güç, uzun çalışma süresi)

| Kanal | Cihaz | Güç | Akım | Notlar |
|-------|-------|-----|------|--------|
| R1 | Mutfak aydınlatma | 5-10W | <1A | LED spot |
| R2 | Mutfak tezgâh aydınlatma | 5-10W | <1A | Dolap altı LED |
| R3 | Orta alan aydınlatma | 10-15W | <1A | Genel aydınlatma |
| R4 | Yatak alanı aydınlatma | 10-15W | <1A | Ana yatak |
| R5 | Popup yatak aydınlatma | 5-10W | <1A | Popup roof içi |
| R6 | Yatak sol baş okuma | 3-5W | <1A | Okuma lambası |
| R7 | Yatak sağ baş okuma | 3-5W | <1A | Okuma lambası |
| R8 | Tente altı aydınlatma | 10-15W | <1A | Dış aydınlatma |

**Durum:** ✅ Mevcut ve çalışıyor

---

### ❌ LOW Latching Relay #2 (8 Kanal) - YENİ GEREKLİ
**Kullanım:** Banyo aydınlatma + Su sistemi pompaları

| Kanal | Cihaz | Güç | Akım | Notlar |
|-------|-------|-----|------|--------|
| R1 | Banyo aydınlatma | 5-10W | <1A | LED genel banyo |
| R2 | Banyo ayna aydınlatması | 5-10W | <1A | Ayna LED |
| R3 | Temiz su hidrofor pompası | 72-96W | 3-4A | 5A sigorta, basınçlı su |
| R4 | Macerator pompa (gri su) | ~192W | 8A | WC atık su boşaltma |
| R5 | **BOŞ** | - | - | Genişleme |
| R6 | **BOŞ** | - | - | Genişleme |
| R7 | **BOŞ** | - | - | Genişleme |
| R8 | **BOŞ** | - | - | Genişleme |

**Durum:** ❌ Yeni sipariş gerekli

---

### ❌ HIGH Latching Relay #1 (8 Kanal) - YENİ GEREKLİ
**Kullanım:** Yüksek güç cihazları (buzdolabı, USB kutuları, prizler)

| Kanal | Cihaz | Güç | Akım | Notlar |
|-------|-------|-----|------|--------|
| R1 | Buzdolabı (Eva Berlin 90L) | 50-80W | 2-3A | Sürekli çalışma |
| R2 | USB Şarj Kutusu #1 | ~200W | 8A | Mutfak bölgesi |
| R3 | USB Şarj Kutusu #2 | ~200W | 8A | Yatak bölgesi |
| R4 | USB Şarj Kutusu #3 | ~200W | 8A | Popup bölgesi |
| R5 | USB Şarj Kutusu #4 | ~200W | 8A | Salon/genel alan |
| R6 | 24V genel prizler | Değişken | Değişken | Portatif cihazlar |
| R7 | 12V genel prizler | 24-60W | 2-5A | Konvertör üzerinden |
| R8 | **BOŞ** | - | - | Genişleme |

**Durum:** ❌ Yeni sipariş gerekli

---

### 🎯 DI/DO Modülü - DO Çıkışları (8 Kanal, 500mA/kanal)
**Kullanım:** Düşük akım kontrol sinyalleri, valfler, kontaktör tetikleme

| Kanal | Cihaz | Güç | Akım | Notlar |
|-------|-------|-----|------|--------|
| DO1 | Elektrikli vana (temiz su) | 2.4W | 0.1A | Kış donma koruması için boşaltma |
| DO2 | Kontaktör tetikleme (klima) | <5W | <0.5A | 24V kontaktör bobini tetikleme |
| DO3 | **BOŞ** | - | - | Genişleme (valf, sensör vb.) |
| DO4 | **BOŞ** | - | - | Genişleme |
| DO5 | **BOŞ** | - | - | Genişleme |
| DO6 | **BOŞ** | - | - | Genişleme |
| DO7 | **BOŞ** | - | - | Genişleme |
| DO8 | **BOŞ** | - | - | Genişleme |

---

### 🔥 Harici Kontaktör (DI/DO ile tetiklenir)
**Kullanım:** Çok yüksek akım çeken cihazlar

| Cihaz | Güç | Akım | Kontrol | Notlar |
|-------|-----|------|---------|--------|
| 24V Klima (Eva Cool 24V 20T) | 720-960W | 30-40A | Kontaktör (DO2 ile tetiklenir) | Ana yatak soğutma |

---

### ⚡ 220V Cihazlar - Finder Kontaktör Sistemi
**Model:** Finder 22.22.9.024.4000 (Modüler Kontaktör)  
**Kontrol:** Waveshare DI/DO modülü üzerinden (her cihaz için 1 DO + 1 DI)

#### 📐 Sistem Mimarisi:

```
Home Assistant
    ↓
Waveshare DI/DO Modülü (DI/DO-02)
    ↓ DO (Digital Output) → Finder Kontaktör Bobin (DO HIGH = AÇ, DO LOW = KAPA)
    ↑ DI (Digital Input)  ← Finder Kontaktör Status (Yardımcı kontak)
    ↓
Finder 22.22.9.024.4000 Kontaktör (25A, 2NO, 24V DC bobin)
    ↓
220V Cihazlar
```

#### 🔧 Finder 22.22.9.024.4000 Kontaktör Özellikleri:

- **Tip:** Modüler kontaktör (DIN rail montaj)
- **Kontaklar:** 2 NO (normally open), 25A @ 250VAC
- **Bobin:** 24V DC (~70mA, ~1.7W)
- **Kontak Malzemesi:** AgSnO2 (endüktif yüklere dayanıklı)
- **Kontrol:** DO HIGH = kontaktör çeker (cihaz açık), DO LOW = kontaktör düşer (cihaz kapalı)
- **Fail-safe:** Güç kesilirse tüm kontaktörler düşer → 220V cihazlar otomatik kapanır
- **Avantajlar:**
  - ✅ Basit kontrol: DO HIGH = AÇ, DO LOW = KAPA (pulse timing gerekmez)
  - ✅ Her cihaz için 1 DO yeterli (impulse relay'deki SET+RESET yerine)
  - ✅ Fail-safe: Güç kesintisinde tüm 220V cihazlar güvenli şekilde kapanır
  - ✅ DI ile gerçek durum feedback'i (yardımcı kontak üzerinden)
  - ✅ 2 NO kontak ile hem L hem N hattı kesilebilir (tam izolasyon)
  - ✅ 25A kapasite tüm cihazlar için fazlasıyla yeterli

#### 🔌 Waveshare DI/DO-02 Kullanımı:

**Digital Output (DO) — Her cihaz 1 DO kanalı:**
- DO HIGH = Kontaktör bobini enerjili → Cihaz AÇ
- DO LOW = Kontaktör bobini enerjisiz → Cihaz KAPA

**Digital Input (DI) — Her cihaz 1 DI kanalı:**
- DI = Kontaktör yardımcı kontak durumu (1=Açık, 0=Kapalı)

#### 📋 Bağlanacak 220V Cihazlar:

**ÖNEMLİ:** Tüm 220V cihazlar bu kontaktör sistemi üzerinden kontrol edilecek:

| # | Cihaz | Model | Güç | Akım (220V) | Kontaktör | Notlar |
|---|-------|-------|-----|-------------|-----------|--------|
| 1 | **İndüksiyon Ocak** | Omake 1800W | 1800W | 8.2A | Finder-1 | Mutfak |
| 2 | **Bulaşık Makinesi** | Electrolux ESF2400O | 1200-1800W | 7.7A | Finder-2 | Mutfak |
| 3 | **Çamaşır Makinesi** | [FİX Mini](https://portofmarin.com/urun/waf-mini-camasir-makinesi-beyaz/) | 160W (maks) | 0.73A | Finder-3 | 3 KG, 50W yıkama + 160W santrifüj |
| 4 | **Mikrodalga Fırın** | Profilo FRIAT9AN | 800W | 3.6A | Finder-4 | 20L kapasite |
| 5 | **Rezerv** | - | - | - | Finder-5 | Genişleme |

**Çamaşır Makinesi Teknik Özellikler:**
- Model: FİX Mini Tekne/Karavan Çamaşır Makinesi
- Güç: 220V/50Hz
- Yıkama Gücü: 50W
- Santrifüj Gücü: 160W (maksimum tüketim)
- Kapasite: 3 KG
- Program Sayısı: 6
- Maksimum Devir: 600 RPM
- **Avantaj:** Çok düşük güç tüketimi (160W), karavan için ideal

**Not:** Impulse/bistable röle kullanılmaz! Finder 22.22.9.024.4000 modüler kontaktör + DI/DO sistemi kullanılır. DO durumu = cihaz durumu, DI ile donanım seviyesinde doğrulama yapılır.

---

### 📊 Özet

```
✅ LOW Latching Relay #1 (8 kanal) → Aydınlatma (8/8 DOLU)
❌ LOW Latching Relay #2 (8 kanal) → Banyo + Su sistemi (4/8 kullanılıyor)
❌ HIGH Latching Relay #1 (8 kanal) → Yüksek güç cihazları (7/8 kullanılıyor)
🎯 DI/DO Modülü #1 (8 DO + 8 DI) → Push buttons + Valfler + Klima kontaktörü
⚡ DI/DO Modülü #2 (8 DO + 8 DI) → Finder 22.22 kontaktör kontrol (220V cihazlar)
🔥 Kontaktör (harici) → 24V Klima (30-40A)
⚡ 5x Finder 22.22.9.024.4000 → 220V cihazlar (DO HIGH=AÇ, DO LOW=KAPA)

TOPLAM: 
- 3x Latching Relay (24V DC cihazlar)
- 2x DI/DO Modülü (#1: Push buttons + valfler, #2: 220V kontaktör kontrol)
- 5x Finder 22.22.9.024.4000 Kontaktör (220V cihazlar)
- 1x Kontaktör (24V Klima)
- 2x Shelly Plus RGBW PM (RGB ambiyans, Wi-Fi)
```

---

## 🔌 IO Haritası - Girişler ve Çıkışlar

### Çıkışlar - Low Latching Relay #1 (8 Kanal) ✅ MEVCUT
Aydınlatma sistemleri için.

| Kanal | Bağlı Cihaz | Güç | Notlar |
|-------|-------------|-----|--------|
| R1 | Mutfak aydınlatma | 24V LED, 5-10W | Ana mutfak |
| R2 | Mutfak tezgâh aydınlatma | 24V LED, 5-10W | Dolap altı |
| R3 | Orta alan aydınlatma | 24V LED, 10-15W | Oturma alanı |
| R4 | Yatak alanı aydınlatma | 24V LED, 10-15W | Ana yatak |
| R5 | Popup yatak aydınlatma | 24V LED, 5-10W | Popup roof |
| R6 | Yatak sol baş okuma | 24V LED, 3-5W | Okuma lambası |
| R7 | Yatak sağ baş okuma | 24V LED, 3-5W | Okuma lambası |
| R8 | Tente altı aydınlatma | 24V LED, 10-15W | Dış aydınlatma |

### Çıkışlar - Low Latching Relay #2 (8 Kanal) ❌ YENİ
Banyo aydınlatma ve su sistemi pompaları için.

| Kanal | Bağlı Cihaz | Güç | Notlar |
|-------|-------------|-----|--------|
| R1 | Banyo aydınlatma | 24V LED, 5-10W | Genel banyo |
| R2 | Banyo ayna aydınlatması | 24V LED, 5-10W | Ayna LED |
| R3 | Temiz su hidrofor | 24V DC, 72-96W | 3-4A, 5A sigorta |
| R4 | Macerator pompa | 24V DC, ~192W | 8A, gri su boşaltma |
| R5 | BOŞ | - | Genişleme |
| R6 | BOŞ | - | Genişleme |
| R7 | BOŞ | - | Genişleme |
| R8 | BOŞ | - | Genişleme |

### Çıkışlar - High Latching Relay #1 (8 Kanal) ❌ YENİ
Yüksek güç cihazları için.

| Kanal | Bağlı Cihaz | Güç | Notlar |
|-------|-------------|-----|--------|
| R1 | Buzdolabı | 24V DC, 50-80W | Sürekli çalışma |
| R2 | USB Kutusu #1 | 24V DC, ~200W | 8A, mutfak |
| R3 | USB Kutusu #2 | 24V DC, ~200W | 8A, yatak |
| R4 | USB Kutusu #3 | 24V DC, ~200W | 8A, popup |
| R5 | USB Kutusu #4 | 24V DC, ~200W | 8A, salon |
| R6 | 24V genel çıkışlar | 24V DC, değişken | Portatif cihazlar |
| R7 | 12V genel çıkışlar | 12V DC, 24-60W | Konvertör üzerinden |
| R8 | BOŞ | - | Genişleme |

### Çıkışlar - Shelly Plus RGBW PM (2 Adet, Wi-Fi)
RGBW LED şeritler ve dimmer kontrolü gereken aydınlatmalar. Her Shelly cihazı 4 kanal PWM çıkışına sahiptir (kanal başı 4A, toplam 10A). 24V DC ile beslenir, Wi-Fi üzerinden Home Assistant'a bağlanır (Modbus gerektirmez).

**Shelly Plus RGBW PM #1 — Tente Ambiyans:**

| Kanal | Bağlı Cihaz | Güç | Kontrol |
|-------|-------------|-----|---------|
| R | Tente RGBW LED — Kırmızı | - | RGBW + dimming |
| G | Tente RGBW LED — Yeşil | - | RGBW + dimming |
| B | Tente RGBW LED — Mavi | - | RGBW + dimming |
| W | Tente RGBW LED — Beyaz | - | RGBW + dimming |
| **Toplam** | Tente ambiyans (RGBW LED şerit) | 10-20W | Wi-Fi, güç ölçümü |

**Shelly Plus RGBW PM #2 — Ortam Ambiyans:**

| Kanal | Bağlı Cihaz | Güç | Kontrol |
|-------|-------------|-----|---------|
| R | Ortam RGBW LED — Kırmızı | - | RGBW + dimming |
| G | Ortam RGBW LED — Yeşil | - | RGBW + dimming |
| B | Ortam RGBW LED — Mavi | - | RGBW + dimming |
| W | Ortam RGBW LED — Beyaz | - | RGBW + dimming |
| **Toplam** | Ortam ambiyans (RGBW LED şerit) | 10-20W | Wi-Fi, güç ölçümü |

**Not:** Shelly Plus RGBW PM cihazları RS485/Modbus kullanmaz. Wi-Fi üzerinden doğrudan Home Assistant'a entegre olur. Güç ölçümü özelliği ile enerji tüketimi izlenebilir. Scripting desteği ile lokal otomasyon senaryoları da oluşturulabilir.

### Çıkışlar - DI/DO Module #1 (8 DO Kanal, 500mA/kanal)
Düşük akım kontrol sinyalleri, valfler, kontaktör tetikleme için.

| Kanal | Bağlı Cihaz | Güç | Akım | Notlar |
|-------|-------------|-----|------|--------|
| DO1 | Elektrikli vana (temiz su) | 2.4W | 0.1A | Kış donma koruması |
| DO2 | Kontaktör tetikleme (24V klima) | <5W | <0.5A | 30-40A kontaktör bobini |
| DO3 | BOŞ | - | - | Genişleme |
| DO4 | BOŞ | - | - | Genişleme |
| DO5 | BOŞ | - | - | Genişleme |
| DO6 | BOŞ | - | - | Genişleme |
| DO7 | BOŞ | - | - | Genişleme |
| DO8 | BOŞ | - | - | Genişleme |

### Girişler - DI/DO Module #1 (8 DI Kanal)
Push button girişleri için dijital input.

| Kanal | Kullanım | Short Press | Long Press | Double Press |
|-------|----------|-------------|------------|--------------|
| DI1 | Sağ yatak butonu | Yatak alanı aç/kapa | Sağ okuma lambası | Tüm aydınlatma kapat |
| DI2 | Sol yatak butonu | Yatak alanı aç/kapa | Sol okuma lambası | Tüm aydınlatma kapat |
| DI3 | Popup yatak butonu | Popup aydınlatma aç/kapa | Popup ambiyans | Tüm aydınlatma kapat |
| DI4 | Dış aydınlatma butonu | Tente altı aç/kapa | Tente ambiyans | Tüm aydınlatma kapat |
| DI5 | Otomatik basamak butonu | Basamak aç/kapa | - | - |
| DI6 | Mutfak butonu | Mutfak lambası | Tezgâh lambası | - |
| DI7 | Orta alan butonu | Orta alan aydınlatma | Ambiyans aydınlatma | Tüm aydınlatma kapat |
| DI8 | Banyo butonu | Banyo aydınlatma | Banyo ayna lambası | - |

### Çıkışlar - DI/DO Module #2 (8 DO Kanal, 500mA/kanal)
220V Finder kontaktör bobin kontrolü. Her DO kanalı bir kontaktörün 24V DC bobinini sürer (~70mA).

| Kanal | Bağlı Cihaz | Güç | Akım | Notlar |
|-------|-------------|-----|------|--------|
| DO0 | **Finder-1 Kontaktör (İndüksiyon Ocak)** | ~1.7W | ~70mA | DO HIGH=AÇ, LOW=KAPA |
| DO1 | **Finder-2 Kontaktör (Bulaşık Makinesi)** | ~1.7W | ~70mA | DO HIGH=AÇ, LOW=KAPA |
| DO2 | **Finder-3 Kontaktör (Çamaşır Makinesi)** | ~1.7W | ~70mA | DO HIGH=AÇ, LOW=KAPA |
| DO3 | **Finder-4 Kontaktör (Mikrodalga Fırın)** | ~1.7W | ~70mA | DO HIGH=AÇ, LOW=KAPA |
| DO4 | **Finder-5 Kontaktör (Rezerv)** | ~1.7W | ~70mA | Genişleme |
| DO5 | BOŞ | - | - | Genişleme |
| DO6 | BOŞ | - | - | Genişleme |
| DO7 | BOŞ | - | - | Genişleme |

### Girişler - DI/DO Module #2 (8 DI Kanal)
Finder kontaktör status feedback. Her DI kanalı bir kontaktörün yardımcı kontağından durum okur.

| Kanal | Kullanım | Açıklama |
|-------|----------|----------|
| DI0 | **Finder-1 Status (İndüksiyon Ocak)** | 1=Açık, 0=Kapalı |
| DI1 | **Finder-2 Status (Bulaşık Makinesi)** | 1=Açık, 0=Kapalı |
| DI2 | **Finder-3 Status (Çamaşır Makinesi)** | 1=Açık, 0=Kapalı |
| DI3 | **Finder-4 Status (Mikrodalga Fırın)** | 1=Açık, 0=Kapalı |
| DI4 | **Finder-5 Status (Rezerv)** | 1=Açık, 0=Kapalı |
| DI5 | BOŞ | Genişleme |
| DI6 | BOŞ | Genişleme |
| DI7 | BOŞ | Genişleme |

**⚡ Kontaktör Kontrol Mantığı:**
- DO HIGH → Kontaktör bobini enerjilenir → Kontak kapanır → 220V cihaz açılır
- DO LOW → Kontaktör bobini enerjisizleşir → Kontak açılır → 220V cihaz kapanır
- DI → Yardımcı kontak ile gerçek durum doğrulanır
- **Fail-safe:** Güç kesilirse tüm kontaktörler düşer, 220V cihazlar güvenli şekilde kapanır

**Push Button Zamanlama:**
* **Short press:** <400ms
* **Long press:** >600ms
* **Double press:** 2x press <300ms aralıkla

### Girişler - Analog Module (8 Kanal)
Analog sensör okumaları (12-bit hassasiyet).

| Kanal | Sensör | Tip | Aralık | Notlar |
|-------|--------|-----|--------|--------|
| AI1 | Temiz su tank seviyesi | Şamandıra/basınç | 0-100% | 150L tank |
| AI2 | Gri su tank seviyesi | Şamandıra/basınç | 0-100% | 100-120L tank |
| AI3 | Rezerv | - | - | Genişleme için |
| AI4 | Rezerv | - | - | Genişleme için |
| AI5 | Rezerv | - | - | Genişleme için |
| AI6 | Rezerv | - | - | Genişleme için |
| AI7 | Rezerv | - | - | Genişleme için |
| AI8 | Rezerv | - | - | Genişleme için |

---

## 🏠 Home Assistant Entegrasyonu

### İzleme ve Kontrol Noktaları

#### Enerji Yönetimi
* **EasySolar-II GX:** Inverter güç, shore durumu, güneş üretimi, batarya SOC, yük profili
* **BMS:** Hücre voltajları, toplam voltaj, akım, sıcaklık, SOC, hata durumları
* **Orion XS:** Alternatör şarj akımı, voltaj, sıcaklık

#### Su Yönetimi
* **Temiz su tank:** Seviye (%), hacim (L), düşük seviye uyarısı
* **Gri su tank:** Seviye (%), hacim (L), yüksek seviye uyarısı
* **Pompalar:** Çalışma durumu, akım tüketimi

#### Aydınlatma
* **Tüm LED ışıklar:** Açık/kapalı durumu, otomatik/manuel kontrol
* **RGB şeritler:** Renk, parlaklık, efekt modları

#### İklim ve Konfor
* **24V Klima:** Sıcaklık, mod, çalışma durumu
* **Truma Combi:** Ortam sıcaklığı, sıcak su sıcaklığı, yakıt tüketimi
* **Hava kalitesi:** Nem, sıcaklık, CO2 (opsiyonel)

#### Cihaz Durumları
* **Buzdolabı:** Çalışma durumu, iç sıcaklık (opsiyonel)
* **Clesana C1:** Torba seviyesi, kullanım sayısı
* **Tüm röleler:** Açık/kapalı durumu, akım tüketimi

### Otomasyon Senaryoları

#### Enerji Optimizasyonu
```yaml
# Düşük batarya - kritik olmayan yükleri kapat
- alias: "Düşük Batarya Koruması"
  trigger:
    - platform: numeric_state
      entity_id: sensor.battery_soc
      below: 20
  action:
    - service: switch.turn_off
      target:
        entity_id:
          - switch.usb_charger_outlets
          - switch.ambient_lighting
          - switch.awning_lights
    - service: notify.mobile_app
      data:
        message: "Düşük batarya! Kritik olmayan yükler kapatıldı."
```

#### Yük Yönetimi - Akıllı Mutfak Kontrol
```yaml
# Ocak açıldığında shore yoksa bulaşık makinesini kapat
- alias: "Yük Yönetimi - Ocak Açıldı"
  trigger:
    - platform: state
      entity_id: switch.induction_cooktop
      to: 'on'
  condition:
    - condition: state
      entity_id: binary_sensor.shore_power_connected
      state: 'off'  # Shore bağlı değil
    - condition: state
      entity_id: switch.dishwasher
      state: 'on'  # Bulaşık makinesi çalışıyor
  action:
    - service: switch.turn_off
      target:
        entity_id: switch.dishwasher
    - service: notify.mobile_app
      data:
        message: "Bulaşık makinesi kapatıldı - inverter modu (ocak aktif)"

# Bulaşık makinesi açıldığında shore yoksa ocağı kapat
- alias: "Yük Yönetimi - Bulaşık Makinesi Açıldı"
  trigger:
    - platform: state
      entity_id: switch.dishwasher
      to: 'on'
  condition:
    - condition: state
      entity_id: binary_sensor.shore_power_connected
      state: 'off'  # Shore bağlı değil
    - condition: state
      entity_id: switch.induction_cooktop
      state: 'on'  # Ocak çalışıyor
  action:
    - service: switch.turn_off
      target:
        entity_id: switch.induction_cooktop
    - service: notify.mobile_app
      data:
        message: "İndüksiyon ocak kapatıldı - inverter modu (bulaşık makinesi aktif)"

# Shore bağlantısı kesilince eş zamanlı çalışmayı kontrol et
- alias: "Yük Yönetimi - Shore Bağlantısı Kesildi"
  trigger:
    - platform: state
      entity_id: binary_sensor.shore_power_connected
      to: 'off'
  condition:
    - condition: state
      entity_id: switch.induction_cooktop
      state: 'on'
    - condition: state
      entity_id: switch.dishwasher
      state: 'on'
  action:
    - service: switch.turn_off
      target:
        entity_id: switch.dishwasher  # Bulaşık makinesini öncelikle kapat
    - service: notify.mobile_app
      data:
        message: "Shore bağlantısı kesildi - bulaşık makinesi kapatıldı (ocak aktif)"

# Shore bağlandığında bildirim (tüm cihazlar serbest)
- alias: "Yük Yönetimi - Shore Bağlantısı Kuruldu"
  trigger:
    - platform: state
      entity_id: binary_sensor.shore_power_connected
      to: 'on'
  action:
    - service: notify.mobile_app
      data:
        message: "Shore power aktif - tüm mutfak cihazları serbest (3520W kapasite)"
```

#### Donma Koruması
```yaml
# Dış sıcaklık 0°C altına düşünce su sistemini boşalt
- alias: "Donma Koruması - Su Sistemi"
  trigger:
    - platform: numeric_state
      entity_id: sensor.outside_temperature
      below: 0
  action:
    - service: valve.open
      target:
        entity_id: valve.fresh_water_drain
    - service: notify.mobile_app
      data:
        message: "Donma koruması aktif - su tankları boşaltılıyor"
```

#### Akıllı Aydınlatma
```yaml
# Hareket algılandığında otomatik aydınlatma
- alias: "Otomatik Aydınlatma - Hareket"
  trigger:
    - platform: state
      entity_id: binary_sensor.motion_sensor
      to: 'on'
  condition:
    - condition: sun
      after: sunset
  action:
    - service: light.turn_on
      target:
        entity_id: light.central_area
      data:
        brightness: 128
```

#### Su Seviye Uyarıları
```yaml
# Temiz su düşük seviye
- alias: "Düşük Temiz Su Uyarısı"
  trigger:
    - platform: numeric_state
      entity_id: sensor.fresh_water_level
      below: 10
  action:
    - service: notify.mobile_app
      data:
        message: "Temiz su seviyesi %10'un altında"

# Gri su yüksek seviye
- alias: "Yüksek Gri Su Uyarısı"
  trigger:
    - platform: numeric_state
      entity_id: sensor.grey_water_level
      above: 80
  action:
    - service: notify.mobile_app
      data:
        message: "Gri su tankı %80 dolu - boşaltma önerilir"
```

---

## 🔧 Kurulum ve Konfigürasyon

### Fiziksel Montaj
1. **Raspberry Pi + Touch Screen:** Mutfak tezgahı üstü, kolay erişim
2. **Ethernet Switch:** Elektrik panosuna DIN rail montaj
3. **RS485 to Ethernet:** Pano içi, RS485 cihazlara merkezi konum
4. **Modbus Modüller:** DIN rail montaj, yeterli havalandırma
5. **Bistable Röleler:** Elektrik panosuna montaj, yüksek akım bağlantıları

### Kablolama
* **24V DC Ana Hat:** 6-10mm² kablo, yüksek akım hatları
* **RS485 Bus:** Twisted pair, 120Ω terminasyon
* **Ethernet:** Cat5e/Cat6, maksimum 100m
* **Push Button Hatları:** 0.5-1mm², ekranlı kablo önerilir

### Home Assistant Konfigürasyon
1. **Modbus TCP Entegrasyonu:** Tüm RS485 cihazlar için
2. **Victron Integration:** VE.Bus/Modbus TCP için
3. **ESPHome (Opsiyonel):** Ek sensörler ve genişlemeler için
4. **Grafana/InfluxDB:** Geçmiş veri kaydı ve analiz

---

## 💡 Bakım ve Genişleme

### Düzenli Bakım
* **Aylık:** Bağlantı kontrolü, hata log inceleme
* **Mevsimlik:** Röle testi, sensör kalibrasyonu
* **Yıllık:** Tam sistem testi, firmware güncelleme

### Genişleme İmkanları
* **Analog modül:** 6 boş kanal (sıcaklık, basınç, akım sensörleri için)
* **DI/DO modül:** Ek push button veya sensör girişleri
* **Shelly Plus RGBW PM:** Her cihaz RGBW veya 4x bağımsız beyaz kanal olarak kullanılabilir; ek Shelly cihazı ile kolayca genişletilebilir
* **Röle modülleri:** Paralel bağlantı ile ek röle kanalları

### Yedekleme ve Güvenlik
* **Home Assistant Yedekleme:** Haftalık otomatik yedekleme
* **SD Kart Yedekleme:** Aylık tam sistem imajı
* **Manuel Kontrol:** Kritik sistemler için fiziksel bypass anahtarları

---

## 🚀 Home Assistant Konfigürasyon Deployment

Home Assistant konfigürasyonları `Automation/ha-configs/` klasöründe bulunur ve **otomatik deployment** ile yüklenebilir.

### Hızlı Deployment:

```bash
cd Automation/ha-configs
python3 deploy.py --auto  # Tam otomatik: Dosyalar + Reload
```

### Deployment Script Özellikleri:

✅ **6 Dosyayı Otomatik Yükler (SCP):**
- `helpers/input_datetime.yaml` (8 buton için press time)
- `helpers/input_number.yaml` (8 buton için press count)
- `helpers/input_boolean.yaml` (8 buton için double wait flag)
- `automations/button_press_detection.yaml` (16 detection automation)
- `automations/button_actions.yaml` (16 action automation)
- `modbus_combined.yaml` (Modbus cihaz tanımları)

✅ **4 Servisi Otomatik Reload Eder:**
- `automation` → Tüm automation'ları yeniden yükler
- `input_datetime` → DateTime helper'ları yeniler
- `input_number` → Number helper'ları yeniler
- `input_boolean` → Boolean helper'ları yeniler

✅ **Hata Kontrolü:** Bağlantı, dosya transfer ve reload kontrolü

### Gereksinimler:

1. **Home Assistant API Token** (Long-Lived Access Token)
2. **SSH Key** (Otomatik oluşturuldu: `~/.ssh/homeassistant`)
3. **Advanced SSH & Web Terminal Addon** (SFTP aktif, username: root)

Detaylı kurulum: [`Automation/ha-configs/README.md`](ha-configs/README.md)

---

## 📚 Dokümantasyon Yapısı

| Dosya | İçerik |
|-------|--------|
| **Automation/readme.md** | Bu dosya - Sistem mimarisi, IO haritası, cihaz listeleri |
| **Automation/ha-configs/README.md** | HA konfigürasyonları, button mapping, troubleshooting |
| **Automation/ha-configs/KURULUM.md** | Adım adım kurulum rehberi |
| **simulators/*/README.md** | Simülatör kullanım kılavuzları |

---

*Bu doküman, karavan otomasyon sisteminin tam teknik referansıdır. Tüm elektrik tüketicileri, IO eşlemeleri ve otomasyon senaryoları bu sayfada toplanmıştır.*
