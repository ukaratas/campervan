#!/usr/bin/env python3
"""
Waveshare Modbus RTU 8-ch Latching Relay Module (C) Simulator
Gerçek cihazın davranışını simüle eder

Register Map (Waveshare'e göre):
- Coils (FC01 Read, FC05 Write, FC0F Write Multiple): 0x0000-0x0007 (8 röle)
- Holding Registers (FC03 Read, FC06 Write): 0x0000-0x0007 (8 röle durumu)
"""

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging
import threading
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

class LatchingRelaySimulator:
    def __init__(self, context):
        self.context = context
        self.running = True
        
        # 8 röle etiketi
        self.relay_labels = [
            "R0: Mutfak Işık",
            "R1: Mutfak Tezgâh Işık",
            "R2: Orta Alan Işık",
            "R3: Yatak Alanı Işık",
            "R4: Popup Yatak Işık",
            "R5: Sol Okuma Işık",
            "R6: Sağ Okuma Işık",
            "R7: Tente Işık"
        ]
        
        # Röle güç tüketimleri (W)
        self.power_watts = [8, 7, 12, 14, 6, 4, 4, 12]
        
        # Başlangıçta tüm röleler KAPALI
        slave_id = 0x00
        self.context[slave_id].setValues(1, 0, [0]*8)  # Coils
        self.context[slave_id].setValues(3, 0, [0]*8)  # Holding Registers
    
    def monitor_relays(self):
        """Röle durumlarını sürekli izle ve logla"""
        previous_states = [0] * 8
        
        while self.running:
            slave_id = 0x00
            
            # Coil durumlarını oku
            coil_states = self.context[slave_id].getValues(1, 0, 8)
            
            # Holding register'ları coil'lerle sync et
            self.context[slave_id].setValues(3, 0, coil_states)
            
            # Değişiklikleri logla
            for i in range(8):
                if coil_states[i] != previous_states[i]:
                    status = "🟢 AÇILDI" if coil_states[i] else "⚫ KAPANDI"
                    timestamp = time.strftime("%H:%M:%S")
                    log.info(f"[{timestamp}] 💡 {self.relay_labels[i]} → {status}")
                    previous_states[i] = coil_states[i]
            
            # Toplam güç hesapla
            total_power = sum(self.power_watts[i] for i in range(8) if coil_states[i])
            
            # Aktif röleleri göster (her 5 saniyede)
            if int(time.time()) % 5 == 0:
                active = [self.relay_labels[i] for i in range(8) if coil_states[i]]
                if active:
                    log.info(f"📊 Aktif Röleler: {len(active)}/8 | Toplam Güç: {total_power}W")
            
            time.sleep(0.2)
    
    def reset_all_relays(self):
        """Tüm röleleri kapat (factory reset)"""
        slave_id = 0x00
        self.context[slave_id].setValues(1, 0, [0]*8)
        self.context[slave_id].setValues(3, 0, [0]*8)
        log.info("🔄 Tüm röleler sıfırlandı (KAPALI)")

def run_server():
    # Data Store - Waveshare'e uygun
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs (kullanılmıyor)
        co=ModbusSequentialDataBlock(0, [0]*8),    # Coils (8 röle durumu)
        hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers (8 röle + config)
        ir=ModbusSequentialDataBlock(0, [0]*100)   # Input Registers
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device identification
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'Modbus RTU Relay (C)'
    identity.VendorUrl = 'https://www.waveshare.com'
    identity.ProductName = 'Modbus RTU 8-ch Latching Relay Module'
    identity.ModelName = 'Latching Relay (C)'
    identity.MajorMinorRevision = '3.00'
    
    # Simulator instance
    global simulator
    simulator = LatchingRelaySimulator(context)
    
    # Monitor thread
    monitor_thread = threading.Thread(target=simulator.monitor_relays, daemon=True)
    monitor_thread.start()
    
    print("\n" + "="*70)
    print("🔌 WAVESHARE LATCHING RELAY MODULE SIMULATOR")
    print("="*70)
    print("📡 Listening on: 0.0.0.0:5023")
    print("🔌 Modbus TCP - Slave ID: 1")
    print()
    print("📋 8 Kanal Latching Relay:")
    for i, label in enumerate(simulator.relay_labels):
        print(f"   Coil {i}: {label}")
    print()
    print("📖 Supported Function Codes:")
    print("   FC01 (0x01): Read Coils (röle durumu oku)")
    print("   FC05 (0x05): Write Single Coil (tek röle kontrol)")
    print("   FC0F (0x0F): Write Multiple Coils (çoklu röle kontrol)")
    print("   FC03 (0x03): Read Holding Registers (durum oku)")
    print("   FC06 (0x06): Write Single Register (tek röle kontrol)")
    print()
    print("🧪 Test Komutları:")
    print("   simulator.reset_all_relays()  # Tüm röleleri kapat")
    print()
    print("⏳ Home Assistant bağlantısı bekleniyor...")
    print("="*70 + "\n")
    
    # Server başlat
    StartTcpServer(
        context=context,
        identity=identity,
        address=("0.0.0.0", 5023)
    )

if __name__ == "__main__":
    run_server()

