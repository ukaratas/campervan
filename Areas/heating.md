# Isıtma ve Sıcak Su Sistemi (Heating & Hot Water)

Karavanın tüm yaşam alanının kış koşullarında konforlu ve güvenli şekilde ısıtılması ve sıcak su ihtiyacı için **Truma Combi D4 inet** kullanılacaktır. Bu sistem tek cihazla hem ortam ısıtması hem de sıcak su üretimi yapar.

## 🎯 Amaç ve Kapsam

### Isıtma Sistemi
- Dış ortam sıcaklığına bakılmaksızın iç ortamı konforlu sıcaklıkta tutmak
- Donma riskine karşı otomatik koruma
- Enerji verimliliği ve güvenli çalışma

### Sıcak Su Sistemi
- Sürekli sıcak su üretimi (10L tank kapasitesi)
- Anlık sıcak su kullanımı
- Ayarlanabilir çıkış sıcaklığı (30-70°C)
- Truma inet sistemi ile akıllı kontrol ve Home Assistant entegrasyonu

## 🛠️ Ürün ve Teknik Özellikler

| Kategori | Ürün/Model | Özellikler | Fiyat Tahmini |
|----------|------------|------------|---------------|
| **Kombi Sistemi** | Truma Combi D4 inet | 4kW ısıtma, 10L sıcak su, 12V DC, dizel, internet bağlantısı | €1800-2200 |
| **Kontrol Sistemi** | Truma inet CP plus | Dijital kontrol paneli, programlanabilir, uzaktan erişim | €200-300 |
| **Hava Dağıtım** | Truma hava dağıtım kiti | İzoleli hortum, menfezler, yaşam alanı dağıtımı | €150-200 |
| **Sıcak Su Dağıtım** | Truma sıcak su kiti | Mikser vana, hortumlar, bağlantı elemanları | €150-200 |
| **Yakıt Sistemi** | Truma yakıt kiti | Yakıt pompası, filtre, dizel hat bağlantısı | €100-150 |
| **Donma Koruması** | Truma donma koruması | Otomatik boşaltma sistemi | €100-150 |

## 🔄 Sistem Kavramsal Yapısı ve Yerleşim

### Montaj Konumu
- **Ana Ünite**: Sürücü koltuğu arkasındaki çift kişilik koltuk içinde konumlandırılır
- **Kompakt Tasarım**: Tek cihazda hem ısıtma hem sıcak su üretimi
- **Kolay Erişim**: Bakım ve servis için uygun konumlandırma

### Sistem Bileşenleri
- **Hava Dağıtım Hatları**: Yaşam alanı ve sürücü kabinine yönlendirme
- **Sıcak Su Hatları**: Mutfak ve banyo sıcak su bağlantıları
- **Yakıt Hattı**: Harici dizel tank veya ana araç deposu bağlantısı
- **Elektrik Bağlantısı**: 12V DC (24V sistemden konvertör ile)

## 💧 Sıcak Su Sistem Detayları

### Sistem Çalışma Prensibi
- **Dahili Tank**: 10L kapasiteli paslanmaz çelik tank
- **Hızlı Isıtma**: 15-20 dakikada soğuktan sıcağa (60°C)
- **Sürekli Üretim**: Tank boşalırken otomatik yeniden ısıtma
- **Verimli Yakıt**: Dizel yakıt ile ekonomik çalışma

### Dağıtım Sistemi
- **Mutfak Hattı**: Evye ve bulaşık makinesi bağlantısı
- **Banyo Hattı**: Duş ve lavabo sıcak su beslemesi
- **Mikser Vana**: Güvenli çıkış sıcaklığı ayarı (termostatik)
- **Devir Hattı**: Sürekli sıcak su dolaşımı (isteğe bağlı)

### Sıcak Su Kapasitesi
- **Tank Kapasitesi**: 10L
- **Sürekli Kullanım**: ~15-20L/saat (yeniden ısıtma ile)
- **Duş Süresi**: 5-8 dakika (normal basınçta)
- **Bulaşık**: 3-5 dakika sürekli sıcak su
- **Çıkış Sıcaklığı**: 30-70°C (ayarlanabilir)

## 🌐 Truma inet Sistemi ve Home Assistant Entegrasyonu

### inet Sistemi Avantajları
- **Uzaktan Kontrol**: Telefon uygulaması ile her yerden kontrol
- **Akıllı Programlama**: Saatlik ve günlük programlama
- **Otomatik Donma Koruması**: Sistem otomatik olarak donmaya karşı koruma
- **Arıza Teşhisi**: Detaylı hata raporlama ve teşhis
- **Enerji İzleme**: Yakıt tüketimi ve çalışma süresi takibi

### Programlanabilir Modlar
- **Eco Mod**: Enerji tasarruflu çalışma (45°C)
- **Konfort Mod**: Standart kullanım (60°C)
- **Boost Mod**: Hızlı ısıtma (70°C)
- **Donma Koruması**: Güvenlik modu (40°C)

### Home Assistant Entegrasyonu
- **Truma inet API**: Resmi API üzerinden Home Assistant entegrasyonu
- **MQTT Bridge**: Truma inet verilerini Home Assistant'a aktarma
- **Otomatik Kontrolör**: Harici sensörlerle gelişmiş otomasyon

### İzleme Noktaları
- **Ortam Sıcaklığı**: İç ve dış ortam sıcaklık izleme
- **Sıcak Su Sıcaklığı**: Anlık sıcak su sıcaklığı
- **Tank Seviyesi**: Su seviyesi yüzdesi
- **Yakıt Tüketimi**: Anlık ve toplam yakıt kullanımı (ısıtma/sıcak su ayrı)
- **Çalışma Durumu**: Sistem modları ve hata durumları
- **Güç Tüketimi**: 12V DC elektrik tüketimi

## 🏠 Gelişmiş Otomasyon Senaryoları

### Akıllı Isıtma Yönetimi
```yaml
# Donma Koruması Otomasyonu
- alias: "Truma Donma Koruması"
  trigger:
    - platform: numeric_state
      entity_id: sensor.outside_temperature
      below: -2
  action:
    - service: climate.set_hvac_mode
      target:
        entity_id: climate.truma_combi
      data:
        hvac_mode: heat
    - service: climate.set_temperature
      target:
        entity_id: climate.truma_combi
      data:
        temperature: 10
```

### Sıcak Su Yönetimi
```yaml
# Sabah Sıcak Su Hazırlama
- alias: "Sabah Sıcak Su Hazırlama"
  trigger:
    - platform: time
      at: "06:30:00"
  condition:
    - condition: state
      entity_id: device_tracker.phone_location
      state: "home"  # Karavanda mıyız?
  action:
    - service: water_heater.turn_on
      target:
        entity_id: water_heater.truma_hotwater
    - service: water_heater.set_temperature
      target:
        entity_id: water_heater.truma_hotwater
      data:
        temperature: 60
```

### Enerji Optimizasyonu
```yaml
# Batarya Seviyesine Göre Sıcak Su
- alias: "Enerji Optimizasyonu Sıcak Su"
  trigger:
    - platform: numeric_state
      entity_id: sensor.battery_soc
      below: 30
  action:
    - service: water_heater.set_temperature
      target:
        entity_id: water_heater.truma_hotwater
      data:
        temperature: 45  # Düşük sıcaklıkta tasarruf
    - service: notify.mobile_app
      data:
        message: "Düşük batarya - sıcak su tasarruf modunda"
```

### Otomasyon Senaryoları
- **Donma Koruması**: Dış sıcaklık -2°C altına inerse otomatik başlat
- **Zamanlayıcı**: Belirli saatlerde otomatik ısıtma ve sıcak su hazırlama
- **Uzaktan Kontrol**: Mobil arayüzden aç/kapat, sıcaklık ayarı
- **Enerji Optimizasyonu**: Batarya seviyesine göre çalışma modları
- **Arıza/Bakım Uyarısı**: Hata durumunda otomatik bildirim

## 🌟 Kullanım Senaryoları

### Günlük Kullanım
- **Sabah**: Otomatik ısıtma ve hazır sıcak su
- **Akşam**: Duş için yeterli sıcak su kapasitesi
- **Bulaşık**: Yüksek sıcaklıkta etkili temizlik
- **Gece**: Düşük sıcaklıkta hazır tutma

### Mevsimsel Kullanım
- **Yaz**: Eco mod ile tasarruflu çalışma
- **Kış**: Donma koruması ile güvenli çalışma
- **Geçiş**: Otomatik sıcaklık ayarları
- **Tatil**: Uzun süre kapalı kalma koruması

### Özel Kullanım Modları
- **Duş Hazırlık**: Duş öncesi otomatik ısıtma
- **Bulaşık Modu**: Yüksek sıcaklıkta su hazırlama
- **Gece Modu**: Düşük sıcaklıkta hazır tutma
- **Tatil Modu**: Uzun süre kapalı kalma koruması

## 📈 Sistem Performansı

### Isıtma Performansı
- **Isıtma Gücü**: 4kW (yaklaşık 70m³ hacim)
- **Yakıt Tüketimi**: 0.4-0.5 L/saat (ortalama ısıtma)
- **Elektrik Tüketimi**: 12V DC, 2-8A (çalışma moduna göre)
- **Gürültü Seviyesi**: <40dB (çok sessiz)

### Sıcak Su Performansı
- **Tank Kapasitesi**: 10L
- **Isıtma Süresi**: 15-20 dakika (soğuktan 60°C'ye)
- **Yakıt Tüketimi**: 0.3-0.5 L/saat (sadece sıcak su modu)
- **Elektrik Tüketimi**: 12V DC, 2-4A (sıcak su modu)
- **Bekletme**: Minimal yakıt tüketimi

### Enerji Verimliliği
- **Kombine Çalışma**: Hem ısıtma hem sıcak su beraber çalışırken optimize edilmiş yakıt kullanımı
- **Sürekli Kullanım**: ~15-20L/saat sıcak su (yeniden ısıtma ile)
- **Bekleme Modu**: Minimal enerji tüketimi

## 🔧 Kurulum ve Bakım

### Kurulum Aşamaları
1. **Ana Ünite Montajı**: Truma Combi D4 inet'in koltuk içine montajı
2. **Hava Dağıtım Sistemi**: İzoleli hortum ve menfezlerle yaşam alanına dağıtım
3. **Sıcak Su Sistemi**: Mikser vana ve hortumlarla banyo/mutfak bağlantısı
4. **Yakıt Sistemi**: Dizel tank ve pompa bağlantısı
5. **Elektrik Bağlantısı**: 12V DC besleme (24V'dan konvertör ile)
6. **inet Konfigürasyonu**: Wifi bağlantısı ve uygulama kurulumu
7. **Home Assistant Entegrasyonu**: API ve MQTT bridge kurulumu

### Bakım Planı
- **Aylık**: Hava filtresi kontrolü ve temizlik, su kalitesi kontrolü
- **Mevsimlik**: Yanma odası ve egzoz hattı kontrol, mikser vana kalibrasyonu
- **Yıllık**: Yakıt sistemi ve elektrik bağlantıları gözden geçirme, tank temizliği
- **Kış Öncesi**: Donma koruması ve otomasyon sistemleri test

## 💡 Sistem Avantajları

### Tek Cihaz Çözümü
- **Kompakt**: Hem ısıtma hem sıcak su tek ünitede
- **Güvenilir**: Truma'nın kanıtlanmış teknolojisi
- **Bakım**: Tek sistem, daha az bakım noktası
- **Maliyet**: Ayrı sistemlerden daha ekonomik

### Akıllı Kontrol
- **Uzaktan Erişim**: Her yerden kontrol imkanı
- **Programlanabilir**: Otomatik çalışma programları
- **Enerji Verimli**: Optimal yakıt ve elektrik kullanımı
- **Güvenli**: Otomatik güvenlik sistemleri

### Home Assistant Entegrasyonu
- **Tam Entegrasyon**: Tüm karavan otomasyonu ile uyumlu
- **Sensör Desteği**: Harici sensörlerle gelişmiş kontrol
- **Veri Analizi**: Tüketim ve performans analizi
- **Bildirimler**: Arıza ve bakım bildirimleri

## ⚡ Elektrik ve Su Tesisatı

### Elektrik Sistemi
- **Ana Besleme**: 12V DC (24V sistemden konvertör ile)
- **Güç Tüketimi**: 2-8A (çalışma moduna göre)
- **Koruma**: Sigorta ve aşırı akım koruması
- **Kontrol**: inet sistemi wifi bağlantısı

### Su Tesisatı
- **Temiz Su**: Ana su tankından besleme
- **Sıcak Su**: Banyo ve mutfak dağıtımı
- **Mikser Vana**: Çıkış sıcaklığı kontrolü (termostatik)
- **Donma Koruması**: Otomatik boşaltma sistemi

### Yakıt Sistemi
- **Dizel**: Harici tank veya ana araç deposu
- **Yakıt Pompası**: Otomatik yakıt beslemesi
- **Filtre**: Yakıt filtreleme sistemi
- **Güvenlik**: Yakıt kesme valfi

---

*Bu sistem, modern karavan standardında hem ısıtma hem de sıcak su ihtiyacını tek cihazla karşılayan, akıllı kontrol ve tam otomasyon özellikli çözüm sunar.*