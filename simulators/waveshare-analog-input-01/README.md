# Waveshare Modbus RTU Analog Input 8CH - Simulatör

## 📋 Genel Bakış

8 kanallı analog input modül simülatörü. Su seviyeleri, sıcaklık ve hava kalitesi sensörlerini simüle eder.

**Modül:** [Waveshare Modbus RTU Analog Input 8CH](https://www.waveshare.com/modbus-rtu-analog-input-8ch.htm)

## 🌡️ Sensörler

| Kanal | Sensör | Aralık | Birim | Açıklama |
|-------|--------|--------|-------|----------|
| AI0 | Temiz Su Seviyesi | 0-100 | % | 10-180Ω şamandıra |
| AI1 | Gri Su Seviyesi | 0-100 | % | 10-180Ω şamandıra |
| AI2 | Banyo Sıcaklık | 10-35 | °C | Konfor kontrolü |
| AI3 | Salon Sıcaklık | 10-35 | °C | Ana yaşam alanı |
| AI4 | Yatak Sıcaklık | 10-35 | °C | Yatak bölgesi |
| AI5 | Elektronik Ortam | 20-50 | °C | Aşırı ısınma koruması |
| AI6 | Salon CO2 | 400-2000 | ppm | Hava kalitesi |
| AI7 | Dış Sıcaklık | -10 to 40 | °C | Dış ortam |

## 🚀 Kullanım

### Simulatörü Başlat
```bash
cd simulators/waveshare-analog-input-01
source ../venv/bin/activate
python3 simulator.py
```

### Sensör Değerlerini Oku
```bash
python3 kontrol.py           # Tüm sensörler
python3 kontrol.py 0          # Sadece AI0 (Temiz Su)
```

### Real-time İzleme
```bash
python3 izle.py              # Canlı izleme (CTRL+C ile çıkış)
```

## 📊 Modbus Detayları

- **Protocol:** Modbus TCP
- **Port:** 5028
- **Slave ID:** 1
- **Function Code:** 03 (Read Holding Registers)
- **Data Format:** 16-bit unsigned integer
- **Scaling:** Değerler 10x ölçeklenmiş (örn: 22.5°C → 225)

## ⚙️ Konfigürasyon

Tüm parametreler `config.py` dosyasında:

```python
PORT = 5028
SLAVE_ID = 1
AI_COUNT = 8
INITIAL_VALUES = [75, 20, 22, 23, 21, 28, 650, 15]
```

## 🏠 Home Assistant Entegrasyonu

1. **Modbus config ekle:**
```yaml
modbus:
  - name: "Analog_Sensorler"
    type: tcp
    host: ugurs-macbook-m4-pro.local
    port: 5028
    sensors:
      # ha-config.yaml dosyasını buraya kopyala
```

2. **Otomatik Deployment:**
```bash
cd Automation/ha-configs
python3 deploy.py --auto
```

## 🎯 Alarm Kuralları

| Sensör | Durum | Eşik | Aksiyon |
|--------|-------|------|---------|
| Temiz Su | Düşük | < 20% | ⚠️ Uyarı |
| Gri Su | Yüksek | > 80% | ⚠️ Uyarı + Otomatik tahliye |
| Elektronik | Sıcak | > 40°C | 🔥 Uyarı + Havalandırma |
| CO2 | Yüksek | > 1000 ppm | 💨 Uyarı + Fan açma |

## 📈 Simülasyon Özellikleri

- **Gerçekçi değişimler:** Her sensör kendi hızında değişir
- **Limit kontrolü:** Min/max değerler korunur
- **Otomatik alarmlar:** Kritik durumlar log'lanır
- **Smooth transitions:** Ani sıçramalar yok

## 🔧 Troubleshooting

### Bağlantı Hatası
```bash
# Simulatör çalışıyor mu?
ps aux | grep simulator.py

# Port kullanımda mı?
lsof -i :5028
```

### Değerler Yanlış
```bash
# Config'i kontrol et
cat config.py

# Manuel okuma yap
python3 kontrol.py
```

## 📝 Notlar

- Gerçek şamandıralar 10-180Ω aralığında çalışır
- Modbus değerleri 10x ölçeklenmiş olarak iletilir
- Home Assistant otomatik olarak 0.1 ile çarparak gerçek değeri bulur
- CO2 sensörü için 400-800 ppm ideal, >1000 ppm kötü hava

## 🔗 Linkler

- [Modül Datasheet](https://www.waveshare.com/modbus-rtu-analog-input-8ch.htm)
- [Proje Ana README](../../README.md)
- [Home Assistant Configs](../../Automation/ha-configs/)

