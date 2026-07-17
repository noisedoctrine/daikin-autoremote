"""Load local-only project configuration without embedding private values."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_FILE = ROOT_DIR / "secrets" / "local.yaml"


def resolve_config_path(path: Optional[Union[str, Path]] = None) -> Path:
    configured = Path(path or os.getenv("DAIKIN_CONFIG", DEFAULT_CONFIG_FILE)).expanduser()
    if not configured.is_absolute():
        configured = ROOT_DIR / configured
    return configured


def load_local_config(path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Return the parsed local YAML configuration, or an empty mapping if absent."""
    config_path = resolve_config_path(path)
    if not config_path.exists():
        return {}

    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Configuration root must be a mapping: {config_path}")
    return data
