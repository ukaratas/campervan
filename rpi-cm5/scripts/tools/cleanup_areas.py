#!/usr/bin/env python3
"""Remove legacy / unwanted Home Assistant areas by name (WebSocket API).

Default: Living Room, Devices — often left from HA defaults or onboarding.
Safe to re-run; missing names are skipped.

Usage: python3 cleanup_areas.py
Env: HA_URL, HA_TOKEN
"""
import asyncio
import json
import os
import sys

import websockets

# Areas to remove from the registry (exact name match).
REMOVE_NAMES = frozenset({"Living Room", "Devices"})


async def main() -> None:
    ha_url = os.environ.get("HA_URL", "").rstrip("/")
    token = os.environ.get("HA_TOKEN")
    if not ha_url or not token:
        print("ERROR: HA_URL and HA_TOKEN must be set")
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
        raw = msg.get("result")
        if isinstance(raw, dict):
            areas_list = raw.get("areas") or raw.get("items") or []
        else:
            areas_list = raw or []

        by_name = {a.get("name"): a for a in areas_list if isinstance(a, dict) and a.get("name")}
        req_id = 2
        for name in sorted(REMOVE_NAMES):
            area = by_name.get(name)
            if not area:
                print(f"  [SKIP] No area named {name!r}")
                continue
            aid = area.get("area_id") or area.get("id")
            if not aid:
                print(f"  [WARN] {name!r} has no area_id: {area}")
                continue
            await ws.send(
                json.dumps({"id": req_id, "type": "config/area_registry/delete", "area_id": aid})
            )
            resp = json.loads(await ws.recv())
            req_id += 1
            if resp.get("success"):
                print(f"  [OK] Deleted area: {name} ({aid})")
            else:
                print(f"  [WARN] {name}: {resp.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
