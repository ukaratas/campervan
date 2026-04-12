#!/usr/bin/env python3
"""
Waveshare Analog Input 8CH: cihaz adresini 1 -> 3 yap (holding 4x4000).
Unicast: 01 06 40 00 00 03 DC 0B — sadece slave 1 yanıtlar.
IO8 de slave 1 ise hatta IO8'i çıkar; Relay (slave 2) takılı kalabilir.

Sonra doğrulama: FC04 slave 3.
"""
import glob
import os
import time

SET_ADDR_1_TO_3 = bytes.fromhex("010640000003dc0b")
FC04_S3 = bytes.fromhex("030400000008f02e")

ports = sorted(glob.glob("/dev/serial/by-id/usb-*"))
port = ports[0] if ports else "/dev/ttyUSB0"
if not os.path.exists(port):
    raise SystemExit(f"Port yok: {port}")

os.system(f"stty -F {port} 9600 cs8 -cstopb -parenb raw -echo 2>/dev/null")
fd = os.open(port, os.O_RDWR | os.O_NOCTTY)
os.write(fd, SET_ADDR_1_TO_3)
time.sleep(0.3)
os.read(fd, 256)
os.write(fd, FC04_S3)
time.sleep(0.25)
resp = os.read(fd, 64)
os.close(fd)
print("Adres yaz (01 06 40 00 00 03) gönderildi.")
print("Doğrulama FC04 slave 3 yanıt:", resp.hex() if resp else "(boş)")
if resp and len(resp) >= 5 and resp[0] == 3 and resp[1] == 4:
    print("OK: Modül slave 3 olarak yanıtlıyor.")
else:
    print("UYARI: Slave 3 FC04 beklenen cevap değil — IO8 hâlâ slave 1 ile hatta olabilir veya yazma başarısız.")
