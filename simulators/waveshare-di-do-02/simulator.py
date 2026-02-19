#!/usr/bin/env python3
"""
Waveshare Modbus RTU IO 8CH - Instance 02
220V Finder Kontaktör Kontrol Sistemi
Finder 22.22.9.024.4000 (Modüler Kontaktör, 25A/2NO, 24V DC bobin)

8 DI (Status Feedback) + 8 DO (Kontaktör Bobin Kontrol)

Mantık:
- DO HIGH = Kontaktör bobini enerjilenir → Kontak kapanır → DI = 1 (Cihaz AÇ)
- DO LOW  = Kontaktör bobini enerjisizleşir → Kontak açılır → DI = 0 (Cihaz KAPA)
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
                
                current_di = self.context[slave_id].getValues(2, START_ADDRESS, DI_COUNT)
                current_do = self.context[slave_id].getValues(1, START_ADDRESS, DO_COUNT)
                
                for i in range(min(DI_COUNT, len(current_di))):
                    if current_di[i] != self.previous_di_states[i]:
                        status = "🟢 AKTIF" if current_di[i] else "⚫ PASIF"
                        log.info(f"📥 {DI_LABELS[i]} → {status}")
                        self.previous_di_states[i] = current_di[i]
                
                for i in range(min(DO_COUNT, len(current_do))):
                    if current_do[i] != self.previous_do_states[i]:
                        status = "🟢 AÇIK" if current_do[i] else "⚫ KAPALI"
                        log.info(f"📤 {DO_LABELS[i]} → {status}")
                        self.previous_do_states[i] = current_do[i]
            except Exception as e:
                pass
            
            time.sleep(0.2)

class Contactor_Logic:
    """
    Finder 22.22.9.024.4000 Kontaktör Simülasyonu
    
    DO HIGH → Kontaktör bobini enerjili → Kontak kapanır → DI = 1
    DO LOW  → Kontaktör bobini enerjisiz → Kontak açılır → DI = 0
    
    Mapping (1:1 DO→DI):
    - DO0 → DI0 (Finder-1: İndüksiyon Ocak)
    - DO1 → DI1 (Finder-2: Bulaşık Makinesi)
    - DO2 → DI2 (Finder-3: Çamaşır Makinesi)
    - DO3 → DI3 (Finder-4: Mikrodalga Fırın)
    - DO4 → DI4 (Finder-5: Rezerv)
    """
    def __init__(self, context):
        self.context = context
        self.running = True
        self.previous_do_states = [0] * DO_COUNT
        
    def simulate(self):
        """DO durumlarını izle ve DI'ları güncelle (DO=DI, 1:1 mapping)"""
        while self.running:
            try:
                slave_id = 0x00
                current_do = self.context[slave_id].getValues(1, START_ADDRESS, DO_COUNT)
                
                for do_index in range(min(DO_COUNT, 5)):  # 5 kontaktör
                    if current_do[do_index] != self.previous_do_states[do_index]:
                        di_index = do_index
                        
                        if current_do[do_index] == 1:
                            self.context[slave_id].setValues(2, di_index, [1])
                            logging.info(f"⚡ Finder-{do_index+1} KONTAKTÖR ÇEKTİ → STATUS=ON (220V AÇ)")
                        else:
                            self.context[slave_id].setValues(2, di_index, [0])
                            logging.info(f"⚡ Finder-{do_index+1} KONTAKTÖR DÜŞTÜ → STATUS=OFF (220V KAPA)")
                        
                        self.previous_do_states[do_index] = current_do[do_index]
                
            except Exception as e:
                logging.error(f"Contactor logic error: {e}")
            
            time.sleep(0.1)
            
# Global simulator instance
monitor = None
contactor_logic = None

def run():
    global monitor, contactor_logic
    
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),
        hr=ModbusSequentialDataBlock(0, [0]*200),
        ir=ModbusSequentialDataBlock(0, [0]*200)
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'Modbus RTU IO 8CH'
    identity.ProductName = f'{DI_COUNT}DI/{DO_COUNT}DO {DEVICE_TYPE}'
    identity.MajorMinorRevision = '2.00'
    
    monitor = DI_DO_Monitor(context)
    monitor_thread = threading.Thread(target=monitor.monitor, daemon=True)
    monitor_thread.start()
    
    contactor_logic = Contactor_Logic(context)
    contactor_thread = threading.Thread(target=contactor_logic.simulate, daemon=True)
    contactor_thread.start()
    
    print("\n" + "="*70)
    print(f"🔌 WAVESHARE {DEVICE_TYPE.upper()} #{DEVICE_NAME} - {DEVICE_DESCRIPTION.upper()}")
    print("="*70)
    print(f"📡 Port: {PORT} | Slave ID: {SLAVE_ID}")
    print("📖 Kontaktör: Finder 22.22.9.024.4000 (25A/2NO, 24V DC)")
    print()
    print("📥 DIGITAL INPUTS (Kontaktör Status):")
    for i, label in enumerate(DI_LABELS):
        print(f"   DI{i}: {label}")
    print()
    print("📤 DIGITAL OUTPUTS (Kontaktör Bobin Kontrol):")
    for i, label in enumerate(DO_LABELS):
        print(f"   DO{i}: {label}")
    print()
    print("⚡ Kontrol: DO HIGH=AÇ, DO LOW=KAPA (sürekli, pulse değil)")
    print("⏳ Bağlantı bekleniyor...")
    print("="*70 + "\n")
    
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", PORT))

if __name__ == "__main__":
    run()
