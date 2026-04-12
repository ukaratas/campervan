#!/usr/bin/env python3
"""Normalize Admin/settings-related strings in configuration.yaml to English (see README)."""
import sys
from pathlib import Path


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "/config/configuration.yaml")
    text = path.read_text(encoding="utf-8")

    subs = [
        ('name: "Gray water level sensor"', 'name: "Gray water"'),
        ('name: "CH1 — Maceratör pompa"', 'name: "CH1 — Macerator pump"'),
        ('name: "CH1 — Macerator"', 'name: "CH1 — Macerator pump"'),
        ('name: "CH1 — ölçüm modu (Modbus yaz)"', 'name: "CH1 — measurement mode (Modbus write)"'),
        ('name: "CH2 — ölçüm modu (Modbus yaz)"', 'name: "CH2 — measurement mode (Modbus write)"'),
        ('name: "CH3 — ölçüm modu (Modbus yaz)"', 'name: "CH3 — measurement mode (Modbus write)"'),
        ('name: "CH4 — ölçüm modu (Modbus yaz)"', 'name: "CH4 — measurement mode (Modbus write)"'),
        ('name: "CH5 — ölçüm modu (Modbus yaz)"', 'name: "CH5 — measurement mode (Modbus write)"'),
        ('name: "CH6 — ölçüm modu (Modbus yaz)"', 'name: "CH6 — measurement mode (Modbus write)"'),
        ('name: "CH7 — ölçüm modu (Modbus yaz)"', 'name: "CH7 — measurement mode (Modbus write)"'),
        ('name: "CH8 — ölçüm modu (Modbus yaz)"', 'name: "CH8 — measurement mode (Modbus write)"'),
        ('- "4 · Ham kod (4096 ölçek)"', '- "4 · Raw code (4096 scale)"'),
        ('name: "Clean Water — mod (metin)"', 'name: "Clean Water — mode (text)"'),
        ('name: "Gray water — mod (metin)"', 'name: "Gray water — mode (text)"'),
    ]
    for old, new in subs:
        text = text.replace(old, new)

    text = text.replace("{% elif m == 4 %}Ham kod{% else %}", "{% elif m == 4 %}Raw code{% else %}")

    path.write_text(text, encoding="utf-8")
    print(f"OK: updated {path}")


if __name__ == "__main__":
    main()
