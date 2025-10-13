#!/usr/bin/env python3
"""
Waveshare Modbus RTU IO 8CH - Instance 02
220V Finder Röle Kontrol Sistemi

8 DI (Status Feedback) + 8 DO (Finder SET/RESET Kontrol)

Mantık:
- DO çift indeksler (0,2,4,6): Finder SET (AÇ) → İlgili DI'yı 1 yap
- DO tek indeksler (1,3,5,7): Finder RESET (KAPA) → İlgili DI'yı 0 yap
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging
import threading
import time
import pathlib
import random

# Config import
from config import (
    DEVICE_NAME, DEVICE_TYPE, DEVICE_DESCRIPTION,
    PORT, SLAVE_ID, DI_COUNT, DO_COUNT, START_ADDRESS,
    DI_LABELS, DO_LABELS, DI_LABELS_WATCH, DO_LABELS_WATCH
)

# Log dizinini belirle
LOG_FILE = pathlib.Path(__file__).parent / "simulator.log"

# Hem console hem de dosyaya loglama
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s - [{DEVICE_NAME}] - %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger()

class DI_DO_Monitor:
    def __init__(self, context):
        self.context = context
        self.running = True
        self.previous_di_states = [0] * DI_COUNT
        self.previous_do_states = [0] * DO_COUNT
        
    def monitor(self):
        """DI/DO değişikliklerini izle"""
        while self.running:
            try:
                slave_id = 0x00
                
                # Digital Input'ları oku (Discrete Inputs - Function 02)
                current_di = self.context[slave_id].getValues(2, START_ADDRESS, DI_COUNT)
                
                # Digital Output'ları oku (Coils - Function 01)
                current_do = self.context[slave_id].getValues(1, START_ADDRESS, DO_COUNT)
                
                # DI değişikliklerini logla
                for i in range(min(DI_COUNT, len(current_di))):
                    if current_di[i] != self.previous_di_states[i]:
                        status = "🟢 AKTIF" if current_di[i] else "⚫ PASIF"
                        log.info(f"📥 {DI_LABELS[i]} → {status}")
                        self.previous_di_states[i] = current_di[i]
                
                # DO değişikliklerini logla
                for i in range(min(DO_COUNT, len(current_do))):
                    if current_do[i] != self.previous_do_states[i]:
                        status = "🟢 AÇIK" if current_do[i] else "⚫ KAPALI"
                        log.info(f"📤 {DO_LABELS[i]} → {status}")
                        self.previous_do_states[i] = current_do[i]
            except Exception as e:
                pass  # Ignore errors
            
            time.sleep(0.2)

class Finder_Logic:
    """
    Finder Röle Mantığı - DO komutlarına göre DI statuslarını günceller
    
    Mantık:
    - DO0,DO2,DO4,DO6 (çift indeksler): SET komutu → İlgili DI'yı 1 yap
    - DO1,DO3,DO5,DO7 (tek indeksler): RESET komutu → İlgili DI'yı 0 yap
    
    Mapping:
    - DO0 (F1-SET) / DO1 (F1-RESET) → DI0 (F1-STATUS)
    - DO2 (F2-SET) / DO3 (F2-RESET) → DI1 (F2-STATUS)
    - DO4 (F3-SET) / DO5 (F3-RESET) → DI2 (F3-STATUS)
    - DO6 (F4-SET) / DO7 (F4-RESET) → DI3 (F4-STATUS)
    """
    def __init__(self, context):
        self.context = context
        self.running = True
        self.previous_do_states = [0] * DO_COUNT
        
    def simulate(self):
        """DO değişikliklerini izle ve DI'ları güncelle"""
        while self.running:
            try:
                slave_id = 0x00
                
                # DO durumlarını oku (Coils - Function 01)
                current_do = self.context[slave_id].getValues(1, START_ADDRESS, DO_COUNT)
                
                # Her DO'yu kontrol et
                for do_index in range(DO_COUNT):
                    if current_do[do_index] != self.previous_do_states[do_index]:
                        # DO aktif edildi
                        if current_do[do_index] == 1:
                            finder_index = do_index // 2  # Hangi Finder? (0-3)
                            di_index = finder_index  # İlgili DI indeksi
                            
                            if do_index % 2 == 0:
                                # Çift indeks = SET komutu → DI'yı 1 yap
                                self.context[slave_id].setValues(2, di_index, [1])
                                logging.info(f"⚡ Finder-{finder_index+1} SET → STATUS=ON")
                            else:
                                # Tek indeks = RESET komutu → DI'yı 0 yap
                                self.context[slave_id].setValues(2, di_index, [0])
                                logging.info(f"⚡ Finder-{finder_index+1} RESET → STATUS=OFF")
                        
                        # DO durumunu güncelle
                        self.previous_do_states[do_index] = current_do[do_index]
                
            except Exception as e:
                logging.error(f"Finder logic error: {e}")
            
            time.sleep(0.1)  # 100ms döngü
            
# Global simulator instance
monitor = None
finder_logic = None

def run():
    global monitor, finder_logic
    
    # Modbus Data Store
    # DI: Discrete Inputs (address 2) - sensörlerden gelen sinyaller
    # DO: Coils (address 1) - kontrol edilebilir çıkışlar
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs (DI)
        co=ModbusSequentialDataBlock(0, [0]*100),  # Coils (DO)
        hr=ModbusSequentialDataBlock(0, [0]*200),  # Holding Registers
        ir=ModbusSequentialDataBlock(0, [0]*200)   # Input Registers
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device ID
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'Modbus RTU IO 8CH'
    identity.ProductName = f'{DI_COUNT}DI/{DO_COUNT}DO {DEVICE_TYPE}'
    identity.MajorMinorRevision = '2.00'
    
    # Monitor başlat
    monitor = DI_DO_Monitor(context)
    monitor_thread = threading.Thread(target=monitor.monitor, daemon=True)
    monitor_thread.start()
    
    # Finder Logic başlat (DO → DI mapping)
    finder_logic = Finder_Logic(context)
    finder_thread = threading.Thread(target=finder_logic.simulate, daemon=True)
    finder_thread.start()
    
    print("\n" + "="*70)
    print(f"🔌 WAVESHARE {DEVICE_TYPE.upper()} #{DEVICE_NAME} - {DEVICE_DESCRIPTION.upper()}")
    print("="*70)
    print(f"📡 Port: {PORT} | Slave ID: {SLAVE_ID}")
    print("📖 Wiki: https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH")
    print()
    print("📥 DIGITAL INPUTS (Sensörler):")
    for i, label in enumerate(DI_LABELS):
        print(f"   DI{i}: {label}")
    print()
    print("📤 DIGITAL OUTPUTS (Kontrol):")
    for i, label in enumerate(DO_LABELS):
        print(f"   DO{i}: {label}")
    print()
    print("⏳ Bağlantı bekleniyor...")
    print("="*70 + "\n")
    
    # Server başlat
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", PORT))

if __name__ == "__main__":
    run()

