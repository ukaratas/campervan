# Isıtma Sistemi (Heating)

Karavanın tüm yaşam alanının kış koşullarında konforlu ve güvenli şekilde ısıtılması için Eberspacher D4L 4kW 24V dizel hava ısıtıcısı kullanılacaktır.

## 🎯 Amaç ve Kapsam
- Dış ortam sıcaklığına bakılmaksızın iç ortamı konforlu sıcaklıkta tutmak
- Donma riskine karşı otomatik koruma
- Enerji verimliliği ve güvenli çalışma
- Home Assistant ile merkezi izleme ve otomasyon

## 🛠️ Ürün ve Teknik Özellikler

| Kategori | Ürün/Model | Özellikler |
|----------|------------|------------|
| **Hava Isıtıcı** | Eberspacher D4L | 4kW, 24V DC, dizel, otomatik mod, sessiz çalışma |
| **Kontrol Paneli** | Eberspacher EasyStart Pro | Dijital, programlanabilir, sıcaklık sensörlü |
| **Hava Dağıtım** | İzoleli spiral hortum, menfezler | Yaşam alanı ve sürücü kabinine dağıtım |

## 🔄 Sistem Kavramsal Yapısı ve Yerleşim
- Isıtıcı, sürücü koltuğu arkasındaki çift kişilik koltuk içinde konumlandırılır (boyler ile yan yana)
- Hava giriş ve çıkışları, yaşam alanı ve sürücü kabinine yönlendirilir
- Yakıt hattı, harici dizel tankından veya aracın ana deposundan alınır
- Elektrik bağlantısı 24V DC ana sistemden sağlanır

## 🏠 Otomasyon ve Home Assistant Entegrasyonu
- Dış sıcaklık sensörü ile otomatik başlatma (ör: dış sıcaklık -2°C altına inerse çalış, iç sıcaklık 10°C'ye ulaşınca dur)
- Manuel ve zamanlayıcı kontrollü çalışma
- Home Assistant üzerinden uzaktan izleme ve kontrol (modül veya röle ile entegrasyon)
- Donma koruması: Don riski durumunda otomatik devreye girme

### Tipik Otomasyon Senaryoları
- **Donma Koruması:** Dış sıcaklık -2°C altına inerse otomatik başlat, iç sıcaklık 10°C'ye ulaşınca kapat
- **Zamanlayıcı:** Belirli saatlerde otomatik ısıtma
- **Uzaktan Kontrol:** Mobil arayüzden aç/kapat
- **Arıza/Bakım Uyarısı:** Hata durumunda bildirim

## 🔧 Kurulum ve Bakım
1. **Isıtıcı Montajı:** Sürücü koltuğu arkasındaki koltuk içine sabitlenir
2. **Hava Dağıtım Hattı:** İzoleli hortum ve menfezlerle yaşam alanına dağıtım
3. **Yakıt ve Elektrik Bağlantısı:** Güvenli ve sızdırmaz şekilde yapılır
4. **Kontrol Paneli ve Sensörler:** Kolay erişilebilir yere monte edilir
5. **Home Assistant Entegrasyonu:** Röle/modül ile bağlantı ve otomasyon tanımları

### Bakım Planı
- **Sezonluk:** Yanma odası ve hava filtresi kontrolü
- **Yıllık:** Yakıt hattı ve elektrik bağlantılarının gözden geçirilmesi
- **Kış Öncesi:** Otomasyon ve sensörlerin test edilmesi

## 💡 Ek Görüşler ve Öneriler
- Isıtıcı ve boyler aynı bölmede yerleştirildiğinde, bakım ve erişim kolaylığı sağlanmalı
- Hava çıkış menfezleri, yaşam alanında homojen ısı dağılımı için iyi planlanmalı
- Dış hava sensörü ve iç ortam sensörü ile otomasyon hassasiyeti artırılabilir
- Yedek sigorta ve acil kapatma anahtarı önerilir

## ⚡ Elektrik ve Su Tesisatı

- **Enerji:** 24V DC ana hat (ısıtıcı ve kontrol paneli)
- **Otomasyon:** Röle/modül ile Home Assistant entegrasyonu, sıcaklık sensörleri
- **Yakıt:** Dizel hattı (harici tank veya ana depo)
- **Su:** Doğrudan bağlantı yok, ancak ısıtıcı bölmesinde nem ve yangın sensörü önerilir

---

*Bu sistem, karavanın kış koşullarında konforlu, güvenli ve otomasyona uygun şekilde ısıtılmasını sağlar.*