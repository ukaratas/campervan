#!/usr/bin/env python3
"""Admin Bench Lovelace (WS-Relay-01/02, DI/DO, AI, Status) — HA WebSocket API.

Naming policy: English on this dashboard (see README — user dashboards use Turkish).
"""
import asyncio
import json
import os
import sys

import websockets

WS_URI = os.environ["HA_URL"].replace("http://", "ws://") + "/api/websocket"
WS_TOKEN = os.environ["HA_TOKEN"]

# Victron Blue Smart Charger (BLE). If HA re-discovers the device, update these entity IDs.
# All Victron BLE sensors share this prefix (update if HA re-discovers the charger).
BSC = "sensor.bsc_ip65_12_15_hq2349fuajv"
# Template sensors (insert_victron_gauge_templates.py) — always numeric so gauge cards never error.
# Eski registry kayıtları (kısa unique_id: victron_gauge_l1_v vb.) canonical slug'ı işgal edip
# unavailable kalabiliyor; güncel şablonlar *_2 entity_id ile oluşuyor — panele onları bağlıyoruz.
VG = {
    "temp": "sensor.victron_gauge_temp",
    "ac_a": "sensor.victron_gauge_ac_current_2",
    "l1_v": "sensor.victron_gauge_l1_voltage_2",
    "l1_a": "sensor.victron_gauge_l1_current_2",
    "l2_v": "sensor.victron_gauge_l2_voltage_2",
    "l2_a": "sensor.victron_gauge_l2_current_2",
    "l3_v": "sensor.victron_gauge_l3_voltage_2",
    "l3_a": "sensor.victron_gauge_l3_current_2",
}

# RPi CM5 / HA host — grouped System Monitor entities (expand if your HA exposes more).
RPI_CM5_GROUPS = [
    (
        "Compute & load",
        [
            "sensor.system_monitor_processor_temperature",
            "sensor.system_monitor_processor_use",
            "sensor.system_monitor_load_1_min",
            "sensor.system_monitor_load_5_min",
            "sensor.system_monitor_load_15_min",
            "sensor.system_monitor_last_boot",
        ],
    ),
    (
        "Memory & swap",
        [
            "sensor.system_monitor_memory_usage",
            "sensor.system_monitor_memory_free",
            "sensor.system_monitor_memory_use",
            "sensor.system_monitor_swap_usage",
            "sensor.system_monitor_swap_free",
            "sensor.system_monitor_swap_use",
        ],
    ),
    (
        "Storage",
        [
            "sensor.system_monitor_disk_usage",
            "sensor.system_monitor_disk_free",
            "sensor.system_monitor_disk_usage_config",
            "sensor.system_monitor_disk_free_config",
            "sensor.system_monitor_disk_usage_media",
            "sensor.system_monitor_disk_free_media",
        ],
    ),
    (
        "Network — IPv4 addresses",
        [
            "sensor.system_monitor_ipv4_address_wlan0",
            "sensor.system_monitor_ipv4_address_end0",
            "sensor.system_monitor_ipv4_address_hassio",
            "sensor.system_monitor_ipv4_address_docker0",
        ],
    ),
    (
        "Network — throughput (B/s)",
        [
            "sensor.system_monitor_network_throughput_in_wlan0",
            "sensor.system_monitor_network_throughput_out_wlan0",
            "sensor.system_monitor_network_throughput_in_end0",
            "sensor.system_monitor_network_throughput_out_end0",
        ],
    ),
    (
        "Kernel pressure (60 s average)",
        [
            "sensor.system_monitor_cpu_pressure_some_60s_average",
            "sensor.system_monitor_memory_pressure_some_60s_average",
            "sensor.system_monitor_io_pressure_some_60s_average",
        ],
    ),
    (
        "Processes & add-ons",
        [
            "binary_sensor.system_monitor_process_go2rtc",
            "binary_sensor.system_monitor_process_python3",
            "sensor.system_monitor_open_file_descriptors_go2rtc",
            "sensor.system_monitor_open_file_descriptors_python3",
        ],
    ),
    (
        "Battery / charging (host)",
        [
            "sensor.system_monitor_battery",
            "sensor.system_monitor_battery_empty",
            "binary_sensor.system_monitor_charging",
        ],
    ),
    (
        "Fan & power",
        [
            "sensor.system_monitor_pwmfan_fan_speed",
            "binary_sensor.rpi_power_status",
        ],
    ),
    (
        "MQTT — CamperVan RPi (setup_sensors.sh)",
        [
            {
                "entity": "sensor.campervan_rpi_cm5_rpi_cpu_sicaklik",
                "name": "CPU temperature (MQTT)",
            },
            {"entity": "sensor.campervan_rpi_cm5_rpi_uptime", "name": "Uptime (MQTT)"},
        ],
    ),
]


def _entities_card(title, rows):
    ent = []
    for row in rows:
        if isinstance(row, str):
            ent.append({"entity": row})
        else:
            ent.append(row)
    return {
        "type": "entities",
        "title": title,
        "show_header_toggle": False,
        "entities": ent,
    }


def _gauge(entity, *, min_v, max_v, name=None):
    g: dict = {
        "type": "gauge",
        "entity": entity,
        "needle": True,
        "min": min_v,
        "max": max_v,
    }
    if name:
        g["name"] = name
    return g


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
        bench_exists = False
        for d in msg.get("result", []):
            if d.get("url_path") == "admin-bench":
                bench_exists = True
                break
            if d.get("url_path") in ("relay-bench", "test-bench"):
                await ws.send(json.dumps({"id": 2, "type": "lovelace/dashboards/delete", "dashboard_id": d["id"]}))
                await ws.recv()

        if not bench_exists:
            await ws.send(
                json.dumps(
                    {
                        "id": 3,
                        "type": "lovelace/dashboards/create",
                        "url_path": "admin-bench",
                        "title": "Admin Bench",
                        "icon": "mdi:shield-crown-outline",
                        "require_admin": False,
                        "show_in_sidebar": True,
                    }
                )
            )
            msg = json.loads(await ws.recv())
            if not msg.get("success"):
                print(f"  [ERROR] {msg.get('error')}")
                return
            print("  [OK] Dashboard 'Admin Bench' created")
        else:
            print("  [OK] Dashboard 'Admin Bench' exists")

        eth_labels = [
            "CH1 — Macerator pump",
            "CH2 — Refrigerator",
            "CH3 — Bed Left Reading Light",
            "CH4 — Bed Right Reading Light",
            "CH5 — Bed Light",
            "CH6 — Kitchen Light",
            "CH7 — Saloon Light",
            "CH8 — Outdoor Light",
            "CH9 — Victron Blue Smart",
            "CH10 — Dishwasher",
            "CH11 — Washing Machine",
            "CH12 — Future use",
            "CH13 — Future use",
            "CH14 — Future use",
            "CH15 — Future use",
            "CH16 — Future use",
        ]
        entity_list = [{"entity": "switch.ch1_maserator_pompa", "name": eth_labels[0]}]
        for i in range(2, 17):
            entity_list.append({"entity": f"switch.ch{i}", "name": eth_labels[i - 1]})

        relay_info = (
            "## Waveshare Modbus PoE Ethernet Relay 16CH\n"
            "| | |\n|---|---|\n"
            "| **Module** | WS-01 |\n"
            f"| **IP** | {os.environ.get('RELAY_IP', '10.0.0.200')}:{os.environ.get('RELAY_PORT', '4196')} |\n"
            "| **Protocol** | Modbus RTU over TCP (native HA) |\n"
            "| **Slave** | 1 |\n"
            "| **Channels** | 16 (CH1–11 assigned loads; CH12–16 reserved) |"
        )

        relay_view_01 = {
            "title": "WS-Relay-01",
            "path": "ws-relay-01",
            "icon": "mdi:electric-switch",
            "cards": [
                {"type": "markdown", "content": relay_info},
                {
                    "type": "entities",
                    "title": "Relay control",
                    "show_header_toggle": False,
                    "entities": entity_list,
                },
            ],
        }

        rtu_labels = [
            "CH1 — 24V Camp Mode",
            "CH2 — 12V Camp Mode",
            "CH3 — 12V Camp Mode",
            "CH4 — Air Condition",
            "CH5 — Future use",
            "CH6 — Future use",
            "CH7 — Future use",
            "CH8 — Future use",
        ]
        rtu_entity_list = [
            {"entity": f"switch.ws_rtu_relay_ch{i}", "name": rtu_labels[i - 1]} for i in range(1, 9)
        ]
        rtu_info = (
            "## Waveshare Modbus RTU Relay (E) — RS485\n"
            "| | |\n|---|---|\n"
            "| **Contact** | **32 A** (8-channel module) |\n"
            "| **Bus** | USB–RS485 → `rs485_bus` (single serial port) |\n"
            "| **Slave** | **2** (same line as IO8=1, Analog=3) |\n"
            "| **Wiki** | [Relay (E)](https://www.waveshare.com/wiki/Modbus_RTU_Relay_(E)) |\n"
            "| **Coils** | 0–7 → CH1–CH4 loads; CH5–8 reserved |\n"
            "\n"
            "`configuration.yaml`: **`slave: 2`** under `rs485_bus`."
        )

        relay_view_02 = {
            "title": "WS-Relay-02",
            "path": "ws-relay-02",
            "icon": "mdi:serial-port",
            "cards": [
                {"type": "markdown", "content": rtu_info},
                {
                    "type": "entities",
                    "title": "RTU Relay (E) — 32 A, 8 ch",
                    "show_header_toggle": False,
                    "entities": rtu_entity_list,
                },
            ],
        }

        do_labels = [
            "DO1 — Warning Light",
            "DO2 — Error Buzzer",
        ] + [f"DO{i}" for i in range(3, 9)]
        do_entities = [{"entity": f"switch.ws_io8_do{i}", "name": do_labels[i - 1]} for i in range(1, 9)]
        di_labels = [
            "DI1 — Bed Left Reading Light",
            "DI2 — Bed Left Light",
            "DI3 — Bed Right Reading Light",
            "DI4 — Bed Right Light",
            "DI5 — Kitchen Light",
            "DI6 — Saloon Light",
            "DI7 — Outdoor Light",
            "DI8 — Future use",
        ]
        di_entities = [
            {"entity": f"binary_sensor.ws_io8_di{i}", "name": di_labels[i - 1]} for i in range(1, 9)
        ]
        io8_info = (
            "## Waveshare Modbus RTU IO 8CH\n"
            "| | |\n|---|---|\n"
            "| **DI** | 8 ch (FC02 discrete) |\n"
            "| **DO** | 8 ch open-drain (FC01/05 coil) |\n"
            "| **Baud** | 9600 8N1 |\n"
            "| **Slave** | 1 |\n"
            "| **Wiki** | [Modbus RTU IO 8CH](https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH) |\n"
            "| **Power** | 7–36 V DC (module needs its own supply) |"
        )

        di_do_view = {
            "title": "WS-DI/DO-01",
            "path": "ws-di-do-01",
            "icon": "mdi:gate-or",
            "cards": [
                {"type": "markdown", "content": io8_info},
                {
                    "type": "entities",
                    "title": "Digital outputs (DO)",
                    "show_header_toggle": False,
                    "entities": do_entities,
                },
                {
                    "type": "entities",
                    "title": "Digital inputs (DI)",
                    "show_header_toggle": False,
                    "entities": di_entities,
                },
            ],
        }

        ai_value_labels = [
            "Clean Water",
            "Gray water",
        ] + [f"AI CH{i}" for i in range(3, 9)]
        ai_entities = [
            {"entity": f"sensor.ws_ai_ch{i}", "name": ai_value_labels[i - 1]} for i in range(1, 9)
        ]
        ai_mode_raw = [
            {"entity": f"sensor.ai_ch{i}_mode_holding", "name": f"CH{i} mode (raw code)"} for i in range(1, 9)
        ]
        ai_mode_ui = [
            {"entity": f"input_select.ai_ch{i}_modbus_mode", "name": f"CH{i} mode (write)"} for i in range(1, 9)
        ]
        ai_mode_text = [
            # Entity IDs follow registry (unique_id); friendly names in YAML are English.
            {"entity": "sensor.clean_water_mod_metin", "name": "Clean Water — mode (text)"},
            {"entity": "sensor.gray_water_mod_metin", "name": "Gray water — mode (text)"},
        ]
        ai_info = (
            "## Waveshare Modbus RTU Analog Input 8CH\n"
            "| | |\n|---|---|\n"
            "| **Bus** | USB–RS485 → `rs485_bus` |\n"
            "| **Slave** | **3** (with IO8=1, Relay=2) |\n"
            "| **Read** | FC04 input registers 0–7, raw `uint16` |\n"
            "| **Mode** | Holding **4096–4103** (wiki 4x1000–); **3** = 4–20 mA |\n"
            "| **Wiki** | [Analog Input 8CH](https://www.waveshare.com/wiki/Modbus_RTU_Analog_Input_8CH) |\n"
            "| **Note** | Mode is writable; for **current** inputs, board **jumpers** must match the wiki. |"
        )
        ai_view = {
            "title": "WS-AI-01",
            "path": "ws-ai-01",
            "icon": "mdi:sine-wave",
            "cards": [
                {"type": "markdown", "content": ai_info},
                {
                    "type": "entities",
                    "title": "Analog inputs (raw)",
                    "show_header_toggle": False,
                    "entities": ai_entities,
                },
                {
                    "type": "entities",
                    "title": "CH1–2 — mode summary",
                    "show_header_toggle": False,
                    "entities": ai_mode_text,
                },
                {
                    "type": "entities",
                    "title": "Channel modes — from device (raw)",
                    "show_header_toggle": False,
                    "entities": ai_mode_raw,
                },
                {
                    "type": "entities",
                    "title": "Channel modes — from UI (Modbus write)",
                    "show_header_toggle": False,
                    "entities": ai_mode_ui,
                },
            ],
        }

        refresh_entity_ids = ["switch.ch1_maserator_pompa"]
        refresh_entity_ids += [f"switch.ch{i}" for i in range(2, 17)]
        for i in range(1, 9):
            refresh_entity_ids.append(f"switch.ws_io8_do{i}")
            refresh_entity_ids.append(f"binary_sensor.ws_io8_di{i}")
            refresh_entity_ids.append(f"switch.ws_rtu_relay_ch{i}")
        for i in range(1, 9):
            refresh_entity_ids.append(f"sensor.ws_ai_ch{i}")
            refresh_entity_ids.append(f"sensor.ai_ch{i}_mode_holding")
        for i in range(1, 9):
            refresh_entity_ids.append(f"input_select.ai_ch{i}_modbus_mode")
        refresh_entity_ids += ["sensor.clean_water_mod_metin", "sensor.gray_water_mod_metin"]

        rpi_cm5_info = (
            "## Raspberry Pi CM5 (Home Assistant host)\n"
            "Grouped **System Monitor** metrics below. MQTT RPi topics appear in the last card when the broker is online.\n\n"
            "| | |\n|---|---|\n"
            "| **Docs** | [System Monitor](https://www.home-assistant.io/integrations/systemmonitor/) |\n"
            "| **MQTT** | `sensor.campervan_rpi_cm5_*` from `setup_sensors.sh` |"
        )
        rpi_cm5_cards = [{"type": "markdown", "content": rpi_cm5_info}]
        for title, rows in RPI_CM5_GROUPS:
            rpi_cm5_cards.append(_entities_card(title, rows))

        rpi_cm5_view = {
            "title": "RPi CM5",
            "path": "rpi-cm5",
            "icon": "mdi:raspberry-pi",
            "cards": rpi_cm5_cards,
        }

        victron_info = (
            "## Victron Blue Smart Charger\n"
            "Gauges use **template sensors** (`sensor.victron_gauge_*`) so missing or non-numeric BLE "
            "values (e.g. power supply mode, unused phases) show as **0** instead of breaking the card.\n\n"
            "| | |\n|---|---|\n"
            "| **Product** | [Blue Smart IP65 (Bluetooth)](https://www.victronenergy.com/chargers/bluesmart-ip65-charger) |\n"
            "| **YAML** | Run `insert_victron_gauge_templates.py` on `configuration.yaml` if gauges are missing |"
        )
        victron_gauges_top = {
            "type": "horizontal-stack",
            "cards": [
                _gauge(VG["temp"], min_v=0, max_v=90, name="Charger temperature"),
                _gauge(VG["ac_a"], min_v=0, max_v=32, name="AC current"),
            ],
        }
        victron_gauges_phases = []
        for n in (1, 2, 3):
            victron_gauges_phases.append(
                {
                    "type": "horizontal-stack",
                    "cards": [
                        _gauge(
                            VG[f"l{n}_v"],
                            min_v=0,
                            max_v=280,
                            name=f"L{n} voltage",
                        ),
                        _gauge(
                            VG[f"l{n}_a"],
                            min_v=0,
                            max_v=32,
                            name=f"L{n} current",
                        ),
                    ],
                }
            )
        victron_view = {
            "title": "Victron Blue Smart",
            "path": "victron-bluesmart",
            "icon": "mdi:battery-charging",
            "cards": [
                {"type": "markdown", "content": victron_info},
                victron_gauges_top,
                *victron_gauges_phases,
                _entities_card(
                    "Status & extras",
                    [
                        f"{BSC}_charge_state",
                        f"{BSC}_charger_error",
                        f"{BSC}_signal_strength",
                    ],
                ),
            ],
        }

        status_info = (
            "## State sync\n"
            "After startup or RS485 delays, switches can lag. **Check states** calls "
            "`homeassistant.update_entity` on all bench Modbus entities to force one poll cycle.\n\n"
            "| Area | Example entity IDs |\n|---|---|\n"
            "| Ethernet 16CH | `switch.ch1_maserator_pompa`, `switch.ch2` … `ch16` |\n"
            "| IO 8CH | `switch.ws_io8_do*`, `binary_sensor.ws_io8_di*` |\n"
            "| RTU Relay (E) | `switch.ws_rtu_relay_ch1` … `ch8` |\n"
            "| Analog 8CH | `sensor.ws_ai_ch1` … `ch8`, `sensor.ai_ch*_mode_holding`, `input_select.ai_ch*_modbus_mode` |"
        )

        status_view = {
            "title": "Status",
            "path": "bench-status",
            "icon": "mdi:refresh-circle",
            "cards": [
                {"type": "markdown", "content": status_info},
                {
                    "type": "button",
                    "name": "Check states",
                    "icon": "mdi:sync",
                    "show_name": True,
                    "show_icon": True,
                    "tap_action": {
                        "action": "call-service",
                        "service": "homeassistant.update_entity",
                        "target": {"entity_id": refresh_entity_ids},
                    },
                },
            ],
        }

        config = {
            "views": [
                relay_view_01,
                relay_view_02,
                di_do_view,
                ai_view,
                rpi_cm5_view,
                victron_view,
                status_view,
            ]
        }

        await ws.send(
            json.dumps({"id": 20, "type": "lovelace/config/save", "url_path": "admin-bench", "config": config})
        )
        msg = json.loads(await ws.recv())
        if msg.get("success"):
            print(
                "  [OK] Tabs WS-Relay-01, WS-Relay-02, WS-DI/DO-01, WS-AI-01, "
                "RPi CM5, Victron Blue Smart, Status saved"
            )
        else:
            print(f"  [ERROR] {msg.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
