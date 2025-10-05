#!/usr/bin/env python3
"""
Latching Relay İzleme - Instance 01
Port 5023'teki simülatörü izler
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymodbus.client import ModbusTcpClient
import time

PORT = 5023
SLAVE = 1

RELAY_LABELS = [
    "R0: Mutfak", "R1: Tezgâh", "R2: Orta Alan", "R3: Yatak",
    "R4: Popup", "R5: Sol Okuma", "R6: Sağ Okuma", "R7: Tente"
]

def main():
    print("\n" + "="*70)
    print("👁️  LATCHING RELAY İZLEME - Instance 01")
    print("="*70)
    print(f"📡 Port: {PORT}")
    print("📺 Röle değişiklikleri izleniyor... (Ctrl+C ile çık)\n")
    
    client = ModbusTcpClient('localhost', port=PORT)
    if not client.connect():
        print(f"❌ Port {PORT}'e bağlanılamadı!")
        print("   Simülatörü başlat: python3 simulator.py")
        sys.exit(1)
    
    print("✅ Bağlandı\n")
    
    previous = [None] * 8
    
    try:
        while True:
            result = client.read_coils(0, 8, slave=SLAVE)
            if result.isError():
                continue
            
            for i in range(8):
                if result.bits[i] != previous[i]:
                    status = "🟢 AÇILDI" if result.bits[i] else "⚫ KAPANDI"
                    timestamp = time.strftime("%H:%M:%S")
                    print(f"[{timestamp}] 💡 {RELAY_LABELS[i]} → {status}")
                    previous[i] = result.bits[i]
            
            time.sleep(0.2)
    
    except KeyboardInterrupt:
        print("\n\n👋 İzleme durduruldu\n")
        client.close()

if __name__ == "__main__":
    main()

