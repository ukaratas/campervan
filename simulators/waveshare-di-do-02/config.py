#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Waveshare DI/DO Module - Instance 02
220V Finder Kontaktör Kontrol Sistemi
Finder 22.22.9.024.4000 (Modüler Kontaktör, 25A/2NO, 24V DC bobin)
"""

# Cihaz Bilgileri
DEVICE_NAME = "DI-DO-02"
DEVICE_TYPE = "DI/DO Module"
DEVICE_DESCRIPTION = "220V Finder Kontaktör Kontrol"

# Network Ayarları
PORT = 5027  # DI/DO-02 için port
SLAVE_ID = 1
HOST = "0.0.0.0"  # Tüm interface'lerde dinle
HA_HOSTNAME = "ugurs-macbook-m4-pro.local"  # Home Assistant'ın bağlanacağı adres

# DI/DO Konfigürasyonu
DI_COUNT = 8
DO_COUNT = 8
START_ADDRESS = 0

# Digital Input Etiketleri (Kontaktör Status Feedback - Yardımcı Kontak)
DI_LABELS = [
    "DI0: Finder-1 STATUS (İndüksiyon Ocak)",
    "DI1: Finder-2 STATUS (Bulaşık Makinesi)",
    "DI2: Finder-3 STATUS (Çamaşır Makinesi - FİX Mini 160W)",
    "DI3: Finder-4 STATUS (Mikrodalga Fırın - Profilo 800W)",
    "DI4: Finder-5 STATUS (Rezerv)",
    "DI5: Rezerv",
    "DI6: Rezerv",
    "DI7: Rezerv"
]

# Digital Output Etiketleri (Kontaktör Bobin Kontrolü)
# DO HIGH = Kontaktör çeker (cihaz AÇ), DO LOW = Kontaktör düşer (cihaz KAPA)
DO_LABELS = [
    "DO0: Finder-1 (İndüksiyon Ocak) - HIGH=AÇ",
    "DO1: Finder-2 (Bulaşık Makinesi) - HIGH=AÇ",
    "DO2: Finder-3 (Çamaşır Makinesi) - HIGH=AÇ",
    "DO3: Finder-4 (Mikrodalga Fırın) - HIGH=AÇ",
    "DO4: Finder-5 (Rezerv) - HIGH=AÇ",
    "DO5: Rezerv",
    "DO6: Rezerv",
    "DO7: Rezerv"
]

# Kısa etiketler (kontrol.py için)
DI_LABELS_SHORT = [
    "İndüksiyon", "Bulaşık Mak.", "Çamaşır Mak.", "Mikrodalga",
    "Rezerv-5", "Rezerv-6", "Rezerv-7", "Rezerv-8"
]

DO_LABELS_SHORT = [
    "İndüksiyon", "Bulaşık", "Çamaşır", "Mikrodalga",
    "Rezerv-5", "Rezerv-6", "Rezerv-7", "Rezerv-8"
]

# İzleme (watch) etiketleri (simulator.py logging için)
DI_LABELS_WATCH = [
    "DI0: F1-Status", "DI1: F2-Status", "DI2: F3-Status", "DI3: F4-Status",
    "DI4: F5-Status", "DI5: Rezerv", "DI6: Rezerv", "DI7: Rezerv"
]

DO_LABELS_WATCH = [
    "DO0: F1-Ocak", "DO1: F2-Bulaşık", "DO2: F3-Çamaşır", "DO3: F4-Mikrodalga",
    "DO4: F5-Rezerv", "DO5: Rezerv", "DO6: Rezerv", "DO7: Rezerv"
]

# Finder Kontaktör Mapping
# Finder 22.22.9.024.4000: Modüler kontaktör, 25A/2NO, 24V DC bobin
# Her kontaktör için 1 DO (bobin kontrol) + 1 DI (status feedback)
# DO HIGH = Kontaktör çeker (cihaz AÇ), DO LOW = Kontaktör düşer (cihaz KAPA)
FINDER_MAPPING = {
    "Finder-1": {
        "name": "İndüksiyon Ocak (Omake 1800W)",
        "power_w": 1800,
        "do_control": 0,   # DO0
        "di_status": 0     # DI0
    },
    "Finder-2": {
        "name": "Bulaşık Makinesi (Electrolux ESF2400O)",
        "power_w": 1700,
        "do_control": 1,   # DO1
        "di_status": 1     # DI1
    },
    "Finder-3": {
        "name": "Çamaşır Makinesi (FİX Mini 160W)",
        "power_w": 160,
        "do_control": 2,   # DO2
        "di_status": 2     # DI2
    },
    "Finder-4": {
        "name": "Mikrodalga Fırın (Profilo FRIAT9AN 800W)",
        "power_w": 800,
        "do_control": 3,   # DO3
        "di_status": 3     # DI3
    },
    "Finder-5": {
        "name": "Rezerv",
        "power_w": 0,
        "do_control": 4,   # DO4
        "di_status": 4     # DI4
    }
}
