#!/usr/bin/env python3
"""
Button Press Tester
Simülatörün çalıştığı sırada button basma simüle et
"""

import socket
import struct
import time

def send_button_press(host='localhost', port=5020, address=0, duration=0.3):
    """
    Modbus TCP üzerinden Discrete Input'u simüle et
    Trick: Context'e doğrudan yazıyoruz (simülasyon için)
    """
    # Modbus Write Coil (Function Code 5) - Holding Register yerine
    # Discrete Input simülasyonu için özel bir yöntem lazım
    
    # Basit çözüm: Simülatörün stdin'inden komut gönder
    print(f"🔘 Button Press Simulating...")
    print(f"   Address: {address}")
    print(f"   Duration: {duration}s")
    print()
    print("⚠️  Bu fonksiyon geliştiriliyor...")
    print("    Şimdilik simülatör terminalinde şunu çalıştır:")
    print(f"    simulator.press_button('sag_yatak', {duration})")

def main():
    print("\n" + "="*60)
    print("🔘 BUTTON PRESS TESTER")
    print("="*60)
    print()
    print("📝 Kullanım:")
    print("   1. Simülatör terminaline git")
    print("   2. Ctrl+Z bas (pause)")
    print("   3. Şunu yaz:")
    print()
    print("      simulator.press_button('sag_yatak')")
    print()
    print("   4. Enter'a bas")
    print("   5. 'fg' yaz ve Enter (devam et)")
    print()
    print("="*60)
    print()
    print("💡 DAHA KOLAY YOL:")
    print("   Home Assistant'tan manuel button entity oluştur!")
    print()
    
    input("Enter'a bas...")

if __name__ == "__main__":
    main()

