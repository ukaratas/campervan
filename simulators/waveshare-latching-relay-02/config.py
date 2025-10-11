#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Waveshare Latching Relay Module - Instance 02
Banyo Aydınlatma ve Su Sistemi Pompaları
"""

# Cihaz Bilgileri
DEVICE_NAME = "Relay-02"
DEVICE_TYPE = "Latching Relay"
DEVICE_DESCRIPTION = "Banyo ve Su Sistemi Kontrol"

# Network Ayarları
PORT = 5025  # Relay-02 için farklı port
SLAVE_ID = 1
HOST = "0.0.0.0"  # Tüm interface'lerde dinle
HA_HOSTNAME = "ugurs-macbook-m4-pro.local"  # Home Assistant'ın bağlanacağı adres

# Röle Konfigürasyonu
RELAY_COUNT = 8
START_ADDRESS = 0

# Röle Etiketleri (Detaylı)
RELAY_LABELS = [
    "R0: Banyo Aydınlatma",
    "R1: Banyo Ayna Aydınlatma", 
    "R2: Temiz Su Hidrofor",
    "R3: Macerator Pompa",
    "R4: Rezerv",
    "R5: Rezerv",
    "R6: Rezerv",
    "R7: Rezerv"
]

# Kısa etiketler (kontrol.py için)
RELAY_LABELS_SHORT = [
    "Banyo",
    "Ayna",
    "Hidrofor",
    "Macerator",
    "Rezerv-5",
    "Rezerv-6",
    "Rezerv-7",
    "Rezerv-8"
]

# İzleme (watch) etiketleri (simulator.py logging için)
RELAY_LABELS_WATCH = [
    "R0: Banyo",
    "R1: Ayna",
    "R2: Hidrofor",
    "R3: Macerator",
    "R4: Rezerv-5",
    "R5: Rezerv-6",
    "R6: Rezerv-7",
    "R7: Rezerv-8"
]

# Güç Tüketimi (Watt)
POWER_WATTS = [8, 8, 84, 192, 0, 0, 0, 0]  # Banyo: 8W, Ayna: 8W, Hidrofor: 84W, Macerator: 192W

