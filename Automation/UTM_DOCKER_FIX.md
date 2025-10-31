# UTM'de Home Assistant Docker Sorunları ve Çözümleri

## 🔴 Sorun
UTM'de VM'i kapatıp birkaç gün sonra açtığımda Docker servisi başlamıyor ve boot'ta takılı kalıyor:
```
A start job is running for Docker Application Container Engine (2min 10s / no limit)
```

## 🎯 Hızlı Çözüm (Şu An Sorun Varsa)

### Seçenek 1: Boot Sırasında
Boot ekranında takıldıysa:
1. **Ctrl + C** ile boot job'ını iptal et
2. Giriş yaptıktan sonra aşağıdaki komutları çalıştır:

```bash
# Docker'ı durdur
sudo systemctl stop docker
sudo systemctl stop docker.socket

# Docker process'lerini temizle
sudo pkill -9 docker
sudo pkill -9 containerd

# Docker'ın pid/socket dosyalarını temizle
sudo rm -rf /var/run/docker.sock
sudo rm -rf /var/run/docker.pid

# Docker'ı yeniden başlat
sudo systemctl start docker

# Durumu kontrol et
sudo systemctl status docker
```

### Seçenek 2: SSH ile Bağlan
Eğer SSH açıksa, Mac'inizden:

```bash
# VM'e bağlan
ssh ugur@[VM-IP-ADRESI]

# Yukarıdaki temizleme komutlarını çalıştır
```

### Seçenek 3: Single User Mode
Hiçbir şey çalışmazsa:
1. UTM'de VM'i yeniden başlat
2. GRUB menüsünde `e` tuşuna bas
3. `linux` satırının sonuna `single` ekle
4. **Ctrl + X** ile boot et
5. Root shell'den Docker'ı temizle

---

## 🔧 Kalıcı Çözüm: Otomatik Tamir Scripti

### 1. Otomatik Temizleme Scripti Oluştur

VM içinde bu scripti oluştur:

```bash
sudo nano /usr/local/bin/docker-cleanup.sh
```

İçeriği:

```bash
#!/bin/bash
# Docker temizleme scripti - UTM VM'lerde boot sorunlarını çözer

echo "Docker cleanup başlıyor..."

# Docker'ı durdur
systemctl stop docker.socket 2>/dev/null
systemctl stop docker 2>/dev/null

# Docker process'lerini temizle
pkill -9 dockerd 2>/dev/null
pkill -9 containerd 2>/dev/null
pkill -9 docker-proxy 2>/dev/null

# Stale dosyaları temizle
rm -rf /var/run/docker.sock 2>/dev/null
rm -rf /var/run/docker.pid 2>/dev/null
rm -rf /var/run/containerd/containerd.sock 2>/dev/null

# Log
echo "$(date): Docker cleanup tamamlandı" >> /var/log/docker-cleanup.log

# Docker'ı tekrar başlat
systemctl start docker

exit 0
```

Script'i çalıştırılabilir yap:

```bash
sudo chmod +x /usr/local/bin/docker-cleanup.sh
```

---

### 2. Systemd Service Oluştur (Boot Sırasında Otomatik Temizlik)

```bash
sudo nano /etc/systemd/system/docker-cleanup.service
```

İçeriği:

```ini
[Unit]
Description=Docker Cleanup Service for UTM VMs
Before=docker.service
DefaultDependencies=no

[Service]
Type=oneshot
ExecStart=/usr/local/bin/docker-cleanup.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Service'i aktifleştir:

```bash
sudo systemctl daemon-reload
sudo systemctl enable docker-cleanup.service
```

---

### 3. Docker Timeout Ayarı (Takılmayı Önle)

Docker'ın timeout süresini kısalt:

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/timeout.conf
```

İçeriği:

```ini
[Service]
TimeoutStartSec=30
TimeoutStopSec=30
```

Reload ve restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 🕐 Zaman Senkronizasyonu (Önemli!)

UTM VM'lerde en büyük sorun zaman uyumsuzluğu. Docker logları future tarihli olabiliyor.

### Chrony veya systemd-timesyncd Kullan

#### Seçenek A: Chrony (Önerilen)

```bash
# Kurulum
sudo apt update
sudo apt install chrony -y

# Ayarlar
sudo nano /etc/chrony/chrony.conf
```

Ekle/düzenle:

```conf
# NTP sunucuları
server time.apple.com iburst
server pool.ntp.org iburst
server time.google.com iburst

# RTC'yi güncelle
rtcsync

# Büyük zaman farklarını düzelt
makestep 1.0 3
```

Başlat:

```bash
sudo systemctl enable chrony
sudo systemctl restart chrony

# Kontrol
chronyc tracking
```

#### Seçenek B: systemd-timesyncd

```bash
sudo nano /etc/systemd/timesyncd.conf
```

Ekle:

```ini
[Time]
NTP=time.apple.com pool.ntp.org time.google.com
FallbackNTP=0.pool.ntp.org 1.pool.ntp.org
```

Başlat:

```bash
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd

# Kontrol
timedatectl status
```

---

## 🛡️ Graceful Shutdown Script

VM'i her kapatışta Docker'ı düzgün kapatmak için:

```bash
sudo nano /usr/local/bin/vm-shutdown.sh
```

İçeriği:

```bash
#!/bin/bash
echo "$(date): VM kapatılıyor, Docker container'ları durduruluyor..." >> /var/log/vm-shutdown.log

# Home Assistant container'ını düzgün kapat
docker stop homeassistant 2>/dev/null

# Diğer container'ları durdur
docker stop $(docker ps -q) 2>/dev/null

# Docker servisini durdur
systemctl stop docker

echo "$(date): Shutdown tamamlandı" >> /var/log/vm-shutdown.log
```

Çalıştırılabilir yap:

```bash
sudo chmod +x /usr/local/bin/vm-shutdown.sh
```

Systemd service:

```bash
sudo nano /etc/systemd/system/vm-shutdown.service
```

İçeriği:

```ini
[Unit]
Description=VM Graceful Shutdown
DefaultDependencies=no
Before=shutdown.target reboot.target halt.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/vm-shutdown.sh
TimeoutStartSec=0

[Install]
WantedBy=halt.target reboot.target shutdown.target
```

Aktifleştir:

```bash
sudo systemctl daemon-reload
sudo systemctl enable vm-shutdown.service
```

---

## 📝 VM Kullanım Önerileri

### VM'i Kapatmadan Önce

```bash
# Docker container'larını kontrol et
docker ps

# Home Assistant'ı düzgün kapat (UI'dan veya CLI'dan)
docker exec homeassistant ha core stop

# Docker'ı durdur
sudo systemctl stop docker

# Şimdi VM'i kapat
sudo shutdown -h now
```

### VM'i Açtıktan Sonra

```bash
# Zaman doğru mu kontrol et
date

# Docker çalışıyor mu?
sudo systemctl status docker

# Home Assistant container çalışıyor mu?
docker ps | grep homeassistant
```

---

## 🔍 Troubleshooting Komutları

### Docker Durumunu Kontrol

```bash
# Servis durumu
sudo systemctl status docker

# Docker logları
sudo journalctl -u docker -n 50 --no-pager

# Docker process'leri
ps aux | grep docker
```

### Container Durumunu Kontrol

```bash
# Çalışan container'lar
docker ps

# Tüm container'lar (durmuş olanlar dahil)
docker ps -a

# Home Assistant logları
docker logs homeassistant
```

### Zaman Kontrolü

```bash
# Sistem zamanı
date

# Donanım saati
sudo hwclock --show

# NTP durumu (chrony)
chronyc tracking

# NTP durumu (systemd-timesyncd)
timedatectl status
```

### Docker Sorun Giderme

```bash
# Docker daemon logları (verbose)
sudo dockerd --debug --log-level=debug

# Socket durumu
ls -la /var/run/docker.sock

# Docker restart (force)
sudo systemctl stop docker
sudo pkill -9 dockerd
sudo systemctl start docker
```

---

## 🚀 Hızlı Komut Özeti

### Acil Durum (Boot Takıldı):
```bash
sudo systemctl stop docker
sudo pkill -9 docker
sudo rm -rf /var/run/docker.sock
sudo systemctl start docker
```

### Günlük Kullanım:
```bash
# Kapatmadan önce
docker exec homeassistant ha core stop
sudo systemctl stop docker
sudo shutdown -h now

# Açtıktan sonra
date  # Zaman kontrolü
sudo systemctl status docker  # Docker kontrolü
docker ps  # Container kontrolü
```

### Düzenli Bakım:
```bash
# Docker temizliği (ayda bir)
docker system prune -a --volumes -f

# Log temizliği
sudo journalctl --vacuum-time=7d

# Disk kontrolü
df -h
```

---

## 📋 Checklist: Kalıcı Çözüm

- [ ] Docker cleanup scripti oluşturuldu (`/usr/local/bin/docker-cleanup.sh`)
- [ ] Docker cleanup service aktif (`docker-cleanup.service`)
- [ ] Docker timeout ayarları yapıldı
- [ ] Zaman senkronizasyonu kuruldu (chrony/timesyncd)
- [ ] Graceful shutdown scripti oluşturuldu
- [ ] VM shutdown service aktif
- [ ] Test edildi (VM'i kapat, bekle, aç)

---

## 🎯 Sonuç

Bu adımları uyguladıktan sonra:
- ✅ VM'i kapatıp açtığınızda Docker sorunsuz başlayacak
- ✅ Zaman senkronizasyonu otomatik düzelecek
- ✅ Boot takılma sorunu olmayacak
- ✅ Container'lar düzgün kapanıp açılacak

---

## 💡 İpuçları

1. **VM'i suspend etmeyin**, her zaman shutdown kullanın
2. **UTM'de "Save State" yerine normal kapatma** yapın
3. **VM'i uzun süre kapalı bırakacaksanız**, açtıktan sonra zaman kontrolü yapın
4. **Weekly backup** alın (Home Assistant snapshot)
5. **Docker container'ları monitör edin** (Portainer veya CLI)

---

İhtiyacınız olursa diğer troubleshooting adımlarını README.md'ye ekleyebilirim! 🚀


