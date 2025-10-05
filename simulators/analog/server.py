#!/usr/bin/env python3
"""
Waveshare Analog Acquisition Module Simulator (8 Kanal)
IP: 0.0.0.0 (localhost)
Port: 5024
Slave ID: 1

Su tank seviye sensörleri
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

class WaterTankSimulator:
    def __init__(self, context):
        self.context = context
        self.running = True
        self.fresh_water_level = 75.0  # %75 dolu
        self.grey_water_level = 25.0   # %25 dolu
        
    def simulate_water_usage(self):
        """Su kullanımı simülasyonu"""
        while self.running:
            slave_id = 0x00
            fx = 4  # Input registers
            
            # Temiz su yavaşça azalır
            if random.random() < 0.3:  # %30 şans
                self.fresh_water_level -= random.uniform(0.1, 0.5)
                self.fresh_water_level = max(0, self.fresh_water_level)
            
            # Gri su yavaşça artar
            if random.random() < 0.2:  # %20 şans
                self.grey_water_level += random.uniform(0.1, 0.4)
                self.grey_water_level = min(100, self.grey_water_level)
            
            # Seviyeleri register'lara yaz (x10 çarpanı ile)
            fresh_level_reg = int(self.fresh_water_level * 10)
            grey_level_reg = int(self.grey_water_level * 10)
            
            # Hacim hesapla
            fresh_volume = int(150 * self.fresh_water_level / 100)  # 150L max
            grey_volume = int(120 * self.grey_water_level / 100)    # 120L max
            
            # Register'lara yaz
            values = [
                fresh_level_reg,  # AI1: Temiz su %
                grey_level_reg,   # AI2: Gri su %
                0, 0, 0, 0, 0, 0  # AI3-AI8: Rezerv
            ]
            self.context[slave_id].setValues(fx, 0, values)
            
            # Hacim değerleri (address 100-101)
            self.context[slave_id].setValues(fx, 100, [fresh_volume, grey_volume])
            
            log.info(f"Temiz Su: {self.fresh_water_level:.1f}% ({fresh_volume}L) | "
                    f"Gri Su: {self.grey_water_level:.1f}% ({grey_volume}L)")
            
            # Uyarılar
            if self.fresh_water_level < 15:
                log.warning(f"⚠️  DÜŞÜK TEMİZ SU SEVİYESİ: {self.fresh_water_level:.1f}%")
            if self.grey_water_level > 85:
                log.warning(f"⚠️  YÜKSEK GRİ SU SEVİYESİ: {self.grey_water_level:.1f}%")
            
            time.sleep(5)
    
    def refill_fresh_water(self):
        """Temiz su tankını doldur"""
        self.fresh_water_level = 100.0
        log.info("✅ Temiz su tankı dolduruldu!")
    
    def drain_grey_water(self):
        """Gri su tankını boşalt"""
        self.grey_water_level = 0.0
        log.info("✅ Gri su tankı boşaltıldı!")

def run_server():
    # Data Store
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),
        hr=ModbusSequentialDataBlock(0, [0]*100),
        ir=ModbusSequentialDataBlock(0, [0]*200)  # Input registers (sensör verileri)
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device identification
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'ANALOG-8CH'
    identity.VendorUrl = 'https://www.waveshare.com'
    identity.ProductName = 'Industrial 8-Ch Analog Acquisition Module'
    identity.ModelName = 'Analog Input Module'
    identity.MajorMinorRevision = '1.0.0'
    
    # Simulator
    simulator = WaterTankSimulator(context)
    monitor_thread = threading.Thread(target=simulator.simulate_water_usage, daemon=True)
    monitor_thread.start()
    
    print("\n" + "="*60)
    print("Waveshare Analog Module Simulator (Water Tanks)")
    print("="*60)
    print(f"Listening on: 0.0.0.0:5024")
    print(f"Slave ID: 1")
    print(f"Input Register 0: Temiz su seviyesi (0-1000 = 0-100%)")
    print(f"Input Register 1: Gri su seviyesi (0-1000 = 0-100%)")
    print(f"Input Register 100: Temiz su hacim (L)")
    print(f"Input Register 101: Gri su hacim (L)")
    print("\nTest komutları:")
    print("  simulator.refill_fresh_water()  # Temiz su doldur")
    print("  simulator.drain_grey_water()    # Gri su boşalt")
    print("="*60 + "\n")
    
    globals()['simulator'] = simulator
    
    StartTcpServer(
        context=context,
        identity=identity,
        address=("0.0.0.0", 5024)
    )

if __name__ == "__main__":
    run_server()

