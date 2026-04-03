# Oturma ve Yatak Alanı (Seating & Bed Area)

Mutfağın karşısında konumlandırılan çok fonksiyonlu oturma, uyku ve çalışma alanı. Gündüz koltuk, gece tek kişilik yatak, iki adet Lagun masa ile yemek ve çalışma alanı sağlar.

## 🛋️ Koltuk / Yatak Sistemi

### Kanepe-Yatak Özellikleri
- **Boyut:** 200 x 70 cm
- **Konum:** Ön yaşam alanı (mutfak karşısı)
- **Gündüz Modu:** Oturma koltuğu (sırt minderleri takılı)
- **Gece Modu:** Tek kişilik sabit yatak (sırt minderleri kaldırılır, 70x200cm düz yatış)
- **Malzeme:** Dayanıklı ve konforlu kumaş/deri
- **Koltuk Altı:** Evacool D31 R çekmeceli buzdolabı + depolama alanı

### Çalışma Sırtlıkları (Ofis Modu)
Kanepe sırt derinliği (~70cm) oturarak çalışmak için fazla olduğundan, ofis modunda oturma derinliğini ~45cm'e düşüren ek çalışma sırtlıkları kullanılır.
- **Adet:** 2
- **Malzeme:** Sert, bel destekli (çalışma koltuğu hissini simüle eder)
- **Yerleşim:** Normal sırt minderlerinin önüne konur, minderlere dayanır
- **Amaç:** Ergonomik oturma derinliği (~45cm) sağlayarak uzun süreli bilgisayar çalışmasını konforlu kılar

## 📋 Masa Sistemi

### Lagun Masa Özellikleri
- **Adet:** 2
- **Tip:** Lagun 360° döner, sökülebilir masa
- **Boyut:** 40 x 80 cm (her biri)
- **Montaj:** Kanepe karkasına monte
- **Hareket:** 360° serbest dönüş
- **Söküm:** Kolay sökülebilir (seyahat veya yatak modu için)

### Kullanım Konfigürasyonları
- **Yemek Modu:** İki masa açık, kanepede oturma
- **Ofis Modu:** Çalışma sırtlıkları takılı + Lagun masa = ergonomik çalışma ortamı
- **Yatak Modu:** Masalar sökülür, sırt minderleri kaldırılır
- **Seyahat Modu:** Masalar sabitlenmiş veya sökülmüş

## ⚡ Elektrik Altyapısı

### Priz Konfigürasyonu ve Yerleşimi
Prizler kanepe karkasının altında (oturma yeri altı), sağlı sollu simetrik yerleşim:

- **Sol taraf:** 1x 220V AC + 1x otomotiv USB-C soket (24V giriş, 100W PD)
- **Sağ taraf:** 1x 220V AC + 1x otomotiv USB-C soket (24V giriş, 100W PD)
- **Toplam:** 2x 220V AC, 2x USB-C

### Aydınlatma Sistemi
- **Oturma Aydınlatması:** Waveshare relay (Modbus) ile kontrol, push button ile tetikleme
- **Ambient Aydınlatma:** Shelly Plus RGBW PM ile dimmer ve renk ayarı (Wi-Fi üzerinden Home Assistant entegrasyonu)

## 🏠 Otomasyon ve Home Assistant Entegrasyonu

### Akıllı Kontroller
- **Aydınlatma:** Çalışma/sosyal mod otomatik geçiş
- **Priz Kontrolü:** Uzaktan açma/kapama
- **Sıcaklık:** Çalışma alanı için optimal ısı

### Otomasyon Senaryoları
- **Ofis Modu:** Aydınlatma + çalışma pozisyonu
- **Dinlenme Modu:** Ambient aydınlatma
- **Yatak Modu:** Tüm ışıklar kısılır, gece modu
- **Gece Modu:** Minimum aydınlatma + güç tasarrufu

### Sensörler ve İzleme
- **Hareket Sensörü:** Otomatik aydınlatma
- **Sıcaklık Sensörü:** Çalışma alanı konforu
- **Işık Sensörü:** Aydınlatma otomatik ayarı

## 🔧 Kurulum ve Montaj

### Kanepe Sistemi Kurulumu
1. **Zemin Hazırlığı:** Kanepe montaj noktaları güçlendirme
2. **Kanepe Karkası:** 200x70 kanepe yapısı ve yatak tabanı
3. **Lagun Montajı:** 2x masa ayağı kanepe karkasına sabitleme
4. **Buzdolabı Yuvası:** Kanepe altı Evacool D31 R boşluğu
5. **Test:** İşlevsellik testleri (dönüş, söküm, yatak dönüşümü)

### Teknoloji Kurulumu
1. **Elektrik Altyapısı:** Priz ve kablo altyapısı
2. **Kablo Yönetimi:** Düzenli kablo geçişleri
3. **Aydınlatma:** Oturma alanı aydınlatma sistemi

## 💡 Ek Özellikler ve Öneriler

### Konfor Geliştirmeleri
- **Yatak Minderi:** 70x200cm, sırt minderleri kaldırıldığında düz yüzey
- **Çalışma Sırtlıkları:** 2 adet sert, bel destekli (oturma derinliği 45cm)
- **Klima:** Çalışma alanı için optimal sıcaklık

### Depolama Çözümleri
- **Kanepe Altı:** Evacool D31 R çekmeceli buzdolabı + ek depolama
- **Duvar Rafları:** Kitap, dokümanlar

### Güvenlik Önlemleri
- **Masa Sabitleme:** Hareket sırasında güvenli (Lagun kilit mekanizması)
- **Elektrik Güvenliği:** Kaçak akım koruması
- **Acil Çıkış:** Kolay erişim imkanı

## 🌟 Kullanım Senaryoları

### Ofis Modu
- **Çalışma sırtlıkları** takılır → oturma derinliği ~45cm'e düşer
- **Lagun masa** çalışma pozisyonuna döner
- **Aydınlatma çalışma moduna** geçer
- **Ergonomik ofis ortamı** hazır

### Sosyal Mod
- **Kanepe** oturma pozisyonunda, sırt minderleri takılı
- **İki masa** açık (yemek / sohbet)
- **Ambient aydınlatma** aktif

### Yatak Modu
- **Masalar sökülür** veya katlanır
- **Sırt minderleri kaldırılır** → 70x200cm düz yüzey
- **Yatak minderi** serilir → tek kişilik uyku

### Seyahat Modu
- **Masalar sabitlenmiş** veya sökülmüş
- **Tüm gevşek eşyalar** sabitlenmiş

## ⚡ Elektrik ve Su Tesisatı

- **220V AC:** 2x priz — kanepe karkası altı (1x sol, 1x sağ)
- **USB Şarj:** 2x otomotiv USB-C soket (24V giriş, 100W PD) — kanepe karkası altı (1x sol, 1x sağ)
- **Aydınlatma:** 24V LED oturma aydınlatma sistemi
- **Otomasyon:** Tüm sistemler Home Assistant entegrasyonlu
- **Su:** Doğrudan su bağlantısı yok

---

*Bu sistem, gündüz oturma ve çalışma, gece tek kişilik yatak olarak kullanılabilen çok fonksiyonlu bir çözümdür. Lagun masalar sökülebilir, kanepe altında çekmeceli buzdolabı yer alır.*
