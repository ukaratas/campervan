#!/usr/bin/env python3
"""
Waveshare Modbus RTU 8-ch Latching Relay Module (C) - Instance 01
Port: 5023 | Slave ID: 1

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Relay-01] - %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger()

# Röle etiketleri
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

POWER_WATTS = [8, 7, 12, 14, 6, 4, 4, 12]

class RelayMonitor:
    def __init__(self, context):
        self.context = context
        self.running = True
        self.previous_states = [0] * 8
        
    def monitor(self):
        """Röle değişikliklerini izle"""
        while self.running:
            try:
                slave_id = 0x00
                current_states = self.context[slave_id].getValues(1, 0, 8)  # Coils
                
                # Holding register sync
                self.context[slave_id].setValues(3, 0, current_states)
                
                # Değişiklikleri logla
                for i in range(min(8, len(current_states))):
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
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*8),    # 8 Coils
        hr=ModbusSequentialDataBlock(0, [0]*200),
        ir=ModbusSequentialDataBlock(0, [0]*200)
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device ID
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'Modbus RTU Relay (C)'
    identity.ProductName = 'Modbus RTU 8-ch Latching Relay Module'
    identity.MajorMinorRevision = '3.00'
    
    # Monitor başlat
    simulator = RelayMonitor(context)
    monitor_thread = threading.Thread(target=simulator.monitor, daemon=True)
    monitor_thread.start()
    
    print("\n" + "="*70)
    print("💡 WAVESHARE LATCHING RELAY #01 - AYDINLATMA KONTROL")
    print("="*70)
    print("📡 Port: 5023 | Slave ID: 1")
    print("📖 Wiki: https://www.waveshare.com/wiki/Modbus_RTU_Relay_(C)")
    print()
    for i, label in enumerate(RELAY_LABELS):
        print(f"   Coil {i}: {label}")
    print()
    print("⏳ Bağlantı bekleniyor...")
    print("="*70 + "\n")
    
    # Server başlat
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 5023))

if __name__ == "__main__":
    run()

