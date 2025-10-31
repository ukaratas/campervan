#!/bin/bash
# VM Hızlı Kontrol ve Tamir Scripti
# Kullanım: ./vm-quick-fix.sh [check|fix|time|docker|all]

SSH_KEY="/Users/ugurkaratas/Local Projects/campervan/Automation/ha-configs/.ssh/homeassistant"
VM_IP="192.168.1.84"
VM_USER="root"

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

function banner() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

function ssh_cmd() {
    ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$VM_USER@$VM_IP" "$1" 2>&1
}

function check_vm() {
    banner "🔍 VM Durum Kontrolü"
    
    echo -ne "SSH Bağlantısı... "
    if ssh_cmd "echo OK" | grep -q "OK"; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
        echo "VM'e bağlanılamıyor!"
        exit 1
    fi
    
    echo ""
    echo "=== Sistem Bilgisi ==="
    ssh_cmd "uptime | head -1"
    echo ""
    
    echo "=== Zaman ==="
    ssh_cmd "date"
    echo ""
    
    echo "=== Chrony Durumu ==="
    ssh_cmd "pgrep chronyd > /dev/null && echo '✅ Chrony çalışıyor' || echo '❌ Chrony çalışmıyor'"
    ssh_cmd "chronyc tracking 2>/dev/null | grep 'Reference ID' || true"
    echo ""
    
    echo "=== Docker Durumu ==="
    ssh_cmd "docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null | head -5 || echo 'Protection mode aktif - ha komutlarını kullanın'"
    echo ""
    
    echo "=== Home Assistant ==="
    ssh_cmd "ha core info | grep -E 'version:|state:' | head -3"
    echo ""
}

function fix_time() {
    banner "⏰ Zaman Senkronizasyonu"
    
    echo "Chrony'yi kontrol ediyorum..."
    ssh_cmd "pgrep chronyd > /dev/null || chronyd"
    sleep 2
    
    echo ""
    echo "Tracking bilgisi:"
    ssh_cmd "chronyc tracking 2>/dev/null | head -8"
    
    echo ""
    echo -e "${GREEN}✅ Zaman sync tamamlandı${NC}"
    echo "Güncel zaman: $(ssh_cmd 'date')"
}

function fix_docker() {
    banner "🐳 Docker Kontrolü"
    
    echo "ℹ️  Home Assistant OS'de Docker doğrudan erişilemez"
    echo "   Protection mode'u kapatmalısınız veya 'ha' komutlarını kullanın"
    echo ""
    
    echo "Home Assistant container durumu:"
    ssh_cmd "ha supervisor info | grep homeassistant -A 3 | head -4"
    
    echo ""
    echo "Eğer sorun varsa, VM'i restart edin:"
    echo "  ssh -i '$SSH_KEY' $VM_USER@$VM_IP 'reboot'"
}

function fix_all() {
    check_vm
    echo ""
    fix_time
    echo ""
    fix_docker
}

function show_usage() {
    echo "VM Hızlı Kontrol ve Tamir Scripti"
    echo ""
    echo "Kullanım:"
    echo "  $0 check     - VM durumunu kontrol et"
    echo "  $0 time      - Zaman senkronizasyonu yap"
    echo "  $0 docker    - Docker durumunu kontrol et"
    echo "  $0 all       - Tüm kontrolleri yap"
    echo "  $0 ssh       - VM'e SSH ile bağlan"
    echo "  $0 reboot    - VM'i restart et"
    echo ""
    echo "Örnekler:"
    echo "  $0 check     # Hızlı durum kontrolü"
    echo "  $0 all       # Komple kontrol"
    echo ""
}

# Ana komut
case "${1:-check}" in
    check)
        check_vm
        ;;
    time)
        fix_time
        ;;
    docker)
        fix_docker
        ;;
    all)
        fix_all
        ;;
    ssh)
        ssh -i "$SSH_KEY" "$VM_USER@$VM_IP"
        ;;
    reboot)
        banner "🔄 VM Restart"
        echo "VM restart ediliyor..."
        ssh_cmd "reboot"
        echo -e "${GREEN}✅ Restart komutu gönderildi${NC}"
        echo "30 saniye bekleyin..."
        ;;
    *)
        show_usage
        ;;
esac


