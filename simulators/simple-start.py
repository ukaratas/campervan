#!/usr/bin/env python3
"""
Basit Başlangıç Simülatörü
1 Push Button + 1 Light için minimal simülasyon

DI/DO + Lighting birleştirilmiş tek simülatör
Port: 5020 (tek port, kolay test)
"""

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging
import threading
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

class SimpleSimulator:
    def __init__(self, context):
        self.context = context
        self.running = True
        
        # Button state tracking için
        self.button_states = {
            'sag_yatak': False,  # DI address 0
        }
        
        # Light state tracking için
        self.light_states = {
            'yatak_alani': False,  # Coil address 0
        }
    
    def press_button(self, button_name='sag_yatak', duration=0.3):
        """
        Push button simülasyonu
        
        Args:
            button_name: 'sag_yatak'
            duration: Basma süresi (saniye)
        """
        slave_id = 0x00
        fx = 2  # Discrete Inputs
        
        button_map = {
            'sag_yatak': 0,
        }
        
        if button_name not in button_map:
            log.error(f"Geçersiz button: {button_name}")
            return
        
        address = button_map[button_name]
        
        # Button PRESSED
        self.context[slave_id].setValues(fx, address, [1])
        self.button_states[button_name] = True
        log.info(f"🔘 [{button_name.upper()}] PRESSED")
        
        # Basılı tutma süresi
        time.sleep(duration)
        
        # Button RELEASED
        self.context[slave_id].setValues(fx, address, [0])
        self.button_states[button_name] = False
        log.info(f"🔘 [{button_name.upper()}] RELEASED")
    
    def monitor_lights(self):
        """Işık durumlarını sürekli izle"""
        while self.running:
            slave_id = 0x00
            fx = 1  # Coils
            
            # Coil 0: Yatak alanı ışığı
            light_value = self.context[slave_id].getValues(fx, 0, 1)[0]
            
            if light_value != self.light_states['yatak_alani']:
                self.light_states['yatak_alani'] = light_value
                
                if light_value:
                    log.info("💡 [YATAK ALANI IŞIK] → 🟢 AÇILDI")
                else:
                    log.info("💡 [YATAK ALANI IŞIK] → ⚫ KAPANDI")
            
            time.sleep(0.5)
    
    def show_status(self):
        """Mevcut durumu göster"""
        print("\n" + "="*60)
        print("📊 MEVCUT DURUM")
        print("="*60)
        print(f"🔘 Sağ Yatak Button: {'BASILI' if self.button_states['sag_yatak'] else 'SERBEST'}")
        print(f"💡 Yatak Alanı Işık: {'🟢 AÇIK' if self.light_states['yatak_alani'] else '⚫ KAPALI'}")
        print("="*60 + "\n")

def run_server():
    # Modbus Data Store
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*8),   # Discrete Inputs (buttons)
        co=ModbusSequentialDataBlock(0, [0]*8),   # Coils (lights)
        hr=ModbusSequentialDataBlock(0, [0]*100),
        ir=ModbusSequentialDataBlock(0, [0]*100)
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device info
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Karavan Project'
    identity.ProductName = 'Simple Test Simulator'
    identity.ModelName = 'v1.0'
    
    # Simulator instance
    global simulator
    simulator = SimpleSimulator(context)
    
    # Monitor thread başlat
    monitor_thread = threading.Thread(target=simulator.monitor_lights, daemon=True)
    monitor_thread.start()
    
    print("\n" + "="*70)
    print("🚀 KARAVAN OTOMASYON - BASİT TEST SİMÜLATÖRÜ")
    print("="*70)
    print("📡 Listening on: 0.0.0.0:5020")
    print("🔌 Modbus TCP - Slave ID: 1")
    print()
    print("📋 Bağlantılar:")
    print("   • Discrete Input 0: Sağ Yatak Push Button")
    print("   • Coil 0: Yatak Alanı Işık")
    print()
    print("🧪 Test Komutları (Python console'da):")
    print("   simulator.press_button('sag_yatak')           # Normal basma")
    print("   simulator.press_button('sag_yatak', 0.8)      # Long press")
    print("   simulator.show_status()                       # Durum göster")
    print()
    print("⏳ Home Assistant bağlantısı bekleniyor...")
    print("="*70 + "\n")
    
    # Server başlat
    StartTcpServer(
        context=context,
        identity=identity,
        address=("0.0.0.0", 5020)
    )

if __name__ == "__main__":
    run_server()

