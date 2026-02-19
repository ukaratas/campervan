# Ana Yatak Alanı (Main Bed)

Karavanın arka bölümünde yer alan ana yatak alanı. Araç boyunca 150cm alan kaplar. 150x200cm King size yatak, Flarespace modifikasyonu ile genişletilmiş iç alanda enine yerleştirilmiştir.

## 🛏️ Ana Yatak Özellikleri

- **Konum:** Araç arkasında, giriş kapısı yanında
- **Alan:** 150cm (araç uzunluğu boyunca)
- **Yatak Boyutu:** 150x200cm 
- **Yerleştirme:** Enine (150cm araç uzunluğu boyunca, 200cm araç genişliği boyunca)
- **Flarespace:** İç genişlik 200-205cm'ye çıkarıldı (200cm yatak enine sığar)
- **Malzeme:** Yüksek kaliteli yatak minderi ve özel çarşaf seti
- **Depolama:** Yatak altında teknik ekipmanlar (batarya, otomasyon)

## ❄️ 220V Klima Sistemi

### Klima Özellikleri
- **Model:** Evacool Eva RV 2700 Premium Klima
- **Soğutma Kapasitesi:** ~2700W
- **Voltaj:** 220V AC
- **Tüketim:** ~900-1100W (~4-5A @220V)
- **Kontrol:** Finder 22.22.9.024.4000 kontaktör + Waveshare DI/DO ile Home Assistant üzerinden aç/kapa
- **Ağırlık:** ~28-31kg

### Montaj Konumu
- **Konum:** Ana yatak üstüne konumlanacak şekilde, araç tavanında, popup tavanın bittiği noktada konumlanacak
- **Tavan Montajı:** Araç tavanına güçlü montaj
- **Havalandırma:** Ana yatak alanına doğrudan soğutma
- **Erişim:** Bakım için kolay erişim imkanı

### Teknik Avantajlar
- **220V AC:** Shore power veya inverter (3000W) ile çalışır
- **Sessiz Çalışma:** Inverter compressor teknolojisi
- **Enerji Verimliliği:** Eco mod ile uzun çalışma süresi, ~1000W tüketim inverter kapasitesinin 1/3'ü
- **Sıcak/Soğuk:** Hem soğutma hem ısıtma fonksiyonu
- **Otomatik Kontrol:** Dijital kontrol paneli ile sıcaklık kontrolü
- **Uzaktan Kontrol:** Kumanda ve Home Assistant entegrasyonu (Finder kontaktör ile aç/kapa)

## 🌟 Heki Roof Window - Yıldız İzleme

### Heki Özellikleri
- **Model:** Dometic Midi Heki Style
- **Boyut:** 50x70cm (büyük boyut)
- **Özellik:** Havalandırma + şeffaf cam
- **Kontrol:** Manuel açma/kapama kolu
- **Perde:** Entegre perde ve sineklik

### Konfor Avantajları
- **Doğal Işık:** Gündüz doğal aydınlatma
- **Panoramik Görüş:** Gece gökyüzü manzarası
- **Taze Hava:** Doğal havalandırma
- **Acil Çıkış:** Acil durum çıkış imkanı (büyük boyut)

## 🔧 Flarespace Modifikasyonu

- **Ürün:** [Flarespace Fiat Ducato Van Flares](https://flarespace.com/products/fiat-ducato-campervan-windows)
- **Malzeme:** Dayanıklı fiberglass yapı
- **Montaj:** Araç yan duvarlarına sabit montaj
- **Genişlik Artışı:** 185cm'den 200-205cm'ye (15-20cm kazanç)
- **Sabit Çıkıntılar:** Hem baş hem ayak tarafında
- **Pencere Durumu:** Her iki extension da pencere olmayan model
- **Yük Kapasitesi:** Güvenli ve test edilmiş yapı
- **Estetik:** Araç tasarımı ile uyumlu görünüm

## Arka Kapı Üstü Pencereler
- **Konum:** Her iki arka kapının üstüne simetrik yerleştirme
- **Boyut:** 30x50cm (her biri)
- **Sayı:** 2 adet (sağ ve sol kapı üstü)
- **Tip:** Açılabilir pencere (havalandırma için)
- **Malzeme:** Çift cam, su sızdırmaz çerçeve
- **Doğal Havalandırma:** Çapraz hava akışı (heki ile birlikte)
- **Geri Görüş:** Araç arkasını izleme imkanı
- **Doğal Işık:** Yatak alanına ek doğal aydınlatma


## 🏠 Otomasyon ve Home Assistant Entegrasyonu

### Aydınlatma Sistemi
- **Genel Yatak Aydınlatması:** Tavan LED'leri, Shelly Plus RGBW PM ile dimmer ve renk ayarlanabilir
- **Okuma Lambası Sol (Mutfak Tarafı):** Yatak başı sol taraf, bağımsız kontrol
- **Okuma Lambası Sağ (Banyo Tarafı):** Yatak başı sağ taraf, bağımsız kontrol
- **Gece Zemin Aydınlatması:** Karanlıkta adım görme, zemin seviyesinde düşük yoğunluklu LED

### Aydınlatma Kontrolleri
- **Yatak Başı Sol:** Genel aydınlatma push button + sol okuma lambası push button
- **Yatak Başı Sağ:** Genel aydınlatma push button + sağ okuma lambası push button
- **Dimmer Kontrol:** Her iki tarafta da Shelly Plus RGBW PM ile genel aydınlatma dimmer ve renk kontrolü
- **Home Assistant:** Tüm aydınlatma otomatik kontrol

### Konfor Kontrolleri
- **Klima Kontrolü:** Evacool Eva RV 2700 Premium, 220V AC, Finder kontaktör ile Home Assistant üzerinden aç/kapa
- **Heki Havalandırma:** Heki açma/kapama durumu izleme
- **Perde Sistemi:** Otomatik veya manuel perde kontrolü
- **Güvenlik:** Hareket sensörü ve gece güvenlik sistemi

### Otomasyon Senaryoları
- **Uyku Modu:** Klima sessiz moda, ışıkları kapat, güvenlik modunu etkinleştir
- **Uyanma Modu:** Kademeli aydınlatma artışı, klima optimal sıcaklığa ayarla
- **Okuma Modu:** Optimum aydınlatma seviyesi, klima sessiz mod
- **Yıldız İzleme Modu:** Tüm ışıkları kapat, heki açık bırak
- **Güvenlik Modu:** Hareket algılandığında otomatik aydınlatma


### Aydınlatma ve Priz Kurulumu
1. **Yatak Başı Sol (Mutfak Tarafı):** 220V priz, 2x otomotiv USB-C soket, push buttonlar, okuma lambası
2. **Yatak Başı Sağ (Banyo Tarafı):** 220V priz, 2x otomotiv USB-C soket, push buttonlar, okuma lambası
3. **Yatak Ayak Ucu:** 220V+24V priz
4. **Kablo Yönetimi:** Gizli kablo kanalları, düzenli bağlantılar

## 💡 Ek Özellikler ve Öneriler

### Depolama Çözümleri
- **Yatak Altı Çekmeceler:** Kıyafet ve kişisel eşya için
- **Yatak Başı Raflar:** Kitap, telefon, gözlük için
- **Gizli Bölmeler:** Değerli eşya depolamesi
- **Teknik Ekipman Alanı:** Batarya, BMS, otomasyon paneli

### Konfor Aksesuarları
- **Özel Çarşaf:** 150x200cm enine yerleştirme için
- **Yorgan Sistemi:** Kompakt ve sıcak tutan
- **Yastık Seçenekleri:** Farklı sertlikte yastıklar
- **Perde Sistemi:** Mahremiyet ve ışık kontrolü

### Güvenlik ve Pratiklik
- **Acil Çıkış:** Yatak alanından kolay çıkış imkanı (heki ve arka pencereler)
- **Havalandırma:** Çapraz hava akışı (heki + arka pencereler)
- **Geri Görüş:** Arka pencerelerden araç arkasını izleme
- **Ses İzolasyonu:** Konforlu uyku için gürültü azaltma
- **Kolay Temizlik:** Yatak çarşafı ve alanın kolay temizliği
- **Güvenlik:** Çok noktalı acil çıkış imkanı

## ⚡ Elektrik ve Su Tesisatı

- **220V Klima:** Evacool Eva RV 2700 Premium, 220V AC, ~900-1100W, Finder kontaktör ile kontrol
- **Aydınlatma:** 24V LED spot ve şerit aydınlatma sistemi

### Yatak Başı Elektrik (Mutfak Tarafı - Sol)
- **Prizler:** 1x 220V
- **USB Şarj:** 2x otomotiv USB-C soket (24V giriş, 100W PD, ayrı hat)
- **Push Buttonlar:** Genel yatak aydınlatması, sol okuma lambası, Shelly Plus RGBW PM dimmer
- **Okuma Lambası:** 24V LED okuma lambası (sol taraf)

### Yatak Başı Elektrik (Banyo Tarafı - Sağ)
- **Prizler:** 1x 220V
- **USB Şarj:** 2x otomotiv USB-C soket (24V giriş, 100W PD, ayrı hat)
- **Push Buttonlar:** Genel yatak aydınlatması, sağ okuma lambası, Shelly Plus RGBW PM dimmer
- **Okuma Lambası:** 24V LED okuma lambası (sağ taraf)

### Yatak Ayak Ucu Elektrik (Banyo Tarafı)
- **Prizler:** 1x 220V, 1x 24V (aksesuarlar)

### Otomasyon ve Kontrol
- **Home Assistant:** Tüm aydınlatma, perde, fan, klima (220V kontaktör) kontrolü
- **Güvenlik:** Hareket sensörü, gece zemin aydınlatması
- **Kablo Yönetimi:** Düzenli kablo kanalları ve gizleme
- **Su:** Doğrudan su bağlantısı yok

---

*Bu sistem, Flarespace modifikasyonu sayesinde dar karavan alanında King size yatak konforu sunar, 220V klima ile soğutma/ısıtma ve büyük heki ile yıldız izleme imkanı sağlar.* 