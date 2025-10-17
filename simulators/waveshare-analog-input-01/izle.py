#!/usr/bin/env python3
"""
Waveshare Analog Input - Real-time İzleme
Analog sensör değerlerini canlı izleme aracı
"""

import sys
import time
from pymodbus.client import ModbusTcpClient
from config import *

def watch_analog_inputs():
    """Analog inputları sürekli izle"""
    client = ModbusTcpClient(HOST, port=PORT)
    
    if not client.connect():
        print(f"❌ Bağlantı hatası: {HOST}:{PORT}")
        return
    
    print("="*80)
    print(f"🌡️ {DEVICE_NAME} - Real-time İzleme (CTRL+C ile çıkış)")
    print("="*80)
    
    previous_values = [None] * AI_COUNT
    
    try:
        while True:
            # Ekranı temizle (terminal için)
            print("\033[2J\033[H", end="")
            
            print("="*80)
            print(f"🌡️ {DEVICE_NAME} - {time.strftime('%H:%M:%S')}")
            print("="*80)
            
            # Holding Registers'ı oku
            result = client.read_holding_registers(START_ADDRESS, AI_COUNT, slave=SLAVE_ID)
            
            if result.isError():
                print(f"❌ Okuma hatası: {result}")
                time.sleep(1)
                continue
            
            print()
            
            # Her sensör için
            for i in range(AI_COUNT):
                scaled_value = result.registers[i]
                actual_value = scaled_value / SCALE_FACTOR
                _, _, unit, precision = SENSOR_RANGES[i]
                
                # Değişim kontrolü
                change_indicator = ""
                if previous_values[i] is not None:
                    diff = actual_value - previous_values[i]
                    if diff > 0:
                        change_indicator = f" ⬆ +{diff:.{precision}f}"
                    elif diff < 0:
                        change_indicator = f" ⬇ {diff:.{precision}f}"
                
                # Alarm kontrolü
                alarm = ""
                if i == 0 and actual_value < 20:  # Temiz su düşük
                    alarm = " ⚠️ DÜŞÜK!"
                elif i == 1 and actual_value > 80:  # Gri su yüksek
                    alarm = " ⚠️ YÜKSEK!"
                elif i == 5 and actual_value > 40:  # Elektronik sıcak
                    alarm = " 🔥 SICAK!"
                elif i == 6 and actual_value > 1000:  # CO2 yüksek
                    alarm = " 💨 KÖTÜ HAVA!"
                
                print(f"  {AI_LABELS_SHORT[i]:20s} │ {actual_value:>7.{precision}f} {unit:>4s}{change_indicator:>12s}{alarm}")
                
                previous_values[i] = actual_value
            
            print("\n" + "="*80)
            print("  Güncelleme: Her 2 saniye | CTRL+C ile çıkış")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n🛑 İzleme durduruldu.")
    except Exception as e:
        print(f"\n❌ Hata: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    watch_analog_inputs()

