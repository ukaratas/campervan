# Otomasyon ve Kontrol Altyapısı

Karavanın tüm sistemlerinin merkezi ve akıllı şekilde izlenmesi, kontrolü ve otomasyonu için Home Assistant tabanlı bir altyapı kurulmuştur. Tüm cihazlar, sensörler ve aktüatörler mümkün olduğunca kablolu (RS485/Modbus) olarak entegre edilir.

## 🎯 Amaç ve Kapsam

- Tüm elektrikli cihazların, sensörlerin ve valflerin merkezi olarak izlenmesi ve kontrolü
- Enerji optimizasyonu, güvenlik, konfor ve bakım kolaylığı
- Uzaktan izleme, bildirim ve otomasyon senaryoları

## 🛠️ Kullanılan Donanımlar

| Kategori | Ürün/Modül | Özellikler |
|----------|------------|------------|
| **Ana Kontrolcü** | Raspberry Pi CM4 + Waveshare Industrial IoT Modül | UPS, M.2 slot, endüstriyel I/O, RS485, genişletilebilir |
| **Röle Modülleri** | Modbus RTU 8-ch Latching Relay (C) | RS485, uzun süre açık kalacak cihazlar için |
| | Modbus RTU 4-ch 30A High Current Relay | RS485, yüksek akım (pompa, motor vb.) için, LED göstergeli |
| **Analog Giriş** | Industrial 8-Ch Analog Acquisition Module | 12-bit hassasiyet, voltaj/akım okuma, RS485 |

## 🏠 Home Assistant Entegrasyonu

- Tüm modüller Home Assistant'a Modbus/RS485 ile entegre edilir
- Cihaz ve sensör durumları, enerji tüketimi, su seviyesi, sıcaklık vb. merkezi olarak izlenir
- Otomasyonlar YAML veya görsel arayüz ile tanımlanır

### Tipik Otomasyon Senaryoları
- **Enerji Yönetimi:** Yüksek akım çeken cihazların (pompa, ısıtıcı vb.) otomatik aç/kapatılması
- **Donma Koruması:** Sıcaklık sensörüne göre valf/pompa otomasyonu
- **Su Yönetimi:** Seviye sensörüne göre pompa ve valf kontrolü
- **Uzaktan İzleme:** Tüm sistemlerin mobil/web arayüzden izlenmesi ve bildirim
- **Güvenlik:** Kaçak akım, aşırı sıcaklık/akım durumunda otomatik müdahale ve alarm

## 🔧 Kurulum ve Bakım

1. **Donanım Montajı:** Raspberry Pi ve modüllerin pano içine yerleştirilmesi
2. **Kablolama:** RS485, güç ve sinyal hatlarının çekilmesi
3. **Home Assistant Kurulumu:** Raspberry Pi üzerinde Home Assistant OS kurulumu
4. **Modül Entegrasyonu:** Modbus cihazlarının Home Assistant'a tanımlanması
5. **Otomasyonların Tanımlanması:** Senaryoların yazılması ve test edilmesi

## 💡 Genişletilebilirlik ve Öneriler
- Ek modüllerle (röle, analog, dijital giriş/çıkış) sistem kolayca büyütülebilir
- MQTT, Modbus TCP gibi ek protokollerle uzaktan izleme ve entegrasyon
- Endüstriyel modüller sayesinde uzun ömür ve güvenilirlik
- Yedekli güç (UPS) ile kesintisiz otomasyon

---

*Bu altyapı, karavanın tüm sistemlerinin akıllı, güvenli ve merkezi olarak yönetilmesini sağlar.*
