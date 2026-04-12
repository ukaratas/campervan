#!/usr/bin/env python3
"""RS485 üzerinde Analog Input 8CH için FC04 (input register) ham okuma testi. 9600 8N1."""
import glob
import os
import struct
import sys
import termios
import time


def modbus_crc(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def build_fc04(slave: int, start: int, count: int) -> bytes:
    pdu = bytes([slave, 4, (start >> 8) & 0xFF, start & 0xFF, (count >> 8) & 0xFF, count & 0xFF])
    c = modbus_crc(pdu)
    return pdu + bytes([c & 0xFF, (c >> 8) & 0xFF])


def open_port(path: str, baud: int = 9600) -> int:
    fd = os.open(path, os.O_RDWR | os.O_NOCTTY)
    attrs = termios.tcgetattr(fd)
    termios.cfsetispeed(attrs, termios.B9600)
    termios.cfsetospeed(attrs, termios.B9600)
    attrs[2] &= ~termios.ICANON
    attrs[2] &= ~termios.ECHO
    attrs[2] &= ~termios.ISIG
    attrs[2] &= ~termios.INPCK
    attrs[2] |= termios.CLOCAL
    attrs[3] &= ~termios.ECHOE
    attrs[3] &= ~termios.ICANON
    attrs[6][termios.VMIN] = 0
    attrs[6][termios.VTIME] = 20  # ~2s timeout per read chunk
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    return fd


def read_response(fd: int, max_len: int = 64, total_timeout: float = 1.0) -> bytes:
    buf = bytearray()
    deadline = time.monotonic() + total_timeout
    while len(buf) < max_len and time.monotonic() < deadline:
        try:
            chunk = os.read(fd, max_len - len(buf))
        except BlockingIOError:
            chunk = b""
        if chunk:
            buf.extend(chunk)
            if len(buf) >= 5 and buf[1] & 0x80:
                break
            if len(buf) >= 3 and buf[2] == len(buf) - 5 and len(buf) >= buf[2] + 5:
                break
        else:
            time.sleep(0.02)
    return bytes(buf)


def main() -> None:
    port = sys.argv[1] if len(sys.argv) > 1 else ""
    if not port:
        cand = sorted(glob.glob("/dev/serial/by-id/usb-*"))
        port = cand[0] if cand else "/dev/ttyUSB0"
    if not os.path.exists(port):
        print(f"HATA: Port yok: {port}", file=sys.stderr)
        sys.exit(1)

    print(f"Port: {port}")
    os.system(f"stty -F {port} 9600 cs8 -cstopb -parenb raw -echo min 0 time 2 2>/dev/null")

    fd = open_port(port, 9600)
    try:
        for slave in (1, 2, 3):
            frame = build_fc04(slave, 0, 8)
            os.read(fd, 4096)  # flush
            os.write(fd, frame)
            time.sleep(0.15)
            resp = read_response(fd, 64, 1.2)
            hexes = resp.hex() if resp else "(boş)"
            print(f"\n--- Slave {slave} FC04 reg0 count8 gönder: {frame.hex()} ---")
            print(f"Yanıt ({len(resp)} byte): {hexes}")
            if len(resp) >= 5 and resp[0] == slave and resp[1] == 4:
                nbytes = resp[2]
                if len(resp) >= 5 + nbytes:
                    regs = struct.unpack(">" + "H" * (nbytes // 2), resp[3 : 3 + nbytes])
                    print(f"  Register değerleri (uint16): {regs}")
            elif len(resp) >= 3 and resp[1] & 0x80:
                print(f"  Modbus exception: fc=0x{resp[1]:02x} code=0x{resp[2]:02x}")
    finally:
        os.close(fd)


if __name__ == "__main__":
    main()
