#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Waveshare Latching Relay Module - Instance 03
Yüksek Tüketim Cihazları (Buzdolabı, USB, Kombi, vb.)
"""

# Cihaz Bilgileri
DEVICE_NAME = "Relay-03"
DEVICE_TYPE = "Latching Relay"
DEVICE_DESCRIPTION = "Yüksek Tüketim Cihazları"

# Network Ayarları
PORT = 5026  # Relay-03 için farklı port
SLAVE_ID = 1
HOST = "0.0.0.0"  # Tüm interface'lerde dinle
HA_HOSTNAME = "ugurs-macbook-m4-pro.local"  # Home Assistant'ın bağlanacağı adres

# Röle Konfigürasyonu
RELAY_COUNT = 8
START_ADDRESS = 0

# Röle Etiketleri (Detaylı)
RELAY_LABELS = [
    "R0: Buzdolabı",
    "R1: USB Kutusu #1 (Mutfak)",
    "R2: USB Kutusu #2 (Yatak)",
    "R3: USB Kutusu #3 (Salon)",
    "R4: USB Kutusu #4 (Popup)",
    "R5: Truma Combi D4",
    "R6: Gri Su Pompası",
    "R7: Rezerv"
]

# Kısa etiketler (kontrol.py için)
RELAY_LABELS_SHORT = [
    "Buzdolabı",
    "USB Mutfak",
    "USB Yatak",
    "USB Salon",
    "USB Popup",
    "Truma",
    "Gri Su",
    "Rezerv-8"
]

# İzleme (watch) etiketleri (simulator.py logging için)
RELAY_LABELS_WATCH = [
    "R0: Buzdolabı",
    "R1: USB-Mutfak",
    "R2: USB-Yatak",
    "R3: USB-Salon",
    "R4: USB-Popup",
    "R5: Truma",
    "R6: Gri Su",
    "R7: Rezerv-8"
]

# Güç Tüketimi (Watt)
POWER_WATTS = [65, 200, 200, 200, 200, 50, 120, 0]  # Buzdolabı: 65W, USB: 200W×4, Truma: 50W, Gri Su: 120W

