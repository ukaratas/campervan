#!/usr/bin/env python3
"""
Home Assistant Area Setup Script
Karavan için area'ları oluşturur ve entity'leri atar
"""

# Bu script'i çalıştırmak için:
# python3 setup_areas.py

print("""
╔══════════════════════════════════════════════════════════════╗
║           Home Assistant Area Kurulum Rehberi                ║
╚══════════════════════════════════════════════════════════════╝

Home Assistant'ta Area (Alan) oluşturma REST API ile mümkün değil.
UI'dan manuel olarak oluşturman gerekiyor.

📋 ADIM 1: AREA'LARI OLUŞTUR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Home Assistant → Settings → Areas, labels & zones → Create Area

🏠 Oluşturulacak Area'lar:

1. 🍳 Mutfak
2. 🛏️ Yatak Alanı
3. 🏠 Orta Alan
4. 🚪 Popup Yatak
5. 🌙 Dış Alan
6. 🚿 Banyo
7. 🔌 Elektrik
8. 💧 Su Sistemi

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 ADIM 2: ENTITY'LERİ AREA'LARA ATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Settings → Devices & services → Entities → Entity'ye tıkla → Area seç

🍳 MUTFAK:
   - light.mutfak_isik
   - light.mutfak_tezgah_isik
   - switch.usb_kutusu_mutfak

🛏️ YATAK ALANI:
   - light.yatak_alani_isik
   - light.sol_okuma_isik
   - light.sag_okuma_isik
   - binary_sensor.sag_yatak_butonu
   - binary_sensor.sol_yatak_butonu
   - switch.usb_kutusu_yatak

🏠 ORTA ALAN:
   - light.orta_alan_isik
   - binary_sensor.orta_alan_butonu

🚪 POPUP YATAK:
   - light.popup_yatak_isik
   - binary_sensor.popup_yatak_butonu
   - switch.usb_kutusu_popup

🌙 DIŞ ALAN:
   - light.tente_isik
   - binary_sensor.dis_aydinlatma_butonu

🚿 BANYO:
   - light.banyo_aydinlatma
   - light.banyo_ayna_aydinlatma
   - binary_sensor.banyo_butonu
   - switch.usb_kutusu_banyo

💧 SU SİSTEMİ:
   - switch.temiz_su_hidrofor
   - switch.macerator_pompa
   - switch.gri_su_pompasi
   - switch.su_pompasi (DI/DO)

🔌 ELEKTRİK:
   - switch.buzdolabi
   - switch.truma_combi_d4
   - switch.alarm_siren
   - switch.havalandirma_fan

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 ADIM 3: DASHBOARD OLUŞTUR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Settings → Dashboards → + Add Dashboard

Dashboard ismi: "Karavan Kontrol"

Sonra: 3 tane VIEW (sekme) ekle:
   1. 🏠 Aydınlatma
   2. 💧 Su Sistemi
   3. 🍳 Mutfak & Cihazlar

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 ADIM 4: KARTLARI EKLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Her view'a + Add Card → 
   - "Area Card" seç → Area'yı seç → Ekle

Otomatik olarak o area'daki tüm entity'ler kartlarda görünür!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VEYA: Hazır YAML config'i kullan!
▶ dashboard_karavan.yaml dosyasını Home Assistant'a yükle

╚══════════════════════════════════════════════════════════════╝
""")

