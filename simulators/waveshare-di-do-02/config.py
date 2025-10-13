#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Waveshare DI/DO Module - Instance 02
220V Finder Röle Kontrol Sistemi
"""

# Cihaz Bilgileri
DEVICE_NAME = "DI-DO-02"
DEVICE_TYPE = "DI/DO Module"
DEVICE_DESCRIPTION = "220V Finder Röle Kontrol"

# Network Ayarları
PORT = 5027  # DI/DO-02 için port
SLAVE_ID = 1
HOST = "0.0.0.0"  # Tüm interface'lerde dinle
HA_HOSTNAME = "ugurs-macbook-m4-pro.local"  # Home Assistant'ın bağlanacağı adres

# DI/DO Konfigürasyonu
DI_COUNT = 8
DO_COUNT = 8
START_ADDRESS = 0

# Digital Input Etiketleri (Finder Status Feedback)
DI_LABELS = [
    "DI0: Finder-1 STATUS (İndüksiyon Ocak)",
    "DI1: Finder-2 STATUS (Bulaşık Makinesi)",
    "DI2: Finder-3 STATUS (Çamaşır Makinesi - FİX Mini 160W)",
    "DI3: Finder-4 STATUS (Rezerv)",
    "DI4: Finder-5 STATUS (Rezerv)",
    "DI5: Finder-6 STATUS (Rezerv)",
    "DI6: Finder-7 STATUS (Rezerv)",
    "DI7: Finder-8 STATUS (Rezerv)"
]

# Digital Output Etiketleri (Finder Kontrol)
DO_LABELS = [
    "DO0: Finder-1 SET (AÇ)",
    "DO1: Finder-1 RESET (KAPA)",
    "DO2: Finder-2 SET (AÇ)",
    "DO3: Finder-2 RESET (KAPA)",
    "DO4: Finder-3 SET (AÇ)",
    "DO5: Finder-3 RESET (KAPA)",
    "DO6: Finder-4 SET (AÇ)",
    "DO7: Finder-4 RESET (KAPA)"
]

# Kısa etiketler (kontrol.py için)
DI_LABELS_SHORT = [
    "İndüksiyon", "Bulaşık Mak.", "Çamaşır Mak.", "Rezerv-4",
    "Rezerv-5", "Rezerv-6", "Rezerv-7", "Rezerv-8"
]

DO_LABELS_SHORT = [
    "İndüksiyon-AÇ", "İndüksiyon-KAPA",
    "Bulaşık-AÇ", "Bulaşık-KAPA",
    "Çamaşır-AÇ", "Çamaşır-KAPA",
    "Rezerv4-AÇ", "Rezerv4-KAPA"
]

# İzleme (watch) etiketleri (simulator.py logging için)
DI_LABELS_WATCH = [
    "DI0: F1-Status", "DI1: F2-Status", "DI2: F3-Status", "DI3: F4-Status",
    "DI4: F5-Status", "DI5: F6-Status", "DI6: F7-Status", "DI7: F8-Status"
]

DO_LABELS_WATCH = [
    "DO0: F1-SET", "DO1: F1-RST", "DO2: F2-SET", "DO3: F2-RST",
    "DO4: F3-SET", "DO5: F3-RST", "DO6: F4-SET", "DO7: F4-RST"
]

# Finder Röle Mapping
# Her Finder için 2 DO (SET/RESET) + 1 DI (STATUS)
FINDER_MAPPING = {
    "Finder-1": {
        "name": "İndüksiyon Ocak (Omake 1800W)",
        "do_set": 0,    # DO0
        "do_reset": 1,  # DO1
        "di_status": 0  # DI0
    },
    "Finder-2": {
        "name": "Bulaşık Makinesi (Electrolux)",
        "do_set": 2,    # DO2
        "do_reset": 3,  # DO3
        "di_status": 1  # DI1
    },
    "Finder-3": {
        "name": "220V Cihaz (Rezerv)",
        "do_set": 4,    # DO4
        "do_reset": 5,  # DO5
        "di_status": 2  # DI2
    },
    "Finder-4": {
        "name": "220V Cihaz (Rezerv)",
        "do_set": 6,    # DO6
        "do_reset": 7,  # DO7
        "di_status": 3  # DI3
    }
}

# Not: 8 DI var ama sadece 4 Finder kontrol ediliyor (8 DO ile 4 Finder)
# Eğer 8 Finder gerekirse, 2. DI/DO modülü (DI-DO-03) eklenecek

