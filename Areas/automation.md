# Otomasyon ve Kontrol Altyapısı

Karavanın tüm sistemlerinin merkezi ve akıllı şekilde izlenmesi, kontrolü ve otomasyonu için Home Assistant tabanlı bir altyapı kurulmuştur. Tüm cihazlar, sensörler ve aktüatörler mümkün olduğunca kablolu (RS485/Modbus) olarak entegre edilir.

## 🎯 Amaç ve Kapsam

- Tüm elektrikli cihazların, sensörlerin ve valflerin merkezi olarak izlenmesi ve kontrolü
- Enerji optimizasyonu, güvenlik, konfor ve bakım kolaylığı
- Uzaktan izleme, bildirim ve otomasyon senaryoları

## 🛠️ Kullanılan Donanımlar

| Kategori | Ürün/Modül | Özellikler |
|----------|------------|------------|
| **Ana Kontrolcü** | Waveshare IPCBOX-CM5-A + RPi CM5 8GB Lite + 512GB NVMe SSD | 4x RS485, CAN, 2DI/2DO, dual ETH (1G+2.5G), 7-36V DC, M.2 4G/5G slot, DIN rail, alüminyum kasa |
| **DI/DO Modülü** | Waveshare 8DI/8DO (RS485) × 1 | Push button girişleri (DI); **Kamp Modu** butonu + **Orion 24/12-70 DC-DC remote on/off** (DO). 12V rail bu DO ile açılır — ayrı röle yok |
| **220V AC röle** | Waveshare 8CH RTU Relay (RS485 CH0, slave 2 / 9600) | **Yalnızca 220V AC yükler.** Beefy 32A kontak → AC motor/rezistans inrush'ında uzun kontak ömrü. HA load-shed (3000W inverter limiti) |
| **24V DC röle** | Waveshare POE ETH 16CH Relay (Modbus TCP) | **Yalnızca 24V DC yükler** — buzdolabı, pompalar, macerator, aydınlatma zonları. Çok kanal = çok zon. Motorlu kanallara flyback/snubber diyot |
| **Analog Giriş** | Industrial 8-Ch Analog Acquisition Module | 12-bit hassasiyet, voltaj/akım okuma, RS485 |
| **Kontrol Paneli** | Waveshare 11.9" HDMI LCD 320×1480 IPS Touch | Giriş kapısı üstü, HDMI + USB direkt bağlantı, HA dashboard |

## 🔌 Kontrol Mimarisi

Temel ilke: **röleler voltaj alanına göre ayrılır** — 220V AC ve 24V DC asla aynı board'da/terminal bloğunda karışmaz (güvenlik + kablaj netliği). Yükler zaten düşük akımlı olduğundan seçim elektriksel değil organizasyoneldir; ağır iş (motor/rezistans inrush) AC tarafındadır, o yüzden beefy 8CH board AC'ye, çok-kanallı 16CH board DC'ye ayrıldı.

### Enerji rail'leri
- **24V bus:** Always-on, **hiç anahtarlanmaz** — otomasyon (IPCBOX-CM5) hiçbir zaman güç kaybetmez.
- **12V rail:** Kamp Modu'nda **Orion 24/12-70 remote on/off (DO)** ile açılır. Ayrı röle/kontaktör yok. 12V yükleri (Clesana C1, Truma Combi kontrol/fan, su pompası) bu rail ile standby'a gelir.
- **İnverter (MultiPlus-II GX):** Default **OFF** (boşta idle çekmesin). Kamp Modu'nda **HA → MultiPlus (ETH / Modbus TCP)** ile açılır; AC OUT 1 canlanınca **tüm 220V outlet'ler otomatik** beslenir (outlet'ler direkt, röle yok).

### Kamp Modu (tek buton)
Push button (8DI) → HA otomasyonu:
1. **DO → Orion 24/12-70 ON** → 12V rail kalkar → Clesana + Combi-12V + pompa standby
2. **HA → MultiPlus ON (ETH)** → AC OUT 1 canlı → tüm outlet'ler otomatik açık

Aydınlatma Kamp Modu'ndan bağımsızdır (24V always-on bus'ta, her zaman kullanılabilir).

### 8CH RTU Relay — 220V AC yükler (RS485 CH0, slave 2/9600)
| Kanal | Yük | Not |
|:---:|---|---|
| 1 | İndüksiyon ocak | ~8A, HA load-shed |
| 2 | Çamaşır makinesi | ~9A, HA load-shed |
| 3 | Bulaşık makinesi | ~7.7A, HA load-shed |
| 4 | Kombi 220V rezistans | ~8A, HA load-shed |
| 5 | Blue Smart float şarj | ~0.3A; sıkışınca ilk kesilen (en düşük öncelik) |
| 6–8 | Yedek | — |

**Load-shed:** MultiPlus'tan ETH/Modbus TCP ile toplam AC yük okunur; 3000W inverter limitine yaklaşınca öncelik/karşılıklı-kilit ile kanallar yönetilir (ör. indüksiyon açıkken bulaşığı beklet). Outlet'lere takılan cihazlar shed edilemez → MultiPlus overload korumasına emanet.

### 16CH POE ETH Relay — 24V DC yükler (Modbus TCP)
| Yük | Akım | Not |
|---|---|---|
| Buzdolabı | ~4A | Secop/Danfoss BD tipi (BLDC + soft-start, **LRA inrush yok**). Röle sadece ara sıra master/depo/düşük-SOC kesme; termostat cycling cihazın kendi içinde |
| Su pompaları | ~2-4A | Küçük PM motor, kayda değer inrush yok |
| Macerator | Seaflo SFMP2-120-01 (24V): ~6A açık akış, **~7.2A working peak** (basınçla artar) | **10A slow-blow sigorta** (datasheet'teki 20A **12V modele** aittir), flyback diyot |
| Aydınlatma zonları | <2A/zon | 24V LED; DC ark önemsiz. Çok zon → 16CH ideal |
| Küçük valf/pompa, diğer | düşük | — |

> **DC ark notu:** 24V, DC ark'ın tehlikeli eşiğinin (~48V+) altında; yüklerin hepsi ≤~7A → 16A röle kontakları rahat keser. Endüktif (motor) kanallara ömür için flyback/snubber diyot eklenir.

## 🏠 Home Assistant Entegrasyonu

- Tüm modüller Home Assistant'a Modbus/RS485 ile entegre edilir
- Cihaz ve sensör durumları, enerji tüketimi, su seviyesi, sıcaklık vb. merkezi olarak izlenir
- Otomasyonlar YAML veya görsel arayüz ile tanımlanır

### Tipik Otomasyon Senaryoları
- **Enerji Yönetimi:** Yüksek akım çeken cihazların (pompa, ısıtıcı vb.) otomatik aç/kapatılması
- **Donma Koruması:** Sıcaklık sensörüne göre valf/pompa otomasyonu
- **Su Yönetimi:** Seviye sensörüne göre pompa ve valf kontrolü
- **Güvenlik:** Kaçak akım, aşırı sıcaklık/akım durumunda otomatik müdahale ve alarm

## 🔧 Kurulum ve Bakım

1. **Donanım Montajı:** IPCBOX-CM5-A ve modüllerin pano içine yerleştirilmesi (DIN rail)
2. **Kablolama:** RS485, güç ve sinyal hatlarının çekilmesi
3. **Home Assistant Kurulumu:** CM5 üzerinde Home Assistant OS kurulumu (512GB NVMe SSD)
4. **Modül Entegrasyonu:** Modbus cihazlarının Home Assistant'a tanımlanması
5. **Otomasyonların Tanımlanması:** Senaryoların yazılması ve test edilmesi

## 💡 Genişletilebilirlik ve Öneriler
- Ek modüllerle (röle, analog, dijital giriş/çıkış) sistem kolayca büyütülebilir
- MQTT, Modbus TCP gibi ek protokollerle uzaktan izleme ve entegrasyon
- Endüstriyel modüller sayesinde uzun ömür ve güvenilirlik
- 24V bataryadan direkt besleme (IPCBOX-CM5 7-36V giriş), ihtiyaç halinde harici UPS eklenebilir

## 🔗 Cihaz Detayları

### Harici Aydınlatma Sistemi (2 devre)
- **Dış Aydınlatma 1 + 2:** 24V LED dış aydınlatma
- **Kontrol:** Push button (DI) → HA → **16CH DC röle** (24V zon)
- **Senaryo:** Kapı açıldığında otomatik aydınlatma, uzaktan kontrol

## ⚡ Elektrik ve Su Tesisatı

- **Enerji:** 24V DC ana hat (IPCBOX-CM5-A 7-36V direkt besleme, modüller, röleler)
- **İletişim:** RS485/Modbus, dijital/analog giriş-çıkışlar
- **Harici Aydınlatma:** 24V LED şeritler (yan taraf + awning/tente)
- **Otomasyon:** Röle, sensör, aktüatör, push button, Home Assistant entegrasyonu
- **Su:** Doğrudan bağlantı yok, ancak su ve nem sensörleriyle izleme yapılabilir

---

*Bu altyapı, karavanın tüm sistemlerinin akıllı, güvenli ve merkezi olarak yönetilmesini sağlar.*
