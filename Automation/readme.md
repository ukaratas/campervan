
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

#### 6. RGB Dimmer Module
* **Model:** RS-485 Modbus RTU 4-channel dimmer WBPRO-LEDDIM
* **Özellikler:** 4 kanal PWM dimming, RGB kontrol
* **Kullanım:** Ambiyans aydınlatma (tente, ortam)

### Ethernet Üzerinden Bağlanan Cihazlar
* **Victron EasySolar-II 3kVA MPPT 250/70 GX** — Inverter/şarj/MPPT kombine, VE.Bus/Modbus TCP
* **RS485 to Ethernet Serial Server** — Modbus RTU → TCP gateway

---

## 📊 Elektrik Tüketicileri - Detaylı Liste

### 24V DC Tüketiciler

#### Yüksek Güç (>100W)
| Cihaz | Güç | Akım | Kontrol | Notlar |
|-------|-----|------|---------|--------|
| 24V Klima (Eva Cool Eva 24V 20T Premium) | 720-960W | 30-40A | High Latching Relay | Ana yatak soğutma |
| Temiz su hidrofor pompası | 240-360W | 10-15A | High Latching Relay | Basınçlı su sistemi |
| Gri su boşaltma pompası | 240-360W | 10-15A | High Current Relay | Atık su boşaltma |

#### Orta Güç (10-100W)
| Cihaz | Güç | Akım | Kontrol | Notlar |
|-------|-----|------|---------|--------|
| Buzdolabı (EvaCool Eva Berlin 90L) | 50-80W | 2-3A | High Latching Relay | Sürekli çalışma |
| USB şarj çıkışları | 50-100W | 2-4A | High Latching Relay | Telefon, tablet |
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
| Tente ambiyans (RGB) | 10-20W | 4C Dimmer | RGB LED şerit |
| Ortam ambiyans (RGB) | 10-20W | 4C Dimmer | RGB LED şerit |

#### Sensörler ve Valfler
| Cihaz | Güç | Kontrol | Notlar |
|-------|-----|---------|--------|
| Su seviye sensörleri | <1W | Analog Module | Temiz/gri su tankları |
| Actuator valf (temiz su) | 5-10W | Home Assistant | Donma koruması |
| Elektrikli vana (gri su) | 5-10W | Home Assistant | Boşaltma kontrolü |
| Hareket sensörleri | <1W | DI Module | Otomatik aydınlatma |
| Nem sensörleri | <1W | Analog Module | Hava kalitesi |
| Popup roof fanı (opsiyonel) | 10-20W | Home Assistant | Havalandırma |
| Banyo fanı (opsiyonel) | 10-20W | Home Assistant | Nem kontrolü |

### 12V DC Tüketiciler (24V'dan Konvertör ile)
| Cihaz | Güç | Akım | Kontrol | Notlar |
|-------|-----|------|---------|--------|
| Truma Combi D4 inet | 24-96W | 2-8A | Truma inet / HA | Dizel kombi |
| Clesana C1 susuz tuvalet | 0.6W standby / 6.6W flush | 0.05A / 0.55A | Home Assistant | Susuz tuvalet |
| 12V genel prizler | 24-60W | 2-5A | High Latching Relay | Portatif cihazlar |
| Macerator pompa | ~120W | 10A | High Current Relay | Kısa süreli |

**24V to 12V DC Konvertör:** 15-20A (180-240W) kapasite

### 220V AC Tüketiciler (EasySolar-II İnverter)

#### Yüksek Güç (>1000W)
| Cihaz | Güç | Kontrol | Notlar |
|-------|-----|---------|--------|
| Omake ankastre indüksiyon ocak | 1800W | EasySolar-II / HA | Yük yönetimi gerekli |
| Electrolux bulaşık makinesi (ESF2400O) | 1500W (ısıtıcı) + 200W (pompa) | EasySolar-II / HA | Yük yönetimi gerekli |
| Profilo FRIAT9AN mikrodalga fırın | 800W | EasySolar-II / HA | 20L kapasite |

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

## 🔌 IO Haritası - Girişler ve Çıkışlar

### Çıkışlar - High Current Relay (30A, 4 Kanal)
Kısa süreli yüksek yük alacak cihazlar için kullanılır.

| Kanal | Bağlı Cihaz | Güç | Çalışma Süresi |
|-------|-------------|-----|----------------|
| R1 | Macerator pompa | 12V, ~120W | Kısa süreli (1-2 dk) |
| R2 | Rezerv | - | - |
| R3 | Rezerv | - | - |
| R4 | Rezerv | - | - |

### Çıkışlar - High Latching Relay (Bistable, 8 Kanal)
Uzun süre açık kalacak yüksek güç yükleri için. DI/DO modülü ile tetiklenir, bistable röle ile kalıcı açık/kapalı.

| Kanal | Bağlı Cihaz | Güç | Notlar |
|-------|-------------|-----|--------|
| DO1 | Buzdolabı | 24V DC, 50-80W | Sürekli çalışma |
| DO2 | Temiz su hidrofor | 24V DC, 240-360W | Talep üzerine |
| DO3 | 24V klima | 24V DC, 720-960W | Mevsimsel |
| DO4 | Truma Combi | 12V DC, 24-96W | Kış/sıcak su |
| DO5 | USB şarj çıkışları | 24V DC, 50-100W | Gerektiğinde |
| DO6 | 24V genel çıkışlar | 24V DC, değişken | Portatif cihazlar |
| DO7 | 12V genel çıkışlar | 12V DC, 24-60W | Konvertör üzerinden |
| DO8 | Rezerv | - | - |

### Çıkışlar - Low Latching Relay (8 Kanal)
Uzun süre açık kalacak düşük güç yükleri (aydınlatma).

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

**Not:** Banyo aydınlatma (5-10W) ve banyo ayna (5-10W) için ek modül veya R1-R8'den birkaç kanal birleştirilebilir.

### Çıkışlar - 4C Dimmer Module (4 Kanal PWM)
RGB LED şeritler ve dimmer kontrolü gereken aydınlatmalar.

| Kanal | Bağlı Cihaz | Güç | Kontrol |
|-------|-------------|-----|---------|
| CH1 | Tente ambiyans (RGB LED) | 10-20W | RGB + dimming |
| CH2 | Ortam ambiyans (RGB LED) | 10-20W | RGB + dimming |
| CH3 | Rezerv | - | - |
| CH4 | Rezerv | - | - |

### Girişler - DI Module (8 Kanal)
Push button girişleri için dijital input.

| Kanal | Push Button | Short Press | Long Press | Double Press |
|-------|-------------|-------------|------------|--------------|
| DI1 | Sağ yatak | Yatak alanı aç/kapa | Sağ okuma lambası | Tüm aydınlatma kapat |
| DI2 | Sol yatak | Yatak alanı aç/kapa | Sol okuma lambası | Tüm aydınlatma kapat |
| DI3 | Popup yatak | Popup aydınlatma aç/kapa | Popup ambiyans | Tüm aydınlatma kapat |
| DI4 | Dış aydınlatma | Tente altı aç/kapa | Tente ambiyans | Tüm aydınlatma kapat |
| DI5 | Otomatik basamak | Basamak aç/kapa | - | - |
| DI6 | Mutfak | Mutfak lambası | Tezgâh lambası | - |
| DI7 | Orta alan | Orta alan aydınlatma | Ambiyans aydınlatma | Tüm aydınlatma kapat |
| DI8 | Banyo | Banyo aydınlatma | Banyo ayna lambası | - |

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
* **4C Dimmer:** 2 boş kanal (ek RGB aydınlatma)
* **Röle modülleri:** Paralel bağlantı ile ek röle kanalları

### Yedekleme ve Güvenlik
* **Home Assistant Yedekleme:** Haftalık otomatik yedekleme
* **SD Kart Yedekleme:** Aylık tam sistem imajı
* **Manuel Kontrol:** Kritik sistemler için fiziksel bypass anahtarları

---

*Bu doküman, karavan otomasyon sisteminin tam teknik referansıdır. Tüm elektrik tüketicileri, IO eşlemeleri ve otomasyon senaryoları bu sayfada toplanmıştır.*
