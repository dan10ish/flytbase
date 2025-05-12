from dataclasses import dataclass, field
from datetime import datetime # Keep for potential future use, but not for timestamp
from typing import List, Tuple


@dataclass
class Waypoint:
    """Represents a single point in space and time (minutes since midnight) for a drone."""
    x: float
    y: float
    timestamp_minutes: int # Time represented as minutes since midnight (0-1439)


@dataclass
class DroneMission:
    """Represents the complete mission plan for a single drone."""
    drone_id: str
    waypoints: List[Waypoint] = field(default_factory=list)


# We might add more specific mission types later, e.g., Primary vs Simulated,
# or add methods for calculations. 