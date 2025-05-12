# Drone Deconfliction System

This project implements a system to detect potential spatial and temporal conflicts between a primary drone mission and other simulated drone flights.

## Setup

1.  **Prerequisites:** Python 3.x
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Data Input

The system currently expects mission data to be provided via a JSON file (e.g., `missions.json`). The structure should include:
*   `primary_mission`: Details for the main drone (waypoints as `[{"x": float, "y": float}, ...]`, `start_time` and `end_time` as integer HHMM).
*   `simulated_missions`: A list of other drone flights, each with waypoints including timestamps (`[{"x": float, "y": float, "timestamp": int_HHMM}, ...]`).

See `utils.py` for the precise loading logic.

## Execution

(Instructions on how to run the application will be added here.)

## Project Structure

*   `deconfliction_system.py`: Main application script.
*   `models.py`: Defines data structures (`Waypoint`, `DroneMission`).
*   `utils.py`: Contains utility functions (e.g., `load_missions_from_json`).
*   `requirements.txt`: Python dependencies.
*   `docs/`: Contains project planning documents (`Project.md`) and assignment details.
*   `README.md`: This file. 