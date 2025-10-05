#!/usr/bin/env python3
"""
Waveshare Modbus RTU IO 8CH Simulator
8-Ch Digital Input / 8-Ch Digital Output Module

Register Map (Waveshare wiki'ye göre):
- Discrete Inputs (FC02): 0x0000-0x0007 (8 DI channels - push buttons)
- Coils (FC01/FC05): 0x0000-0x0007 (8 DO channels - relay triggers)
- Input Registers (FC04): 0x0000-0x0007 (DI status as registers)
- Holding Registers (FC03/FC06): 0x0000-0x0007 (DO control mode)

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
    format='%(asctime)s - [DI/DO-%(port)s] - %(message)s',
    datefmt='%H:%M:%S'
)

class WaveshareDI_DO_Simulator:
    def __init__(self, context, port, instance_name="DI/DO-1"):
        self.context = context
        self.port = port
        self.instance_name = instance_name
        self.running = True
        
        # 8 DI etiketi (push buttons)
        self.di_labels = [
            "DI0: Sağ Yatak Button",
            "DI1: Sol Yatak Button",
            "DI2: Popup Yatak Button",
            "DI3: Dış Aydınlatma Button",
            "DI4: Basamak Button",
            "DI5: Mutfak Button",
            "DI6: Orta Alan Button",
            "DI7: Banyo Button"
        ]
        
        # 8 DO etiketi (bistable relay triggers)
        self.do_labels = [
            "DO0: Buzdolabı Tetik",
            "DO1: Hidrofor Tetik",
            "DO2: 24V Klima Tetik",
            "DO3: Truma Combi Tetik",
            "DO4: USB Şarj Tetik",
            "DO5: 24V Çıkış Tetik",
            "DO6: 12V Çıkış Tetik",
            "DO7: Rezerv"
        ]
        
        self.log = logging.LoggerAdapter(logging.getLogger(), {'port': port})
    
    def press_button(self, di_channel, duration=0.3):
        """
        Push button basma simülasyonu
        
        Args:
            di_channel: 0-7 arası DI kanalı
            duration: Basma süresi (saniye)
        """
        if di_channel < 0 or di_channel > 7:
            self.log.error(f"Geçersiz DI kanal: {di_channel}")
            return
        
        slave_id = 0x00
        fx_di = 2  # Discrete Inputs
        fx_ir = 4  # Input Registers
        
        # Button PRESSED
        self.context[slave_id].setValues(fx_di, di_channel, [1])
        self.context[slave_id].setValues(fx_ir, di_channel, [1])
        self.log.info(f"🔘 {self.di_labels[di_channel]} → BASILDI")
        
        time.sleep(duration)
        
        # Button RELEASED
        self.context[slave_id].setValues(fx_di, di_channel, [0])
        self.context[slave_id].setValues(fx_ir, di_channel, [0])
        self.log.info(f"🔘 {self.di_labels[di_channel]} → BIRAKILDI")
    
    def monitor_outputs(self):
        """DO çıkışlarını izle (pulse detection)"""
        previous_do = [0] * 8
        
        while self.running:
            slave_id = 0x00
            fx_coil = 1  # Coils (DO)
            
            current_do = self.context[slave_id].getValues(fx_coil, 0, 8)
            
            for i in range(8):
                if current_do[i] != previous_do[i]:
                    if current_do[i]:
                        self.log.info(f"⚡ {self.do_labels[i]} → PULSE START")
                    else:
                        self.log.info(f"⚡ {self.do_labels[i]} → PULSE END")
                    previous_do[i] = current_do[i]
            
            time.sleep(0.1)
    
    def show_status(self):
        """Mevcut durumu göster"""
        slave_id = 0x00
        di_values = self.context[slave_id].getValues(2, 0, 8)  # Discrete Inputs
        do_values = self.context[slave_id].getValues(1, 0, 8)  # Coils
        
        print(f"\n{'='*70}")
        print(f"📊 [{self.instance_name}] DURUM")
        print(f"{'='*70}")
        print("🔘 Digital Inputs (Push Buttons):")
        for i in range(8):
            status = "🟢 BASILI" if di_values[i] else "⚫ SERBEST"
            print(f"   {self.di_labels[i]}: {status}")
        
        print("\n⚡ Digital Outputs (Relay Triggers):")
        for i in range(8):
            status = "🟢 ACTIVE" if do_values[i] else "⚫ INACTIVE"
            print(f"   {self.do_labels[i]}: {status}")
        print(f"{'='*70}\n")

def run_server(port=5022, slave_id=1, instance_name="DI/DO-1"):
    """
    Waveshare DI/DO simülatörü başlat
    
    Args:
        port: TCP port (varsayılan: 5022)
        slave_id: Modbus slave ID (varsayılan: 1)
        instance_name: Instance adı (log için)
    """
    
    # Data Store - Waveshare DI/DO'ya uygun
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*8),    # Discrete Inputs (DI channels)
        co=ModbusSequentialDataBlock(0, [0]*8),    # Coils (DO channels)
        hr=ModbusSequentialDataBlock(0, [0]*200),  # Holding Registers (config)
        ir=ModbusSequentialDataBlock(0, [0]*200)   # Input Registers (DI status)
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device identification
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Waveshare'
    identity.ProductCode = 'Modbus RTU IO 8CH'
    identity.VendorUrl = 'https://www.waveshare.com'
    identity.ProductName = 'Industrial 8-Ch Digital Input & Output Module'
    identity.ModelName = 'DI/DO 8CH'
    identity.MajorMinorRevision = '2.00'
    
    # Simulator instance
    global simulator
    simulator = WaveshareDI_DO_Simulator(context, port, instance_name)
    
    # Monitor thread
    monitor_thread = threading.Thread(target=simulator.monitor_outputs, daemon=True)
    monitor_thread.start()
    
    print("\n" + "="*80)
    print(f"🔌 WAVESHARE DI/DO MODULE SIMULATOR - {instance_name}")
    print("="*80)
    print(f"📡 Listening on: 0.0.0.0:{port}")
    print(f"🔌 Modbus TCP - Slave ID: {slave_id}")
    print(f"📖 Wiki: https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH")
    print()
    print("📋 8x Digital Inputs (Discrete Inputs 0-7):")
    for label in simulator.di_labels:
        print(f"   {label}")
    print()
    print("📋 8x Digital Outputs (Coils 0-7):")
    for label in simulator.do_labels:
        print(f"   {label}")
    print()
    print("📖 Supported Function Codes:")
    print("   FC01 (0x01): Read Coils (DO durumu)")
    print("   FC02 (0x02): Read Discrete Inputs (DI durumu)")
    print("   FC04 (0x04): Read Input Registers (DI durumu - register)")
    print("   FC05 (0x05): Write Single Coil (tek DO kontrol)")
    print("   FC0F (0x0F): Write Multiple Coils (çoklu DO kontrol)")
    print()
    print("🧪 Interaktif Komutlar:")
    print(f"   simulator.press_button(0)              # DI0 basma simülasyonu")
    print(f"   simulator.press_button(0, 1.0)         # DI0 long press (1 saniye)")
    print(f"   simulator.show_status()                # Tüm DI/DO durumunu göster")
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
    parser = argparse.ArgumentParser(description='Waveshare DI/DO Module Simulator')
    parser.add_argument('--port', type=int, default=5022, help='TCP port (default: 5022)')
    parser.add_argument('--slave', type=int, default=1, help='Modbus Slave ID (default: 1)')
    parser.add_argument('--name', type=str, default='DI/DO-1', help='Instance name (default: DI/DO-1)')
    
    args = parser.parse_args()
    
    print(f"\n🚀 Starting {args.name} on port {args.port}...\n")
    run_server(port=args.port, slave_id=args.slave, instance_name=args.name)

