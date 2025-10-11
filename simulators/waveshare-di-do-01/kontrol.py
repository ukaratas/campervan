#!/usr/bin/env python3
"""
DI/DO Kontrol Aracı
Digital Output (DO) kontrolü ve Digital Input (DI) okuma
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymodbus.client import ModbusTcpClient

# Config import
from config import (
    DEVICE_NAME, PORT, SLAVE_ID, HOST,
    DI_COUNT, DO_COUNT, START_ADDRESS,
    DI_LABELS_SHORT, DO_LABELS_SHORT
)

SLAVE = SLAVE_ID

def connect():
    client = ModbusTcpClient(HOST, port=PORT)
    if client.connect():
        return client
    print(f"❌ {HOST}:{PORT}'e bağlanılamadı!")
    print("   Simülatörün çalıştığından emin ol:")
    print("   python3 simulator.py")
    sys.exit(1)

# ========== DIGITAL OUTPUT (DO) İşlemleri ==========

def do_ac(do_num):
    """Digital Output'u aç"""
    client = connect()
    client.write_coil(do_num, True, slave=SLAVE)
    print(f"📤 {DO_LABELS_SHORT[do_num]} → 🟢 AÇILDI")
    client.close()

def do_kapat(do_num):
    """Digital Output'u kapat"""
    client = connect()
    client.write_coil(do_num, False, slave=SLAVE)
    print(f"📤 {DO_LABELS_SHORT[do_num]} → ⚫ KAPANDI")
    client.close()

def do_toggle(do_num):
    """Digital Output'u toggle et"""
    client = connect()
    result = client.read_coils(do_num, 1, slave=SLAVE)
    yeni = not result.bits[0]
    client.write_coil(do_num, yeni, slave=SLAVE)
    print(f"📤 {DO_LABELS_SHORT[do_num]} → {'🟢 AÇILDI' if yeni else '⚫ KAPANDI'}")
    client.close()

def do_tumunu_kapat():
    """Tüm Digital Output'ları kapat"""
    client = connect()
    client.write_coils(START_ADDRESS, [False]*DO_COUNT, slave=SLAVE)
    print("⚫ Tüm çıkışlar KAPANDI")
    client.close()

# ========== DIGITAL INPUT (DI) İşlemleri ==========

def di_oku(di_num):
    """Tek bir Digital Input'u oku"""
    client = connect()
    result = client.read_discrete_inputs(di_num, 1, slave=SLAVE)
    status = "🟢 AKTIF" if result.bits[0] else "⚫ PASIF"
    print(f"📥 {DI_LABELS_SHORT[di_num]}: {status}")
    client.close()

def di_tumunu_oku():
    """Tüm Digital Input'ları oku"""
    client = connect()
    result = client.read_discrete_inputs(START_ADDRESS, DI_COUNT, slave=SLAVE)
    
    print("\n" + "="*50)
    print("📥 DIGITAL INPUT DURUMLARI (Sensörler)")
    print("="*50)
    
    bits = result.bits if hasattr(result, 'bits') else []
    for i in range(DI_COUNT):
        status = "🟢 AKTIF" if (i < len(bits) and bits[i]) else "⚫ PASIF"
        print(f"   DI{i} {DI_LABELS_SHORT[i]}: {status}")
    print("="*50 + "\n")
    client.close()

# ========== Genel Durum ==========

def durum():
    """Tüm DI ve DO durumlarını göster"""
    client = connect()
    
    # DI'ları oku
    di_result = client.read_discrete_inputs(START_ADDRESS, DI_COUNT, slave=SLAVE)
    
    # DO'ları oku
    do_result = client.read_coils(START_ADDRESS, DO_COUNT, slave=SLAVE)
    
    print("\n" + "="*60)
    print(f"📊 {DEVICE_NAME} DURUM TABLOSU")
    print("="*60)
    
    print("\n📥 DIGITAL INPUTS (Sensörler):")
    print("-" * 60)
    di_bits = di_result.bits if hasattr(di_result, 'bits') else []
    for i in range(DI_COUNT):
        status = "🟢 AKTIF" if (i < len(di_bits) and di_bits[i]) else "⚫ PASIF"
        print(f"   DI{i} {DI_LABELS_SHORT[i]}: {status}")
    
    print("\n📤 DIGITAL OUTPUTS (Kontrol):")
    print("-" * 60)
    do_bits = do_result.bits if hasattr(do_result, 'bits') else []
    for i in range(DO_COUNT):
        status = "🟢 AÇIK" if (i < len(do_bits) and do_bits[i]) else "⚫ KAPALI"
        print(f"   DO{i} {DO_LABELS_SHORT[i]}: {status}")
    
    print("="*60 + "\n")
    client.close()

def yardim():
    print("\n" + "="*60)
    print(f"🎮 DI/DO KONTROL - {DEVICE_NAME}")
    print("="*60)
    print("\nKullanım: python3 kontrol.py <komut> [numara]")
    print("\n📤 Digital Output (DO) Komutları:")
    print(f"  do-ac <0-{DO_COUNT-1}>      - DO'yu aç")
    print(f"  do-kapat <0-{DO_COUNT-1}>   - DO'yu kapat")
    print(f"  do-toggle <0-{DO_COUNT-1}>  - DO'yu toggle et")
    print("  do-tumunu-kapat  - Tüm DO'ları kapat")
    print("\n📥 Digital Input (DI) Komutları:")
    print(f"  di-oku <0-{DI_COUNT-1}>     - DI'yı oku")
    print("  di-tumunu-oku    - Tüm DI'ları oku")
    print("\n📊 Genel Komutlar:")
    print("  durum            - Tüm DI/DO durumlarını göster")
    print("\n📤 Digital Output (DO) Listesi:")
    for i, label in enumerate(DO_LABELS_SHORT):
        print(f"  DO{i}: {label}")
    print("\n📥 Digital Input (DI) Listesi:")
    for i, label in enumerate(DI_LABELS_SHORT):
        print(f"  DI{i}: {label}")
    print("\nÖrnekler:")
    print("  python3 kontrol.py do-ac 2        # Pompayı aç")
    print("  python3 kontrol.py di-oku 0       # Kapı sensörünü oku")
    print("  python3 kontrol.py durum          # Tüm durumları göster")
    print("="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        yardim()
        sys.exit(0)
    
    komut = sys.argv[1].lower()
    
    # DO komutları
    if komut in ["do-ac", "do-kapat", "do-toggle"]:
        if len(sys.argv) < 3:
            print(f"❌ DO numarası gerekli! (0-{DO_COUNT-1})")
            sys.exit(1)
        do_num = int(sys.argv[2])
        if do_num < 0 or do_num >= DO_COUNT:
            print(f"❌ Geçersiz DO numarası! (0-{DO_COUNT-1})")
            sys.exit(1)
        
        if komut == "do-ac":
            do_ac(do_num)
        elif komut == "do-kapat":
            do_kapat(do_num)
        elif komut == "do-toggle":
            do_toggle(do_num)
    
    # DI komutları
    elif komut == "di-oku":
        if len(sys.argv) < 3:
            print(f"❌ DI numarası gerekli! (0-{DI_COUNT-1})")
            sys.exit(1)
        di_num = int(sys.argv[2])
        if di_num < 0 or di_num >= DI_COUNT:
            print(f"❌ Geçersiz DI numarası! (0-{DI_COUNT-1})")
            sys.exit(1)
        di_oku(di_num)
    
    elif komut == "di-tumunu-oku":
        di_tumunu_oku()
    
    elif komut == "do-tumunu-kapat":
        do_tumunu_kapat()
    
    elif komut == "durum":
        durum()
    
    else:
        print(f"❌ Bilinmeyen komut: {komut}")
        yardim()
        sys.exit(1)

