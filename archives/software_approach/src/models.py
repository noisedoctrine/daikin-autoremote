from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ACState:
    power: bool
    temp: float
    fan_speed: str # Auto, Quiet, 1, 2, 3, 4, 5
    mode: str # Cool, Heat, Dry, Fan

@dataclass
class ProfileStep:
    offset_minutes: int
    state: ACState

@dataclass
class ComfortProfile:
    id: str
    name: str
    steps: List[ProfileStep]
