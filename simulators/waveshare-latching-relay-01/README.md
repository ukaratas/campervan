# Waveshare Latching Relay Instance 01

8 kanallı aydınlatma kontrol modülü simülatörü.

## 🚀 Başlatma

```bash
cd waveshare-latching-relay-01
source ../venv/bin/activate
python3 simulator.py
```

## 🎮 Kontrol

```bash
# Röle aç/kapat
python3 kontrol.py ac 3        # R3: Yatak Alanı Işık AÇ
python3 kontrol.py kapat 3     # R3: Yatak Alanı Işık KAPAT
python3 kontrol.py toggle 0    # R0: Mutfak Işık TOGGLE

# Durumları göster
python3 kontrol.py durum

# Tümünü kapat
python3 kontrol.py tumunu-kapat
```

## 📺 İzleme

```bash
python3 izle.py
```

## 🏠 Home Assistant

`ha-config.yaml` içeriğini Home Assistant `configuration.yaml`'a ekle.

## 📋 Röle Haritası

| Coil | Röle | Açıklama |
|------|------|----------|
| 0 | R0 | Mutfak Işık (8W) |
| 1 | R1 | Mutfak Tezgâh Işık (7W) |
| 2 | R2 | Orta Alan Işık (12W) |
| 3 | R3 | Yatak Alanı Işık (14W) |
| 4 | R4 | Popup Yatak Işık (6W) |
| 5 | R5 | Sol Okuma Işık (4W) |
| 6 | R6 | Sağ Okuma Işık (4W) |
| 7 | R7 | Tente Işık (12W) |

