#!/usr/bin/env python3
"""
Simülatör Kontrol Aracı
Komut satırından simülatöre komut gönder
"""

from pymodbus.client import ModbusTcpClient
import sys
import time

def connect():
    """Simülatöre bağlan"""
    client = ModbusTcpClient('localhost', port=5020)
    if client.connect():
        return client
    else:
        print("❌ Simülatöre bağlanılamadı!")
        print("   Simülatörün çalıştığından emin ol:")
        print("   python3 simple-start.py")
        sys.exit(1)

def isik_ac():
    """Işığı aç"""
    client = connect()
    client.write_coil(0, True)
    print("💡 Yatak Işık → 🟢 AÇILDI")
    client.close()

def isik_kapat():
    """Işığı kapat"""
    client = connect()
    client.write_coil(0, False)
    print("💡 Yatak Işık → ⚫ KAPANDI")
    client.close()

def isik_toggle():
    """Işığı toggle et (aç/kapa)"""
    client = connect()
    result = client.read_coils(0, 1)
    yeni_durum = not result.bits[0]
    client.write_coil(0, yeni_durum)
    print(f"💡 Yatak Işık → {'🟢 AÇILDI' if yeni_durum else '⚫ KAPANDI'}")
    client.close()

def isik_durum():
    """Işık durumunu oku"""
    client = connect()
    result = client.read_coils(0, 1)
    durum = "🟢 AÇIK" if result.bits[0] else "⚫ KAPALI"
    print(f"📊 Yatak Işık durumu: {durum}")
    client.close()

def yanip_son(kez=3):
    """Işığı yanıp sön (blink)"""
    client = connect()
    print(f"💡 {kez}x Yanıp Sön başlıyor...")
    for i in range(kez):
        client.write_coil(0, True)
        print(f"   {i+1}. AÇ", end='', flush=True)
        time.sleep(0.3)
        client.write_coil(0, False)
        print(" → KAPAT")
        time.sleep(0.3)
    print("✅ Tamamlandı!")
    client.close()

def yardim():
    """Yardım mesajı"""
    print("\n" + "="*60)
    print("🎮 SİMÜLATÖR KONTROL ARACI")
    print("="*60)
    print("\nKullanım:")
    print("  python3 kontrol.py <komut>")
    print("\nKomutlar:")
    print("  ac          - Işığı aç")
    print("  kapat       - Işığı kapat")
    print("  toggle      - Işığı aç/kapa (toggle)")
    print("  durum       - Mevcut durumu göster")
    print("  blink [N]   - N kez yanıp sön (varsayılan: 3)")
    print("  yardim      - Bu mesajı göster")
    print("\nÖrnekler:")
    print("  python3 kontrol.py ac")
    print("  python3 kontrol.py toggle")
    print("  python3 kontrol.py blink 5")
    print("="*60 + "\n")

def main():
    if len(sys.argv) < 2:
        yardim()
        sys.exit(0)
    
    komut = sys.argv[1].lower()
    
    if komut == "ac":
        isik_ac()
    elif komut == "kapat":
        isik_kapat()
    elif komut == "toggle":
        isik_toggle()
    elif komut == "durum":
        isik_durum()
    elif komut == "blink":
        kez = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        yanip_son(kez)
    elif komut == "yardim" or komut == "help":
        yardim()
    else:
        print(f"❌ Bilinmeyen komut: {komut}")
        print("   Yardım için: python3 kontrol.py yardim")
        sys.exit(1)

if __name__ == "__main__":
    main()

