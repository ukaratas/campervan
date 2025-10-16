# 📊 Dashboard Kurulum Rehberi

Bu rehber, Home Assistant'a 3 farklı dashboard'un nasıl ekleneceğini açıklar.

## 🎯 Dashboard Yapısı

Projede **3 ana dashboard** var:

### 1️⃣ 🚐 Karavan (Ana Dashboard)
**5 view (tab) içerir:**
- 📊 Genel Bakış
- 💡 Aydınlatma
- 🔌 220V Cihazlar
- 💧 Su Sistemi
- 🛋️ Konfor & Diğer

### 2️⃣ ⚡ Enerji
**2 view (tab) içerir:**
- 📊 Güç Tüketim
- 🔋 Batarya & Şarj

### 3️⃣ 🔧 Teknik
**2 view (tab) içerir:**
- 📡 Modbus Cihazlar
- 🐛 Test & Debug

---

## 📋 Kurulum Adımları

### Yöntem 1: UI Üzerinden (Önerilen)

#### 1. İlk Dashboard'u Oluştur (Karavan)

1. **Home Assistant'a giriş yap**
2. **Sol menüden "Overview" → Sağ üst köşe "···" → "Edit Dashboard"**
3. **Sağ üst köşe "···" → "Raw configuration editor"**
4. **Tüm içeriği sil**
5. **`karavan_ana.yaml` dosyasının içeriğini yapıştır**
6. **"Save" → "Done"**

✅ İlk dashboard hazır! Şimdi üstte **"🚐 Karavan"** görünecek ve **5 tab** olacak.

#### 2. İkinci Dashboard'u Ekle (Enerji)

1. **Sol menüden "Settings" → "Dashboards"**
2. **Sağ alt köşe "+ ADD DASHBOARD"**
3. **"New dashboard from scratch" seç**
4. **Başlık: `⚡ Enerji`**
5. **Icon: `mdi:flash`**
6. **Sidebar görünsün: ✅**
7. **"Create"**
8. **Yeni oluşan dashboard'a gir → Sağ üst "···" → "Edit Dashboard"**
9. **Sağ üst "···" → "Raw configuration editor"**
10. **`enerji.yaml` dosyasının içeriğini yapıştır**
11. **"Save" → "Done"**

✅ İkinci dashboard hazır! Sol menüde **"⚡ Enerji"** görünecek.

#### 3. Üçüncü Dashboard'u Ekle (Teknik)

1. **Sol menüden "Settings" → "Dashboards"**
2. **Sağ alt köşe "+ ADD DASHBOARD"**
3. **"New dashboard from scratch" seç**
4. **Başlık: `🔧 Teknik`**
5. **Icon: `mdi:cog`**
6. **Sidebar görünsün: ✅**
7. **"Create"**
8. **Yeni oluşan dashboard'a gir → Sağ üst "···" → "Edit Dashboard"**
9. **Sağ üst "···" → "Raw configuration editor"**
10. **`teknik.yaml` dosyasının içeriğini yapıştır**
11. **"Save" → "Done"**

✅ Üçüncü dashboard hazır! Sol menüde **"🔧 Teknik"** görünecek.

---

### Yöntem 2: Dosya Yönetimi (İleri Seviye)

#### 1. Dosyaları Yükle

```bash
# SSH ile bağlan
ssh root@homeassistant.local -i ~/.ssh/homeassistant

# Dashboard klasörü oluştur
mkdir -p /config/dashboards

# Dosyaları kopyala (local'den)
scp -i ~/.ssh/homeassistant \
  dashboards/karavan_ana.yaml \
  dashboards/enerji.yaml \
  dashboards/teknik.yaml \
  root@homeassistant.local:/config/dashboards/
```

#### 2. Lovelace Konfigürasyonunu Güncelle

**`/config/configuration.yaml` dosyasına ekle:**

```yaml
lovelace:
  mode: storage  # UI üzerinden yönetim
  dashboards:
    karavan:
      mode: yaml
      title: 🚐 Karavan
      icon: mdi:camper-van
      show_in_sidebar: true
      filename: dashboards/karavan_ana.yaml
    
    enerji:
      mode: yaml
      title: ⚡ Enerji
      icon: mdi:flash
      show_in_sidebar: true
      filename: dashboards/enerji.yaml
    
    teknik:
      mode: yaml
      title: 🔧 Teknik
      icon: mdi:cog
      show_in_sidebar: true
      filename: dashboards/teknik.yaml
```

#### 3. Home Assistant'ı Restart Et

```bash
# API üzerinden
curl -X POST "http://homeassistant.local:8123/api/services/homeassistant/restart" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" -d '{}'
```

---

## 🎨 Dashboard'ları Özelleştirme

### Entity İsimlerini Değiştirme

UI üzerinden:
1. **Entity'ye tıkla → ⚙️ Settings icon → "Name" değiştir**

### Icon Değiştirme

UI üzerinden:
1. **Entity'ye tıkla → ⚙️ Settings icon → "Icon" seç**
2. **Örnek iconlar:**
   - `mdi:lightbulb` - Işık
   - `mdi:water-pump` - Pompa
   - `mdi:stove` - Ocak
   - `mdi:dishwasher` - Bulaşık makinesi

### Kart Ekleme/Çıkarma

1. **Dashboard'da "Edit" moduna geç**
2. **"+ ADD CARD"** ya da mevcut kartı **"Edit"**
3. **Kart tipini seç:**
   - `entities` - Liste halinde
   - `button` - Tek buton
   - `light` - Işık kontrolü
   - `markdown` - Metin/bilgi
   - `glance` - Özet görünüm

---

## 🔧 Troubleshooting

### Dashboard Görünmüyor

**Çözüm 1:** Sidebar'ı aç/kapa
- Sol üst hamburger menü → Dashboard listesini kontrol et

**Çözüm 2:** Cache temizle
- Tarayıcıyı yenile (Ctrl+F5 / Cmd+Shift+R)
- Gizli sekme dene

**Çözüm 3:** Restart
- Home Assistant'ı restart et

### Entity Bulunamadı Hatası

**Nedeni:** Entity ID'ler doğru değil veya entity yok.

**Çözüm:**
1. **Developer Tools → States** bölümünden entity ID'leri kontrol et
2. **Dashboard YAML'da entity ID'yi düzelt**
3. **Örnek:**
   ```yaml
   # Yanlış
   entity: light.mutfak
   
   # Doğru
   entity: light.mutfak_isik
   ```

### Kartlar Bozuk Görünüyor

**Çözüm:** YAML indentation kontrol et
- YAML'da boşluklar çok önemli!
- 2 boşluk kullan (tab değil)

---

## 📱 Mobil Görünüm

Dashboard'lar **otomatik olarak mobil uyumlu**! 

**İpucu:**
- Telefondan erişmek için: `http://homeassistant.local:8123`
- Mobil uygulama: Home Assistant iOS/Android app

---

## 🎯 İleri Seviye İpuçları

### 1. Dashboard'ları Sıralama

**Settings → Dashboards** bölümünden:
- Dashboard'ları sürükleyerek sırala
- Sidebar'da görünme sırasını değiştir

### 2. Kullanıcı Bazlı Dashboard

Her kullanıcı kendi dashboard'unu özelleştirebilir:
- Kendi profilinizde: **"Edit Dashboard" → "Take Control"**

### 3. Badge Ekleme

Dashboard üstüne badge ekle (durum göstergesi):
```yaml
badges:
  - entity: sensor.batarya_seviyesi
  - entity: sensor.su_deposu_seviyesi
```

### 4. Conditional Cards

Kartları koşula bağla:
```yaml
type: conditional
conditions:
  - entity: switch.induksiyon_ocak
    state: "on"
card:
  type: markdown
  content: "⚠️ İndüksiyon ocak AÇIK!"
```

---

## 📚 Ek Kaynaklar

- [Home Assistant Dashboard Dökümantasyonu](https://www.home-assistant.io/dashboards/)
- [Material Design Icons](https://materialdesignicons.com/)
- [Card Mod (CSS Özelleştirme)](https://github.com/thomasloven/lovelace-card-mod)

---

## ✅ Kontrol Listesi

Kurulum tamamlandı mı?

- [ ] 🚐 Karavan dashboard'u görünüyor (5 tab)
- [ ] ⚡ Enerji dashboard'u görünüyor (2 tab)
- [ ] 🔧 Teknik dashboard'u görünüyor (2 tab)
- [ ] Tüm entity'ler doğru görünüyor
- [ ] Butonlar çalışıyor
- [ ] Mobilde düzgün görünüyor

**Tamamsa hazırsın! 🎉**


