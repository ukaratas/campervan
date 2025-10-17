#!/usr/bin/env python3
"""
Waveshare Analog Input - Kontrol ve Okuma
Analog sensör değerlerini okuma aracı
"""

import sys
from pymodbus.client import ModbusTcpClient
from config import *

def read_analog_inputs():
    """Tüm analog inputları oku"""
    client = ModbusTcpClient(HOST, port=PORT)
    
    if not client.connect():
        print(f"❌ Bağlantı hatası: {HOST}:{PORT}")
        return
    
    print("="*70)
    print(f"🌡️ {DEVICE_NAME} - Analog Input Okuma")
    print("="*70)
    
    try:
        # Holding Registers'ı oku (Function Code 03)
        result = client.read_holding_registers(START_ADDRESS, AI_COUNT, slave=SLAVE_ID)
        
        if result.isError():
            print(f"❌ Okuma hatası: {result}")
            return
        
        print(f"\n📊 Sensör Değerleri:\n")
        
        # Her sensör için
        for i in range(AI_COUNT):
            # Ölçeklenmiş değeri al ve gerçek değere çevir
            scaled_value = result.registers[i]
            actual_value = scaled_value / SCALE_FACTOR
            
            min_val, max_val, unit, precision = SENSOR_RANGES[i]
            
            # Progress bar oluştur
            if unit == "%":
                percentage = actual_value
            elif unit == "ppm":
                percentage = (actual_value - 400) / 1600 * 100  # 400-2000 ppm arası
            else:  # Sıcaklık
                range_min, range_max = min_val, max_val
                percentage = (actual_value - range_min) / (range_max - range_min) * 100
            
            bar_length = 30
            filled = int(bar_length * percentage / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            # Renk kodu (terminal için)
            if percentage < 20:
                color = "🔴"
            elif percentage < 50:
                color = "🟡"
            else:
                color = "🟢"
            
            print(f"  {AI_LABELS_SHORT[i]:20s} │ {bar} │ {actual_value:.{precision}f}{unit:>4s} {color}")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        client.close()

def read_single_input(ai_index):
    """Tek bir analog input oku"""
    if ai_index < 0 or ai_index >= AI_COUNT:
        print(f"❌ Geçersiz AI indeks: {ai_index} (0-{AI_COUNT-1} arası olmalı)")
        return
    
    client = ModbusTcpClient(HOST, port=PORT)
    
    if not client.connect():
        print(f"❌ Bağlantı hatası: {HOST}:{PORT}")
        return
    
    try:
        result = client.read_holding_registers(START_ADDRESS + ai_index, 1, slave=SLAVE_ID)
        
        if result.isError():
            print(f"❌ Okuma hatası: {result}")
            return
        
        scaled_value = result.registers[0]
        actual_value = scaled_value / SCALE_FACTOR
        _, _, unit, precision = SENSOR_RANGES[ai_index]
        
        print(f"\n📊 {AI_LABELS[ai_index]}")
        print(f"   Değer: {actual_value:.{precision}f} {unit}")
        print(f"   Raw (Modbus): {scaled_value}\n")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            ai_index = int(sys.argv[1])
            read_single_input(ai_index)
        except ValueError:
            print("❌ Geçersiz indeks. Sayı giriniz (0-7)")
    else:
        read_analog_inputs()

