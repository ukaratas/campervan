#!/usr/bin/env python3
"""
Latching Relay Kontrol Aracı
Komut satırından röle kontrolü
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymodbus.client import ModbusTcpClient

PORT = 5023
SLAVE = 1

RELAY_LABELS = [
    "Mutfak", "Tezgâh", "Orta Alan", "Yatak Alanı",
    "Popup", "Sol Okuma", "Sağ Okuma", "Tente"
]

def connect():
    client = ModbusTcpClient('localhost', port=PORT)
    if client.connect():
        return client
    print(f"❌ Port {PORT}'e bağlanılamadı!")
    print("   Simülatörün çalıştığından emin ol:")
    print("   python3 simulator.py")
    sys.exit(1)

def ac(role):
    """Röleyi aç"""
    client = connect()
    client.write_coil(role, True, slave=SLAVE)
    print(f"💡 {RELAY_LABELS[role]} → 🟢 AÇILDI")
    client.close()

def kapat(role):
    """Röleyi kapat"""
    client = connect()
    client.write_coil(role, False, slave=SLAVE)
    print(f"💡 {RELAY_LABELS[role]} → ⚫ KAPANDI")
    client.close()

def toggle(role):
    """Röleyi toggle et"""
    client = connect()
    result = client.read_coils(role, 1, slave=SLAVE)
    yeni = not result.bits[0]
    client.write_coil(role, yeni, slave=SLAVE)
    print(f"💡 {RELAY_LABELS[role]} → {'🟢 AÇILDI' if yeni else '⚫ KAPANDI'}")
    client.close()

def durum():
    """Tüm röle durumlarını göster"""
    client = connect()
    result = client.read_coils(0, 8, slave=SLAVE)
    
    print("\n" + "="*50)
    print("📊 RÖLE DURUMLARI")
    print("="*50)
    
    bits = result.bits if hasattr(result, 'bits') else []
    for i in range(8):
        status = "🟢 AÇIK" if (i < len(bits) and bits[i]) else "⚫ KAPALI"
        print(f"   R{i} {RELAY_LABELS[i]}: {status}")
    print("="*50 + "\n")
    client.close()

def tumunu_kapat():
    """Tüm röleleri kapat"""
    client = connect()
    client.write_coils(0, [False]*8, slave=SLAVE)
    print("⚫ Tüm ışıklar KAPANDI")
    client.close()

def yardim():
    print("\n" + "="*60)
    print("🎮 LATCHING RELAY KONTROL - Instance 01")
    print("="*60)
    print("\nKullanım: python3 kontrol.py <komut> [role]")
    print("\nKomutlar:")
    print("  ac <0-7>      - Röleyi aç")
    print("  kapat <0-7>   - Röleyi kapat")
    print("  toggle <0-7>  - Röleyi toggle et")
    print("  durum         - Tüm röle durumlarını göster")
    print("  tumunu-kapat  - Tüm röleleri kapat")
    print("\nRöle Listesi:")
    for i, label in enumerate(RELAY_LABELS):
        print(f"  {i}: {label}")
    print("\nÖrnekler:")
    print("  python3 kontrol.py ac 3         # Yatak Alanı Işık aç")
    print("  python3 kontrol.py toggle 0     # Mutfak Işık toggle")
    print("  python3 kontrol.py durum        # Tüm durumları göster")
    print("="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        yardim()
        sys.exit(0)
    
    komut = sys.argv[1].lower()
    
    if komut in ["ac", "kapat", "toggle"]:
        if len(sys.argv) < 3:
            print("❌ Röle numarası gerekli! (0-7)")
            sys.exit(1)
        role = int(sys.argv[2])
        if role < 0 or role > 7:
            print("❌ Geçersiz röle numarası! (0-7)")
            sys.exit(1)
        
        if komut == "ac":
            ac(role)
        elif komut == "kapat":
            kapat(role)
        elif komut == "toggle":
            toggle(role)
    elif komut == "durum":
        durum()
    elif komut == "tumunu-kapat":
        tumunu_kapat()
    else:
        print(f"❌ Bilinmeyen komut: {komut}")
        yardim()
        sys.exit(1)

