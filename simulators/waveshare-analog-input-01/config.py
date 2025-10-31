# ==========================================
# Waveshare Modbus RTU Analog Input 8CH
# Konfigürasyon Dosyası
# ==========================================

# Cihaz Bilgileri
DEVICE_NAME = "Analog-Input-01"
DEVICE_TYPE = "Analog Input Module"
DEVICE_DESCRIPTION = "Su Seviyeleri ve Sıcaklık Sensörleri"

# Modbus Konfigürasyonu
PORT = 5028  # Yeni port
SLAVE_ID = 1
HOST = "0.0.0.0"  # Tüm interface'lerde dinle (Home Assistant erişimi için)
HA_HOSTNAME = "ugurs-macbook-m4-pro.local"

# Analog Input Konfigürasyonu
AI_COUNT = 8
START_ADDRESS = 0  # Holding Registers başlangıç adresi

# Analog Input Etiketleri (Detaylı)
AI_LABELS = [
    "AI0: Temiz Su Seviyesi (%)",
    "AI1: Gri Su Seviyesi (%)",
    "AI2: Banyo Sıcaklık (°C)",
    "AI3: Salon Sıcaklık (°C)",
    "AI4: Yatak Sıcaklık (°C)",
    "AI5: Elektronik Ortam Sıcaklık (°C)",
    "AI6: Salon Hava Kalitesi CO2 (ppm)",
    "AI7: Dış Sıcaklık (°C)"
]

# Kısa etiketler (kontrol.py için)
AI_LABELS_SHORT = [
    "Temiz Su",
    "Gri Su",
    "Banyo °C",
    "Salon °C",
    "Yatak °C",
    "Elektronik °C",
    "CO2 ppm",
    "Dış °C"
]

# İzleme (watch) etiketleri (simulator.py logging için)
AI_LABELS_WATCH = [
    "Temiz Su",
    "Gri Su",
    "Banyo",
    "Salon",
    "Yatak",
    "Elektronik",
    "CO2",
    "Dış"
]

# Sensör Tipleri ve Değer Aralıkları
# Format: (min_value, max_value, unit, precision)
SENSOR_RANGES = [
    (0, 100, "%", 1),      # AI0: Temiz Su Seviyesi (0-100%)
    (0, 100, "%", 1),      # AI1: Gri Su Seviyesi (0-100%)
    (10, 35, "°C", 1),     # AI2: Banyo Sıcaklık (10-35°C)
    (10, 35, "°C", 1),     # AI3: Salon Sıcaklık (10-35°C)
    (10, 35, "°C", 1),     # AI4: Yatak Sıcaklık (10-35°C)
    (20, 50, "°C", 1),     # AI5: Elektronik Sıcaklık (20-50°C)
    (400, 2000, "ppm", 0), # AI6: CO2 (400-2000 ppm)
    (-10, 40, "°C", 1)     # AI7: Dış Sıcaklık (-10 to 40°C)
]

# Başlangıç Değerleri (Gerçekçi)
INITIAL_VALUES = [
    75,    # AI0: Temiz Su %75
    20,    # AI1: Gri Su %20
    22,    # AI2: Banyo 22°C
    23,    # AI3: Salon 23°C
    21,    # AI4: Yatak 21°C
    28,    # AI5: Elektronik 28°C
    650,   # AI6: CO2 650 ppm (iyi hava)
    15     # AI7: Dış 15°C
]

# Simülasyon Parametreleri
# Her sensör için (değişim_hızı, değişim_olasılığı)
SIMULATION_PARAMS = [
    (2, 0.05),   # AI0: Su seviyesi yavaş değişir
    (3, 0.08),   # AI1: Gri su daha hızlı değişir
    (0.5, 0.3),  # AI2: Banyo sıcaklık orta hızda
    (0.3, 0.3),  # AI3: Salon sıcaklık yavaş
    (0.4, 0.3),  # AI4: Yatak sıcaklık yavaş
    (1, 0.4),    # AI5: Elektronik sıcaklık daha hızlı
    (50, 0.4),   # AI6: CO2 orta hızda değişir
    (1, 0.2)     # AI7: Dış sıcaklık yavaş
]

# Modbus Ölçekleme (Holding Register 16-bit integer olarak)
# Değerler 10x ölçeklenecek (örn: 22.5°C → 225)
SCALE_FACTOR = 10

