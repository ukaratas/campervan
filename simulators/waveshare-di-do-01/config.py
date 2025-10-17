"""
Waveshare Modbus RTU IO 8CH - Instance 01 - Configuration
8 DI (Digital Input) + 8 DO (Digital Output) Modülü

Wiki: https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH
"""

# Cihaz Bilgileri
DEVICE_NAME = "DI-DO-01"
DEVICE_TYPE = "DI/DO Module"
DEVICE_DESCRIPTION = "Dijital Giriş/Çıkış Kontrol"

# Network Ayarları
PORT = 5024
SLAVE_ID = 1
HOST = "localhost"  # Yerel testler için localhost, uzaktan erişim için IP veya hostname

# Modbus Ayarları
DI_COUNT = 8  # Digital Input kanalları
DO_COUNT = 8  # Digital Output kanalları
START_ADDRESS = 0

# Digital Input Etiketleri (Push Buttons)
DI_LABELS = [
    "DI0: Sağ Yatak Butonu",
    "DI1: Sol Yatak Butonu",
    "DI2: Popup Yatak Butonu",
    "DI3: Dış Aydınlatma Butonu",
    "DI4: Otomatik Basamak Butonu",
    "DI5: Mutfak Butonu",
    "DI6: Orta Alan Butonu",
    "DI7: Banyo Butonu"
]

# Digital Output Etiketleri (Aktüatörler, vb.)
DO_LABELS = [
    "DO0: Alarm Siren",
    "DO1: Havalandırma Fan",
    "DO2: Temiz Su Boşaltma Vanası",
    "DO3: Isıtıcı",
    "DO4: Soğutucu",
    "DO5: Valf 1",
    "DO6: Valf 2",
    "DO7: Uyarı Lambası"
]

# Kısa etiketler (kontrol.py için)
DI_LABELS_SHORT = [
    "Sağ Yatak", "Sol Yatak", "Popup Yatak", "Dış Aydınlatma",
    "Basamak", "Mutfak", "Orta Alan", "Banyo"
]

DO_LABELS_SHORT = [
    "Alarm", "Fan", "Temiz Su Vana", "Isıtıcı",
    "Soğutucu", "Valf 1", "Valf 2", "Uyarı"
]

# İzleme (watch) etiketleri (simulator.py logging için)
DI_LABELS_WATCH = [
    "DI0: Sağ Yatak", "DI1: Sol Yatak", "DI2: Popup Yatak", "DI3: Dış Aydınlatma",
    "DI4: Basamak", "DI5: Mutfak", "DI6: Orta Alan", "DI7: Banyo"
]

DO_LABELS_WATCH = [
    "DO0: Alarm", "DO1: Fan", "DO2: Temiz Su Vana", "DO3: Isıtıcı",
    "DO4: Soğutucu", "DO5: Valf 1", "DO6: Valf 2", "DO7: Uyarı"
]

# Home Assistant Ayarları
HA_HOSTNAME = "ugurs-macbook-m4-pro.local"  # Dinamik IP'den bağımsız

