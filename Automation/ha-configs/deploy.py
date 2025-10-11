#!/usr/bin/env python3
"""
Home Assistant Configuration Deployment Tool
Otomatik olarak tüm konfigürasyonları Home Assistant'a yükler

KULLANIM:
    python3 deploy.py           # Sadece reload (dosya yüklemesi yok)
    python3 deploy.py --auto    # Tam otomatik: Dosyalar + Reload

ÖZELLİKLER:
    ✅ 6 dosyayı SCP ile otomatik yükler
    ✅ 4 servisi REST API ile reload eder
    ✅ Bağlantı ve hata kontrolü
    ✅ Dependency-free (sadece Python stdlib)

GEREKSİNİMLER:
    1. ha_credentials.py (API token)
    2. ~/.ssh/homeassistant (SSH private key)
    3. Advanced SSH & Web Terminal addon (SFTP=true, username=root)

DOSYA TRANSFERLERI:
    helpers/input_datetime.yaml → /config/helpers/
    helpers/input_number.yaml → /config/helpers/
    helpers/input_boolean.yaml → /config/helpers/
    automations/button_press_detection.yaml → /config/automations/
    automations/button_actions.yaml → /config/automations/
    modbus_combined.yaml → /config/

SERVİS RELOAD:
    - automation
    - input_datetime
    - input_number
    - input_boolean
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

# Credentials import
try:
    from ha_credentials import HA_URL, HA_TOKEN
except ImportError:
    print("❌ Hata: ha_credentials.py bulunamadı!")
    print("💡 ha_credentials.example dosyasını ha_credentials.py olarak kopyalayın ve token'ınızı girin.")
    sys.exit(1)

# Base directory
BASE_DIR = Path(__file__).parent

def make_request(url, method="GET", data=None):
    """urllib ile HTTP request yap"""
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, str(e)

def check_connection():
    """Home Assistant bağlantısını kontrol et"""
    print("🔍 Home Assistant bağlantısı kontrol ediliyor...")
    status, data = make_request(f"{HA_URL}/api/")
    
    if status == 200 and data:
        print(f"✅ Home Assistant bağlantısı başarılı: {data.get('message', 'OK')}")
        return True
    else:
        print(f"❌ Bağlantı hatası: {status}")
        return False

def reload_service(domain):
    """Belirli bir domain'i reload et"""
    print(f"🔄 {domain} reload ediliyor...")
    status, data = make_request(f"{HA_URL}/api/services/{domain}/reload", method="POST", data={})
    
    if status == 200:
        print(f"✅ {domain} başarıyla reload edildi")
        return True
    else:
        print(f"❌ Reload hatası: {status}")
        return False

def deploy_files_via_scp(host="homeassistant.local", user="root"):
    """
    SCP ile dosyaları kopyala (SSH key kullanarak)
    """
    import subprocess
    
    print("\n📦 Dosyalar SCP ile kopyalanıyor...")
    
    ssh_key = str(Path.home() / ".ssh" / "homeassistant")
    
    files_to_copy = [
        ("helpers/input_datetime.yaml", "/config/helpers/input_datetime.yaml"),
        ("helpers/input_number.yaml", "/config/helpers/input_number.yaml"),
        ("helpers/input_boolean.yaml", "/config/helpers/input_boolean.yaml"),
        ("automations/button_press_detection.yaml", "/config/automations/button_press_detection.yaml"),
        ("automations/button_actions.yaml", "/config/automations/button_actions.yaml"),
        ("modbus_combined.yaml", "/config/modbus_combined.yaml"),
    ]
    
    success_count = 0
    for local_file, remote_file in files_to_copy:
        local_path = BASE_DIR / local_file
        
        if not local_path.exists():
            print(f"⚠️  {local_file} bulunamadı, atlanıyor...")
            continue
        
        print(f"📤 {local_file} yükleniyor...")
        
        # SCP komutu
        cmd = [
            "scp",
            "-i", ssh_key,
            "-o", "StrictHostKeyChecking=no",
            str(local_path),
            f"{user}@{host}:{remote_file}"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {local_file} başarıyla yüklendi")
                success_count += 1
            else:
                print(f"❌ {local_file} yüklenemedi: {result.stderr.decode()}")
        except Exception as e:
            print(f"❌ {local_file} yüklenemedi: {e}")
    
    print(f"\n✅ {success_count}/{len(files_to_copy)} dosya başarıyla yüklendi")
    return success_count > 0

def show_manual_instructions():
    """Manuel deployment talimatlarını göster"""
    print("\n" + "="*60)
    print("📋 MANUEL DEPLOYMENT TALİMATLARI")
    print("="*60)
    print("\n1️⃣ HELPER DOSYALARINI YÜKLE:")
    print("   • Home Assistant → File Editor")
    print("   • /config/helpers/ klasörüne şu dosyaları kopyala:")
    print("     - input_datetime.yaml")
    print("     - input_number.yaml")
    print("     - input_boolean.yaml")
    
    print("\n2️⃣ AUTOMATION DOSYALARINI YÜKLE:")
    print("   • /config/automations/ klasörüne şu dosyaları kopyala:")
    print("     - button_press_detection.yaml")
    print("     - button_actions.yaml")
    
    print("\n3️⃣ MODBUS CONFIG'İ GÜNCELLE:")
    print("   • /config/ klasörüne modbus_combined.yaml'ı kopyala")
    print("   • /config/configuration.yaml'da şu satırları ekle:")
    print("     modbus: !include modbus_combined.yaml")
    
    print("\n4️⃣ RELOAD ET:")
    print("   • Developer Tools → YAML → All YAML Configuration → Reload")
    
    print("\n" + "="*60)

def main():
    print("🚀 Home Assistant Configuration Deployment Tool")
    print("="*60)
    
    # Bağlantı kontrolü
    if not check_connection():
        print("\n❌ Home Assistant'a bağlanılamadı!")
        print("💡 ha_credentials.py dosyasındaki URL ve TOKEN'ı kontrol edin.")
        sys.exit(1)
    
    print("\n✅ Bağlantı başarılı!")
    
    # Komut satırı argümanlarını kontrol et
    import sys
    auto_deploy = "--auto" in sys.argv or "-a" in sys.argv
    
    if auto_deploy:
        # Otomatik deployment - dosyaları SCP ile yükle
        print("\n🚀 OTOMATIK DEPLOYMENT MODU")
        print("="*60)
        
        if deploy_files_via_scp():
            print("\n✅ Dosyalar başarıyla yüklendi!")
        else:
            print("\n⚠️  Bazı dosyalar yüklenemedi.")
            print("💡 Manuel olarak yüklemeyi deneyin veya hata mesajlarını kontrol edin.")
    
    # Reload servisleri çağır
    print("\n🔄 Servisler reload ediliyor...")
    
    services_to_reload = [
        "automation",
        "input_datetime", 
        "input_number",
        "input_boolean"
    ]
    
    success_count = 0
    for service in services_to_reload:
        if reload_service(service):
            success_count += 1
    
    print(f"\n✅ {success_count}/{len(services_to_reload)} servis başarıyla reload edildi")
    
    if not auto_deploy:
        # Manuel talimatları göster
        show_manual_instructions()
        
        print("\n💡 TİPLER:")
        print("   • Manuel yükleme sonrası reload için:")
        print(f"     python3 {Path(__file__).name}")
        print("\n   • Tam otomatik deployment için:")
        print(f"     python3 {Path(__file__).name} --auto")

if __name__ == "__main__":
    main()

