# Main script for the Drone Deconfliction System

import argparse
from typing import List, Tuple

# Import core functions from other modules
from utils import load_missions_from_json
from conflict_checks import find_conflicts

def check_mission_conflicts(mission_file_path: str, safety_buffer: float) -> Tuple[str, List[str]]:
    """Loads mission data, checks for conflicts, and returns status and details.

    Args:
        mission_file_path: Path to the JSON file containing mission data.
        safety_buffer: The minimum safety distance for conflict checks.

    Returns:
        A tuple containing:
          - str: Status ("Clear" or "Conflict Detected").
          - List[str]: List of conflict descriptions (empty if clear).
    """
    try:
        primary_mission, simulated_missions = load_missions_from_json(mission_file_path)
    except (FileNotFoundError, ValueError, KeyError) as e:
        # Handle errors during loading (e.g., file not found, bad format)
        return "Error Loading Mission", [f"Failed to load or parse mission file: {e}"]

    try:
        conflict_found, conflict_details = find_conflicts(
            primary_mission,
            simulated_missions,
            safety_buffer
        )
    except Exception as e:
        # Catch potential errors during conflict checking (e.g., Shapely errors not caught deeper)
        # Log this properly in a real application
        print(f"Error during conflict check: {e}")
        return "Error During Check", [f"An unexpected error occurred during conflict analysis: {e}"]

    if conflict_found:
        status = "Conflict Detected"
    else:
        status = "Clear"
        conflict_details = [] # Ensure details are empty if clear
        
    return status, conflict_details


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check drone mission for spatio-temporal conflicts.")
    parser.add_argument("mission_file", help="Path to the mission JSON file.")
    parser.add_argument("-b", "--buffer", type=float, default=5.0, 
                        help="Safety buffer distance (default: 5.0 units).")
    
    args = parser.parse_args()

    print(f"Checking mission file: {args.mission_file}")
    print(f"Using safety buffer: {args.buffer}")
    print("---")

    status, details = check_mission_conflicts(args.mission_file, args.buffer)

    print(f"Mission Status: {status}")
    if details:
        print("Conflict Details:")
        for detail in details:
            print(f"- {detail}")
    print("---") 