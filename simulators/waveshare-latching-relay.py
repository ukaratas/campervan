#!/usr/bin/env python3
"""
Waveshare Modbus RTU 8-ch Latching Relay Module (C) Simulator
8 Kanal Latching (Bistable) Relay Module

Register Map (Waveshare wiki'ye göre):
- Coils (FC01 Read, FC05 Write, FC0F Write Multiple): 0x0000-0x0007 (8 röle)
- Holding Registers (FC03 Read, FC06 Write): 0x0000-0x0007 (8 röle durumu)

Özellikler:
- Latching relay: Durum kalıcı (güç kesilse bile)
- Hem READ hem WRITE destekli
- Multi-instance: Birden fazla modül aynı anda çalışabilir

Multi-instance support: Port ve Slave ID parametre olarak alınır
"""

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging
import threading
import time
import sys
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Relay-%(port)s] - %(message)s',
    datefmt='%H:%M:%S'
)

class WaveshareLatchingRelaySimulator:
    def __init__(self, context, port, instance_name="Relay-1"):
        self.context = context
        self.port = port
        self.instance_name = instance_name
        self.running = True
        
        # 8 röle etiketi (aydınlatma için)
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
        
        self.log = logging.LoggerAdapter(logging.getLogger(), {'port': port})
        
        # Başlangıçta tüm röleler KAPALI
        self._reset_all()
    
    def _reset_all(self):
        """Factory reset - tüm röleleri kapat"""
        slave_id = 0x00
        self.context[slave_id].setValues(1, 0, [0]*8)  # Coils
        self.context[slave_id].setValues(3, 0, [0]*8)  # Holding Registers
        self.log.info("🔄 Factory Reset - Tüm röleler KAPALI")
    
    def monitor_relays(self):
        """Röle durumlarını sürekli izle ve değişiklikleri logla"""
        previous_states = [0] * 8
        last_summary = 0
        
        while self.running:
            slave_id = 0x00
            
            # Coil durumlarını oku (FC01)
            coil_states = self.context[slave_id].getValues(1, 0, 8)
            
            # Holding register'ları coil'lerle sync et (Waveshare davranışı)
            self.context[slave_id].setValues(3, 0, coil_states)
            
            # Değişiklikleri logla
            for i in range(8):
                if coil_states[i] != previous_states[i]:
                    status = "🟢 AÇILDI" if coil_states[i] else "⚫ KAPANDI"
                    self.log.info(f"💡 {self.relay_labels[i]} → {status}")
                    previous_states[i] = coil_states[i]
            
            # Her 10 saniyede özet göster
            if time.time() - last_summary > 10:
                active_count = sum(coil_states)
                if active_count > 0:
                    total_power = sum(self.power_watts[i] for i in range(8) if coil_states[i])
                    self.log.info(f"📊 Aktif: {active_count}/8 röle | Toplam Güç: {total_power}W")
                last_summary = time.time()
            
            time.sleep(0.2)
    
    def set_relay(self, channel, state):
        """Tek röleyi kontrol et (test için)"""
        if channel < 0 or channel > 7:
            self.log.error(f"Geçersiz röle kanal: {channel}")
            return
        
        slave_id = 0x00
        self.context[slave_id].setValues(1, channel, [1 if state else 0])
        status = "AÇILDI" if state else "KAPANDI"
        self.log.info(f"🎮 Manuel: {self.relay_labels[channel]} → {status}")
    
    def show_status(self):
        """Mevcut durumu göster"""
        slave_id = 0x00
        relay_states = self.context[slave_id].getValues(1, 0, 8)
        
        print(f"\n{'='*70}")
        print(f"📊 [{self.instance_name}] RÖLE DURUMLARI")
        print(f"{'='*70}")
        
        active_relays = []
        total_power = 0
        
        for i in range(8):
            status = "🟢 AÇIK" if relay_states[i] else "⚫ KAPALI"
            power = self.power_watts[i] if relay_states[i] else 0
            print(f"   {self.relay_labels[i]}: {status} ({power}W)")
            
            if relay_states[i]:
                active_relays.append(self.relay_labels[i])
                total_power += self.power_watts[i]
        
        print(f"\n📊 Özet: {len(active_relays)}/8 röle aktif | Toplam: {total_power}W")
        print(f"{'='*70}\n")

def run_server(port=5023, slave_id=1, instance_name="Relay-1"):
    """
    Waveshare Latching Relay simülatörü başlat
    
    Args:
        port: TCP port (varsayılan: 5023)
        slave_id: Modbus slave ID (varsayılan: 1)
        instance_name: Instance adı (log için)
    """
    
    # Data Store - Waveshare Latching Relay'e uygun
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*8),    # Coils (8 röle)
        hr=ModbusSequentialDataBlock(0, [0]*200),  # Holding Registers
        ir=ModbusSequentialDataBlock(0, [0]*200)   # Input Registers
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
    simulator = WaveshareLatchingRelaySimulator(context, port, instance_name)
    
    # Monitor thread
    monitor_thread = threading.Thread(target=simulator.monitor_relays, daemon=True)
    monitor_thread.start()
    
    print("\n" + "="*80)
    print(f"💡 WAVESHARE LATCHING RELAY MODULE SIMULATOR - {instance_name}")
    print("="*80)
    print(f"📡 Listening on: 0.0.0.0:{port}")
    print(f"🔌 Modbus TCP - Slave ID: {slave_id}")
    print(f"📖 Wiki: https://www.waveshare.com/wiki/Modbus_RTU_Relay_(C)")
    print()
    print("📋 8x Latching Relays (Coils 0-7):")
    for label in simulator.relay_labels:
        print(f"   {label}")
    print()
    print("📖 Supported Function Codes:")
    print("   FC01 (0x01): Read Coils (röle durumu oku)")
    print("   FC05 (0x05): Write Single Coil (tek röle SET/RESET)")
    print("   FC0F (0x0F): Write Multiple Coils (çoklu röle kontrol)")
    print("   FC03 (0x03): Read Holding Registers (durum oku)")
    print("   FC06 (0x06): Write Single Register (tek röle kontrol)")
    print()
    print("🔑 Latching Relay Özelliği:")
    print("   ✓ Durum kalıcı (güç kesilse bile)")
    print("   ✓ Hem READ hem WRITE destekli")
    print("   ✓ Coil Write: 1=SET (AÇ), 0=RESET (KAPAT)")
    print()
    print("🧪 Interaktif Komutlar:")
    print(f"   simulator.set_relay(3, True)           # R3 (Yatak Işık) AÇ")
    print(f"   simulator.set_relay(3, False)          # R3 (Yatak Işık) KAPAT")
    print(f"   simulator.show_status()                # Tüm röle durumları")
    print()
    print("⏳ Home Assistant bağlantısı bekleniyor...")
    print("="*80 + "\n")
    
    # Server başlat
    StartTcpServer(
        context=context,
        identity=identity,
        address=("0.0.0.0", port)
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Waveshare Latching Relay Module Simulator')
    parser.add_argument('--port', type=int, default=5023, help='TCP port (default: 5023)')
    parser.add_argument('--slave', type=int, default=1, help='Modbus Slave ID (default: 1)')
    parser.add_argument('--name', type=str, default='Relay-1', help='Instance name (default: Relay-1)')
    
    args = parser.parse_args()
    
    print(f"\n🚀 Starting {args.name} on port {args.port}...\n")
    run_server(port=args.port, slave_id=args.slave, instance_name=args.name)

