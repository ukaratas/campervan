#!/usr/bin/env python3
"""Admin Bench Lovelace (WS-Relay-01/02, DI/DO, AI, Status) — HA WebSocket API.

Naming policy: English on this dashboard (see README — user dashboards use Turkish).
"""
import asyncio
import json
import os
import sys
from pathlib import Path

import websockets

WS_URI = os.environ["HA_URL"].replace("http://", "ws://") + "/api/websocket"
WS_TOKEN = os.environ["HA_TOKEN"]

# Ethernet 16CH — entity_id = slugified `name` from modbus/10_waveshare_ws01.yaml (not switch.ch2).
ETH_WS01_SWITCHES = [
    "switch.ch1_macerator_pump",
    "switch.ch2_refrigerator",
    "switch.ch3_bed_left_reading_light",
    "switch.ch4_bed_right_reading_light",
    "switch.ch5_bed_light",
    "switch.ch6_kitchen_light",
    "switch.ch7_saloon_light",
    "switch.ch8_outdoor_light",
    "switch.ch9_victron_blue_smart",
    "switch.ch10_dishwasher",
    "switch.ch11_washing_machine",
    "switch.ch12_truma_combi_d4",
    "switch.ch13_future_use",
    "switch.ch14_future_use",
    "switch.ch15_future_use",
    "switch.ch16_future_use",
]

# RS485 RTU Relay (E) slave 2 — slugified names from rs485_bus_devices/switches/20_relay_e.yaml
RTU_RELAY_E_SWITCHES = [
    "switch.ch1_220v_outlets",
    "switch.ch2_clesana_c1",
    "switch.ch3_usb_outlets",
    "switch.ch4_air_condition",
    "switch.ch5_future_use",
    "switch.ch6_future_use",
    "switch.ch7_future_use",
    "switch.ch8_future_use",
]

# IO8 DO — DO1/2 use "DO1 — …" names; DO3–8 use "WS-IO8 DOx" in YAML (see 10_io8_do.yaml)
IO8_DO_SWITCHES = [
    "switch.do1_warning_light",
    "switch.do2_error_buzzer",
    "switch.ws_io8_do3",
    "switch.ws_io8_do4",
    "switch.ws_io8_do5",
    "switch.ws_io8_do6",
    "switch.ws_io8_do7",
    "switch.ws_io8_do8",
]

# IO8 DI — slugified from rs485_bus_devices/binary_sensors/10_io8_di.yaml
IO8_DI_BINARY_SENSORS = [
    "binary_sensor.di1_bed_left_reading_light",
    "binary_sensor.di2_bed_left_light",
    "binary_sensor.di3_bed_right_reading_light",
    "binary_sensor.di4_bed_right_light",
    "binary_sensor.di5_kitchen_light",
    "binary_sensor.di6_saloon_light",
    "binary_sensor.di7_outdoor_light",
    "binary_sensor.di8_future_use",
]

# Victron Blue Smart Charger (BLE). If HA re-discovers the device, update these entity IDs.
# All Victron BLE sensors share this prefix (update if HA re-discovers the charger).
BSC = "sensor.bsc_ip65_12_15_hq2349fuajv"
# Template sensors from homeassistant/templates/30_victron_gauges.yaml — slug = unique_id (no _2 suffix).
# Cihaz yeniden eşlenirse BSC + templates içindeki BLE entity ID'lerini güncelleyin.
VG = {
    "temp": "sensor.victron_gauge_temp",
    "ac_a": "sensor.victron_gauge_ac_current",
    "l1_v": "sensor.victron_gauge_l1_voltage",
    "l1_a": "sensor.victron_gauge_l1_current",
    "l2_v": "sensor.victron_gauge_l2_voltage",
    "l2_a": "sensor.victron_gauge_l2_current",
    "l3_v": "sensor.victron_gauge_l3_voltage",
    "l3_a": "sensor.victron_gauge_l3_current",
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
            # Teltonika LAN is usually end0; wlan0 stays unknown if Wi‑Fi unused
            "sensor.system_monitor_ipv4_address_end0",
            "sensor.system_monitor_ipv4_address_wlan0",
            "sensor.system_monitor_ipv4_address_hassio",
            "sensor.system_monitor_ipv4_address_docker0",
        ],
    ),
    (
        "Network — throughput (B/s)",
        [
            "sensor.system_monitor_network_throughput_in_end0",
            "sensor.system_monitor_network_throughput_out_end0",
            "sensor.system_monitor_network_throughput_in_wlan0",
            "sensor.system_monitor_network_throughput_out_wlan0",
        ],
    ),
    # PSI / kernel pressure: often "unknown" on HA OS — omitted to avoid empty cards
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
        "Power (RPi)",
        [
            "binary_sensor.rpi_power_status",
        ],
    ),
]


def build_refresh_entity_ids() -> list[str]:
    """Tek kaynak: Status sekmesi + scripts.yaml (sıralı update_entity)."""
    out: list[str] = []
    out.extend(ETH_WS01_SWITCHES)
    out.extend(IO8_DO_SWITCHES)
    out.extend(IO8_DI_BINARY_SENSORS)
    out.extend(RTU_RELAY_E_SWITCHES)
    for i in range(1, 9):
        out.append(f"sensor.ws_ai_ch{i}")
        out.append(f"sensor.ai_ch{i}_mode_holding")
    for i in range(1, 9):
        out.append(f"input_select.ai_ch{i}_modbus_mode")
    out.extend(["sensor.clean_water_mode_text", "sensor.gray_water_mode_text"])
    return out


def write_admin_bench_sync_script() -> None:
    """homeassistant/scripts.yaml — tek tek update + RS485 için kısa gecikme."""
    root = Path(__file__).resolve().parent.parent.parent
    out = root / "homeassistant" / "scripts.yaml"
    ids = build_refresh_entity_ids()
    lines = [
        "# Admin Bench: Modbus/RS485 entity yenileme (Check states).",
        "# Bu dosya lovelace_push_admin_bench.py tarafından güncellenir.",
        "admin_bench_sync_modbus:",
        '  alias: "Admin Bench — sync Modbus entity states"',
        "  icon: mdi:sync",
        "  mode: restart",
        "  sequence:",
        "    - repeat:",
        "        for_each:",
    ]
    for eid in ids:
        lines.append(f"          - {eid}")
    lines.extend(
        [
            "        sequence:",
            "          - service: homeassistant.update_entity",
            "            target:",
            '              entity_id: "{{ repeat.item }}"',
            "          - delay:",
            "              milliseconds: 45",
        ]
    )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


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

        write_admin_bench_sync_script()
        print("  [OK] Regenerated homeassistant/scripts.yaml (admin_bench_sync_modbus)")

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
            "CH12 — Truma Combi D4",
            "CH13 — Future use",
            "CH14 — Future use",
            "CH15 — Future use",
            "CH16 — Future use",
        ]
        ws01_entities = [{"entity": ETH_WS01_SWITCHES[i], "name": eth_labels[i]} for i in range(16)]

        relay_info = (
            "## Waveshare Modbus PoE Ethernet Relay 16CH\n"
            "| | |\n|---|---|\n"
            "| **Module** | WS-01 |\n"
            f"| **IP** | {os.environ.get('RELAY_IP', '192.168.50.20')}:{os.environ.get('RELAY_PORT', '4196')} |\n"
            "| **Protocol** | Modbus RTU over TCP (native HA) |\n"
            "| **Slave** | 1 |\n"
            "| **Channels** | 16 (CH1–11 + CH12 Truma; CH13–16 reserved) |"
        )

        relay_view_01 = {
            "title": "WS-Relay-01",
            "path": "ws-relay-01",
            "icon": "mdi:electric-switch",
            "cards": [
                {"type": "markdown", "content": relay_info},
                {
                    "type": "entities",
                    "title": "Relay control — CH1–CH8",
                    "show_header_toggle": False,
                    "entities": ws01_entities[:8],
                },
                {
                    "type": "entities",
                    "title": "Relay control — CH9–CH16",
                    "show_header_toggle": False,
                    "entities": ws01_entities[8:],
                },
            ],
        }

        rtu_labels = [
            "CH1 — 220V Outlets",
            "CH2 — Clesana C1",
            "CH3 — USB Outlets",
            "CH4 — Air Condition",
            "CH5 — Future use",
            "CH6 — Future use",
            "CH7 — Future use",
            "CH8 — Future use",
        ]
        rtu_info = (
            "## Waveshare Modbus RTU Relay (E) — RS485\n"
            "| | |\n|---|---|\n"
            "| **Contact** | **32 A** (8-channel module) |\n"
            "| **Bus** | USB–RS485 → `rs485_bus` (single serial port) |\n"
            "| **Slave** | **2** (same line as IO8=1, Analog=3) |\n"
            "| **Wiki** | [Relay (E)](https://www.waveshare.com/wiki/Modbus_RTU_Relay_(E)) |\n"
            "| **Coils** | CH1 220V outlets, CH2 Clesana C1, CH3 USB outlets, CH4 AC; CH5–8 reserved |\n"
            "\n"
            "`configuration.yaml`: **`slave: 2`** under `rs485_bus`."
        )

        rtu_entities = [{"entity": RTU_RELAY_E_SWITCHES[i], "name": rtu_labels[i]} for i in range(8)]

        relay_view_02 = {
            "title": "WS-Relay-02",
            "path": "ws-relay-02",
            "icon": "mdi:serial-port",
            "cards": [
                {"type": "markdown", "content": rtu_info},
                {
                    "type": "entities",
                    "title": "RTU Relay (E) — CH1–CH4",
                    "show_header_toggle": False,
                    "entities": rtu_entities[:4],
                },
                {
                    "type": "entities",
                    "title": "RTU Relay (E) — CH5–CH8",
                    "show_header_toggle": False,
                    "entities": rtu_entities[4:],
                },
            ],
        }

        do_labels = [
            "DO1 — Warning Light",
            "DO2 — Error Buzzer",
        ] + [f"DO{i}" for i in range(3, 9)]
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

        do_entities = [{"entity": IO8_DO_SWITCHES[i], "name": do_labels[i]} for i in range(8)]
        di_entities = [{"entity": IO8_DI_BINARY_SENSORS[i], "name": di_labels[i]} for i in range(8)]

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
        ai_entities = [{"entity": f"sensor.ws_ai_ch{i}", "name": ai_value_labels[i - 1]} for i in range(1, 9)]
        ai_mode_raw = [
            {"entity": f"sensor.ai_ch{i}_mode_holding", "name": f"CH{i} mode (raw code)"} for i in range(1, 9)
        ]
        ai_mode_ui = [
            {"entity": f"input_select.ai_ch{i}_modbus_mode", "name": f"CH{i} mode (write)"} for i in range(1, 9)
        ]
        ai_mode_text = [
            # Slug from template `name:` in templates/10_ai_modes_text.yaml
            {"entity": "sensor.clean_water_mode_text", "name": "Clean Water — mode (text)"},
            {"entity": "sensor.gray_water_mode_text", "name": "Gray water — mode (text)"},
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

        rpi_cm5_info = (
            "## Raspberry Pi CM5 (Home Assistant host)\n"
            "Grouped **System Monitor** metrics below.\n\n"
            "| | |\n|---|---|\n"
            "| **Docs** | [System Monitor](https://www.home-assistant.io/integrations/systemmonitor/) |\n"
            "| **LAN** | Primary IPv4 is often **`end0`** (Ethernet); **`wlan0`** is unknown if Wi‑Fi is off. |\n"
            "| **MQTT RPi** | Run `scripts/setup/setup_sensors.sh` after Mosquitto; discovery entity IDs "
            "are typically `sensor.rpi_cpu_sicaklik` / `sensor.rpi_uptime` — confirm under **Developer Tools → States**. |"
        )
        rpi_cm5_cards = [{"type": "markdown", "content": rpi_cm5_info}]
        for title, rows in RPI_CM5_GROUPS:
            rpi_cm5_cards.append(_entities_card(title, rows))
        rpi_cm5_cards.append(
            {
                "type": "markdown",
                "content": (
                    "### MQTT — CamperVan RPi (optional)\n"
                    "No MQTT rows here until discovery runs. From the repo machine (with `mosquitto_pub`): "
                    "`bash scripts/setup/setup_sensors.sh` — then search states for **`rpi`** / **`campervan`**.\n\n"
                    "Host CPU/temp are already covered by **System Monitor** above."
                ),
            }
        )

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
            "| **YAML** | `homeassistant/templates/30_victron_gauges.yaml` → `sync_ha_config.sh` |"
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
            "After startup or RS485 delays, switches can lag. **Check states** runs the script "
            "`script.admin_bench_sync_modbus`: each entity gets `homeassistant.update_entity` **one at a time** "
            "with a short delay (RS485 bus spacing). Same entity list as `build_refresh_entity_ids()` in "
            "`lovelace_push_admin_bench.py`.\n\n"
            "| Area | Example entity IDs |\n|---|---|\n"
            "| Ethernet 16CH | `switch.ch1_macerator_pump`, … (`ETH_WS01_SWITCHES`) |\n"
            "| IO 8CH DO | `switch.do1_warning_light`, `do2_error_buzzer`, `ws_io8_do3`… (`IO8_DO_SWITCHES`) |\n"
            "| IO 8CH DI | `binary_sensor.di1_bed_left_reading_light`, … (`IO8_DI_BINARY_SENSORS`) |\n"
            "| RTU Relay (E) | `switch.ch1_220v_outlets`, … (`RTU_RELAY_E_SWITCHES`) |\n"
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
                    "entity": "script.admin_bench_sync_modbus",
                    "name": "Check states",
                    "icon": "mdi:sync",
                    "show_name": True,
                    "show_icon": True,
                    "show_state": False,
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
