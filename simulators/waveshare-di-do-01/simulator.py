#!/usr/bin/env python3
"""
Waveshare Modbus RTU IO 8CH - Instance 01
8 DI (Digital Input) + 8 DO (Digital Output)

Wiki: https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH
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

class DI_Simulator:
    """Digital Input simülatörü - Push button davranışı"""
    def __init__(self, context):
        self.context = context
        self.running = True
        
    def simulate(self):
        """DI'ları periyodik olarak değiştir (Push button simülasyonu)"""
        while self.running:
            try:
                # Her 3-8 saniyede bir rastgele bir butona basılsın
                time.sleep(random.randint(3, 8))
                
                slave_id = 0x00
                di_index = random.randint(0, DI_COUNT - 1)
                
                # Basma süresi rastgele: %70 short press, %20 long press, %10 double press
                press_type = random.choices(['short', 'long', 'double'], weights=[70, 20, 10])[0]
                
                if press_type == 'short':
                    # Short press: 0.1-0.3 saniye
                    press_duration = random.uniform(0.1, 0.3)
                    logging.info(f"🔘 {DI_LABELS_WATCH[di_index]} - SHORT PRESS ({press_duration:.2f}s)")
                    self.context[slave_id].setValues(2, di_index, [1])  # Bas
                    time.sleep(press_duration)
                    self.context[slave_id].setValues(2, di_index, [0])  # Bırak
                    
                elif press_type == 'long':
                    # Long press: 1.0-2.0 saniye
                    press_duration = random.uniform(1.0, 2.0)
                    logging.info(f"🔘 {DI_LABELS_WATCH[di_index]} - LONG PRESS ({press_duration:.2f}s)")
                    self.context[slave_id].setValues(2, di_index, [1])  # Bas
                    time.sleep(press_duration)
                    self.context[slave_id].setValues(2, di_index, [0])  # Bırak
                    
                elif press_type == 'double':
                    # Double press: 2x short press, 0.2 saniye aralıkla
                    logging.info(f"🔘 {DI_LABELS_WATCH[di_index]} - DOUBLE PRESS")
                    self.context[slave_id].setValues(2, di_index, [1])  # İlk bas
                    time.sleep(0.15)
                    self.context[slave_id].setValues(2, di_index, [0])  # Bırak
                    time.sleep(0.2)  # Kısa bekleme
                    self.context[slave_id].setValues(2, di_index, [1])  # İkinci bas
                    time.sleep(0.15)
                    self.context[slave_id].setValues(2, di_index, [0])  # Bırak
                
            except Exception as e:
                logging.error(f"DI simulation error: {e}")
            
# Global simulator instance
simulator = None
di_simulator = None

def run():
    global simulator, di_simulator
    
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
    simulator = DI_DO_Monitor(context)
    monitor_thread = threading.Thread(target=simulator.monitor, daemon=True)
    monitor_thread.start()
    
    # DI Simulator başlat (opsiyonel - sensör simülasyonu)
    di_simulator = DI_Simulator(context)
    di_sim_thread = threading.Thread(target=di_simulator.simulate, daemon=True)
    di_sim_thread.start()
    
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

