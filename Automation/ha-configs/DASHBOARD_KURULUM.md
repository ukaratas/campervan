# 🎨 Karavan Dashboard Kurulum Rehberi

Home Assistant için karavan kontrol paneli kurulum adımları.

---

## 📋 İçindekiler

1. [Area (Alan) Oluşturma](#1-area-alan-oluşturma)
2. [Entity'leri Area'lara Atama](#2-entityleri-arealara-atama)
3. [Dashboard Kurulumu](#3-dashboard-kurulumu)
4. [Özelleştirme](#4-özelleştirme)

---

## 1. Area (Alan) Oluşturma

### Neden Area Gerekli?

Area'lar fiziksel mekanları temsil eder ve entity'leri gruplar. Dashboard'larda "Area Card" kullanarak tüm alan cihazlarını otomatik gösterebilirsin.

### Area'ları Oluştur

**Home Assistant → Settings → Areas, labels & zones → Create Area**

| Icon | Area İsmi | Açıklama |
|------|-----------|----------|
| 🍳 | Mutfak | Mutfak aydınlatma ve cihazları |
| 🛏️ | Yatak Alanı | Ana yatak, okuma lambaları |
| 🏠 | Orta Alan | Oturma alanı |
| 🚪 | Popup Yatak | Popup roof alanı |
| 🌙 | Dış Alan | Tente ve dış aydınlatma |
| 🚿 | Banyo | Banyo aydınlatma |
| 💧 | Su Sistemi | Pompalar ve su kontrol |
| 🔌 | Elektrik | Güç cihazları ve USB |

**Her area için:**
1. "Create Area" tıkla
2. İsmi gir (örn: "Mutfak")
3. Icon seç (isteğe bağlı)
4. "Add" tıkla

---

## 2. Entity'leri Area'lara Atama

**Home Assistant → Settings → Devices & services → Entities**

### 🍳 Mutfak

Entity'yi bul → Tıkla → Area seç

- `light.mutfak_isik` → **Mutfak**
- `light.mutfak_tezgah_isik` → **Mutfak**
- `binary_sensor.mutfak_butonu` → **Mutfak**
- `switch.usb_kutusu_mutfak` → **Mutfak**

### 🛏️ Yatak Alanı

- `light.yatak_alani_isik` → **Yatak Alanı**
- `light.sol_okuma_isik` → **Yatak Alanı**
- `light.sag_okuma_isik` → **Yatak Alanı**
- `binary_sensor.sag_yatak_butonu` → **Yatak Alanı**
- `binary_sensor.sol_yatak_butonu` → **Yatak Alanı**
- `switch.usb_kutusu_yatak` → **Yatak Alanı**

### 🏠 Orta Alan

- `light.orta_alan_isik` → **Orta Alan**
- `binary_sensor.orta_alan_butonu` → **Orta Alan**

### 🚪 Popup Yatak

- `light.popup_yatak_isik` → **Popup Yatak**
- `binary_sensor.popup_yatak_butonu` → **Popup Yatak**
- `switch.usb_kutusu_popup` → **Popup Yatak**

### 🌙 Dış Alan

- `light.tente_isik` → **Dış Alan**
- `binary_sensor.dis_aydinlatma_butonu` → **Dış Alan**

### 🚿 Banyo

- `light.banyo_aydinlatma` → **Banyo**
- `light.banyo_ayna_aydinlatma` → **Banyo**
- `binary_sensor.banyo_butonu` → **Banyo**
- `switch.usb_kutusu_banyo` → **Banyo**

### 💧 Su Sistemi

- `switch.temiz_su_hidrofor` → **Su Sistemi**
- `switch.macerator_pompa` → **Su Sistemi**
- `switch.gri_su_pompasi` → **Su Sistemi**
- `switch.su_pompasi` → **Su Sistemi**
- `switch.valf_1` → **Su Sistemi**
- `switch.valf_2` → **Su Sistemi**

### 🔌 Elektrik

- `switch.buzdolabi` → **Elektrik**
- `switch.truma_combi_d4` → **Elektrik**
- `switch.alarm_siren` → **Elektrik**
- `switch.havalandirma_fan` → **Elektrik**
- `switch.isitici` → **Elektrik**
- `switch.sogutucu` → **Elektrik**

---

## 3. Dashboard Kurulumu

### Option 1: YAML İle Otomatik (Önerilen) 🚀

1. **Dashboard Oluştur:**
   - Settings → Dashboards → + Add Dashboard
   - "Start with an empty dashboard" seç
   - Title: **"Karavan Kontrol"**
   - Icon: `mdi:rv-truck` veya `mdi:camper`
   - Create

2. **YAML Import Et:**
   - Dashboard'a gir
   - Sağ üst köşe → ⋮ (3 nokta) → **"Edit Dashboard"**
   - Sağ üst köşe → ⋮ (3 nokta) → **"Raw configuration editor"**
   - `dashboard_karavan.yaml` dosyasının **içeriğini kopyala**
   - Yapıştır
   - Save

3. **Bitir!**
   - Dashboard otomatik olarak 3 sekme ile oluşturulur:
     - 🏠 Aydınlatma
     - 💧 Su Sistemi
     - 🍳 Mutfak & Cihazlar

### Option 2: Manuel Oluşturma (UI ile)

1. **Dashboard Oluştur:**
   - Settings → Dashboards → + Add Dashboard
   - Title: "Karavan Kontrol"
   - Icon: `mdi:rv-truck`

2. **View (Sekme) Ekle:**
   - Dashboard'a gir → Edit
   - + Add View
   - Title: "Aydınlatma", Icon: `mdi:lightbulb-group`
   - Tekrarla: "Su Sistemi", "Mutfak & Cihazlar"

3. **Kartları Ekle:**
   - Her view'da → + Add Card
   - **"Entities Card"** seç
   - Title gir (örn: "🍳 Mutfak")
   - Entity'leri ekle
   - Save

---

## 4. Özelleştirme

### Kart Tipleri

Dashboard'da farklı kart tipleri kullanabilirsin:

**Entities Card:**
```yaml
- type: entities
  title: Mutfak
  entities:
    - light.mutfak_isik
    - light.mutfak_tezgah_isik
```

**Button Card:**
```yaml
- type: button
  entity: light.mutfak_isik
  name: Mutfak Işık
  icon: mdi:lightbulb
  tap_action:
    action: toggle
```

**Light Card:**
```yaml
- type: light
  entity: light.mutfak_isik
  name: Mutfak Işık
```

**Area Card:**
```yaml
- type: area
  area: mutfak
  navigation_path: /lovelace/aydinlatma
```

### Renk ve Tema

**Settings → Profile → Theme** seçerek tema değiştirebilirsin.

Kendi temanı oluşturmak için:
- `themes/` klasörü oluştur
- `karavan_theme.yaml` dosyası ekle

---

## 🎯 Sonuç

Dashboard kurulumu tamamlandı! ✅

### Kontrol Et:

- ✅ 8 Area oluşturuldu
- ✅ 31 Entity area'lara atandı
- ✅ 3 View'lı dashboard oluşturuldu
- ✅ Tüm cihazlar kontrol edilebilir

### Sonraki Adımlar:

1. **Sensör Ekle:** Batarya, su seviyesi, sıcaklık
2. **Automation Oluştur:** Otomatik aydınlatma, alarm
3. **Bildirimler:** Push notification, email
4. **Grafik Ekle:** Enerji tüketimi, su kullanımı

---

## 📚 Faydalı Linkler

- [Home Assistant Dashboard Docs](https://www.home-assistant.io/dashboards/)
- [Area Card](https://www.home-assistant.io/dashboards/area/)
- [Entities Card](https://www.home-assistant.io/dashboards/entities/)
- [Material Design Icons](https://pictogrammers.com/library/mdi/)

---

**Kolay gelsin! 🎉**

