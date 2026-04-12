"""Resolve rpi-cm5 repo root (directory containing homeassistant/configuration.yaml)."""
from pathlib import Path


def repo_root() -> Path:
    p = Path(__file__).resolve().parent
    for _ in range(10):
        if (p / "homeassistant" / "configuration.yaml").is_file():
            return p
        if p.parent == p:
            break
        p = p.parent
    raise FileNotFoundError("homeassistant/configuration.yaml not found above scripts/")
