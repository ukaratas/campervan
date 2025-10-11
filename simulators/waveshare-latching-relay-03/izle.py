#!/usr/bin/env python3
"""
Latching Relay İzleme
Simülatörü gerçek zamanlı izler
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymodbus.client import ModbusTcpClient
import time

# Config import
from config import (
    DEVICE_NAME, PORT, SLAVE_ID, HOST,
    RELAY_COUNT, START_ADDRESS, RELAY_LABELS_WATCH
)

SLAVE = SLAVE_ID
RELAY_LABELS = RELAY_LABELS_WATCH

def main():
    print("\n" + "="*70)
    print(f"👁️  LATCHING RELAY İZLEME - {DEVICE_NAME}")
    print("="*70)
    print(f"📡 Host: {HOST}:{PORT}")
    print("📺 Röle değişiklikleri izleniyor... (Ctrl+C ile çık)\n")
    
    client = ModbusTcpClient(HOST, port=PORT)
    if not client.connect():
        print(f"❌ {HOST}:{PORT}'e bağlanılamadı!")
        print("   Simülatörü başlat: python3 simulator.py")
        sys.exit(1)
    
    print("✅ Bağlandı\n")
    
    previous = [None] * RELAY_COUNT
    
    try:
        while True:
            result = client.read_coils(START_ADDRESS, RELAY_COUNT, slave=SLAVE)
            if result.isError():
                continue
            
            for i in range(RELAY_COUNT):
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

