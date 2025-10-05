from pymodbus.client import ModbusTcpClient
import time

print("\n🧪 Simülatör Bağlantı Testi")
print("="*50)

client = ModbusTcpClient('localhost', port=5020)

if client.connect():
    print("✅ Simülatöre bağlandı!")
    
    # Işığı aç
    print("\n💡 Işığı AÇIYORUM...")
    client.write_coil(0, True)
    time.sleep(1)
    
    # Durumu oku
    result = client.read_coils(0, 1)
    print(f"   Durum: {'🟢 AÇIK' if result.bits[0] else '⚫ KAPALI'}")
    
    time.sleep(2)
    
    # Işığı kapat
    print("\n💡 Işığı KAPATIYORUM...")
    client.write_coil(0, False)
    time.sleep(1)
    
    # Durumu oku
    result = client.read_coils(0, 1)
    print(f"   Durum: {'🟢 AÇIK' if result.bits[0] else '⚫ KAPALI'}")
    
    print("\n✅ Test başarılı!")
    client.close()
else:
    print("❌ Bağlantı hatası!")

print("="*50 + "\n")
