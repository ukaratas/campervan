#!/usr/bin/env python3
"""Remove one or more entities from Home Assistant entity registry (WebSocket API).

Use for stale \"restored\" entities left after YAML/integration changes.
Reads HA_URL and HA_TOKEN from ../.env (same as ha_enable_entities.py).
"""

import asyncio
import json
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


async def remove_entities(entity_ids):
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
        req_id = 1
        for eid in entity_ids:
            await ws.send(
                json.dumps(
                    {
                        "id": req_id,
                        "type": "config/entity_registry/remove",
                        "entity_id": eid,
                    }
                )
            )
            resp = json.loads(await ws.recv())
            ok = resp.get("success", False)
            print(f"[{'OK' if ok else 'FAIL'}] {eid}")
            if not ok:
                print(resp)
            req_id += 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <entity_id> [entity_id ...]")
        sys.exit(1)
    asyncio.run(remove_entities(sys.argv[1:]))
