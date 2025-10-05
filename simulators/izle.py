#!/usr/bin/env python3
"""
Simülatör İzleme Aracı
Işık durumunu sürekli izler ve değişiklikleri gösterir
"""

from pymodbus.client import ModbusTcpClient
import time
import sys

def izle():
    print("\n" + "="*60)
    print("👁️  SİMÜLATÖR İZLEME MODU")
    print("="*60)
    print("Işık durumu sürekli izleniyor...")
    print("Çıkmak için Ctrl+C\n")
    
    client = ModbusTcpClient('localhost', port=5020)
    
    if not client.connect():
        print("❌ Simülatöre bağlanılamadı!")
        sys.exit(1)
    
    print("✅ Bağlantı kuruldu\n")
    
    onceki_durum = None
    
    try:
        while True:
            result = client.read_coils(0, 1)
            durum = result.bits[0]
            
            if durum != onceki_durum:
                timestamp = time.strftime("%H:%M:%S")
                if durum:
                    print(f"[{timestamp}] 💡 Yatak Işık → 🟢 AÇILDI")
                else:
                    print(f"[{timestamp}] 💡 Yatak Işık → ⚫ KAPANDI")
                onceki_durum = durum
            
            time.sleep(0.2)  # 200ms polling
    
    except KeyboardInterrupt:
        print("\n\n👋 İzleme durduruldu")
        client.close()

if __name__ == "__main__":
    izle()

