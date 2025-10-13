#!/usr/bin/env python3
"""
DI/DO İzleme
Digital Input ve Digital Output değişikliklerini gerçek zamanlı izler
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymodbus.client import ModbusTcpClient
import time

# Config import
from config import (
    DEVICE_NAME, PORT, SLAVE_ID, HOST,
    DI_COUNT, DO_COUNT, START_ADDRESS,
    DI_LABELS, DO_LABELS
)

SLAVE = SLAVE_ID

def main():
    print("\n" + "="*70)
    print(f"👁️  DI/DO İZLEME - {DEVICE_NAME}")
    print("="*70)
    print(f"📡 Host: {HOST}:{PORT}")
    print("📺 DI/DO değişiklikleri izleniyor... (Ctrl+C ile çık)\n")
    
    client = ModbusTcpClient(HOST, port=PORT)
    if not client.connect():
        print(f"❌ {HOST}:{PORT}'e bağlanılamadı!")
        print("   Simülatörü başlat: python3 simulator.py")
        sys.exit(1)
    
    print("✅ Bağlandı\n")
    
    previous_di = [None] * DI_COUNT
    previous_do = [None] * DO_COUNT
    
    try:
        while True:
            # Digital Input'ları oku
            di_result = client.read_discrete_inputs(START_ADDRESS, DI_COUNT, slave=SLAVE)
            if not di_result.isError():
                for i in range(DI_COUNT):
                    if di_result.bits[i] != previous_di[i]:
                        status = "🟢 AKTIF" if di_result.bits[i] else "⚫ PASIF"
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[{timestamp}] 📥 {DI_LABELS[i]} → {status}")
                        previous_di[i] = di_result.bits[i]
            
            # Digital Output'ları oku
            do_result = client.read_coils(START_ADDRESS, DO_COUNT, slave=SLAVE)
            if not do_result.isError():
                for i in range(DO_COUNT):
                    if do_result.bits[i] != previous_do[i]:
                        status = "🟢 AÇIK" if do_result.bits[i] else "⚫ KAPALI"
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[{timestamp}] 📤 {DO_LABELS[i]} → {status}")
                        previous_do[i] = do_result.bits[i]
            
            time.sleep(0.2)
    
    except KeyboardInterrupt:
        print("\n\n👋 İzleme durduruldu\n")
        client.close()

if __name__ == "__main__":
    main()

