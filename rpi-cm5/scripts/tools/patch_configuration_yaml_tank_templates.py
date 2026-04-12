#!/usr/bin/env python3
"""Insert tank template sensors after Gray water mode template."""
import sys
from pathlib import Path

_scripts = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_scripts))
from repo_paths import repo_root  # noqa: E402

repo_tank = repo_root() / "homeassistant" / "templates" / "20_tank_levels.yaml"
if len(sys.argv) == 1 and repo_tank.is_file() and "tank_temiz_su_seviye_pct" in repo_tank.read_text():
    print("Modular tank templates already in homeassistant/templates/20_tank_levels.yaml; skip")
    raise SystemExit(0)

p = Path(sys.argv[1] if len(sys.argv) > 1 else "/config/configuration.yaml")
text = p.read_text()
if "tank_temiz_su_seviye_pct" in text:
    print("Tank template sensors already present; skip")
    raise SystemExit(0)

marker = (
    "unique_id: gray_water_mod_metin\n"
    "        state: >-\n"
    "          {% set m = states('sensor.ai_ch2_mode_holding') | int(-1) %}\n"
    "          {% if m == 0 %}0–5 V{% elif m == 1 %}1–5 V{% elif m == 2 %}0–20 mA{% elif m == 3 %}4–20 mA{% elif m == 4 %}Raw code{% else %}—{% endif %}"
)
if marker not in text:
    print("ERROR: marker not found")
    raise SystemExit(1)

insert = """

      - name: "Tank Temiz Su seviye"
        unique_id: tank_temiz_su_seviye_pct
        unit_of_measurement: "%"
        state_class: measurement
        icon: mdi:water
        state: >-
          {% set raw = states('sensor.ws_ai_ch1') | float(0) %}
          {{ ([0, (raw / 65535 * 100), 100] | sort)[1] | round(1) }}
      - name: "Tank Kirli Su seviye"
        unique_id: tank_kirli_su_seviye_pct
        unit_of_measurement: "%"
        state_class: measurement
        icon: mdi:water-off
        state: >-
          {% set raw = states('sensor.ws_ai_ch2') | float(0) %}
          {{ ([0, (raw / 65535 * 100), 100] | sort)[1] | round(1) }}
      - name: "Tank Temiz Su hacim"
        unique_id: tank_temiz_su_hacim_l
        unit_of_measurement: "L"
        state_class: measurement
        icon: mdi:water
        state: >-
          {% set raw = states('sensor.ws_ai_ch1') | float(0) %}
          {% set p = ([0, (raw / 65535 * 100), 100] | sort)[1] %}
          {{ (p / 100 * 180) | round(1) }}
      - name: "Tank Kirli Su hacim"
        unique_id: tank_kirli_su_hacim_l
        unit_of_measurement: "L"
        state_class: measurement
        icon: mdi:water-off
        state: >-
          {% set raw = states('sensor.ws_ai_ch2') | float(0) %}
          {% set p = ([0, (raw / 65535 * 100), 100] | sort)[1] %}
          {{ (p / 100 * 100) | round(1) }}"""

text = text.replace(marker + "\n", marker + insert + "\n", 1)
p.write_text(text)
print("Inserted tank template sensors OK")
