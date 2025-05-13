# Drone Deconfliction System

This project implements a system to detect spatio-temporal conflicts between a primary drone mission and multiple simulated drone flights. The system now supports 3D spatial coordinates (x, y, z) and provides 2D, 3D static, and 4D (animated 3D) visualizations.

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
│   ├── conflict_checks.py    # Core spatio-temporal conflict logic (2D and 3D)
│   ├── deconfliction_system.py # Main execution script and CLI
│   ├── gui.py               # GUI implementation using PySimpleGUI
│   ├── models.py             # Data models (Waypoint, DroneMission)
│   ├── utils.py              # Utility functions (JSON loading, time conversion, distance calcs)
│   └── visualization.py      # Mission plotting (2D, 3D static, 3D animated) using Matplotlib
├── .gitignore                # (Optional: Recommended Git ignore file)
├── app.py                    # Main GUI application entry point
├── Explained.md              # Detailed explanation of the project
├── missions.json             # Default/example mission file, now with 3D data
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## Features Implemented

### Phase 1 & 2 (Core Functionality - Extended for 3D)

*   **Data Loading:** Loads primary and simulated mission data from JSON files, now including `z` (altitude) coordinates.
*   **Time Handling:** Uses HHMM integer format for input times, converting to minutes since midnight for calculations.
*   **Primary Mission Timestamps:** Calculates waypoint timestamps for the primary drone assuming constant speed between its overall start and end times, now in 3D space.
*   **Spatial Conflict Check (3D):**
    *   Performs 3D distance calculations between path segments.
    *   Detects proximity conflicts where paths come closer than a defined safety buffer in 3D space. (Note: Original 2D Shapely-based check replaced with custom 3D logic).
*   **Temporal Conflict Check:** Determines the time intervals drones occupy specific path segments.
*   **Spatio-Temporal Conflict Detection (3D):** Identifies conflicts only if 3D spatial overlap/proximity occurs *during* overlapping time intervals.
*   **Waypoint Collision Check (3D):** Detects if two drones occupy the exact same 3D coordinates at the exact same time.
*   **Command-Line Interface:** Allows running conflict checks via `deconfliction_system.py`, specifying the mission file (which can contain 3D data) and safety buffer.
*   **Visualization (2D):** Generates a 2D plot using Matplotlib showing:
    *   Primary and simulated drone paths projected onto the X-Y plane.
    *   Highlighted conflict locations/segments (if any).

### Phase 3 (GUI Implementation - Extended for 3D)

*   **User-Friendly Interface:** A modern, intuitive GUI built with PySimpleGUI.
*   **Input Methods:**
    *   Manual input of drone mission parameters directly in the GUI, now including `z` coordinates for waypoints.
    *   File loading for predefined mission scenarios (JSON files can contain 3D data).
*   **Interactive Controls:**
    *   Adjustable safety buffer using a slider.
*   **Results Display:**
    *   Clear status indicators showing "Clear" or "Conflict Detected".
    *   Detailed explanation of any detected conflicts, including 3D coordinates.
    *   Mission visualizations (2D, static 3D, and animated 3D) with highlighted conflict areas, each opening in separate windows.

### Phase 5 (3D/4D Enhancements)

*   **3D Coordinate System:** Full integration of `z` (altitude) coordinate in all calculations and data structures.
*   **3D Conflict Logic:** Conflict detection algorithms (segment proximity, waypoint collision) operate in 3D space.
*   **Static 3D Visualization:**
    *   Generation of static 3D plots showing drone paths in x,y,z space.
    *   Includes an overview plot and individual plots for primary vs. simulated drone comparisons.
    *   Conflicts are highlighted on these 3D paths.
*   **4D Visualization (Animated 3D):**
    *   Generation of an animated 3D plot showing drone markers moving along their 3D paths over time.
    *   Provides a dynamic view of the spatio-temporal evolution of missions.
    *   Includes on-screen display of the current animation time.

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

### GUI Application (Recommended)

Run the GUI application from the root directory of the project (`flytbase/`) using:

```bash
python app.py
```

The GUI application provides the following features:

1. **Primary Mission Input:**
   - Drone ID
   - Waypoints in format `x1,y1,z1;x2,y2,z2;...` (semicolon-separated 3D coordinates). The system also attempts to handle `x,y` by defaulting `z=0` with a warning.
   - Start and end times in HHMM format (e.g., 0800 for 8:00 AM)

2. **Simulated Mission Input:**
   - Drone ID
   - Waypoints in the same `x,y,z` format as the primary mission.
   - Timestamps for each waypoint in HHMM format (semicolon-separated).

3. **Safety Settings:**
   - Adjustable safety buffer using a slider control (1-20 units), applied in 3D.

4. **Mission Check Controls:**
   - "Check from Inputs" button to analyze the manually entered mission data.
   - "Load Mission File" button to select and analyze a pre-defined mission JSON file (which can contain 2D or 3D data).

5. **Results Display:**
   - Status indicator showing "CLEAR" or "CONFLICT DETECTED".
   - Detailed conflict information when conflicts are found (now including `z` coordinates).
   - Visualization of the missions with highlighted conflict areas in separate windows:
     - 2D X-Y projection plots.
     - Static 3D plots.
     - An animated 3D plot showing movement over time (4D visualization).

### Command-Line Interface (Alternative)

Run the deconfliction system from the command line using:

```bash
python -m src.deconfliction_system <path_to_mission_file> [options]
```

*   `<path_to_mission_file>`: Path to the JSON file containing the mission data (e.g., `data/scenario_conflict_st.json` or the root `missions.json`). This file should now contain `z` coordinates for 3D analysis.
*   `[options]`: 
    *   `-b BUFFER` or `--buffer BUFFER`: Set the safety buffer distance (default: 5.0), applied in 3D.
    *   `--no-plot`: Suppress all mission visualization plots. If not suppressed, 2D, 3D static, and 3D animated plots will be generated.

**Examples:**

*   Check the default `missions.json` (which now has 3D data) with default buffer and show all plots:
    ```bash
    python -m src.deconfliction_system missions.json
    ```
*   Check a 3D scenario with a buffer of 10 units and hide the plots:
    ```bash
    python -m src.deconfliction_system data/scenario_conflict_st_3d.json -b 10 --no-plot 
    ```
    *(Assuming `scenario_conflict_st_3d.json` is a hypothetical 3D scenario file)*

## Mission File Format

The system works with JSON mission files. For 3D operations, waypoints should include `x`, `y`, and `z` coordinates:

```json
{
  "primary_mission": {
    "drone_id": "primary_3D_01",
    "waypoints": [
      {"x": 0, "y": 0, "z": 10},
      {"x": 100, "y": 0, "z": 10},
      {"x": 100, "y": 100, "z": 15}
    ],
    "start_time": 800,  
    "end_time": 810     
  },
  "simulated_missions": [
    {
      "drone_id": "sim_3D_A",
      "waypoints": [
        {"x": 50, "y": -10, "z": 5, "timestamp": 803}, 
        {"x": 50, "y": 10, "z": 5, "timestamp": 806}  
      ]
    }
    // ... more simulated missions with x, y, z coordinates
  ]
}
```

The primary mission specifies overall start and end times, while simulated missions include timestamps for each waypoint.
If `z` coordinates are omitted from the JSON file, their behavior in 3D conflict checks is undefined by default, though loading in `utils.py` currently makes `z` mandatory for waypoints being loaded from JSON for 3D operations. The GUI provides a fallback for `x,y` input by setting `z=0`. 