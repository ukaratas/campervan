#!/usr/bin/env python3
"""
Waveshare Modbus RTU Analog Input 8CH Simulator
8 Kanal Analog Sensör Simülasyonu
"""

import sys
import time
import random
import logging
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# Config dosyasını import et
from config import *

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('simulator.log')
    ]
)

class AnalogInputSimulator:
    """
    Analog Input Simülatörü - Gerçekçi sensör değerleri üretir
    
    Sensörler:
    - AI0-1: Su seviyeleri (yavaş değişim)
    - AI2-5: Sıcaklıklar (orta hızda değişim)
    - AI6: CO2 (dalgalı değişim)
    - AI7: Dış sıcaklık (çok yavaş değişim)
    """
    def __init__(self, context):
        self.context = context
        self.running = True
        self.current_values = list(INITIAL_VALUES)  # Başlangıç değerleri
        
    def simulate(self):
        """Analog değerleri sürekli güncelle"""
        while self.running:
            try:
                slave_id = SLAVE_ID
                
                # Her sensör için değer güncelle
                for ai_index in range(AI_COUNT):
                    min_val, max_val, unit, precision = SENSOR_RANGES[ai_index]
                    change_rate, change_prob = SIMULATION_PARAMS[ai_index]
                    
                    # Rastgele değişim olasılığı
                    if random.random() < change_prob:
                        # Rastgele değişim miktarı
                        change = random.uniform(-change_rate, change_rate)
                        new_value = self.current_values[ai_index] + change
                        
                        # Limitlere uygunluk kontrolü
                        new_value = max(min_val, min(max_val, new_value))
                        
                        # Hassasiyet kontrolü
                        new_value = round(new_value, precision)
                        
                        # Değer değiştiyse güncelle
                        if new_value != self.current_values[ai_index]:
                            old_value = self.current_values[ai_index]
                            self.current_values[ai_index] = new_value
                            
                            # Modbus'a yaz (10x ölçeklenmiş integer olarak)
                            scaled_value = int(new_value * SCALE_FACTOR)
                            self.context[slave_id].setValues(3, ai_index, [scaled_value])
                            
                            # Log (sadece önemli değişimlerde)
                            if self._is_significant_change(ai_index, old_value, new_value):
                                logging.info(
                                    f"📊 {AI_LABELS_WATCH[ai_index]}: "
                                    f"{old_value:.{precision}f}{unit} → "
                                    f"{new_value:.{precision}f}{unit}"
                                )
                
                # Özel durumlar ve alarmlar
                self._check_alarms()
                
                time.sleep(2)  # Her 2 saniyede bir güncelle
                
            except Exception as e:
                logging.error(f"Simulation error: {e}")
    
    def _is_significant_change(self, index, old_val, new_val):
        """Önemli değişim mi kontrol et (log karmaşasını önle)"""
        thresholds = [5, 5, 1, 1, 1, 2, 100, 2]  # Her sensör için eşik
        return abs(new_val - old_val) >= thresholds[index]
    
    def _check_alarms(self):
        """Kritik durum kontrolü"""
        # Temiz su düşük
        if self.current_values[0] < 20:
            if random.random() < 0.1:  # Her 20 saniyede bir log
                logging.warning(f"⚠️ UYARI: Temiz su seviyesi düşük! {self.current_values[0]:.1f}%")
        
        # Gri su yüksek
        if self.current_values[1] > 80:
            if random.random() < 0.1:
                logging.warning(f"⚠️ UYARI: Gri su seviyesi yüksek! {self.current_values[1]:.1f}%")
        
        # Elektronik sıcaklık yüksek
        if self.current_values[5] > 40:
            if random.random() < 0.1:
                logging.warning(f"🔥 UYARI: Elektronik ortam sıcak! {self.current_values[5]:.1f}°C")
        
        # CO2 yüksek
        if self.current_values[6] > 1000:
            if random.random() < 0.1:
                logging.warning(f"💨 UYARI: Hava kalitesi düşük! CO2: {self.current_values[6]:.0f} ppm")

def run_server():
    """Modbus TCP sunucusunu başlat"""
    
    # Holding Registers oluştur (8 analog input için)
    # Başlangıç değerlerini 10x ölçeklenmiş olarak yaz
    initial_scaled = [int(val * SCALE_FACTOR) for val in INITIAL_VALUES]
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),
        hr=ModbusSequentialDataBlock(0, initial_scaled + [0]*92),  # Holding Registers
        ir=ModbusSequentialDataBlock(0, [0]*100)
    )
    
    context = ModbusServerContext(slaves={SLAVE_ID: store}, single=False)
    
    # Cihaz kimlik bilgileri
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'Modbus RTU Analog Input 8CH'
    identity.VendorUrl = 'https://www.waveshare.com'
    identity.ProductName = DEVICE_NAME
    identity.ModelName = DEVICE_TYPE
    identity.MajorMinorRevision = '1.0.0'
    
    # Simülatörü başlat (thread olarak)
    import threading
    simulator = AnalogInputSimulator(context)
    sim_thread = threading.Thread(target=simulator.simulate, daemon=True)
    sim_thread.start()
    
    logging.info("="*60)
    logging.info(f"🌡️ {DEVICE_NAME} - {DEVICE_DESCRIPTION}")
    logging.info("="*60)
    logging.info(f"📡 Modbus TCP Server: {HOST}:{PORT}")
    logging.info(f"🔢 Slave ID: {SLAVE_ID}")
    logging.info(f"📊 Analog Inputs: {AI_COUNT}")
    logging.info("")
    logging.info("Sensörler:")
    for i, label in enumerate(AI_LABELS):
        min_val, max_val, unit, _ = SENSOR_RANGES[i]
        logging.info(f"  {label}: {min_val}-{max_val}{unit} (Başlangıç: {INITIAL_VALUES[i]}{unit})")
    logging.info("")
    logging.info("✅ Sunucu başlatılıyor...")
    logging.info("="*60)
    
    # Sunucuyu başlat
    StartTcpServer(
        context=context,
        identity=identity,
        address=(HOST, PORT)
    )

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        logging.info("\n🛑 Sunucu kapatılıyor...")
        sys.exit(0)

