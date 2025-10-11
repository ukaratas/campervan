#!/usr/bin/env python3
"""
Waveshare Modbus RTU 8-ch Latching Relay Module (C) - Instance 01

Wiki: https://www.waveshare.com/wiki/Modbus_RTU_Relay_(C)
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

# Config import
from config import (
    DEVICE_NAME, DEVICE_TYPE, DEVICE_DESCRIPTION,
    PORT, SLAVE_ID, RELAY_COUNT, START_ADDRESS,
    RELAY_LABELS, POWER_WATTS
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

class RelayMonitor:
    def __init__(self, context):
        self.context = context
        self.running = True
        self.previous_states = [0] * RELAY_COUNT
        
    def monitor(self):
        """Röle değişikliklerini izle"""
        while self.running:
            try:
                slave_id = 0x00
                current_states = self.context[slave_id].getValues(1, START_ADDRESS, RELAY_COUNT)  # Coils
                
                # Holding register sync
                self.context[slave_id].setValues(3, START_ADDRESS, current_states)
                
                # Değişiklikleri logla
                for i in range(min(RELAY_COUNT, len(current_states))):
                    if current_states[i] != self.previous_states[i]:
                        status = "🟢 AÇILDI" if current_states[i] else "⚫ KAPANDI"
                        log.info(f"💡 {RELAY_LABELS[i]} → {status}")
                        self.previous_states[i] = current_states[i]
            except Exception as e:
                pass  # Ignore errors
            
            time.sleep(0.2)

# Global simulator instance (interaktif kullanım için)
simulator = None

def run():
    global simulator
    
    # Modbus Data Store
    # NOT: ModbusSequentialDataBlock başlangıç adresi 0, ama 8 element için 0-7 erişimi gerekli
    # Waveshare için address 0-7, toplam 8 coil
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),   # Coils - 100 element (0-99 erişim)
        hr=ModbusSequentialDataBlock(0, [0]*200),
        ir=ModbusSequentialDataBlock(0, [0]*200)
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device ID
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'Modbus RTU Relay (C)'
    identity.ProductName = f'Modbus RTU {RELAY_COUNT}-ch {DEVICE_TYPE} Module'
    identity.MajorMinorRevision = '3.00'
    
    # Monitor başlat
    simulator = RelayMonitor(context)
    monitor_thread = threading.Thread(target=simulator.monitor, daemon=True)
    monitor_thread.start()
    
    print("\n" + "="*70)
    print(f"💡 WAVESHARE {DEVICE_TYPE.upper()} #{DEVICE_NAME} - {DEVICE_DESCRIPTION.upper()}")
    print("="*70)
    print(f"📡 Port: {PORT} | Slave ID: {SLAVE_ID}")
    print("📖 Wiki: https://www.waveshare.com/wiki/Modbus_RTU_Relay_(C)")
    print()
    for i, label in enumerate(RELAY_LABELS):
        print(f"   Coil {i}: {label}")
    print()
    print("⏳ Bağlantı bekleniyor...")
    print("="*70 + "\n")
    
    # Server başlat
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", PORT))

if __name__ == "__main__":
    run()

