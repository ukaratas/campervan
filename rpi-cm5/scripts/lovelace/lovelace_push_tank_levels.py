#!/usr/bin/env python3
"""Tank Seviyeleri (tank-levels) — Modbus analog + maceratör; yakıt CAN için yer tutucu."""
import asyncio
import json
import os
import sys

import websockets

WS_URI = os.environ["HA_URL"].replace("http://", "ws://") + "/api/websocket"
WS_TOKEN = os.environ["HA_TOKEN"]


async def main() -> None:
    async with websockets.connect(WS_URI, max_size=2**22, ping_interval=20, open_timeout=15) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": WS_TOKEN}))
        msg = json.loads(await ws.recv())
        if msg["type"] != "auth_ok":
            print("  [ERROR] Auth failed")
            sys.exit(1)

        await ws.send(json.dumps({"id": 1, "type": "lovelace/dashboards/list"}))
        msg = json.loads(await ws.recv())
        exists = False
        for d in msg.get("result", []):
            if d.get("url_path") == "tank-levels":
                exists = True
                break

        if not exists:
            await ws.send(
                json.dumps(
                    {
                        "id": 2,
                        "type": "lovelace/dashboards/create",
                        "url_path": "tank-levels",
                        "title": "Tank Levels",
                        "icon": "mdi:water",
                        "require_admin": False,
                        "show_in_sidebar": True,
                    }
                )
            )
            msg = json.loads(await ws.recv())
            if not msg.get("success"):
                print(f"  [ERROR] {msg.get('error')}")
                return
            print("  [OK] Dashboard 'tank-levels' created")
        else:
            print("  [OK] Dashboard 'tank-levels' exists")

        fuel_note = (
            "## Yakıt (90 L)\n"
            "Seviye **ileride araç CAN bus** üzerinden okunacak. "
            "Şimdilik bu sütunda kart yok; hata/uyarı üretmemesi için MQTT şablon entity’leri kaldırıldı."
        )

        config = {
            "views": [
                {
                    "title": "Tank Seviyeleri",
                    "path": "default_view",
                    "icon": "mdi:water",
                    "type": "sections",
                    "max_columns": 3,
                    "sections": [
                        {
                            "title": "Temiz Su (180L)",
                            "type": "grid",
                            "cards": [
                                {
                                    "type": "gauge",
                                    "entity": "sensor.tank_temiz_su_seviye",
                                    "name": "Temiz Su",
                                    "unit": "%",
                                    "min": 0,
                                    "max": 100,
                                    "needle": True,
                                    "severity": {"green": 50, "yellow": 20, "red": 0},
                                },
                                {
                                    "type": "tile",
                                    "entity": "sensor.tank_temiz_su_hacim",
                                    "name": "Temiz Su",
                                    "icon": "mdi:water",
                                    "color": "cyan",
                                },
                                {
                                    "type": "entity",
                                    "entity": "sensor.tank_temiz_su_seviye",
                                    "name": "Seviye",
                                    "icon": "mdi:water",
                                },
                            ],
                        },
                        {
                            "title": "Kirli Su (100L)",
                            "type": "grid",
                            "cards": [
                                {
                                    "type": "gauge",
                                    "entity": "sensor.tank_kirli_su_seviye",
                                    "name": "Kirli Su",
                                    "unit": "%",
                                    "min": 0,
                                    "max": 100,
                                    "needle": True,
                                    "severity": {"green": 0, "yellow": 60, "red": 80},
                                },
                                {
                                    "type": "tile",
                                    "entity": "sensor.tank_kirli_su_hacim",
                                    "name": "Kirli Su",
                                    "icon": "mdi:water-off",
                                    "color": "grey",
                                },
                                {
                                    "type": "entity",
                                    "entity": "sensor.tank_kirli_su_seviye",
                                    "name": "Seviye",
                                    "icon": "mdi:water-off",
                                },
                                {
                                    "type": "tile",
                                    "entity": "switch.ch1_macerator_pump",
                                    "name": "Maceratör pompa",
                                    "icon": "mdi:pump",
                                    "color": "red",
                                    "features": [{"type": "toggle"}],
                                },
                            ],
                        },
                        {
                            "title": "Yakıt (90L)",
                            "type": "grid",
                            "cards": [{"type": "markdown", "content": fuel_note}],
                        },
                    ],
                }
            ]
        }

        await ws.send(
            json.dumps({"id": 20, "type": "lovelace/config/save", "url_path": "tank-levels", "config": config})
        )
        msg = json.loads(await ws.recv())
        if msg.get("success"):
            print("  [OK] tank-levels: Modbus tank + yakıt notu kaydedildi")
        else:
            print(f"  [ERROR] {msg.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
