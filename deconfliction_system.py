# Main script for the Drone Deconfliction System

import argparse
from typing import List, Tuple, Optional

# Import core functions from other modules
from utils import load_missions_from_json
from conflict_checks import find_conflicts
from visualization import plot_missions
from models import DroneMission

def check_mission_conflicts(
    mission_file_path: str, 
    safety_buffer: float,
    show_plot: bool = True
) -> Tuple[str, List[str], Optional[DroneMission], Optional[List[DroneMission]]]:
    """Loads mission data, checks for conflicts, and returns status and details.

    Optionally triggers a plot of the missions.

    Args:
        mission_file_path: Path to the JSON file containing mission data.
        safety_buffer: The minimum safety distance for conflict checks.
        show_plot: If True, display the plot using Matplotlib.

    Returns:
        A tuple containing:
          - str: Status ("Clear", "Conflict Detected", or "Error...").
          - List[str]: List of conflict descriptions (empty if clear).
          - Optional[DroneMission]: Primary mission object (for plotting).
          - Optional[List[DroneMission]]: List of simulated mission objects (for plotting).
    """
    primary_mission: Optional[DroneMission] = None
    simulated_missions: Optional[List[DroneMission]] = None
    try:
        primary_mission, simulated_missions = load_missions_from_json(mission_file_path)
    except (FileNotFoundError, ValueError, KeyError) as e:
        # Handle errors during loading
        return "Error Loading Mission", [f"Failed to load or parse mission file: {e}"], None, None

    try:
        conflict_found, conflict_details = find_conflicts(
            primary_mission,
            simulated_missions,
            safety_buffer
        )
    except Exception as e:
        # Catch potential errors during conflict checking
        print(f"Error during conflict check: {e}")
        # Return missions data even if check fails, plot might still be useful
        return "Error During Check", [f"An unexpected error occurred during conflict analysis: {e}"], primary_mission, simulated_missions

    if conflict_found:
        status = "Conflict Detected"
    else:
        status = "Clear"
        conflict_details = [] # Ensure details are empty if clear
        
    # Trigger plot if requested and missions were loaded successfully
    if show_plot and primary_mission and simulated_missions:
        try:
            print("\nGenerating mission plot...")
            plot_missions(primary_mission, simulated_missions, safety_buffer, conflict_details if conflict_found else None)
        except Exception as plot_e:
            print(f"Warning: Failed to generate plot. Error: {plot_e}")
            # Don't let plotting errors stop the main flow

    return status, conflict_details, primary_mission, simulated_missions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check drone mission for spatio-temporal conflicts and optionally visualize.")
    parser.add_argument("mission_file", help="Path to the mission JSON file.")
    parser.add_argument("-b", "--buffer", type=float, default=5.0, 
                        help="Safety buffer distance (default: 5.0 units).")
    parser.add_argument("--no-plot", action="store_true",
                        help="Suppress the mission visualization plot.")
    
    args = parser.parse_args()

    print(f"Checking mission file: {args.mission_file}")
    print(f"Using safety buffer: {args.buffer}")
    print(f"Plotting enabled: {not args.no_plot}")
    print("---")

    # Pass the plotting flag
    status, details, _, _ = check_mission_conflicts(args.mission_file, args.buffer, show_plot=not args.no_plot)

    print(f"\n--- Final Result ---")
    print(f"Mission Status: {status}")
    if details:
        print("Conflict Details:")
        for detail in details:
            print(f"- {detail}")
    else:
        print("(No conflicts detected)")
    print("--------------------") 