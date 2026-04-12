RS485 bus (hub adı: rs485_bus) — cihaz dosyaları
===============================================

switches/        IO8 DO (slave 1), Relay E (slave 2) — tamsayı; adres değişirse YAML’da güncelle
binary_sensors/  IO8 DI (slave 1)
sensors/         Analog 8CH + holding modları (slave 3)

Karavan HAOS’a geçince: önce secrets.yaml içinde rs485_serial_port ve gerekiyorsa slave
numaralarını güncelleyin; bu klasördeki YAML’ları çoğu zaman değiştirmeniz gerekmez.
