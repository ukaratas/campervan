#!/usr/bin/env python3
"""Append Victron gauge template sensors after the tank template block (legacy monolithic configuration.yaml).

Modüler kurulumda `homeassistant/templates/30_victron_gauges.yaml` zaten tamdır; argümansız çalıştırınca atlanır.
"""
import sys
from pathlib import Path

_scripts = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_scripts))
from repo_paths import repo_root  # noqa: E402

BSC = "sensor.bsc_ip65_12_15_hq2349fuajv"

# Jinja: 0 when BLE returns non-numeric / missing (e.g. power supply mode, unused phases).
def _tpl(src_entity):
    return (
        "          {% set e = '" + src_entity + "' %}\n"
        "          {{ iif(states(e) | is_number, states(e) | float(0), 0) }}"
    )


def _sensor(name, uid, unit, src, dev_class=None):
    lines = [
        f'      - name: "{name}"',
        f"        unique_id: {uid}",
        f'        unit_of_measurement: "{unit}"',
        "        state_class: measurement",
    ]
    if dev_class:
        lines.append(f'        device_class: {dev_class}')
    lines.append("        state: >-")
    lines.append(_tpl(src))
    return "\n".join(lines) + "\n"


def build_insert() -> str:
    parts = [
        _sensor("Victron gauge temp", "victron_gauge_temp", "°C", f"{BSC}_temperature", "temperature"),
        _sensor("Victron gauge AC current", "victron_gauge_ac_current", "A", f"{BSC}_ac_current", "current"),
    ]
    for n in (1, 2, 3):
        parts.append(
            _sensor(
                f"Victron gauge L{n} voltage",
                f"victron_gauge_l{n}_voltage",
                "V",
                f"{BSC}_output_phase_{n}_voltage",
                "voltage",
            )
        )
        parts.append(
            _sensor(
                f"Victron gauge L{n} current",
                f"victron_gauge_l{n}_current",
                "A",
                f"{BSC}_output_phase_{n}_current",
                "current",
            )
        )
    return "\n" + "".join(parts)


def main() -> None:
    root = repo_root()
    repo_v = root / "homeassistant" / "templates" / "30_victron_gauges.yaml"
    if len(sys.argv) == 1 and repo_v.is_file() and "victron_gauge_temp" in repo_v.read_text(encoding="utf-8"):
        print("Modular Victron templates already in homeassistant/templates/30_victron_gauges.yaml; skip.")
        return

    p = Path(sys.argv[1] if len(sys.argv) > 1 else "/config/configuration.yaml")
    text = p.read_text(encoding="utf-8")
    if "victron_gauge_temp" in text:
        print("Victron gauge template sensors already present; skip")
        return

    marker = "          {{ (p / 100 * 100) | round(1) }}"
    if marker not in text:
        print("ERROR: tank template marker not found (expected after Gray water tank volume line)")
        sys.exit(1)

    insert = build_insert()
    text = text.replace(marker + "\n", marker + "\n" + insert, 1)
    p.write_text(text, encoding="utf-8")
    print(f"OK: appended Victron gauge templates to {p}")


if __name__ == "__main__":
    main()
