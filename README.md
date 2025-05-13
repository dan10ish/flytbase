# Drone Deconfliction System

This project implements a system to detect spatio-temporal conflicts between a primary drone mission and multiple simulated drone flights in a 2D environment.

## Project Structure

```
flytbase/
├── data/                     # Mission scenario JSON files
│   ├── scenario_buffer.json
│   ├── scenario_clear.json
│   ├── scenario_conflict_spatial_only.json
│   └── scenario_conflict_st.json
├── docs/                     # Project documentation and assignment details
│   ├── Assignment.pdf
│   └── Project.md
├── src/                      # Source code
│   ├── __init__.py             # Makes 'src' a Python package
│   ├── conflict_checks.py    # Core spatio-temporal conflict logic
│   ├── deconfliction_system.py # Main execution script and CLI
│   ├── models.py             # Data models (Waypoint, DroneMission)
│   ├── utils.py              # Utility functions (JSON loading, time conversion)
│   └── visualization.py      # Mission plotting using Matplotlib
├── .gitignore                # (Optional: Recommended Git ignore file)
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## Features Implemented (Phase 1 & 2)

*   **Data Loading:** Loads primary and simulated mission data from JSON files.
*   **Time Handling:** Uses HHMM integer format for input times, converting to minutes since midnight for calculations.
*   **Primary Mission Timestamps:** Calculates waypoint timestamps for the primary drone assuming constant speed between its overall start and end times.
*   **Spatial Conflict Check:** Uses the Shapely library to detect:
    *   Intersections between path segments.
    *   Proximity conflicts where paths come closer than a defined safety buffer.
*   **Temporal Conflict Check:** Determines the time intervals drones occupy specific path segments.
*   **Spatio-Temporal Conflict Detection:** Identifies conflicts only if spatial overlap/proximity occurs *during* overlapping time intervals.
*   **Waypoint Collision Check:** Detects if two drones occupy the exact same coordinates at the exact same time.
*   **Command-Line Interface:** Allows running conflict checks via `deconfliction_system.py`, specifying the mission file and safety buffer.
*   **Visualization:** Generates a 2D plot using Matplotlib showing:
    *   Primary and simulated drone paths.
    *   Highlighted conflict locations/segments (if any).

## Setup

1.  **Clone the repository (or ensure you have the project files).**
2.  **Ensure you have Python 3 installed.**
3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the deconfliction system from the root directory of the project (`flytbase/`) using the following command format:

```bash
python -m src.deconfliction_system <path_to_mission_file> [options]
```

*   `<path_to_mission_file>`: Path to the JSON file containing the mission data (e.g., `data/scenario_conflict_st.json`).
*   `[options]`: 
    *   `-b BUFFER` or `--buffer BUFFER`: Set the safety buffer distance (default: 5.0).
    *   `--no-plot`: Suppress the visualization plot.

**Examples:**

*   Check the spatio-temporal conflict scenario with default buffer and show plot:
    ```bash
    python -m src.deconfliction_system data/scenario_conflict_st.json
    ```
*   Check the clear scenario with a buffer of 10 units and hide the plot:
    ```bash
    python -m src.deconfliction_system data/scenario_clear.json -b 10 --no-plot
    ```

## Next Steps (Phase 3)

*   Implement a graphical user interface (GUI) using PySimpleGUI. 