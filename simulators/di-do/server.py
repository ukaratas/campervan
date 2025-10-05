#!/usr/bin/env python3
"""
Waveshare DI/DO Module Simulator
IP: 0.0.0.0 (localhost)
Port: 5022
Slave ID: 1

Digital Inputs (DI): 8 push buttons (Discrete Inputs, address 0-7)
Digital Outputs (DO): 8 bistable relay triggers (Coils, address 0-7)
"""

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging
import threading
import time

# Logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

class DI_DO_Simulator:
    def __init__(self, context):
        self.context = context
        self.running = True
        
    def simulate_button_press(self, button_id):
        """Simüle button press (DI girişi)"""
        slave_id = 0x00
        fx = 2  # Discrete Inputs
        address = button_id
        
        # Button press (1)
        self.context[slave_id].setValues(fx, address, [1])
        log.info(f"Button {button_id + 1} PRESSED")
        
        # 500ms sonra release
        time.sleep(0.5)
        self.context[slave_id].setValues(fx, address, [0])
        log.info(f"Button {button_id + 1} RELEASED")
    
    def monitor_outputs(self):
        """DO çıkışlarını izle"""
        while self.running:
            slave_id = 0x00
            fx = 1  # Coils
            values = self.context[slave_id].getValues(fx, 0, 8)
            
            status = []
            labels = [
                "Buzdolabı", "Hidrofor", "24V Klima", "Truma Combi",
                "USB Şarj", "24V Çıkış", "12V Çıkış", "Rezerv"
            ]
            
            for i, val in enumerate(values):
                if val:
                    status.append(f"{labels[i]}: ON")
            
            if status:
                log.info(f"Active Outputs: {', '.join(status)}")
            
            time.sleep(5)

def run_server():
    # Data Store
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*8),   # 8 Digital Inputs (push buttons)
        co=ModbusSequentialDataBlock(0, [0]*8),   # 8 Coils (DO outputs)
        hr=ModbusSequentialDataBlock(0, [0]*100), # Holding registers
        ir=ModbusSequentialDataBlock(0, [0]*100)  # Input registers
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device identification
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'DI-DO-8CH'
    identity.VendorUrl = 'https://www.waveshare.com'
    identity.ProductName = 'Industrial 8-Ch Digital Input & Output Module'
    identity.ModelName = 'DI-DO Module'
    identity.MajorMinorRevision = '1.0.0'
    
    # Simulator instance
    simulator = DI_DO_Simulator(context)
    
    # Monitor thread
    monitor_thread = threading.Thread(target=simulator.monitor_outputs, daemon=True)
    monitor_thread.start()
    
    # Server başlat
    print("\n" + "="*60)
    print("Waveshare DI/DO Module Simulator")
    print("="*60)
    print(f"Listening on: 0.0.0.0:5022")
    print(f"Slave ID: 1")
    print(f"Digital Inputs (DI): 8 push buttons (address 0-7)")
    print(f"Digital Outputs (DO): 8 relay triggers (address 0-7)")
    print("\nTest için Python console'dan:")
    print("  simulator.simulate_button_press(0)  # Sağ yatak button")
    print("="*60 + "\n")
    
    # Global erişim için
    globals()['simulator'] = simulator
    
    StartTcpServer(
        context=context,
        identity=identity,
        address=("0.0.0.0", 5022)
    )

if __name__ == "__main__":
    run_server()

