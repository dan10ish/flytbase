from dataclasses import dataclass, field
from datetime import datetime # Keep for potential future use, but not for timestamp
from typing import List, Tuple


@dataclass # to auto generate dunder methods
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

    def get_path_segments(self) -> List[Tuple[Waypoint, Waypoint]]:
        """Generates a list of path segments from the mission's waypoints.

        Each segment is represented as a tuple of two consecutive Waypoint objects.
        Returns an empty list if there are fewer than two waypoints.
        """
        segments: List[Tuple[Waypoint, Waypoint]] = []
        if len(self.waypoints) >= 2:
            for i in range(len(self.waypoints) - 1):
                segment = (self.waypoints[i], self.waypoints[i+1])
                segments.append(segment)
        return segments


# We might add more specific mission types later, e.g., Primary vs Simulated,
# or add methods for calculations. 