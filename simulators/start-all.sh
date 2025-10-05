#!/bin/bash
# Tüm Waveshare Simülatörlerini Başlat
# Multi-instance destekli

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Virtual environment aktive et
source venv/bin/activate

echo "================================"
echo "🚀 WAVESHARE SİMÜLATÖRLER"
echo "================================"
echo ""

# Örnek 1: Tek modül (basit)
echo "📋 Seçenek 1: Basit Başlangıç (1 DI/DO + 1 Relay)"
echo "   python3 waveshare-di-do.py"
echo "   python3 waveshare-latching-relay.py"
echo ""

# Örnek 2: İki latching relay (farklı portlarda)
echo "📋 Seçenek 2: İki Latching Relay Modülü"
echo "   python3 waveshare-latching-relay.py --port 5023 --name Relay-1"
echo "   python3 waveshare-latching-relay.py --port 5024 --name Relay-2"
echo ""

# Örnek 3: Full sistem
echo "📋 Seçenek 3: Tam Sistem (2 DI/DO + 2 Relay)"
echo "   python3 waveshare-di-do.py --port 5022 --name DI/DO-1"
echo "   python3 waveshare-di-do.py --port 5025 --name DI/DO-2"
echo "   python3 waveshare-latching-relay.py --port 5023 --name Relay-Lighting"
echo "   python3 waveshare-latching-relay.py --port 5024 --name Relay-Misc"
echo ""
echo "================================"
echo ""

# Kullanıcıdan seçim al
read -p "Hangi konfigürasyonu başlatmak istersin? (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Başlatılıyor: 1 DI/DO + 1 Latching Relay"
        echo ""
        echo "Terminal-1: DI/DO Module (Port 5022)"
        echo "Terminal-2: Latching Relay (Port 5023)"
        echo ""
        echo "Şimdi iki ayrı terminal aç ve şunları çalıştır:"
        echo ""
        echo "# Terminal 1:"
        echo "cd $SCRIPT_DIR && source venv/bin/activate && python3 waveshare-di-do.py"
        echo ""
        echo "# Terminal 2:"
        echo "cd $SCRIPT_DIR && source venv/bin/activate && python3 waveshare-latching-relay.py"
        ;;
    2)
        echo ""
        echo "🚀 Başlatılıyor: 2 Latching Relay Modülü"
        echo ""
        echo "# Terminal 1:"
        echo "cd $SCRIPT_DIR && source venv/bin/activate && python3 waveshare-latching-relay.py --port 5023 --name Relay-1"
        echo ""
        echo "# Terminal 2:"
        echo "cd $SCRIPT_DIR && source venv/bin/activate && python3 waveshare-latching-relay.py --port 5024 --name Relay-2"
        ;;
    3)
        echo ""
        echo "🚀 Başlatılıyor: Tam Sistem (4 Modül)"
        echo ""
        echo "# Terminal 1: DI/DO-1"
        echo "cd $SCRIPT_DIR && source venv/bin/activate && python3 waveshare-di-do.py --port 5022 --name DI/DO-1"
        echo ""
        echo "# Terminal 2: DI/DO-2"
        echo "cd $SCRIPT_DIR && source venv/bin/activate && python3 waveshare-di-do.py --port 5025 --name DI/DO-2"
        echo ""
        echo "# Terminal 3: Relay-Lighting"
        echo "cd $SCRIPT_DIR && source venv/bin/activate && python3 waveshare-latching-relay.py --port 5023 --name Relay-Lighting"
        echo ""
        echo "# Terminal 4: Relay-Misc"
        echo "cd $SCRIPT_DIR && source venv/bin/activate && python3 waveshare-latching-relay.py --port 5024 --name Relay-Misc"
        ;;
    *)
        echo "❌ Geçersiz seçim!"
        exit 1
        ;;
esac

echo ""
echo "================================"

