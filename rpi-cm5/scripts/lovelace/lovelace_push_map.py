#!/usr/bin/env python3
"""User Overview (map) dashboard — caravan-friendly responsive layout."""
import asyncio
import json
import os
import sys
from typing import Optional

import websockets

WS_URI = os.environ["HA_URL"].replace("http://", "ws://") + "/api/websocket"
WS_TOKEN = os.environ["HA_TOKEN"]


def _toggle_tile(entity: str, name: str, icon: Optional[str] = None) -> dict:
    card = {
        "type": "tile",
        "entity": entity,
        "name": name,
        "features": [{"type": "toggle"}],
    }
    if icon:
        card["icon"] = icon
    return card


def _info_tile(entity: str, name: str, icon: Optional[str] = None) -> dict:
    card = {
        "type": "tile",
        "entity": entity,
        "name": name,
    }
    if icon:
        card["icon"] = icon
    return card


def _favorite_tile(entity: str, name: str) -> dict:
    return {
        **_toggle_tile(entity, name),
        "vertical": False,
    }


def _area_button(name: str, icon: str, path: str) -> dict:
    return {
        "type": "button",
        "name": name,
        "icon": icon,
        "tap_action": {"action": "navigate", "navigation_path": path},
    }


def _area_view(title: str, path: str, icon: str, cards: list[dict]) -> dict:
    return {
        "title": title,
        "path": path,
        "icon": icon,
        "type": "sections",
        "max_columns": 3,
        "sections": [
            {
                "type": "grid",
                "cards": cards,
            }
        ],
    }


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
            if d.get("url_path") == "map":
                exists = True
                break

        if not exists:
            await ws.send(
                json.dumps(
                    {
                        "id": 2,
                        "type": "lovelace/dashboards/create",
                        "url_path": "map",
                        "title": "CamperNeo",
                        "icon": "mdi:caravan",
                        "require_admin": False,
                        "show_in_sidebar": True,
                    }
                )
            )
            msg = json.loads(await ws.recv())
            if not msg.get("success"):
                print(f"  [ERROR] {msg.get('error')}")
                return
            print("  [OK] Dashboard 'CamperNeo' (map) created")
        else:
            print("  [OK] Dashboard 'map' exists")
            await ws.send(
                json.dumps(
                    {
                        "id": 3,
                        "type": "lovelace/dashboards/update",
                        "dashboard_id": "map",
                        "title": "CamperNeo",
                        "icon": "mdi:caravan",
                        "require_admin": False,
                        "show_in_sidebar": True,
                    }
                )
            )
            msg = json.loads(await ws.recv())
            if msg.get("success"):
                print("  [OK] Dashboard title/icon updated to CamperNeo")
            else:
                print(f"  [WARN] Dashboard metadata update skipped: {msg.get('error')}")

        favorites = [
            _favorite_tile("switch.ch4_air_condition", "Air Condition"),
            _favorite_tile("switch.ch5_bed_light", "Bed Light"),
            _favorite_tile("switch.ch1_220v_outlets", "220V Outlets"),
            _favorite_tile("switch.ch2_clesana_c1", "Clesana C1"),
            _favorite_tile("switch.ch1_macerator_pump", "Macerator pump"),
            _favorite_tile("switch.ch2_refrigerator", "Refrigerator"),
            _favorite_tile("switch.ch3_bed_left_reading_light", "Left reading light"),
            _favorite_tile("switch.ws_io8_do3", "Warning output"),
        ]

        areas = [
            _area_button("Kitchen", "mdi:silverware-fork-knife", "/map/kitchen"),
            _area_button("Bedroom", "mdi:bed-king-outline", "/map/bedroom"),
            _area_button("Bathroom", "mdi:shower", "/map/bathroom"),
            _area_button("Saloon", "mdi:sofa-outline", "/map/saloon"),
            _area_button("Utility", "mdi:tools", "/map/utility"),
            _area_button("Systems", "mdi:car-coolant-level", "/map/systems"),
            _area_button("Tank Levels", "mdi:water", "/tank-levels/default_view"),
        ]

        kitchen_view = _area_view(
            "Kitchen",
            "kitchen",
            "mdi:silverware-fork-knife",
            [
                {"type": "heading", "heading": "Kitchen controls"},
                _toggle_tile("switch.ch6_kitchen_light", "Kitchen light"),
                _toggle_tile("switch.ch2_refrigerator", "Refrigerator"),
                _toggle_tile("switch.ch10_dishwasher", "Dishwasher"),
                {"type": "heading", "heading": "Kitchen status"},
                _info_tile("binary_sensor.di5_kitchen_light", "Wall switch (DI5)"),
                _area_button("Back to overview", "mdi:arrow-left", "/map/default_view"),
            ],
        )

        bedroom_view = _area_view(
            "Bedroom",
            "bedroom",
            "mdi:bed-king-outline",
            [
                {"type": "heading", "heading": "Bedroom controls"},
                _toggle_tile("switch.ch3_bed_left_reading_light", "Left reading light"),
                _toggle_tile("switch.ch4_bed_right_reading_light", "Right reading light"),
                _toggle_tile("switch.ch5_bed_light", "Bed light"),
                {"type": "heading", "heading": "Bedroom status"},
                _info_tile("binary_sensor.di1_bed_left_reading_light", "DI1 Left reading"),
                _info_tile("binary_sensor.di2_bed_left_light", "DI2 Left bed light"),
                _info_tile("binary_sensor.di3_bed_right_reading_light", "DI3 Right reading"),
                _info_tile("binary_sensor.di4_bed_right_light", "DI4 Right bed light"),
                _area_button("Back to overview", "mdi:arrow-left", "/map/default_view"),
            ],
        )

        bathroom_view = _area_view(
            "Bathroom",
            "bathroom",
            "mdi:shower",
            [
                {"type": "heading", "heading": "Bathroom controls"},
                _toggle_tile("switch.ch1_macerator_pump", "Macerator pump"),
                _toggle_tile("switch.ch2_clesana_c1", "Clesana C1"),
                {"type": "heading", "heading": "Tank quick status"},
                _info_tile("sensor.tank_temiz_su_seviye", "Clean water (%)"),
                _info_tile("sensor.tank_kirli_su_seviye", "Gray water (%)"),
                _area_button("Back to overview", "mdi:arrow-left", "/map/default_view"),
            ],
        )

        saloon_view = _area_view(
            "Saloon",
            "saloon",
            "mdi:sofa-outline",
            [
                {"type": "heading", "heading": "Saloon controls"},
                _toggle_tile("switch.ch7_saloon_light", "Saloon light"),
                _toggle_tile("switch.ch11_washing_machine", "Washing machine"),
                {"type": "heading", "heading": "Saloon status"},
                _info_tile("binary_sensor.di6_saloon_light", "Wall switch (DI6)"),
                _area_button("Back to overview", "mdi:arrow-left", "/map/default_view"),
            ],
        )

        utility_view = _area_view(
            "Utility",
            "utility",
            "mdi:tools",
            [
                {"type": "heading", "heading": "Utility controls"},
                _toggle_tile("switch.ch1_220v_outlets", "220V outlets"),
                _toggle_tile("switch.ch3_usb_outlets", "USB outlets"),
                _toggle_tile("switch.ch4_air_condition", "Air condition"),
                _toggle_tile("switch.ch9_victron_blue_smart", "Victron Blue Smart power"),
                _toggle_tile("switch.ch8_outdoor_light", "Outdoor light"),
                {"type": "heading", "heading": "Utility status"},
                _info_tile("binary_sensor.di7_outdoor_light", "Outdoor switch (DI7)"),
                _area_button("Back to overview", "mdi:arrow-left", "/map/default_view"),
            ],
        )

        systems_view = _area_view(
            "Systems",
            "systems",
            "mdi:car-coolant-level",
            [
                {"type": "heading", "heading": "Water levels"},
                _info_tile("sensor.tank_temiz_su_seviye", "Clean water (%)"),
                _info_tile("sensor.tank_temiz_su_hacim", "Clean water (L)"),
                _info_tile("sensor.tank_kirli_su_seviye", "Gray water (%)"),
                _info_tile("sensor.tank_kirli_su_hacim", "Gray water (L)"),
                {"type": "heading", "heading": "Power / weather"},
                _info_tile("weather.forecast_home", "Weather"),
                _info_tile("binary_sensor.rpi_power_status", "RPi power"),
                _area_button("Back to overview", "mdi:arrow-left", "/map/default_view"),
            ],
        )

        overview_view = {
            "title": "Overview",
            "path": "default_view",
            "icon": "mdi:home",
            "type": "sections",
            "max_columns": 3,
            "sections": [
                {
                    "title": "Welcome camper-neo",
                    "type": "grid",
                    "cards": [{"type": "heading", "heading": "Favorites"}] + favorites,
                },
                {
                    "title": "Summaries",
                    "type": "grid",
                    "cards": [
                        {
                            "type": "tile",
                            "entity": "weather.forecast_home",
                            "name": "Weather",
                            "icon": "mdi:weather-partly-cloudy",
                        },
                        {
                            "type": "tile",
                            "entity": "sensor.tank_temiz_su_seviye",
                            "name": "Clean water",
                            "icon": "mdi:water",
                        },
                        {
                            "type": "tile",
                            "entity": "sensor.tank_kirli_su_seviye",
                            "name": "Gray water",
                            "icon": "mdi:water-off",
                        },
                    ],
                },
                {
                    "title": "Areas",
                    "type": "grid",
                    "cards": areas,
                },
            ],
        }

        config = {
            "views": [
                overview_view,
                kitchen_view,
                bedroom_view,
                bathroom_view,
                saloon_view,
                utility_view,
                systems_view,
            ]
        }

        await ws.send(json.dumps({"id": 20, "type": "lovelace/config/save", "url_path": "map", "config": config}))
        msg = json.loads(await ws.recv())
        if msg.get("success"):
            print("  [OK] map: overview sections saved")
        else:
            print(f"  [ERROR] {msg.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())

