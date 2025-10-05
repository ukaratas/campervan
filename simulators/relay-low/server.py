#!/usr/bin/env python3
"""
Waveshare Low Latching Relay Module Simulator (8 Kanal)
IP: 0.0.0.0 (localhost)
Port: 5023
Slave ID: 1

Aydınlatma kontrol röleleri
"""

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging
import threading
import time
import random

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

class LightingSimulator:
    def __init__(self, context):
        self.context = context
        self.running = True
        self.labels = [
            "Mutfak", "Mutfak Tezgâh", "Orta Alan", "Yatak Alanı",
            "Popup Yatak", "Sol Okuma", "Sağ Okuma", "Tente"
        ]
        self.power_watts = [8, 7, 12, 14, 6, 4, 4, 12]  # Her LED'in gücü
        
    def update_power_consumption(self):
        """LED güç tüketimini güncelle"""
        while self.running:
            slave_id = 0x00
            fx_coil = 1  # Coils (röle durumu)
            fx_input = 4  # Input registers (güç tüketimi)
            
            coil_values = self.context[slave_id].getValues(fx_coil, 0, 8)
            power_values = []
            total_power = 0
            
            for i, is_on in enumerate(coil_values):
                if is_on:
                    power = self.power_watts[i]
                    power_values.append(power)
                    total_power += power
                else:
                    power_values.append(0)
            
            # Input register'lara güç değerlerini yaz
            self.context[slave_id].setValues(fx_input, 0, power_values)
            self.context[slave_id].setValues(fx_input, 100, [total_power])  # Toplam güç
            
            # Aktif ışıkları logla
            active = [self.labels[i] for i, v in enumerate(coil_values) if v]
            if active:
                log.info(f"Active Lights: {', '.join(active)} | Total: {total_power}W")
            
            time.sleep(3)

def run_server():
    # Data Store
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*8),   # Discrete inputs (röle geri bildirimi)
        co=ModbusSequentialDataBlock(0, [0]*8),   # Coils (röle kontrol)
        hr=ModbusSequentialDataBlock(0, [0]*100), # Holding registers
        ir=ModbusSequentialDataBlock(0, [0]*100)  # Input registers (güç tüketimi)
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device identification
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'RELAY-LATCH-8CH'
    identity.VendorUrl = 'https://www.waveshare.com'
    identity.ProductName = 'Modbus RTU 8-ch Latching Relay Module'
    identity.ModelName = 'Low Power Latching Relay'
    identity.MajorMinorRevision = '1.0.0'
    
    # Simulator
    simulator = LightingSimulator(context)
    monitor_thread = threading.Thread(target=simulator.update_power_consumption, daemon=True)
    monitor_thread.start()
    
    print("\n" + "="*60)
    print("Waveshare Low Latching Relay Module Simulator (Lighting)")
    print("="*60)
    print(f"Listening on: 0.0.0.0:5023")
    print(f"Slave ID: 1")
    print(f"Coils (0-7): Aydınlatma kontrol")
    print(f"Input Registers (0-7): LED güç tüketimi (W)")
    print(f"Input Register 100: Toplam güç tüketimi (W)")
    print("="*60 + "\n")
    
    globals()['simulator'] = simulator
    
    StartTcpServer(
        context=context,
        identity=identity,
        address=("0.0.0.0", 5023)
    )

if __name__ == "__main__":
    run_server()

