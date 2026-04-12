#!/usr/bin/env python3
"""Enable disabled entities for a given HA integration platform via WebSocket API."""

import json
import asyncio
import os
import sys
from pathlib import Path

_scripts = Path(__file__).resolve().parent.parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))
from repo_paths import repo_root  # noqa: E402

try:
    import websockets
except ImportError:
    print("Installing websockets...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
    import websockets


def load_env():
    env_file = repo_root() / ".env"
    if not os.path.exists(env_file):
        print(f"ERROR: .env not found at {env_file}")
        sys.exit(1)
    env = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


async def enable_platform_entities(platform: str, entity_filter=None):
    env = load_env()
    ha_url = env["HA_URL"]
    ha_token = env["HA_TOKEN"]

    uri = ha_url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"
    async with websockets.connect(uri) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": ha_token}))
        msg = json.loads(await ws.recv())
        if msg["type"] != "auth_ok":
            print(f"Auth failed: {msg}")
            return

        await ws.send(json.dumps({"id": 1, "type": "config/entity_registry/list"}))
        msg = json.loads(await ws.recv())
        entities = msg.get("result", [])

        targets = [e for e in entities if e.get("platform") == platform]
        if entity_filter:
            targets = [e for e in targets if entity_filter(e)]

        disabled = [e for e in targets if e.get("disabled_by")]
        print(f"Platform '{platform}': {len(targets)} total, {len(disabled)} disabled")

        req_id = 2
        for e in disabled:
            await ws.send(json.dumps({
                "id": req_id,
                "type": "config/entity_registry/update",
                "entity_id": e["entity_id"],
                "disabled_by": None,
            }))
            resp = json.loads(await ws.recv())
            ok = resp.get("success", False)
            status = "OK" if ok else "FAIL"
            print(f"  [{status}] {e['entity_id']}")
            req_id += 1

        print(f"\nEnabled {len(disabled)} entities.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <platform_name>")
        print("Example: python3 ha_enable_entities.py systemmonitor")
        sys.exit(1)

    asyncio.run(enable_platform_entities(sys.argv[1]))
