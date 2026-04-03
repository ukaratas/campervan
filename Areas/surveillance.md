# Güvenlik ve İzleme Sistemi (Surveillance)

Aracın dört yönünden sürekli görüntü kaydı ve canlı izleme. Park halinde, seyir halinde ve kamp konumunda güvenlik sağlar.

## 📹 Sistem Mimarisi

```
4x Analog TVI Kamera ──(aviation kablo)──► HK Vision DS-M5504HM ──(Ethernet)──► Network Switch ──► IPCBOX-CM5-A (HA)
```

- Kameralar analog TVI (720p) — DVR'ın native formatı, maliyet ve sadelik avantajı
- DVR, kamera beslemesini aviation konnektör üzerinden sağlar (12V)
- DVR, Network Switch üzerinden Ethernet ile IPCBOX-CM5-A'ya bağlı
- Home Assistant üzerinden canlı görüntü ve kayıt erişimi

## 🎥 Donanım

### Mobile DVR

| Özellik | Detay |
|---------|-------|
| **Model** | Hikvision DS-M5504HM-T |
| **Kanal** | 4 (analog TVI native) |
| **Çözünürlük** | 720p (ana akış), WD1/4CIF (alt akış) |
| **Sıkıştırma** | H.264 / H.264+ |
| **Depolama** | 1x 2.5" HDD/SSD (2TB'a kadar) + 1x SD kart (256GB'a kadar) |
| **Ses** | 4 kanal ses kaydı, 1 kanal çift yönlü ses |
| **Bağlantı** | 1x RJ45 10/100M Ethernet, opsiyonel 3G/4G + Wi-Fi + GPS |
| **Kamera Giriş** | 4x aviation konnektör (4-pin, video + güç + ses) |
| **Besleme** | 9-32V DC (24V sistemle doğrudan uyumlu) |
| **Boyut** | 206 × 219 × 60 mm |
| **Ağırlık** | 1.6 kg |
| **Konum** | Teknik alan (yatak altı) |

### Kameralar (4 adet, analog TVI)

| # | Konum | Montaj Yeri | Görüş Açısı | Notlar |
|---|-------|-------------|-------------|--------|
| 1 | Ön | Kabin ön üst / ön tampon ortası | İleri yön | Seyir kaydı + park güvenliği |
| 2 | Arka | Arka kapı üst ortası | Geri yön | Geri manevra + park güvenliği |
| 3 | Sol | Sol ayna altı | Sol yön | Kör nokta + giriş kapısı izleme |
| 4 | Sağ | Sağ ayna altı | Sağ yön | Kör nokta + park güvenliği |

- **Tip:** TVI 720p, IR gece görüş, 4-pin aviation konnektör
- **Lens:** Geniş açı ≥150° (fisheye tercih) — 360° stitching için overlap bölgeleri gerekli
- **Koruma:** IP67, araç tipi vibrasyon dayanıklı
- **Besleme:** DVR aviation kablo üzerinden 12V (PoE gerekmez)

> Yan kameralar ayna altı montaj — aracın en geniş noktası olduğu için maksimum görüş açısı ve minimum kör nokta sağlar. Surround view sistemlerinin endüstri standardı pozisyonudur.

### Neden Analog TVI?

- **Maliyet**: TVI kamera ~$15-30, IP kamera ~$50-100+ (kamera + DVR tarafı toplam %50-70 tasarruf)
- **DVR uyumu**: DS-M5504HM-T native olarak TVI DVR, analog en stabil çalışma modu
- **Sadelik**: ağ konfigürasyonu yok, PoE switch gerekmez, tak-çalıştır
- **Aviation konnektör**: araç vibrasyon ve sıcaklık koşullarına dayanıklı, BNC'den sağlam
- **720p yeterli**: araç güvenliği için fazlasıyla yeterli çözünürlük

## ⚡ Elektrik ve Bağlantı

| Bileşen | Besleme | Bağlantı |
|---------|---------|----------|
| DVR | 24V DC (24V Startup rail veya doğrudan batarya) | Ethernet → Network Switch |
| Kameralar | 12V (DVR aviation kablo üzerinden) | Aviation kablo → DVR |

### Güç Yönetimi

- DVR 9-32V DC giriş — 24V sistemden doğrudan beslenebilir
- Kameralar DVR üzerinden 12V ile beslenir (ayrı güç hattı gerekmez)
- Park modunda DVR sürekli çalışabilir (düşük güç tüketimi, ~10-15W)
- HA otomasyonu ile "park modu" / "seyir modu" / "kapalı" senaryoları tetiklenebilir
- Batarya SOC düşükse HA otomasyonu DVR'ı kapatabilir (enerji tasarrufu)

## 🔄 360° Surround View

4 geniş açılı (≥150° / fisheye) kameranın görüntüleri HA tarafında birleştirilerek kuşbakışı (bird's-eye-view) harita oluşturulur.

### Çalışma Prensibi

1. DVR'dan 4 kamera RTSP stream'i alınır
2. OpenCV perspektif dönüşüm (homography) ile her kamera görüntüsü top-down düzleme yansıtılır
3. Overlap bölgelerinde blending uygulanarak tek bir kuşbakışı görüntü üretilir
4. HA dashboard'da gerçek zamanlı surround view gösterilir

### Kalibrasyon

- İlk kurulumda araç etrafına kalibrasyon deseni yerleştirilir
- Her kameranın lens distorsiyonu ve perspektif matrisi hesaplanır
- Kalibrasyon bir kez yapılır, parametreler kaydedilir

### Kullanım Senaryoları

- **Park manevraları**: kuşbakışı görüntü ile engel tespiti
- **Dar yol geçişi**: araç genişliğinin etrafındaki mesafe kontrolü
- **Kamp park**: çadır, masa vb. çevre düzenini izleme

## 🏠 Home Assistant Entegrasyonu

### İzleme

- 4 kameranın bireysel canlı görüntüsü + 360° surround view HA dashboard'da
- DVR Ethernet üzerinden RTSP/HTTP stream sağlar → HA kamera entegrasyonu
- Surround view işleme IPCBOX-CM5-A üzerinde çalışır (OpenCV + Python)
- Kayıt durumu, disk doluluk, kamera bağlantı sağlığı izleme
- Hareket algılama bildirimleri (DVR tarafında)

### Otomasyon Senaryoları

| Senaryo | Tetik | Aksiyon |
|---------|-------|---------|
| Park modu | Motor stop + el freni | DVR sürekli kayıt, hareket algılama aktif |
| Seyir modu | Motor çalışıyor | DVR sürekli kayıt, geri kamera ayna ekranına yönlendirme |
| Gece bekçi | Gece saatleri + park | Hareket algılamada bildirim gönder |
| Enerji tasarrufu | SOC < %20 | DVR kapat, batarya koru |
| Kamp modu | Camper ON + park | 4 yön canlı izleme, sürekli kayıt |

## 🔧 Kablo Güzergahları

| Kamera | Kablo güzergahı |
|--------|----------------|
| Ön | Teknik alan → tavan içi → kabin ön üst |
| Arka | Teknik alan → arka kapı üst çerçeve |
| Sol | Teknik alan → tavan içi → A sütunu → sol ayna altı |
| Sağ | Teknik alan → tavan içi → A sütunu → sağ ayna altı |

> Tüm kameralar aviation kablo (4-pin) ile DVR'a doğrudan bağlanır. Ayna altı kablolar A sütunu içinden geçirilir. Kablo döşeme 5.2 kapsamında yapılır.

## 📦 BOM

| Ürün | Model | Adet | Fiyat | Önden |
|------|-------|------|-------|-------|
| Mobile DVR | Hikvision DS-M5504HM-T | 1 | TBD | E |
| Analog TVI Kamera | Araç tipi, 720p, IR, IP67, aviation konnektör | 4 | TBD | E |
| HDD/SSD | 2.5" 1TB (DVR depolama) | 1 | TBD | E |
| Aviation Kablo | 4-pin, araç tipi shielded (kamera-DVR arası) | 4x ~8m | TBD | E |
| Kamera montaj braketi | Araç tipi vibrasyon dayanıklı | 4 | TBD | E |
