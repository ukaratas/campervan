#!/bin/bash
# VM Docker Tamiri - Uzaktan çalıştırılabilir
# Kullanım: Mac'ten VM'e kopyala ve çalıştır

echo "🔧 VM Docker Tamir Scripti Başlıyor..."
echo "======================================"
echo ""

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Durum Kontrolü
echo -e "${YELLOW}[1/8] Docker Durum Kontrolü${NC}"
systemctl is-active docker >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Docker çalışıyor${NC}"
else
    echo -e "${RED}✗ Docker çalışmıyor${NC}"
fi
echo ""

# 2. Zaman Kontrolü
echo -e "${YELLOW}[2/8] Zaman Kontrolü${NC}"
echo "Sistem zamanı: $(date)"
echo ""

# 3. Docker Process Kontrolü
echo -e "${YELLOW}[3/8] Docker Process Kontrolü${NC}"
DOCKER_PROCS=$(ps aux | grep -E 'docker|containerd' | grep -v grep | wc -l)
echo "Çalışan Docker process sayısı: $DOCKER_PROCS"
echo ""

# 4. Docker'ı Durdur
echo -e "${YELLOW}[4/8] Docker Servisi Durduruluyor${NC}"
sudo systemctl stop docker.socket 2>/dev/null
sudo systemctl stop docker 2>/dev/null
sleep 2
echo -e "${GREEN}✓ Docker servisleri durduruldu${NC}"
echo ""

# 5. Docker Process'leri Temizle
echo -e "${YELLOW}[5/8] Docker Process'leri Temizleniyor${NC}"
sudo pkill -9 dockerd 2>/dev/null && echo "  → dockerd killed"
sudo pkill -9 containerd 2>/dev/null && echo "  → containerd killed"
sudo pkill -9 docker-proxy 2>/dev/null && echo "  → docker-proxy killed"
echo -e "${GREEN}✓ Process'ler temizlendi${NC}"
echo ""

# 6. Stale Dosyaları Temizle
echo -e "${YELLOW}[6/8] Stale Dosyalar Temizleniyor${NC}"
sudo rm -rf /var/run/docker.sock 2>/dev/null && echo "  → docker.sock silindi"
sudo rm -rf /var/run/docker.pid 2>/dev/null && echo "  → docker.pid silindi"
sudo rm -rf /var/run/containerd/containerd.sock 2>/dev/null && echo "  → containerd.sock silindi"
echo -e "${GREEN}✓ Stale dosyalar temizlendi${NC}"
echo ""

# 7. Docker'ı Başlat
echo -e "${YELLOW}[7/8] Docker Başlatılıyor${NC}"
sudo systemctl start docker
sleep 5

systemctl is-active docker >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Docker başarıyla başlatıldı${NC}"
else
    echo -e "${RED}✗ Docker başlatılamadı! Logları kontrol edin:${NC}"
    echo "  sudo journalctl -u docker -n 50"
    exit 1
fi
echo ""

# 8. Container'ları Kontrol Et ve Başlat
echo -e "${YELLOW}[8/8] Container'lar Kontrol Ediliyor${NC}"
echo ""
echo "Tüm container'lar:"
sudo docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

# Home Assistant'ı başlat (eğer varsa ve durmuşsa)
if sudo docker ps -a | grep -q homeassistant; then
    if ! sudo docker ps | grep -q homeassistant; then
        echo "Home Assistant başlatılıyor..."
        sudo docker start homeassistant
        sleep 3
        echo -e "${GREEN}✓ Home Assistant başlatıldı${NC}"
    else
        echo -e "${GREEN}✓ Home Assistant zaten çalışıyor${NC}"
    fi
else
    echo -e "${YELLOW}ℹ Home Assistant container bulunamadı${NC}"
fi
echo ""

# Final Durum
echo "======================================"
echo -e "${GREEN}✅ Tamir Scripti Tamamlandı!${NC}"
echo "======================================"
echo ""
echo "Çalışan container'lar:"
sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "Docker servis durumu:"
sudo systemctl status docker --no-pager | head -n 5
echo ""
echo -e "${GREEN}Sorun devam ederse logları kontrol edin:${NC}"
echo "  sudo journalctl -u docker -n 100"
echo "  sudo docker logs homeassistant"


