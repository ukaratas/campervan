#!/usr/bin/env bash
# Install and configure Terminal & SSH addon.
# Uses WebSocket API (no SSH dependency - this IS the SSH setup).
# Idempotent - safe to run multiple times.
#
# Usage: ./setup_ssh.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../ha_helpers.sh"

ADDON_SLUG="core_ssh"

echo "=== SSH Addon Setup ==="
ha_check_connection
echo ""

# ── Step 1: Install SSH addon via WebSocket ──────────────────────
echo "Step 1: Install SSH addon"

ha_ws "
async def main():
    async with websockets.connect(WS_URI, max_size=2**22, ping_interval=20, ping_timeout=120, open_timeout=30) as ws:
        await _ws_auth(ws)

        # Check if already installed
        await ws.send(json.dumps({
            'id': 1, 'type': 'supervisor/api',
            'endpoint': '/addons/${ADDON_SLUG}/info', 'method': 'get'
        }))
        msg = json.loads(await ws.recv())
        info = msg.get('result', {})

        if info.get('version'):
            print(f'  [SKIP] SSH already installed (v{info[\"version\"]}, state={info.get(\"state\")})')
            return

        # Reload store
        await ws.send(json.dumps({
            'id': 2, 'type': 'supervisor/api',
            'endpoint': '/store/reload', 'method': 'post'
        }))
        await ws.recv()
        await asyncio.sleep(3)

        # Install
        print('  [INSTALL] Downloading SSH addon...')
        await ws.send(json.dumps({
            'id': 3, 'type': 'supervisor/api',
            'endpoint': '/store/addons/${ADDON_SLUG}/install', 'method': 'post'
        }))
        try:
            msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=300))
            if msg.get('success'):
                print('  [OK] SSH addon installed')
            else:
                err = msg.get('error', {}).get('message', 'unknown')
                print(f'  [ERROR] Install failed: {err}')
                print('  [HINT] If this fails, install manually from HA UI: Settings > Apps > Terminal & SSH')
                sys.exit(1)
        except asyncio.TimeoutError:
            print('  [WARN] Install timed out - image may still be downloading')
            print('  [HINT] Re-run this script in a few minutes')
            sys.exit(1)
"

echo ""

# ── Step 2: Configure SSH addon (key-based auth) ────────────────
echo "Step 2: Configure SSH addon"

# Mac'te key yoksa otomatik üret. Public key add-on'a authorized_keys olarak gönderilir.
SSH_KEY_PATH="${SSH_KEY:-$HOME/.ssh/id_ed25519_haos}"
if [[ ! -f "$SSH_KEY_PATH" ]]; then
    echo "  [GEN] SSH key yok, üretiliyor: $SSH_KEY_PATH"
    mkdir -p "$(dirname "$SSH_KEY_PATH")"
    ssh-keygen -t ed25519 -f "$SSH_KEY_PATH" -N "" -C "$(whoami)@$(hostname -s) → haos-cv $(date +%Y%m%d)"
fi
PUB_KEY="$(cat "${SSH_KEY_PATH}.pub")"
export PUB_KEY

# ~/.ssh/config'e haos-cv host bloğu ekle (yoksa)
SSH_CFG="$HOME/.ssh/config"
mkdir -p "$HOME/.ssh"
touch "$SSH_CFG"
chmod 600 "$SSH_CFG"
if ! grep -q "^Host haos-cv" "$SSH_CFG"; then
    cat >> "$SSH_CFG" <<EOF

# HAOS — Camper-Neo (LAN); setup_ssh.sh tarafından eklendi
Host haos-cv ${HA_HOST}
    HostName ${HA_HOST}
    User root
    IdentityFile ${SSH_KEY_PATH}
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new
    ServerAliveInterval 15
    ServerAliveCountMax 4
EOF
    echo "  [OK] ~/.ssh/config'e Host haos-cv eklendi"
fi

ha_ws "
async def main():
    async with websockets.connect(WS_URI, max_size=2**22, ping_interval=20, ping_timeout=60, open_timeout=30) as ws:
        await _ws_auth(ws)

        # Authorized key + password disable (key-only login)
        await ws.send(json.dumps({
            'id': 1, 'type': 'supervisor/api',
            'endpoint': '/addons/${ADDON_SLUG}/options',
            'method': 'post',
            'data': {'options': {
                'authorized_keys': ['${PUB_KEY}'],
                'password': '',
                'sftp': True
            }}
        }))
        msg = json.loads(await ws.recv())
        if msg.get('success'):
            print('  [OK] authorized_keys configured (password disabled)')
        else:
            print(f'  [ERROR] Config failed: {msg.get(\"error\", {})}')
            sys.exit(1)

        # Enable port 22, auto-start
        await ws.send(json.dumps({
            'id': 2, 'type': 'supervisor/api',
            'endpoint': '/addons/${ADDON_SLUG}/options/config',
            'method': 'post',
            'data': {'boot': 'auto', 'watchdog': True, 'network': {'22/tcp': 22}}
        }))
        msg = json.loads(await ws.recv())
        print(f'  [{\"OK\" if msg.get(\"success\") else \"WARN\"}] Auto-start + port 22 + watchdog')
"

echo ""

# ── Step 3: Start SSH addon ─────────────────────────────────────
echo "Step 3: Start SSH addon"

ha_ws "
async def main():
    async with websockets.connect(WS_URI, max_size=2**22, ping_interval=20, ping_timeout=60, open_timeout=30) as ws:
        await _ws_auth(ws)

        # Check state
        await ws.send(json.dumps({
            'id': 1, 'type': 'supervisor/api',
            'endpoint': '/addons/${ADDON_SLUG}/info', 'method': 'get'
        }))
        msg = json.loads(await ws.recv())
        state = msg.get('result', {}).get('state')

        if state == 'started':
            print('  [SKIP] SSH already running')
            return

        # Restart if running (to pick up config changes), otherwise start
        action = 'restart' if state == 'started' else 'start'
        await ws.send(json.dumps({
            'id': 2, 'type': 'supervisor/api',
            'endpoint': f'/addons/${ADDON_SLUG}/{action}', 'method': 'post'
        }))
        msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=30))
        if msg.get('success'):
            print(f'  [OK] SSH {action}ed')
        else:
            print(f'  [ERROR] {action} failed: {msg.get(\"error\", {})}')
            sys.exit(1)
"

echo ""

# ── Step 4: Verify SSH connectivity ─────────────────────────────
echo "Step 4: Verify SSH connectivity"

require_sshpass
sleep 3

if ssh_ha_check; then
    echo "  [OK] SSH connection verified (root@${HA_HOST}:22)"
    VERSION=$(ssh_ha "ha core info --raw-json" 2>/dev/null | \
        python3 -c "import sys,json; print(json.load(sys.stdin)['data']['version'])" 2>/dev/null || echo "?")
    echo "  [OK] HA Core version via SSH: $VERSION"
else
    echo "  [WARN] SSH connection failed - port may not be exposed yet"
    echo "  [HINT] In HA UI: Apps > Terminal & SSH > Configuration > Network > enable port 22 > Save > Restart"
fi

echo ""
echo "=== SSH Setup complete ==="
echo ""
echo "  Connect: ssh haos-cv    (or: ssh root@${HA_HOST})"
echo "  Auth:    key-based (${SSH_KEY_PATH})"
echo "  Note:    password login disabled — only this Mac's key is accepted"
