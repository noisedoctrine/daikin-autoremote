import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from src.config import ROOT_DIR, load_local_config

DATA_DIR = ROOT_DIR / "data"
CONFIG_FILE = Path(os.getenv("DAIKIN_UNITS_FILE", DATA_DIR / "units.json"))
if not CONFIG_FILE.is_absolute():
    CONFIG_FILE = ROOT_DIR / CONFIG_FILE


class ACInventory:
    def __init__(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.units = self.load_units()

    def load_units(self) -> List[Dict]:
        if CONFIG_FILE.exists():
            try:
                with CONFIG_FILE.open("r", encoding="utf-8") as handle:
                    units = json.load(handle)
                return units if isinstance(units, list) else []
            except (OSError, json.JSONDecodeError):
                return []

        units = load_local_config().get("units", [])
        return units if isinstance(units, list) else []

    def save_units(self) -> None:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with CONFIG_FILE.open("w", encoding="utf-8") as handle:
            json.dump(self.units, handle, indent=4)

    def add_unit(self, name: str, gpio_pin: int, location: str = "") -> None:
        next_id = max((int(unit.get("id", 0)) for unit in self.units), default=0) + 1
        self.units.append(
            {
                "id": next_id,
                "name": name,
                "gpio": gpio_pin,
                "location": location,
                "last_state": None,
            }
        )
        self.save_units()

    def get_unit(self, unit_id: int) -> Optional[Dict]:
        for unit in self.units:
            if unit.get("id") == unit_id:
                return unit
        return None


if __name__ == "__main__":
    inventory = ACInventory()
    if inventory.units:
        print(f"Loaded {len(inventory.units)} unit(s) from local configuration.")
    else:
        print("No units configured. Copy secrets/local.example.yaml to secrets/local.yaml.")
