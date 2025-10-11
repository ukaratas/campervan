# Home Assistant Konfigürasyon Dosyaları
## Campervan Automation System

Bu klasörde Waveshare DI/DO modülü ve Latching Relay için Home Assistant konfigürasyon dosyaları bulunur.

---

## 🚀 Otomatik Deployment

Artık konfigürasyonları manuel copy/paste yapmak yerine otomatik deployment kullanabilirsiniz!

### Hızlı Kullanım:

```bash
cd Automation/ha-configs
python3 deploy.py
```

**Bu script:**
- ✅ Home Assistant bağlantısını kontrol eder
- ✅ Tüm servisleri otomatik reload eder (automation, helpers)
- 📋 Manuel deployment talimatlarını gösterir

### İlk Kurulum:

1. **Credentials dosyasını oluştur:**
   ```bash
   cp ha_credentials.example ha_credentials.py
   ```

2. **Token'ı al:**
   - Home Assistant → Profile → Long-Lived Access Tokens → Create Token
   - `ha_credentials.py` dosyasını aç ve token'ı yapıştır

3. **SSH Key Kurulumu (Otomatik deployment için):**
   - SSH key zaten oluşturuldu ve proje içinde saklanıyor:
     - **Private key:** `.ssh/homeassistant` (bu dosyayı `~/.ssh/` klasörüne kopyala)
     - **Public key:** `.ssh/homeassistant.pub`
   
   **Key'i sisteme kopyala:**
   ```bash
   cp Automation/ha-configs/.ssh/homeassistant ~/.ssh/
   chmod 600 ~/.ssh/homeassistant
   ```
   
   - Public key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAZCJMe6kENt2pVkxT3TbYkjLx6mQq+180BDbxp1+HIx homeassistant-deploy`
   - Home Assistant'ta: Settings → Add-ons → Advanced SSH & Web Terminal → Configuration:
     ```yaml
     ssh:
       username: root
       password: ""
       authorized_keys:
         - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAZCJMe6kENt2pVkxT3TbYkjLx6mQq+180BDbxp1+HIx homeassistant-deploy
       sftp: true
     ```

4. **Tam Otomatik Deployment:**
   ```bash
   python3 deploy.py --auto  # Dosyaları yükle + Reload! 🚀
   ```

---

## 📁 Dosya Yapısı

```
ha-configs/
├── helpers/
│   ├── input_datetime.yaml    # DateTime helpers (8 buton)
│   ├── input_number.yaml      # Number helpers (8 buton)
│   └── input_boolean.yaml     # Boolean helpers (8 buton)
├── automations/
│   ├── button_press_detection.yaml  # Press pattern algılama (16 automation)
│   └── button_actions.yaml          # Press action'ları (16 automation)
├── modbus_combined.yaml       # Modbus cihaz tanımlamaları
├── deploy.py                  # 🚀 Otomatik deployment script
├── ha_credentials.py          # 🔒 API credentials (gitignore'da!)
├── ha_credentials.example     # Örnek credentials dosyası
├── KURULUM.md                 # Detaylı kurulum rehberi
└── README.md                  # Bu dosya
```

### 1. `helpers/` klasörü
**Helper tanımlamaları (3 dosya)**
- `input_datetime.yaml` - Button press zamanları (8 adet)
- `input_number.yaml` - Press count sayaçları (8 adet)
- `input_boolean.yaml` - Double press wait flag'leri (8 adet)

**TOPLAM:** 24 helper (8 buton × 3 tip)

### 2. `automations/` klasörü
**Automation tanımlamaları (2 dosya)**

#### `button_press_detection.yaml`
- Her buton için press/release detection
- Short press (< 800ms)
- Long press (> 800ms)
- Double press (2 kere basma, 400ms timeout)
- Event firing: `{button}_short_press`, `{button}_long_press`, `{button}_double_press`

#### `button_actions.yaml`
- Event listener'lar
- Light toggle/turn_on/turn_off aksiyonları
- Kendi entity'lerinize göre düzenlenebilir (template)

**TOPLAM:** ~32 automation (16 detection + 16 action)

### 3. `modbus_combined.yaml` 
**Modbus cihazları tanımlamaları**
- Latching Relay (Port 5023) - 8 kanal aydınlatma
- DI/DO Module (Port 5024) - 8 button + 8 switch

### 4. `KURULUM.md`
**Detaylı kurulum rehberi**
- Adım adım Home Assistant'a ekleme
- Troubleshooting
- Test yöntemleri
- Özelleştirme önerileri

---

## 🚀 Hızlı Başlangıç

1. **KURULUM.md**'yi oku
2. Dosyaları Home Assistant config klasörüne kopyala
3. `configuration.yaml`'ı güncelle
4. Config check yap
5. Restart et
6. Test et!

---

## 🎮 Button Mapping

| Buton | DI | Short | Long | Double |
|-------|----|---------|---------|--------------------|
| Sağ Yatak | 0 | Yatak alanı | Sağ okuma | Tümünü kapat |
| Sol Yatak | 1 | Yatak alanı | Sol okuma | Tümünü kapat |
| Popup | 2 | Popup | Popup ambiyans | Tümünü kapat |
| Dış | 3 | Tente | Tente ambiyans | Tümünü kapat |
| Basamak | 4 | Basamak | - | - |
| Mutfak | 5 | Mutfak | Tezgâh | - |
| Orta Alan | 6 | Orta alan | Ambiyans | Tümünü kapat |
| Banyo | 7 | Banyo | Ayna | - |

---

## 🔧 Özelleştirme

### Light Entity'leri Değiştir

`button_actions.yaml` içinde:

```yaml
entity_id: light.yatak_alani_isik  # ← Burası
```

### Press Süreleri Ayarla

`button_press_detection.yaml` içinde:

```yaml
is_long: "{{ press_duration > 0.8 }}"  # Long press: 800ms
delay: milliseconds: 400               # Double timeout: 400ms
```

### Aksiyonları Değiştir

`button_actions.yaml` içinde istediğin servisi çağırabilirsin:
- `light.toggle`
- `light.turn_on` (brightness, color, etc.)
- `light.turn_off`
- `scene.turn_on`
- `script.run`
- `notify.send`
- ... herhangi bir HA servisi

---

## 📊 Sistem Mimarisi

```
┌─────────────────┐
│  Push Buttons   │
│   (DI 0-7)      │
└────────┬────────┘
         │
         ├─ Binary Sensor → on/off
         │
         ↓
┌────────────────────────────┐
│  Press Detection           │
│  (button_press_detection)  │
│                            │
│  • Press time kaydı        │
│  • Release'de süre hesapla │
│  • Pattern detect:         │
│    - Short (< 800ms)       │
│    - Long (> 800ms)        │
│    - Double (2x + timeout) │
│                            │
│  • Event fire              │
└────────┬───────────────────┘
         │
         ├─ Event: {button}_short_press
         ├─ Event: {button}_long_press
         └─ Event: {button}_double_press
         │
         ↓
┌────────────────────────────┐
│  Actions                   │
│  (button_actions)          │
│                            │
│  Event listener →          │
│  Light/Switch control      │
└────────────────────────────┘
```

---

## 🎯 Özellikler

✅ **Short Press Detection** - Hızlı basma (< 800ms)  
✅ **Long Press Detection** - Uzun basılı tutma (> 800ms)  
✅ **Double Press Detection** - Çift basma (400ms içinde 2 kere)  
✅ **Event-Based Architecture** - Modüler ve özelleştirilebilir  
✅ **No External Dependencies** - Sadece HA native features  
✅ **8 Button Support** - Tüm DI kanalları desteklenir  
✅ **Configurable Timing** - Press süreleri ayarlanabilir  

---

## 📝 Notlar

- **Binary Sensor Scan Interval:** 1 saniye (ihtiyaç halinde düşürülebilir)
- **Event Fire:** Automation çalıştığında custom event fırlatılır
- **Helpers:** Her buton için 3 helper (datetime, number, boolean)
- **Automations:** Toplam ~32 automation (16 detection + 16 action)

---

## 🐛 Troubleshooting

### Sorun: Automations hata veriyor - "uses an unknown action"

**Sebep:** Event syntax'ı yanlış (`service: event.fire` veya eski syntax kullanılmış)

**Çözüm:** Event fırlatmak için doğru syntax:
```yaml
# ❌ YANLIŞ
- service: event.fire
  data:
    event_type: my_event

# ✅ DOĞRU
- event: my_event
  event_data: {}
```

---

### Sorun: Template hatası - "as_datetime" çalışmıyor

**Sebep:** `as_datetime` filter'ı datetime string'i template'e çeviremez

**Çözüm:** `as_timestamp` kullan:
```yaml
# ❌ YANLIŞ
press_duration: >
  {{ (now() - states('input_datetime.xxx') | as_datetime).total_seconds() }}

# ✅ DOĞRU
press_duration: >
  {{ as_timestamp(now()) - as_timestamp(states('input_datetime.xxx')) }}
```

---

### Sorun: SSH/SCP çalışmıyor - "Permission denied" veya "Connection refused"

**Çözüm Adımları:**

1. **Username kontrol:** `root` olmalı (hassio değil!)
   ```yaml
   ssh:
     username: root  # ← ÖNEMLİ!
   ```

2. **SFTP aktif:** `sftp: true` olmalı
   ```yaml
   ssh:
     sftp: true  # ← ÖNEMLİ!
   ```

3. **authorized_keys liste formatında:**
   ```yaml
   authorized_keys:
     - ssh-ed25519 AAA...  # ← Tire ve liste formatı
   ```

4. **Addon başlatılmış:** Settings → Add-ons → Start

---

### Sorun: Events fırlatılıyor ama actions çalışmıyor

**Kontrol:**
1. Developer Tools → Events → "Listen to events"
2. Event type: `sag_yatak_short_press` yaz
3. Start Listening
4. Butona bas
5. Event geldi mi?

**Event geliyorsa ama action yok:**
- `button_actions.yaml` yüklü mü kontrol et
- Entity ID'ler doğru mu? (`light.yatak_alani_isik`)
- Automation enabled mı? (Settings → Automations)

---

### Sorun: Binary sensor değişmiyor

**Kontrol:**
1. DI/DO simülatörü çalışıyor mu?
2. Modbus connection aktif mi?
3. Binary sensor entity mevcut mu? (Developer Tools → States)

**Log kontrolü:**
```bash
# Home Assistant log
Settings → System → Logs → Filter: "modbus"
```

---

## 🐛 Bilinen Limitasyonlar

1. **Very Fast Double Press:** Çok hızlı çift basmalarda ilk press kaçabilir
2. **Long + Double Conflict:** Long press algılandıktan sonra double press olmaz
3. **Scan Interval:** 1 saniye scan interval, bazı durumlarda gecikme yaşanabilir

**Çözümler:**
- Scan interval'i 0.5 saniyeye düşür (`scan_interval: 0.5`)
- Press timeout'ları ayarla
- Event trace'lerini incele (Automation → ⋮ → Traces)

---

## 🚀 Gelecek Geliştirmeler

- [ ] Triple press desteği
- [ ] Pattern templates (configurable patterns)
- [ ] Notification desteği (optional)
- [ ] Scene integration örnekleri
- [ ] Condition examples (time, state, etc.)

---

Başarılar! 🎉

