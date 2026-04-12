#!/usr/bin/env python3
"""Create Home Assistant areas (rooms) via WebSocket API if they do not exist.

Usage (from rpi-cm5/):  python3 scripts/setup/setup_areas.py

Requires: HA_URL, HA_TOKEN in .env, websockets
"""
import asyncio
import json
import os
import sys

import websockets

# Camper logical areas (English). Icons: MDI.
DEFAULT_AREAS = [
    {"name": "Bedroom", "icon": "mdi:bed"},
    {"name": "Bathroom", "icon": "mdi:shower"},
    {"name": "Kitchen", "icon": "mdi:stove"},
    {"name": "Saloon", "icon": "mdi:sofa-outline"},
    {"name": "Utility", "icon": "mdi:wrench-outline"},
]


async def main() -> None:
    ha_url = os.environ.get("HA_URL", "").rstrip("/")
    token = os.environ.get("HA_TOKEN")
    if not ha_url or not token:
        print("ERROR: HA_URL and HA_TOKEN must be set (e.g. source .env)")
        sys.exit(1)

    uri = ha_url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"
    async with websockets.connect(uri, max_size=2**22, ping_interval=20, open_timeout=15) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        msg = json.loads(await ws.recv())
        if msg["type"] != "auth_ok":
            print("ERROR: Auth failed", msg)
            sys.exit(1)

        await ws.send(json.dumps({"id": 1, "type": "config/area_registry/list"}))
        msg = json.loads(await ws.recv())
        if msg.get("type") != "result" or not msg.get("success", True):
            print("ERROR: area_registry/list failed", msg)
            sys.exit(1)

        raw = msg.get("result")
        if isinstance(raw, dict):
            areas_list = raw.get("areas") or raw.get("items") or []
        else:
            areas_list = raw or []
        existing = {a.get("name") for a in areas_list if isinstance(a, dict)}
        print(f"  Existing areas: {len(existing)}")

        req_id = 2
        for spec in DEFAULT_AREAS:
            name = spec["name"]
            if name in existing:
                print(f"  [SKIP] {name}")
                continue
            await ws.send(
                json.dumps(
                    {
                        "id": req_id,
                        "type": "config/area_registry/create",
                        "name": name,
                        "icon": spec.get("icon", "mdi:home-outline"),
                    }
                )
            )
            resp = json.loads(await ws.recv())
            req_id += 1
            if resp.get("success"):
                print(f"  [OK] Created area: {name}")
                existing.add(name)
            else:
                err = resp.get("error", {})
                print(f"  [WARN] {name}: {err}")


if __name__ == "__main__":
    asyncio.run(main())
