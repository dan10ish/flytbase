import json
import math
# Remove datetime imports as we simplify time handling
from typing import List, Dict, Any, Tuple

# Assuming models.py is in the same directory or accessible via PYTHONPATH
from .models import Waypoint, DroneMission

def _parse_hhmm_to_minutes(hhmm: int) -> int:
    """Converts time in HHMM integer format to minutes since midnight (0-1439)."""
    if not isinstance(hhmm, int) or not (0 <= hhmm <= 2359):
        raise ValueError(f"Invalid HHMM time format: {hhmm}. Must be an integer between 0 and 2359.")
    
    hour = hhmm // 100
    minute = hhmm % 100
    
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
         raise ValueError(f"Invalid HHMM time value: {hhmm}. Hour must be 0-23, Minute must be 0-59.")
         
    return hour * 60 + minute


def _calculate_distance(p1: Dict[str, float], p2: Dict[str, float]) -> float:
    """Calculates Euclidean distance between two points {x, y, z}."""
    # Ensure coordinates are floats before calculation
    try:
        x1, y1, z1 = float(p1['x']), float(p1['y']), float(p1.get('z', 0.0)) # Default z to 0.0 if not present
        x2, y2, z2 = float(p2['x']), float(p2['y']), float(p2.get('z', 0.0)) # Default z to 0.0 if not present
    except (KeyError, TypeError, ValueError) as e:
        raise ValueError(f"Invalid coordinate format for distance calculation. Points: {p1}, {p2}. Error: {e}") from e
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def load_missions_from_json(filepath: str) -> Tuple[DroneMission, List[DroneMission]]:
    """
    Loads primary and simulated drone missions from a JSON file.
    Expects time values (start_time, end_time, timestamp) in HHMM integer format.

    Calculates timestamps (as minutes since midnight) for the primary drone 
    based on constant speed between start_time and end_time.
    Parses timestamps directly for simulated drones.

    Args:
        filepath: Path to the JSON file.

    Returns:
        A tuple containing:
            - The primary DroneMission object.
            - A list of simulated DroneMission objects.

    Raises:
        FileNotFoundError: If the filepath does not exist.
        ValueError: If JSON is invalid, data format is incorrect,
                    or times cannot be parsed.
        KeyError: If expected keys are missing in the JSON structure.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Input file not found at {filepath}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: Invalid JSON format in {filepath}. Details: {e}") from e

    simulated_missions: List[DroneMission] = []
    primary_mission: DroneMission | None = None

    # --- Parse Simulated Missions ---
    if "simulated_missions" not in data:
        raise KeyError("Missing 'simulated_missions' key in JSON data.")

    for sim_data in data["simulated_missions"]:
        if not all(k in sim_data for k in ["drone_id", "waypoints"]):
            raise KeyError("Simulated mission data missing 'drone_id' or 'waypoints'.")

        sim_waypoints: List[Waypoint] = []
        for wp_data in sim_data["waypoints"]:
            # Expect x, y, z, and timestamp for simulated waypoints
            if not all(k in wp_data for k in ["x", "y", "z", "timestamp"]):
                # For backward compatibility, we can make z optional and default to 0, or raise error.
                # For Phase 5, let's assume Z is expected.
                raise KeyError(f"Simulated waypoint for drone {sim_data['drone_id']} missing 'x', 'y', 'z', or 'timestamp' (expected HHMM int).")
            try:
                # Parse HHMM timestamp to minutes since midnight
                timestamp_minutes = _parse_hhmm_to_minutes(int(wp_data["timestamp"]))
                waypoint = Waypoint(x=float(wp_data["x"]), y=float(wp_data["y"]), z=float(wp_data["z"]), timestamp_minutes=timestamp_minutes)
                sim_waypoints.append(waypoint)
            except (ValueError, TypeError, KeyError) as e:
                 raise ValueError(f"Invalid data in waypoint for simulated drone {sim_data['drone_id']}. Check format (x,y,z, HHMM time). Details: {e}") from e

        # Sort waypoints by timestamp for consistency
        sim_waypoints.sort(key=lambda wp: wp.timestamp_minutes)
        simulated_missions.append(DroneMission(drone_id=sim_data["drone_id"], waypoints=sim_waypoints))

    # --- Parse Primary Mission ---
    if "primary_mission" not in data:
        raise KeyError("Missing 'primary_mission' key in JSON data.")

    primary_data = data["primary_mission"]
    if not all(k in primary_data for k in ["drone_id", "waypoints", "start_time", "end_time"]):
        raise KeyError("Primary mission data missing 'drone_id', 'waypoints', 'start_time' (HHMM int), or 'end_time' (HHMM int).")
    if not primary_data["waypoints"]:
         raise ValueError("Primary mission must have at least one waypoint.")

    primary_drone_id = primary_data["drone_id"]
    # Ensure waypoints only contain x, y, z as expected for primary mission input
    raw_waypoints = [] 
    for i, wp in enumerate(primary_data["waypoints"]):
        # For Phase 5, let's assume Z is expected.
        if not isinstance(wp, dict) or 'x' not in wp or 'y' not in wp or 'z' not in wp:
            raise ValueError(f"Primary mission waypoint {i} for drone {primary_drone_id} must be a dict with 'x', 'y', and 'z'.")
        if 'timestamp' in wp:
            raise ValueError(f"Primary mission waypoint {i} for drone {primary_drone_id} should only contain 'x', 'y', 'z', not 'timestamp'.")
        try:
            # Validate coordinate types early
            raw_waypoints.append({"x": float(wp['x']), "y": float(wp['y']), "z": float(wp['z'])})
        except (TypeError, ValueError) as e:
             raise ValueError(f"Invalid coordinate type in primary mission waypoint {i} for drone {primary_drone_id}. Details: {e}") from e
    

    try:
        start_time_minutes = _parse_hhmm_to_minutes(int(primary_data["start_time"]))
        end_time_minutes = _parse_hhmm_to_minutes(int(primary_data["end_time"]))
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid start/end time (expected HHMM int) for primary drone {primary_drone_id}. Details: {e}") from e

    # We assume the time window is within a single 24-hour cycle for simplicity.
    # Handling overnight missions would require additional logic (e.g., adding 1440 minutes to end_time if end_time < start_time).
    if start_time_minutes >= end_time_minutes:
        raise ValueError(f"Primary mission start_time ({primary_data['start_time']}) must be before end_time ({primary_data['end_time']}) for drone {primary_drone_id}.")

    # --- Calculate Primary Drone Timestamps (Minutes Since Midnight) ---
    calculated_waypoints: List[Waypoint] = []
    total_duration_minutes = end_time_minutes - start_time_minutes
    if total_duration_minutes <= 0: # Should be caught by check above, but good safety net
         raise ValueError(f"Primary mission duration must be positive for drone {primary_drone_id}.")

    if len(raw_waypoints) == 1:
        # If only one waypoint, it occurs at the start time
        wp_data = raw_waypoints[0]
        calculated_waypoints.append(Waypoint(x=wp_data['x'], y=wp_data['y'], z=wp_data['z'], timestamp_minutes=start_time_minutes))
    else:
        # Calculate total distance
        total_distance = 0
        for i in range(len(raw_waypoints) - 1):
            # Distance calculation now uses validated float coordinates
            dist = _calculate_distance(raw_waypoints[i], raw_waypoints[i+1]) 
            total_distance += dist

        if total_distance == 0:
            # All waypoints are the same. Assign start time to all.
            current_time_minutes = start_time_minutes
            for wp_data in raw_waypoints:
                 calculated_waypoints.append(Waypoint(x=wp_data['x'], y=wp_data['y'], z=wp_data['z'], timestamp_minutes=current_time_minutes))
        else:
            # Calculate constant speed in distance units per minute
            speed = total_distance / total_duration_minutes 

            current_time_minutes = start_time_minutes
            # First waypoint is at start_time_minutes
            calculated_waypoints.append(Waypoint(x=raw_waypoints[0]['x'], y=raw_waypoints[0]['y'], z=raw_waypoints[0]['z'], timestamp_minutes=current_time_minutes))

            # Calculate time for subsequent waypoints
            for i in range(len(raw_waypoints) - 1):
                segment_distance = _calculate_distance(raw_waypoints[i], raw_waypoints[i+1])
                if speed > 1e-9: # Use tolerance for float comparison
                     time_for_segment_minutes = segment_distance / speed
                else: 
                     # Should not happen if distance > 0 and duration > 0
                     # Fallback: Distribute remaining time equally across remaining segments
                     remaining_segments = len(raw_waypoints) - 1 - i
                     remaining_time = end_time_minutes - current_time_minutes
                     if remaining_segments > 0 and remaining_time > 0:
                         time_for_segment_minutes = remaining_time / remaining_segments
                     else:
                         time_for_segment_minutes = 0

                # Use round() to minimize floating point accumulation issues, converting to int only at the end?
                # Or just add float minutes. Let's add float minutes for now, final timestamp will be int.
                current_time_minutes += time_for_segment_minutes
                
                # Ensure we don't exceed end_time_minutes due to float inaccuracies. Clamp and round.
                final_timestamp_minutes = min(round(current_time_minutes), end_time_minutes) 
                
                calculated_waypoints.append(Waypoint(x=raw_waypoints[i+1]['x'], y=raw_waypoints[i+1]['y'], z=raw_waypoints[i+1]['z'], timestamp_minutes=final_timestamp_minutes))

            # Final check/adjustment: ensure last waypoint has exactly end_time_minutes if calculated time is very close
            if calculated_waypoints and abs(calculated_waypoints[-1].timestamp_minutes - end_time_minutes) <= 1: # Tolerance of 1 min
                 if calculated_waypoints[-1].timestamp_minutes != end_time_minutes:
                      calculated_waypoints[-1].timestamp_minutes = end_time_minutes
                 

    primary_mission = DroneMission(drone_id=primary_drone_id, waypoints=calculated_waypoints)

    return primary_mission, simulated_missions

# Example usage (requires a 'missions.json' file with HHMM times):
# if __name__ == '__main__':
#     try:
#         # Example: Create a dummy missions.json
#         dummy_data = {
#             "primary_mission": {
#                 "drone_id": "primary_01",
#                 "waypoints": [{"x": 0, "y": 0}, {"x": 100, "y": 0}],
#                 "start_time": 800,  # 08:00
#                 "end_time": 810   # 08:10
#             },
#             "simulated_missions": [
#                 {
#                     "drone_id": "sim_A",
#                     "waypoints": [
#                         {"x": 50, "y": -10, "timestamp": 805}, # 08:05
#                         {"x": 50, "y": 10, "timestamp": 808}  # 08:08
#                     ]
#                 }
#             ]
#         }
#         with open('missions.json', 'w') as f:
#             json.dump(dummy_data, f, indent=2)

#         primary, simulated = load_missions_from_json('missions.json')
#         print("Primary Mission Loaded:")
#         print(primary)
#         print("\nSimulated Missions Loaded:")
#         for sim in simulated:
#             print(sim)

#     except (FileNotFoundError, ValueError, KeyError) as e:
#         print(f"Error loading missions: {e}") 