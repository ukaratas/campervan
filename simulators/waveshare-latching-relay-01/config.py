"""
Waveshare Latching Relay Instance 01 - Configuration
Aydınlatma Kontrol Modülü
"""

# Cihaz Bilgileri
DEVICE_NAME = "Relay-01"
DEVICE_TYPE = "Latching Relay"
DEVICE_DESCRIPTION = "Aydınlatma Kontrol"

# Network Ayarları
PORT = 5023
SLAVE_ID = 1
HOST = "0.0.0.0"  # Tüm interface'lerde dinle (Home Assistant erişimi için)

# Modbus Ayarları
RELAY_COUNT = 8
START_ADDRESS = 0

# Röle Etiketleri
RELAY_LABELS = [
    "R0: Mutfak Işık",
    "R1: Mutfak Tezgâh Işık",
    "R2: Orta Alan Işık",
    "R3: Yatak Alanı Işık",
    "R4: Popup Yatak Işık",
    "R5: Sol Okuma Işık",
    "R6: Sağ Okuma Işık",
    "R7: Tente Işık"
]

# Kısa etiketler (kontrol.py için)
RELAY_LABELS_SHORT = [
    "Mutfak", "Tezgâh", "Orta Alan", "Yatak Alanı",
    "Popup", "Sol Okuma", "Sağ Okuma", "Tente"
]

# İzleme etiketleri (izle.py için)
RELAY_LABELS_WATCH = [
    "R0: Mutfak", "R1: Tezgâh", "R2: Orta Alan", "R3: Yatak",
    "R4: Popup", "R5: Sol Okuma", "R6: Sağ Okuma", "R7: Tente"
]

# Güç Tüketimi (Watt)
POWER_WATTS = [8, 7, 12, 14, 6, 4, 4, 12]

# Home Assistant Ayarları
HA_HOSTNAME = "ugurs-macbook-m4-pro.local"  # Dinamik IP'den bağımsız

