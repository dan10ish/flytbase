# Drone Deconfliction System: Comprehensive Explanation

This document provides a detailed explanation of the Drone Deconfliction System project, covering every file, its purpose, the functions within it, their logic, naming conventions, and illustrative examples. The system has been enhanced to support 3D spatial coordinates and 4D (3D + time) animated visualizations.

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [File Structure and Explanations](#file-structure-and-explanations)
    - [`README.md`](#readmemd)
    - [`app.py`](#apppy)
    - [`requirements.txt`](#requirementstxt)
    - [`.gitignore`](#gitignore)
    - [`missions.json`](#missionsjson)
    - [`src/__init__.py`](#src__init__py)
    - [`src/models.py`](#srcmodels_py)
    - [`src/utils.py`](#srcutils_py)
    - [`src/conflict_checks.py`](#srcconflict_checks_py)
    - [`src/visualization.py`](#srcvisualization_py)
    - [`src/deconfliction_system.py`](#srcdeconfliction_system_py)
    - [`src/gui.py`](#srcgui_py)
    - [Data Files (`data/*.json`)](#data-files)
      - [`data/scenario_clear.json`](#datascenario_clearjson)
      - [`data/scenario_conflict_buffer.json`](#datascenario_conflict_bufferjson)
      - [`data/scenario_conflict_spatial_only.json`](#datascenario_conflict_spatial_onlyjson)
      - [`data/scenario_conflict_st.json`](#datascenario_conflict_stjson)
    - [Documentation Files (`Docs/*`)](#documentation-files)
      - [`Docs/Project.md`](#docsprojectmd)
      - [`Docs/Assignment.pdf`](#docsassignmentpdf)
3.  [Core Concepts and Logic](#core-concepts-and-logic)
    - [Time Handling](#time-handling)
    - [Spatial Checks](#spatial-checks)
    - [Temporal Checks](#temporal-checks)
    - [Spatio-Temporal Conflict](#spatio-temporal-conflict)
    - [Safety Buffer](#safety-buffer)
    - [Waypoint Collision](#waypoint-collision)
    - [3D Coordinates and Operations](#3d-coordinates-and-operations)
    - [4D Visualization (3D Animation)](#4d-visualization-3d-animation)
4.  [Naming Conventions](#naming-conventions)
    - [File Naming](#file-naming)
    - [Function and Variable Naming](#function-and-variable-naming)
    - [Drone IDs](#drone-ids)
5.  [Example Test Cases and Scenarios](#example-test-cases-and-scenarios)
6.  [Installation](#installation)
7.  [Running the Program](#running-the-program)
8.  [How to Create the Mission JSON File](#how-to-create-the-mission-json-file)
9.  [Detailed Scenario Walkthroughs](#detailed-scenario-walkthroughs)

---

## 1. Project Overview

The Drone Deconfliction System is a Python application designed to detect and report potential spatio-temporal conflicts between a primary drone's mission and one or more simulated drone flights. It now operates in a **3D environment (x, y, z coordinates)** and considers both spatial proximity (including a safety buffer) and temporal overlaps. Phase 5 enhancements also include **4D visualization through 3D animations over time**.

Key Functionalities:

- Loading mission data from JSON files (now including `z` coordinates).
- Calculating timestamps for the primary drone's path based on constant speed in 3D space.
- Checking for 3D spatial conflicts (path segment proximity and waypoint collisions).
- Checking for temporal overlaps between drones on potentially conflicting path segments.
- Identifying exact 3D waypoint collisions (same location, same time).
- Providing detailed conflict reports with 3D coordinates.
- Visualizing missions and conflicts in:
    - 2D (X-Y projection).
    - Static 3D (X-Y-Z paths).
    - Animated 3D (drones moving along X-Y-Z paths over time - 4D).
- Offering a GUI for easier interaction and mission input (now supporting `z` coordinates).

---

## 2. File Structure and Explanations

The project follows a modular structure to separate concerns:

```
flytbase/
├── data/                     # Mission scenario JSON files
│   ├── scenario_buffer.json
│   ├── scenario_clear.json
│   ├── scenario_conflict_spatial_only.json
│   └── scenario_conflict_st.json
├── Docs/                     # Project documentation and assignment details
│   ├── Assignment.pdf
│   └── Project.md
├── src/                      # Source code
│   ├── __init__.py             # Makes 'src' a Python package
│   ├── conflict_checks.py    # Core spatio-temporal conflict logic (now 3D)
│   ├── deconfliction_system.py # Main execution script and CLI for core logic
│   ├── gui.py                  # GUI implementation using PySimpleGUI (handles 3D input)
│   ├── models.py               # Data models (Waypoint with Z, DroneMission)
│   ├── utils.py                # Utility functions (JSON loading with Z, time conversion, 3D distance)
│   └── visualization.py        # Mission plotting (2D, static 3D, animated 3D) using Matplotlib
├── .gitignore                # Specifies intentionally untracked files that Git should ignore
├── app.py                    # Main GUI application entry point
├── Explained.md              # This file: Detailed explanation of the project
├── missions.json             # Default/example mission file (now with 3D data)
└── requirements.txt          # Python dependencies
```

### `README.md`

- **Purpose:** Provides a high-level overview of the project, its features, the project structure, setup instructions, and usage guidelines for both the GUI and CLI.
- **Content:**
  - Project title and brief description.
  - Detailed project structure tree.
  - List of implemented features (Phase 1, 2, and 3).
  - Setup instructions: cloning, virtual environment, installing dependencies.
  - Usage instructions for the GUI (`app.py`).
  - Usage instructions for the CLI (`src.deconfliction_system`).
  - Example CLI commands.
  - Explanation of the `missions.json` file format.
- **How it Works:** Serves as the main entry point for users and developers to understand and run the project.
- **Naming Conventions:** Standard markdown file naming.

### `app.py`

- **Purpose:** This is the main entry point for launching the Graphical User Interface (GUI) of the Drone Deconfliction System. It now supports 3D mission inputs and triggers 2D, 3D, and animated 4D visualizations.
- **Content:**

  ```python
  """
  Drone Deconfliction System - GUI Application

  This is the main entry point for the Drone Deconfliction System GUI application.
  Run this file to start the application.
  """

  from src.gui import main_window

  if __name__ == "__main__":
      main_window()
  ```

- **Logic:**
  - It imports the `main_window` function from the `src.gui` module.
  - The `if __name__ == "__main__":` block ensures that `main_window()` is called only when `app.py` is executed directly (not when imported as a module).
  - Calling `main_window()` initializes and displays the GUI, which now handles 3D inputs and triggers enhanced visualizations.
- **Naming Conventions:** `app.py` is a common name for the main application starter script.
- **Example Usage:**
  ```bash
  python app.py
  ```
  This command, run from the `flytbase/` directory, will launch the GUI.

### `requirements.txt`

- **Purpose:** Lists all the external Python libraries (dependencies) required for the project to run correctly.
- **Content:**
  ```
  matplotlib>=3.0 # For visualization (2D, 3D, animation)
  PySimpleGUI>=4.60.0 # For GUI implementation
  # Shapely is no longer a direct dependency for core conflict checks as 3D logic is custom.
  # It might still be present if other non-core functionalities were to use it.
  ```
- **Logic:**
  - `matplotlib`: Used for plotting drone paths and conflicts (2D, 3D static, and 3D animated).
  - `PySimpleGUI`: Used to create the graphical user interface.
- **How it Works:** Users can install all necessary dependencies using pip:
  ```bash
  pip install -r requirements.txt
  ```
- **Naming Conventions:** `requirements.txt` is the standard name for such files in Python projects.

### `.gitignore`

- **Purpose:** Specifies intentionally untracked files that Git should ignore. This helps keep the repository clean from generated files or local configurations.
- **Content:**
  ```
  __pycache__/
  ```
- **Logic:**
  - `__pycache__/`: This directory is automatically created by Python to store compiled bytecode (`.pyc` files). These are not needed in version control as they are specific to the Python interpreter and system that generated them.
- **How it Works:** Git reads this file and avoids tracking or committing any files or directories matching the patterns listed.
- **Naming Conventions:** `.gitignore` is the standard name recognized by Git.

### `missions.json`

- **Purpose:** An example JSON file that defines a set of drone missions, including one primary mission and several simulated missions. This file is used by default by the CLI if no other file is specified, and can be loaded via the GUI. It should now include `z` coordinates for 3D operations.
- **Content Snippet (with `z` coordinates):**
  ```json
  {
    "primary_mission": {
      "drone_id": "Alpha_3D",
      "waypoints": [
        { "x": 0, "y": 0, "z": 10 },
        { "x": 100, "y": 0, "z": 10 },
        { "x": 100, "y": 100, "z": 15 }
      ],
      "start_time": 800,
      "end_time": 820
    },
    "simulated_missions": [
      {
        "drone_id": "Bravo_3D",
        "waypoints": [
          { "x": 0, "y": 50, "z": 5, "timestamp": 805 },
          { "x": 100, "y": 50, "z": 5, "timestamp": 815 }
        ]
      }
      // ... more simulated missions with x, y, z coordinates
    ]
  }
  ```
- **Logic:**
  - `primary_mission`:
    - `drone_id`: A unique identifier for the primary drone.
    - `waypoints`: A list of `{"x": x_val, "y": y_val, "z": z_val}` dictionaries. Timestamps are _not_ provided here for the primary mission; they are calculated based on `start_time` and `end_time` assuming constant 3D speed.
    - `start_time`: The overall mission start time in HHMM format.
    - `end_time`: The overall mission end time in HHMM format.
  - `simulated_missions`: A list of mission objects for simulated drones.
    - `drone_id`: A unique identifier for the simulated drone.
    - `waypoints`: A list of `{"x": x_val, "y": y_val, "z": z_val, "timestamp": hhmm_time}` dictionaries. Each waypoint has an explicit timestamp and 3D coordinates.
- **How it Works:** This file is read by `src.utils.load_missions_from_json()` to create `DroneMission` objects. `load_missions_from_json` now expects `z` coordinates for all waypoints if 3D operations are intended.
- **Naming Conventions:** `missions.json` clearly indicates its purpose. Drone IDs like "Alpha_3D", "Bravo_3D" are descriptive.

### `src/__init__.py`

- **Purpose:** This empty file tells Python that the `src` directory should be treated as a package. This allows for relative imports between modules within the `src` directory.
- **Content:** It is typically empty.
- **How it Works:** When Python encounters an `__init__.py` file in a directory, it recognizes that directory as a package, enabling structured organization of modules. For example, `from .models import Waypoint` works because `src` is a package.
- **Naming Conventions:** `__init__.py` is a special, required name for this purpose.

### `src/models.py`

- **Purpose:** Defines the core data structures (data classes) used throughout the application to represent waypoints and drone missions. `Waypoint` now includes a `z` coordinate for 3D space.
- **Content:**

  - `Waypoint` data class:
    - `x: float`: The x-coordinate of the waypoint.
    - `y: float`: The y-coordinate of the waypoint.
    - `z: float`: The z-coordinate (altitude) of the waypoint.
    - `timestamp_minutes: int`: The time at which the drone is at this waypoint, represented as minutes since midnight (0-1439).
  - `DroneMission` data class:
    - `drone_id: str`: A unique identifier for the drone.
    - `waypoints: List[Waypoint]`: A list of `Waypoint` objects (which are now 3D) defining the drone's path and timing.
    - `get_path_segments()` method:
      - **Logic:** Converts the list of waypoints into a list of path segments. A segment is a tuple of two consecutive `Waypoint` objects `(Waypoint_i, Waypoint_i+1)`.
      - **Returns:** `List[Tuple[Waypoint, Waypoint]]`. Returns an empty list if there are fewer than two waypoints.
      - **Example:** If `waypoints` is `[wp1, wp2, wp3]`, `get_path_segments()` returns `[(wp1, wp2), (wp2, wp3)]`.

- **How it Works:** These classes provide a structured and type-safe way to handle mission data. `dataclasses` automatically generate methods like `__init__`, `__repr__`, etc., reducing boilerplate code.
- **Naming Conventions:**
  - `models.py`: Standard name for files containing data model definitions.
  - Class names `Waypoint` and `DroneMission` are descriptive and use CamelCase.
  - Field names like `drone_id`, `timestamp_minutes` use snake_case.
  - `timestamp_minutes`: Clearly indicates the unit and reference (minutes since midnight).

### `src/utils.py`

- **Purpose:** Contains utility functions used across different parts of the project, primarily for data loading, parsing, and time/distance calculations. Now handles 3D coordinates in loading and distance calculations.
- **Key Functions:**

  - **`_parse_hhmm_to_minutes(hhmm: int) -> int`:**

    - **Logic:** Converts an integer time in HHMM format (e.g., `800` for 08:00, `1430` for 14:30) into total minutes since midnight (0-1439).
    - **Input:** `hhmm` (integer between 0 and 2359).
    - **Output:** Total minutes (integer).
    - **Error Handling:** Raises `ValueError` for invalid HHMM format or values (e.g., `2500`, `870`).
    - **Example:** `_parse_hhmm_to_minutes(800)` returns `480`. `_parse_hhmm_to_minutes(1430)` returns `870`.

  - **`_calculate_distance(p1: Dict[str, float], p2: Dict[str, float]) -> float`:**

    - **Logic:** Calculates the Euclidean distance between two 3D points. Points are expected as dictionaries `{'x': float, 'y': float, 'z': float}`. If `z` is missing from a dict, it defaults to `0.0` for that point in the calculation, though `load_missions_from_json` makes `z` mandatory from the file.
    - **Input:** `p1`, `p2` (dictionaries, expecting `x`, `y`, `z` keys).
    - **Output:** 3D Distance (float).
    - **Error Handling:** Raises `ValueError` if points have missing `x` or `y` keys or non-numeric coordinates.
    - **Example:** `_calculate_distance({'x': 0, 'y': 0, 'z':0}, {'x': 3, 'y': 4, 'z':0})` returns `5.0`.
             `_calculate_distance({'x':0,'y':0,'z':0}, {'x':0,'y':0,'z':10})` returns `10.0`.

  - **`load_missions_from_json(filepath: str) -> Tuple[DroneMission, List[DroneMission]]`:**
    - **Logic:** This is a crucial function for loading and processing mission data from a JSON file. It now expects and processes `z` coordinates.
      1.  Reads the JSON file specified by `filepath`.
      2.  **Parses Simulated Missions:**
          - Iterates through each mission in the `"simulated_missions"` list.
          - For each waypoint, it parses the `x`, `y`, `z` coordinates and the `timestamp` (HHMM format) using `_parse_hhmm_to_minutes`.
          - Creates `Waypoint` objects (now including `z`) and then a `DroneMission` object for each simulated drone.
          - Sorts waypoints by their `timestamp_minutes`.
      3.  **Parses Primary Mission:**
          - Retrieves data from the `"primary_mission"` object.
          - Parses `start_time` and `end_time` (HHMM) into minutes since midnight.
          - Validates that `start_time` is before `end_time`.
          - **Calculates Primary Drone Timestamps (in 3D):** This logic remains similar but `_calculate_distance` now uses 3D distances.
            - If only one waypoint, its timestamp is `start_time_minutes` (waypoint includes `z`).
            - If multiple waypoints:
              - Calculates the total 3D path distance by summing 3D distances between consecutive waypoints using `_calculate_distance`.
              - Calculates the total mission duration (`end_time_minutes - start_time_minutes`).
              - If `total_distance` is 0 (all waypoints at the same 3D spot), all waypoints get `start_time_minutes`.
              - Otherwise, calculates a constant `speed` (3D distance units per minute).
              - The first waypoint is assigned `start_time_minutes`.
              - For subsequent waypoints, it calculates the time taken to travel the 3D segment (`segment_distance_3d / speed`) and adds it to the previous waypoint's time.
              - Timestamps are rounded and clamped to ensure the last waypoint does not exceed `end_time_minutes`. The final waypoint's time is adjusted to be exactly `end_time_minutes` if the calculated value is very close.
          - Creates `Waypoint` objects (including `z`) with these calculated timestamps and then the primary `DroneMission` object.
    - **Input:** `filepath` (string path to JSON, expected to contain `z` coordinates for waypoints).
    - **Output:** A tuple `(primary_mission_object, list_of_simulated_mission_objects)`.
    - **Error Handling:** Raises `FileNotFoundError`, `json.JSONDecodeError`, `ValueError` (for data format issues, invalid times), or `KeyError` (if `x`, `y`, or `z` keys are missing in waypoints from the JSON, as `z` is now treated as mandatory by this function).
    - **Naming Conventions:**
      - `_parse_hhmm_to_minutes` and `_calculate_distance` start with an underscore, suggesting they are intended as internal helper functions within this module.
      - `load_missions_from_json` is descriptive of its action.
      - Variables like `hhmm`, `start_time_minutes`, `total_distance` are clear.

- **How it Works:** Provides reusable components for common tasks, promoting cleaner code in other modules.
- **Example Test Case (for `_parse_hhmm_to_minutes`):**
  - Input: `1030` -> Output: `630`
  - Input: `0` -> Output: `0`
  - Input: `2359` -> Output: `1439`
  - Input: `1060` -> Raises `ValueError` (invalid minute)
- **Example Test Case (for `load_missions_from_json` primary mission timestamp calculation):**
  - Primary mission: waypoints `(0,0,10), (100,0,10), (100,100,15)`, start_time `800`, end_time `820`.
    - Total distance = 200. Total duration = 20 minutes. Speed = 10 units/min.
    - Waypoint 1 `(0,0,10)`: timestamp `480` (08:00).
    - Waypoint 2 `(100,0,10)`: time for segment = 100/10 = 10 mins. Timestamp = 480 + 10 = `490` (08:10).
    - Waypoint 3 `(100,100,15)`: time for segment = 100/10 = 10 mins. Timestamp = 480 + 10 = `490` (08:10).

### `src/conflict_checks.py`

- **Purpose:** Contains the core logic for detecting spatio-temporal conflicts between drone missions, now adapted for 3D space. **Shapely is no longer used for segment conflict checks.**
- **Key Constants:**

  - `FLOAT_TOLERANCE = 1e-9`: A small value used for comparing floating-point numbers to account for precision issues. For example, instead of `a == b`, use `abs(a - b) < FLOAT_TOLERANCE`.

- **New 3D Geometry Helper Functions:**
  - **`_subtract_vectors(v1: Waypoint, v2: Waypoint) -> Dict[str, float]`**: Subtracts 3D coordinates of `v2` from `v1`.
  - **`_dot_product(vec1: Dict[str, float], vec2: Dict[str, float]) -> float`**: Calculates the dot product of two 3D vectors (represented as dicts).
  - **`_vector_norm_sq(vec: Dict[str, float]) -> float`**: Calculates the squared norm (length squared) of a 3D vector.
  - **`distance_point_to_segment_3d(point: Waypoint, seg_start: Waypoint, seg_end: Waypoint) -> float`**:
    - **Logic:** Calculates the minimum Euclidean distance from a 3D `point` to a 3D line segment defined by `seg_start` and `seg_end`. It projects the point onto the line containing the segment and checks if the projection falls within the segment. If not, the distance to the closest endpoint is used.

- **Key Functions (Updated for 3D):**

  - **`_get_time_interval_for_segment(segment: Tuple[Waypoint, Waypoint]) -> Tuple[int, int]`:**

    - **Logic:** Extracts the start and end timestamps (in minutes since midnight) from the two `Waypoint` objects that define a path segment. Assumes waypoints in a segment are chronologically ordered.
    - **Input:** `segment` (a tuple of two `Waypoint` objects).
    - **Output:** A tuple `(start_minutes, end_minutes)`.

  - **`check_segment_spatial_conflict(segment1: Tuple[Waypoint, Waypoint], segment2: Tuple[Waypoint, Waypoint], safety_buffer: float) -> bool`:**
    - **Logic (New 3D Implementation):** This function no longer uses Shapely. It checks for spatial proximity between two 3D path segments.
      1.  Unpacks the start and end `Waypoint` objects for `segment1` (p1_start, p1_end) and `segment2` (p2_start, p2_end).
      2.  It uses a simplified proximity check:
          - Calculates the distance from `p1_start` to `segment2` using `distance_point_to_segment_3d`.
          - Calculates the distance from `p1_end` to `segment2`.
          - Calculates the distance from `p2_start` to `segment1`.
          - Calculates the distance from `p2_end` to `segment1`.
      3.  If any of these calculated distances is less than `safety_buffer` (minus `FLOAT_TOLERANCE`), a spatial conflict is considered to exist.
    - **Note:** This is an approximation for segment-to-segment distance, focusing on endpoint-to-segment checks. A full 3D segment-to-segment minimum distance algorithm is more complex.
    - **Input:** `segment1`, `segment2` (tuples of 3D `Waypoint` objects), `safety_buffer`.
    - **Output:** `True` if a spatial conflict (proximity based on the above logic) exists, `False` otherwise.

  - **`check_spatio_temporal_segment_conflict(segment1: Tuple[Waypoint, Waypoint], segment2: Tuple[Waypoint, Waypoint], safety_buffer: float) -> bool`:**
    - **Logic:** (Structure remains similar, but uses the new 3D `check_segment_spatial_conflict`)
      1.  First, calls the 3D `check_segment_spatial_conflict`. If no spatial conflict, returns `False`.
      2.  If spatial conflict, retrieves time intervals and checks for overlap (same temporal logic as before).
    - **Input:** `segment1`, `segment2` (tuples of 3D `Waypoint` objects), `safety_buffer`.
    - **Output:** `True` if both 3D spatial conflict and temporal overlap exist, `False` otherwise.

  - **`check_waypoint_collision(wp1: Waypoint, wp2: Waypoint) -> bool`:**
    - **Logic (Updated for 3D):** Checks if two 3D waypoints represent the exact same 3D location at the exact same time.
      1.  Compares `wp1.timestamp_minutes` and `wp2.timestamp_minutes`.
      2.  Compares `x`, `y`, and now `z` coordinates using `abs(coord1 - coord2) < FLOAT_TOLERANCE`.
    - **Input:** `wp1`, `wp2` (two 3D `Waypoint` objects).
    - **Output:** `True` if timestamps and all three coordinates (within tolerance) match, `False` otherwise.

  - **`find_conflicts(primary_mission: DroneMission, simulated_missions: List[DroneMission], safety_buffer: float) -> Tuple[bool, List[str]]`:**
    - **Logic:** (Structure remains similar, but calls the 3D-aware conflict check functions).
      - The conflict description strings generated now include `z` coordinates for waypoint collisions.

- **How it Works:** Systematically compares the primary mission against each simulated mission, checking for both types of conflicts (segment-based spatio-temporal and exact waypoint collisions).
- **Test Case (Conceptual for `find_conflicts`):**
  - **Scenario:** Primary drone flies (0,0,10)@08:00 -> (100,0,10)@08:10. Sim drone flies (50,0,5)@08:05 -> (50,0,5)@08:15. Safety buffer = 5.
  - **Expected Output:** `find_conflicts` should identify a spatio-temporal conflict. The primary path is y=0 from t=08:00 to 08:10. The sim path crosses x=50 from y=0 to y=0 between t=08:05 and t=08:15. The paths are spatially close (within buffer 5 around y=0 for the primary drone). The time intervals [08:00, 08:10] and [08:05, 08:15] overlap.

### `src/visualization.py`

- **Purpose:** Handles the generation of plots to visualize drone mission paths and highlight conflicts. It now supports 2D plots, static 3D plots, and animated 3D (4D) plots using Matplotlib.
- **Key Imports Added:**
  - `from mpl_toolkits.mplot3d import Axes3D`
  - `from matplotlib.animation import FuncAnimation`
- **Key Constants (Colors):**

  - `PRIMARY_COLOR = 'blue'`
  - `SIMULATED_COLOR = 'gray'` (though a colormap `plt.cm.viridis_r` is used for multiple sim drones)
  - `CONFLICT_COLOR = 'red'`
  - `BUFFER_COLOR = 'lightblue'` (defined but not explicitly used to draw buffer areas in the current implementation, buffer value is in the title).

- **Key Functions (Updates and New Additions):**

  - **`_interpolate_position_3d(waypoints: List[Waypoint], time_minutes: float) -> Optional[Tuple[float, float, float]]` (New Helper for Animation):**
    - **Logic:** Calculates a drone's interpolated (x,y,z) position at a specific `time_minutes` along its path defined by a list of `Waypoint` objects. Handles cases for time outside mission segment or single-waypoint missions.
    - **Input:** List of `Waypoint` objects, target `time_minutes`.
    - **Output:** `(x,y,z)` tuple or `None`.

  - **`_plot_path(ax, waypoints: List[Waypoint], color: str, label: str, ..., is_3d: bool = False)` (Updated):**
    - **Logic:** Helper to plot a single drone path. Now takes an `is_3d` boolean flag. If `True`, it extracts `z` coordinates and plots in 3D using `ax.plot(x, y, z, ...)`. Otherwise, plots in 2D (`ax.plot(x, y, ...)`).

  - **`_parse_conflict_details(conflict_details: List[str]) -> dict`:**
    - **Logic:** Parses the human-readable conflict description strings (generated by `find_conflicts`) to extract structured information about which segments and waypoints are involved in conflicts. Uses regular expressions (`re` module) to find patterns like "Primary Segment X ... Sim Drone Y Segment Z".
    - **Input:** `conflict_details` (list of strings).
    - **Output:** A dictionary categorizing conflicting entities:
      ```python
      {
          "primary_segments": [index1, index2, ...], # Indices of conflicting primary segments
          "sim_segments": [(drone_id, index1), ...], # (Sim drone_id, index of its conflicting segment)
          "primary_waypoints": [index1, ...],       # Indices of conflicting primary waypoints
          "sim_waypoints": [(drone_id, index1), ...] # (Sim drone_id, index of its conflicting waypoint)
      }
      ```
    - **Example:** If a detail string is "Spatio-Temporal Conflict: Primary Segment 0 ... Sim Drone sim_A Segment 1", it would add `0` to `conflicts["primary_segments"]` and `("sim_A", 1)` to `conflicts["sim_segments"]`.

  - **`plot_missions(primary_mission: DroneMission, simulated_missions: List[DroneMission], safety_buffer: float, conflict_details: Optional[List[str]] = None)` (Significantly Updated):**
    - **Logic:** This function now orchestrates the creation of multiple types of plots:
      1.  **2D Overview Plot:** (Existing logic, plots X-Y projection).
      2.  **3D Static Overview Plot (New):**
          - Creates a new Matplotlib figure with a `projection='3d'` subplot.
          - Sets X, Y, Z labels and title.
          - Calls `_plot_path` with `is_3d=True` for primary and simulated missions.
          - If `conflict_details` are provided, parses them and highlights conflicting segments/waypoints in 3D using `ax_overview_3d.plot()` with X, Y, and Z coordinates.
      3.  **2D Individual Plots:** (Existing logic, plots X-Y projections for primary vs. each sim drone).
      4.  **3D Static Individual Plots (New):**
          - Similar to 2D individual plots, but creates subplots with `projection='3d'`.
          - Calls `_plot_path` with `is_3d=True`.
          - Highlights conflicts in 3D on these individual plots.
      5.  **Calls `plot_animated_3d_missions` (New - see below) to generate the 4D animation.**
      6.  Uses `plt.show(block=False)` to display all generated figures without blocking.

  - **`plot_animated_3d_missions(primary_mission: DroneMission, simulated_missions: List[DroneMission], safety_buffer: float)` (New Function):**
    - **Logic:** Creates an animated 3D plot representing the 4D (3D space + time) evolution of missions.
      1.  Sets up a Matplotlib figure with a 3D subplot.
      2.  Determines the global `min_time` and `max_time` for the animation from all waypoints.
      3.  Plots static 3D paths for all drones as a background using `_plot_path(is_3d=True, marker='')`.
      4.  Initializes `ax.scatter` objects for each drone to represent their current positions. These will be updated in each frame.
      5.  Adds a `ax.text2D` object to display the current animation time.
      6.  **`update(frame_num)` function:** This is the core of the animation.
          - Calculates `current_time` based on `frame_num`.
          - Updates the time display text.
          - For each drone marker: 
            - Calls `_interpolate_position_3d` to get the drone's (x,y,z) position at `current_time`.
            - Updates the marker's 3D position (`marker._offsets3d = ([x],[y],[z])`).
      7.  Creates a `FuncAnimation` object, passing it the figure, the `update` function, number of frames, interval, etc. `blit=False` is used for robustness with 3D.
      8.  Stores the `FuncAnimation` object in a global list `Held_animations` to prevent it from being garbage collected (which would stop the animation).
      9.  Calls `plt.show(block=False)` for the animation figure.
    - **Output:** Displays an animated 3D plot in a new window.

- **How it Works:** Provides comprehensive visualization. Static plots give an overview of paths and conflict locations. The animation provides an intuitive understanding of the temporal aspect of drone movements and conflicts in 3D space.
- **Test Case (Conceptual):**
  - Given a primary mission, a simulated mission that conflicts with it, and the corresponding `conflict_details` string.
  - `plot_missions` should display both paths, and the specific segment(s) or waypoint(s) mentioned in `conflict_details` should be drawn in red. The legend should correctly label the drones and conflict markers.

### `src/deconfliction_system.py`

- **Purpose:** This script serves as the main entry point for the command-line interface (CLI). It now processes 3D data from JSON files and, if plotting is enabled, triggers the generation of 2D, 3D static, and 3D animated plots.
- **Key Functions:**

  - **`check_mission_conflicts(mission_file_path: str, safety_buffer: float, show_plot: bool = True) -> Tuple[str, List[str], Optional[DroneMission], Optional[List[DroneMission]]]`:**
    - **Logic:**
      1.  **Load Missions:** Calls `utils.load_missions_from_json(mission_file_path)` to load the primary and simulated missions. Handles potential errors during loading (e.g., `FileNotFoundError`, `ValueError`) and returns an "Error Loading Mission" status with error details.
      2.  **Find Conflicts:** Calls `conflict_checks.find_conflicts(primary_mission, simulated_missions, safety_buffer)` to perform the conflict analysis. Handles potential exceptions during this step and returns an "Error During Check" status.
      3.  **Determine Status:** Based on the `conflict_found` boolean from `find_conflicts`, sets the overall `status` to "Conflict Detected" or "Clear". If clear, ensures `conflict_details` is an empty list.
      4.  **Plot Missions (Optional):** If `show_plot` is `True` and missions were loaded successfully, calls `visualization.plot_missions(...)` to display the plot. Catches and prints warnings for plotting errors but doesn't let them stop the main flow.
    - **Input:**
      - `mission_file_path: str`: Path to the mission JSON file.
      - `safety_buffer: float`: The safety buffer distance.
      - `show_plot: bool`: Flag to enable/disable plotting (defaults to `True`).
    - **Output:** A tuple containing:
      - `status: str`: "Clear", "Conflict Detected", or an error message.
      - `details: List[str]`: List of conflict descriptions.
      - `primary_mission: Optional[DroneMission]`: The loaded primary mission object (or `None` on error).
      - `simulated_missions: Optional[List[DroneMission]]`: The loaded simulated missions (or `None` on error). This return is useful for the GUI to get the mission objects for plotting.
    - **Naming Conventions:** `check_mission_conflicts` is descriptive. `mission_file_path`, `safety_buffer`, `show_plot` are clear parameter names.

- **Command-Line Interface Logic (within `if __name__ == "__main__":`)**
  - **Argument Parsing:** Uses `argparse` to define and parse command-line arguments:
    - `mission_file` (positional argument): Path to the mission JSON file.
    - `-b` or `--buffer` (optional argument): Safety buffer distance (default: 5.0).
    - `--no-plot` (optional flag): Suppresses the mission visualization plot.
  - **Execution:**
    1.  Prints information about the provided file, buffer, and plotting status.
    2.  Calls `check_mission_conflicts` with the parsed arguments.
    3.  Prints the final status ("Clear" or "Conflict Detected").
    4.  If conflicts were detected, prints each conflict detail.
- **How it Works:** Provides a way to run the deconfliction analysis without a GUI, suitable for scripting or automated checks. It neatly ties together the functionality from `utils`, `conflict_checks`, and `visualization`.
- **Example CLI Usage:**

  ```bash
  # Check scenario_conflict_st.json with default buffer (5.0) and show plot
  python -m src.deconfliction_system data/scenario_conflict_st.json

  # Check scenario_clear.json with buffer 10 and no plot
  python -m src.deconfliction_system data/scenario_clear.json -b 10 --no-plot
  ```

  (Note: `python -m src.deconfliction_system` is used to run it as a module from the `flytbase/` directory, ensuring relative imports within the `src` package work correctly.)

### `src/gui.py`

- **Purpose:** Implements the GUI using PySimpleGUI. It now handles 3D waypoint inputs (`x,y,z`) and triggers the display of 2D, static 3D, and animated 3D visualizations.
- **Key UI Elements & Layout (Updated for 3D):**

  - Input fields for Primary Drone Mission: Waypoints now prompt for `x1,y1,z1;x2,y2,z2;...`.
  - Input fields for Simulated Drone Mission: Waypoints also prompt for `x,y,z`.
  - Other elements (Slider, Buttons, Display areas) remain similar in function but operate on 3D data where applicable.

- **Key Functions (Updated for 3D):**

  - **`convert_waypoints_to_text(waypoints: List[Dict[str, float]]) -> str`:**
    - **Logic:** Now converts waypoint dictionaries (which may contain `x,y,z`) to strings like `"x,y,z"`. Defaults `z` to `0.0` if not present in a dictionary for display.

  - **`parse_waypoints_text(waypoints_text: str) -> List[Dict[str, float]]`:**
    - **Logic:** Parses waypoint strings like `x1,y1,z1;x2,y2,z2;...` into a list of dictionaries `[{'x': ..., 'y': ..., 'z': ...}, ...]`.
    - **Fallback for 2D input:** If only `x,y` are provided for a waypoint (e.g., `x1,y1`), it defaults `z` to `0.0` for that waypoint and shows a `sg.popup_warn` to the user.

  - **`create_json_from_inputs(values: Dict[str, Any]) -> Optional[Dict[str, Any]]`:**
    - **Logic:** Constructs the mission data dictionary from GUI inputs. Now includes `z` coordinates in the waypoint dictionaries it creates, based on the output of `parse_waypoints_text`.

  - **`display_results(window, status: str, details: List[str], primary_mission: DroneMission, simulated_missions: List[DroneMission], safety_buffer: float)`:**
    - **Logic:** (Structure similar)
      - Calls `visualization.plot_missions(...)` which will now generate and show all three types of plots (2D, 3D static, 3D animated) in separate Matplotlib windows.

  - **`main_window()`:**
    - **Logic:** (Event loop structure similar)
      - **`'-CHECK_INPUTS-'` and `'-LOAD_FILE-'` events:** Now pass 3D-aware data (from GUI inputs or loaded files) to `deconfliction_system.check_mission_conflicts`. The subsequent call to `display_results` leads to 3D and animated visualizations.

- **How it Works:** Provides an interactive way to define/load missions and see results. It leverages the core logic from `deconfliction_system.py` (which in turn uses `utils.py`, `conflict_checks.py`, and `visualization.py`). The GUI acts as a frontend to this existing backend logic.
- **Naming Conventions:**
  - PySimpleGUI element keys are typically uppercase strings enclosed in hyphens (e.g., `'-PRIMARY_WAYPOINTS-'`).
  - Event names match button keys.
  - Functions follow standard Python naming.
- **Test Case (Manual):**
  1.  Run `python app.py`.
  2.  Leave default values. Click "Check from Inputs".
      - Expected: Status "Conflict Detected" (based on default values in `missions.json` which often model a conflict). Details will list the conflict. A plot window will appear showing the paths and highlighted conflict.
  3.  Change primary waypoints to `0,0,10;10,0,10`, start `900`, end `905`.
  4.  Change simulated waypoints to `0,50,5;10,50,5`, timestamps `900;905`.
  5.  Click "Check from Inputs".
      - Expected: Status "CLEAR". No conflict details. Plot shows two parallel, non-conflicting paths.
  6.  Click "Load Mission File", select `data/scenario_clear.json`.
      - Expected: Status "CLEAR". Plot shows the missions from the file.

### Data Files (`data/*.json`)

These files provide various predefined mission scenarios for testing the deconfliction system. They all follow the same JSON structure as `missions.json`.

- **`data/scenario_clear.json`**

  - **Purpose:** Defines a scenario where the primary mission and simulated missions are spatially and temporally separated, resulting in no conflicts.
  - **Example Content:** Primary drone flies east. One sim drone flies parallel but far north. Another sim drone flies in a similar area but much later.
  - **Expected Outcome:** "Clear" status.

- **`data/scenario_conflict_buffer.json`**

  - **Purpose:** Defines a scenario where drone paths do not intersect but come closer than a typical safety buffer, resulting in a conflict due to buffer breach.
  - **Example Content:** Primary drone flies east along y=0. Sim drone flies north, passing close to the primary path (e.g., at x=50, its path is y=2 to y=20) during an overlapping time window. If buffer is e.g. 5 units, this is a conflict.
  - **Expected Outcome:** "Conflict Detected" (due to buffer).

- **`data/scenario_conflict_spatial_only.json`**

  - **Purpose:** Defines a scenario where drone paths intersect spatially, but their time intervals on those intersecting segments do _not_ overlap.
  - **Example Content:** Primary drone path A to B from T1 to T2. Sim drone path C to D from T3 to T4. Paths A-B and C-D cross. However, the time interval [T1, T2] does not overlap with [T3, T4].
  - **Expected Outcome:** "Clear" status (because although paths cross, they don't do so at the same time).

- **`data/scenario_conflict_st.json`** (Spatio-Temporal)
  - **Purpose:** Defines a scenario with a clear spatio-temporal conflict: paths intersect or breach buffer, _and_ the time intervals overlap.
  - **Example Content:** Primary drone path A to B from T1 to T2. Sim drone path C to D from T3 to T4. Paths A-B and C-D cross _and_ the time interval [T1, T2] overlaps with [T3, T4].
  - **Expected Outcome:** "Conflict Detected".

### Documentation Files (`Docs/*`)

- **`Docs/Project.md`**

  - **Purpose:** Contains the detailed build plan, phased approach, technical stack recommendations, and checkpoints for the project development. It seems to be the guiding document for the project's implementation.
  - **Content:**
    - Recommended Python tech stack (Shapely, Matplotlib, PySimpleGUI).
    - Phased workflow (Phase 1: Core Logic, Phase 2: Visualization & Testing, Phase 3: GUI, Phase 4: Docs, Phase 5: Extra Credit 3D).
    - Detailed steps, actions, and objectives for each phase.
    - Checkpoints corresponding to deliverables (likely from an assignment specification).
    - Tips for the development sprint.
  - **How it Relates:** The implemented codebase largely follows the plan outlined in this document, covering Phases 1, 2, and 3. The file structure, choice of libraries, and core functionalities align with its descriptions.

- **`Docs/Assignment.pdf`**
  - **Purpose:** This is likely the original assignment specification or problem statement document that `Docs/Project.md` is based on.
  - **Content:** (Cannot be read by the AI) Typically would contain:
    - Problem description.
    - Requirements and constraints.
    - Deliverables.
    - Evaluation criteria.
  - **How it Relates:** The entire project is an answer to the tasks set out in this document. Understanding this PDF would provide the ultimate context for why certain features were prioritized or implemented in specific ways. For a full understanding of project origins and constraints, this document would need manual review.

---

## 3. Core Concepts and Logic

### Time Handling

- **Input Format:** Time is consistently taken as input in **HHMM integer format** (e.g., `800` for 08:00, `1430` for 14:30). This applies to `start_time`, `end_time` in primary missions, and `timestamp` for waypoints in simulated missions in the JSON files and GUI.
- **Internal Representation:** Internally, all HHMM times are converted to **minutes since midnight** (an integer from 0 to 1439). This is done by the `_parse_hhmm_to_minutes` function in `src/utils.py`.
  - Example: `800` (08:00) becomes `8 * 60 + 0 = 480` minutes.
  - Example: `1430` (14:30) becomes `14 * 60 + 30 = 870` minutes.
- **Primary Mission Timestamp Calculation:**
  - For the primary drone, only an overall `start_time` and `end_time` are given for its entire multi-waypoint path.
  - The `load_missions_from_json` function in `src/utils.py` calculates the timestamp for each individual waypoint of the primary mission.
  - It assumes the primary drone travels at a **constant speed** throughout its mission.
  - The logic is:
    1.  Calculate total mission duration in minutes.
    2.  Calculate the total Euclidean distance of the path by summing segment lengths.
    3.  Speed = Total Distance / Total Duration.
    4.  The first waypoint's timestamp is the mission `start_time` (in minutes).
    5.  For each subsequent segment, time_for_segment = segment_distance / speed.
    6.  The next waypoint's timestamp = previous waypoint's timestamp + time_for_segment.
    7.  Timestamps are rounded, and the final waypoint's timestamp is adjusted to match the mission `end_time` precisely to avoid accumulated floating-point errors.
- **Simulated Mission Timestamps:**
  - Simulated drones have an explicit HHMM `timestamp` provided for _each_ waypoint in the input JSON. These are directly converted to minutes since midnight.

### Spatial Checks (now 3D)

Spatial checks are now performed in 3D and **no longer use the Shapely library** for segment-to-segment conflict detection. The logic resides in `check_segment_spatial_conflict` within `src/conflict_checks.py`.

1.  **Custom 3D Proximity Check:** For any two path segments (one from primary, one from a simulated drone):
    - The system uses a simplified 3D proximity check based on calculating the minimum distance from each endpoint of one segment to the entirety of the other segment. This is done using the `distance_point_to_segment_3d` helper function.
    - If any of these four endpoint-to-segment distances (endpoint A1 to segment B, endpoint A2 to segment B, endpoint B1 to segment A, endpoint B2 to segment A) is less than the `safety_buffer`, a spatial conflict is flagged.
    - This is an approximation and does not calculate the true minimum distance between the two 3D line segments in all geometric configurations but serves as a practical measure for buffer breach detection.

### Temporal Checks

If a 3D spatial conflict is detected between two segments, a temporal check is performed by `check_spatio_temporal_segment_conflict`:

1.  **Time Intervals:** For each of the two spatially conflicting segments, the time interval during which the respective drone traverses that segment is determined.
    - `segmentA_interval = [waypoint_A1.timestamp_minutes, waypoint_A2.timestamp_minutes]`
    - `segmentB_interval = [waypoint_B1.timestamp_minutes, waypoint_B2.timestamp_minutes]`
      (Timestamps are already in minutes since midnight).
2.  **Overlap Check:** The function checks if these two time intervals overlap. Two intervals `[s1, e1]` and `[s2, e2]` overlap if `s1 <= e2` AND `s2 <= e1`.

### Spatio-Temporal Conflict (now 3D)

A spatio-temporal conflict between two path segments is declared **if and only if**:

1.  The segments are in **3D spatial conflict** (based on the custom proximity check described above being less than the `safety_buffer`).
    AND
2.  Their **time intervals overlap**.

This is handled by `check_spatio_temporal_segment_conflict`, which now calls the 3D version of `check_segment_spatial_conflict`.

### Safety Buffer (applied in 3D)

- **Concept:** A configurable minimum 3D distance that must be maintained.
- **Implementation:** Used in the custom 3D `check_segment_spatial_conflict`.

### Waypoint Collision (now 3D)

- **Concept:** Two drones are at the _exact same 3D coordinates at the exact same time_.
- **Implementation:** Handled by `check_waypoint_collision` in `src/conflict_checks.py`.
  1.  Checks `timestamp_minutes`.
  2.  Checks equality (within `FLOAT_TOLERANCE`) for `x`, `y`, AND `z` coordinates.

### 3D Coordinates and Operations (New Section)

- **Waypoint Data:** The `Waypoint` model in `src/models.py` now includes a `z: float` attribute for altitude.
- **JSON Input:** Mission files (e.g., `missions.json`) are expected to provide `x`, `y`, `z` for each waypoint for 3D operations. `src/utils.py` enforces this when loading.
- **GUI Input:** The GUI in `src/gui.py` has been updated to accept `x,y,z` string for waypoints (e.g., "0,0,10;100,0,10"). It includes a fallback where if only `x,y` are entered, `z` defaults to `0.0` with a user warning.
- **Distance Calculation:** `src/utils._calculate_distance` now computes 3D Euclidean distance.
- **Conflict Checks:** As detailed above, `check_segment_spatial_conflict` and `check_waypoint_collision` in `src/conflict_checks.py` operate in 3D.
- **Visualization:** `src/visualization.py` now generates static 3D plots showing paths in X-Y-Z space.

### 4D Visualization (3D Animation) (New Section)

- **Concept:** To represent the fourth dimension (time) in conjunction with 3D spatial data, the system provides an animated 3D plot.
- **Implementation (`src/visualization.py`):**
  - A new function `plot_animated_3d_missions` is responsible for this.
  - It uses `matplotlib.animation.FuncAnimation`.
  - **Interpolation:** A helper function `_interpolate_position_3d` calculates the (x,y,z) position of a drone at any given `time_minutes` along its path by linear interpolation between its defined waypoints.
  - **Animation Setup:**
    - A 3D plot is created, and the static 3D paths of all drones are drawn as a background.
    - Markers (e.g., `ax.scatter`) are created for each drone to represent their current positions.
    - A text field is added to display the current animation time.
  - **Update Function:** For each frame of the animation:
    - The current simulation time is calculated.
    - The on-screen time display is updated.
    - The 3D position of each drone marker is updated using the interpolated position for the current time.
  - **Display:** The animation is shown in a new Matplotlib window. A global list `Held_animations` is used to keep animation objects in memory so they don't get garbage collected prematurely.

---

## 4. Naming Conventions

### File Naming

- Python modules: `snake_case.py` (e.g., `conflict_checks.py`, `utils.py`).
- Main application script: `app.py` (common convention).
- Data files: `snake_case.json` or descriptive names (e.g., `missions.json`, `scenario_clear.json`).
- Documentation: `CamelCase.md` or `snake_case.md` (e.g., `Project.md`, `README.md`).
- Special Python files: `__init__.py`, `.gitignore` (standard names).

### Function and Variable Naming

- **Functions:** `snake_case` (e.g., `load_missions_from_json`, `check_segment_spatial_conflict`).
  - Internal/helper functions are sometimes prefixed with an underscore: `_parse_hhmm_to_minutes`.
- **Variables:** `snake_case` (e.g., `primary_mission`, `safety_buffer`, `conflict_details`).
- **Class Names:** `CamelCase` (e.g., `DroneMission`, `Waypoint`).
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `PRIMARY_COLOR`, `FLOAT_TOLERANCE`).
- **Clarity:** Names are generally descriptive of their purpose or the data they hold.
  - `timestamp_minutes`: Explicitly states the unit and reference point.
  - `p_segment`, `s_wp`: Prefixes `p_` for primary and `s_` for simulated are used in `find_conflicts` for local variables to distinguish between entities from the primary and simulated missions during comparisons.
  - GUI element keys in PySimpleGUI: `'-KEY_NAME-'` (e.g., `'-PRIMARY_WAYPOINTS-'`).

### Drone IDs

- **Format:** Strings (e.g., `"primary_01"`, `"sim_A"`, `"P_Clear"`, `"S_CloseCall"`).
- **Convention:**
  - Often start with `"primary_"` or `"P_"` for the primary drone.
  - Often start with `"sim_"` or `"S_"` for simulated drones.
  - The rest of the ID can be descriptive of the drone or its scenario role (e.g., `"sim_A_conflict"`, `"S_Far"`).
- **Uniqueness:** Assumed to be unique within a given mission scenario loaded from a JSON file, as they are used to identify drones in conflict reports and visualization labels. The system doesn't enforce global uniqueness across different files but relies on context within a single check.

---

## 5. Example Test Cases and Scenarios

The `data/` directory contains several JSON files. For 3D testing, these would need to be updated or new ones created with `z` coordinates. The `missions.json` in the root directory has been updated to include `z` values.

- **`missions.json` (Example with 3D data):**
  - **Description:** Primary drone Alpha_3D flies from (0,0,10) -> (100,0,10) -> (100,100,15) between 08:00 and 08:20. Simulated drone Bravo_3D flies (0,50,5) -> (100,50,5) between 08:05 and 08:15.
  - **Expected (Conceptual for 3D):** Conflict status will depend on the safety buffer and the 3D proximity of these paths during their overlapping time window [08:05, 08:15]. For instance, even if X-Y paths are parallel, a Z difference might clear them, or a small Z difference might still cause a buffer breach.
  - **To Run (CLI):** `python -m src.deconfliction_system missions.json -b 5` (This will use the 3D data in `missions.json`)

- **Waypoint Collision Test (3D):**
  - **Primary Mission:** Waypoints `0,0,10; 10,0,10`, Start Time `1000`, End Time `1002`.
    - (0,0,10) at 10:00 (600 min)
    - (5,0,10) at 10:01 (601 min)
    - (10,0,10) at 10:02 (602 min)
  - **Simulated Mission:** Waypoints `5,0,10`, Timestamps `1001`.
  - **Expected:** "Conflict Detected" with a "Waypoint Collision" detail for `(5,0,10)` at minute `601`.

This comprehensive explanation should provide a solid understanding of the Drone Deconfliction System, including its 3D and 4D enhancements.

---

## 6. Installation

To set up and run the Drone Deconfliction System, follow these steps:

### Prerequisites
- Python 3.7 or higher.
- `pip` for installing packages.
- `git` for cloning the repository.

### Setup Steps

1.  **Clone the Repository:**
    Open your terminal or command prompt and run:
    ```bash
    git clone https://github.com/dan10ish/flytbase.git
    cd flytbase
    ```
    *If the project is already cloned and you are in the `flytbase` directory, you can skip this step and proceed to activate virtual environment or install dependencies if not already done.*

2.  **Navigate to Project Directory:**
    Ensure you are in the project's root directory (e.g., `flytbase/`).

3.  **Create and Activate a Virtual Environment (Recommended):**
    It's good practice to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    Your terminal prompt should now indicate that you are in the `(venv)` environment.

4.  **Install Dependencies:**
    Install all the required Python packages listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    This will install libraries such as `matplotlib` and `PySimpleGUI`.

---

## 7. Running the Program

The Drone Deconfliction System can be run in two ways: through a Graphical User Interface (GUI) or a Command-Line Interface (CLI). Ensure you have completed the [Installation](#installation) steps and activated your virtual environment if you created one.

### Running the GUI Application

The GUI provides an interactive way to load mission files, input primary drone parameters, trigger conflict checks, and visualize drone paths in 2D, static 3D, and animated 3D (4D).

1.  **Navigate to the project's root directory** (e.g., `flytbase/`) in your terminal.
2.  **Run the application:**
    ```bash
    python app.py
    ```
    This will launch the main application window.

### Running the Command-Line Interface (CLI)

The CLI is useful for batch processing or integrating the deconfliction logic into scripts. It allows you to specify mission files and parameters directly via command arguments.

1.  **Navigate to the project's root directory** (e.g., `flytbase/`) in your terminal.
2.  **Execute the deconfliction system script:**
    The main CLI script is `src/deconfliction_system.py`. You can run it as a module:
    ```bash
    python -m src.deconfliction_system -f <path_to_mission_file.json> -b <buffer_meters> [options]
    ```

    **Key Arguments:**
    -   `-f FILE`, `--file FILE`: **(Required)** Path to the mission JSON file (e.g., `data/missions.json`, `data/scenario_conflict_st.json`).
    -   `-b BUFFER`, `--buffer BUFFER`: **(Required)** Safety buffer radius in meters (e.g., `5` for a 5-meter buffer).
    -   `-v`, `--visualize`: (Optional) Show a 2D plot (X-Y projection) of the drone paths and conflicts.
    -   `-v3d`, `--visualize3d`: (Optional) Show a static 3D plot (X-Y-Z) of the drone paths.
    -   `-a`, `--animate`: (Optional) Show a 4D animated visualization (3D paths over time). This is the most comprehensive visualization.
    -   `-s SPEED`, `--speed SPEED`: (Optional) Specify the speed of the primary drone in meters per second. If provided, this may alter how `start_time` and `end_time` from the primary mission are used. Typically, if speed is given, the system might calculate duration, or vice-versa. The system calculates primary drone speed based on total path length and the duration specified by `start_time` and `end_time` in its mission definition if speed is not given.

    **Example Usages:**
    -   Check for conflicts in `data/scenario_conflict_st.json` with a 10-meter buffer and show the 4D animation:
        ```bash
        python -m src.deconfliction_system -f data/scenario_conflict_st.json -b 10 -a
        ```
    -   Check for conflicts in `missions.json` with a 5-meter buffer and show the static 3D plot:
        ```bash
        python -m src.deconfliction_system -f missions.json -b 5 -v3d
        ```
    The CLI will print conflict reports to the console.

---

## 8. How to Create the Mission JSON File

The drone missions are defined in a JSON file. This file structure is crucial for the system to correctly interpret the primary and simulated drone flight plans. All coordinates are expected in 3D (x, y, z).

### General Structure

The JSON file should contain a single root object with two main keys:
-   `"primary_mission"`: An object defining the primary drone's flight plan.
-   `"simulated_missions"`: A list of objects, each defining a simulated drone's flight plan.

### `primary_mission` Object

Defines the mission for the main drone whose path is being checked for conflicts.

-   **`drone_id` (String):** A unique identifier for the primary drone (e.g., `"Alpha_Prime_3D"`).
-   **`waypoints` (List of Objects):** An ordered list of waypoints the drone will visit. Each waypoint object must contain:
    -   `"x"` (Number): The x-coordinate of the waypoint in meters.
    -   `"y"` (Number): The y-coordinate of the waypoint in meters.
    -   `"z"` (Number): The z-coordinate (altitude) of the waypoint in meters.
-   **`start_time` (Integer):** The scheduled start time of the primary drone's mission in HHMM format (e.g., `800` for 08:00, `1345` for 13:45).
-   **`end_time` (Integer):** The scheduled end time of the primary drone's mission in HHMM format.
-   **Note on Timestamps:** For the primary mission, individual waypoint timestamps are *not* specified in the input JSON. The system calculates them automatically by distributing the total mission duration (`end_time` - `start_time`) proportionally across the path segments based on their 3D lengths, assuming a constant speed.

### `simulated_missions` List

An array of mission objects, each representing a drone whose flight path is simulated and checked against the primary mission.

Each object in the list has:
-   **`drone_id` (String):** A unique identifier for the simulated drone (e.g., `"Sim_Echo_3D"`).
-   **`waypoints` (List of Objects):** An ordered list of waypoints. Each waypoint object must contain:
    -   `"x"` (Number): The x-coordinate in meters.
    -   `"y"` (Number): The y-coordinate in meters.
    -   `"z"` (Number): The z-coordinate (altitude) in meters.
    -   `"timestamp"` (Integer): The specific time the drone is scheduled to be at this waypoint, in HHMM format. Timestamps for simulated drone waypoints must be explicit and monotonically increasing.

### Example `missions.json` content:

```json
{
  "primary_mission": {
    "drone_id": "SkyGuardian_01",
    "waypoints": [
      { "x": 0, "y": 0, "z": 50 },
      { "x": 500, "y": 0, "z": 60 },
      { "x": 500, "y": 500, "z": 50 },
      { "x": 0, "y": 500, "z": 60 }
    ],
    "start_time": 1000,
    "end_time": 1015
  },
  "simulated_missions": [
    {
      "drone_id": "Pathfinder_A",
      "waypoints": [
        { "x": 10, "y": 250, "z": 55, "timestamp": 1002 },
        { "x": 600, "y": 250, "z": 55, "timestamp": 1010 }
      ]
    },
    {
      "drone_id": "Observer_B",
      "waypoints": [
        { "x": 250, "y": 10, "z": 40, "timestamp": 958 },
        { "x": 250, "y": 600, "z": 70, "timestamp": 1008 }
      ]
    }
  ]
}
```

### Data Validation Notes:
- Ensure all coordinates (`x`, `y`, `z`) are numerical values.
- Time values (`start_time`, `end_time`, `timestamp`) must be integers in HHMM format (e.g., 0 to 2359).
- For simulated missions, waypoints should be chronologically ordered by their timestamps.
- The system strictly expects `x`, `y`, and `z` keys for all waypoints.

---

## 9. Detailed Scenario Walkthroughs

This section provides examples of different mission configurations to illustrate how the deconfliction system identifies various types of potential issues. You can create JSON files with these examples and run them through the system (either GUI or CLI) to observe the behavior and output. The safety buffer for these examples can be set (e.g., to 5 or 10 meters) when running the check.

### Scenario 1: Clear Path

**Description:** The primary drone and simulated drones operate in the same airspace but their paths and timing are such that no conflicts occur, even considering the safety buffer.

**`clear_path_scenario.json`:**
```json
{
  "primary_mission": {
    "drone_id": "Primary_Clear",
    "waypoints": [
      { "x": 0, "y": 0, "z": 20 },
      { "x": 100, "y": 0, "z": 20 }
    ],
    "start_time": 1400,
    "end_time": 1402
  },
  "simulated_missions": [
    {
      "drone_id": "Sim_FarAway",
      "waypoints": [
        { "x": 0, "y": 100, "z": 30, "timestamp": 1400 },
        { "x": 100, "y": 100, "z": 30, "timestamp": 1402 }
      ]
    },
    {
      "drone_id": "Sim_DifferentTime",
      "waypoints": [
        { "x": 0, "y": 0, "z": 20, "timestamp": 1500 },
        { "x": 100, "y": 0, "z": 20, "timestamp": 1502 }
      ]
    }
  ]
}
```
**Expected Output:** "No conflicts detected." Visualizations will show separate flight paths or paths executed at distinctly different times.

### Scenario 2: Spatio-Temporal Conflict (Path Proximity)

**Description:** The primary drone's path and a simulated drone's path come within the defined safety buffer of each other during overlapping time intervals.

**`st_conflict_proximity_scenario.json`:**
```json
{
  "primary_mission": {
    "drone_id": "Primary_Risk",
    "waypoints": [
      { "x": 0, "y": 0, "z": 10 },
      { "x": 200, "y": 0, "z": 10 }
    ],
    "start_time": 1100,
    "end_time": 1102
  },
  "simulated_missions": [
    {
      "drone_id": "Sim_CloseCall",
      "waypoints": [
        { "x": 0, "y": 8, "z": 12, "timestamp": 1100 },
        { "x": 200, "y": 8, "z": 12, "timestamp": 1102 }
      ]
    }
  ]
}
```
**To Trigger Conflict (Example):** Run with a safety buffer of `-b 10` (10 meters). The 3D distance between paths is ~8.24m. If buffer is 10m, this is a conflict.
**Expected Output:** A conflict report detailing `Primary_Risk` and `Sim_CloseCall`, the conflicting segments, and the time window of the conflict.

### Scenario 3: Exact Waypoint Collision (Spatio-Temporal)

**Description:** A waypoint of the primary drone and a waypoint of a simulated drone are at the exact same 3D coordinates and occur at the exact same calculated time.

**`waypoint_collision_scenario.json`:**
```json
{
  "primary_mission": {
    "drone_id": "Primary_Precise",
    "waypoints": [
      { "x": 0, "y": 0, "z": 25 },
      { "x": 100, "y": 100, "z": 25 },
      { "x": 200, "y": 200, "z": 25 }
    ],
    "start_time": 1600,
    "end_time": 1604
  },
  "simulated_missions": [
    {
      "drone_id": "Sim_Interceptor",
      "waypoints": [
        { "x": 0, "y": 200, "z": 25, "timestamp": 1600 },
        // Primary reaches (100,100,25) approx. at 1602 (midpoint of 4 min journey)
        { "x": 100, "y": 100, "z": 25, "timestamp": 1602 },
        { "x": 200, "y": 0, "z": 25, "timestamp": 1604 }
      ]
    }
  ]
}
```
**Expected Output:** A conflict report specifically highlighting a "Waypoint Collision" between `Primary_Precise` and `Sim_Interceptor` at `(100,100,25)` at time `1602`.

### Scenario 4: Spatial-Only Conflict (Different Times)

**Description:** The drones' paths intersect or come very close in 3D space, but they pass through these points at significantly different times.

**`spatial_only_scenario.json`:**
```json
{
  "primary_mission": {
    "drone_id": "Primary_EarlyBird",
    "waypoints": [
      { "x": 0, "y": 50, "z": 15 },
      { "x": 100, "y": 50, "z": 15 }
    ],
    "start_time": 900,
    "end_time": 902
  },
  "simulated_missions": [
    {
      "drone_id": "Sim_LateFlyer",
      "waypoints": [
        { "x": 50, "y": 0, "z": 15, "timestamp": 930 },
        { "x": 50, "y": 100, "z": 15, "timestamp": 932 }
      ]
    }
  ]
}
```
**Expected Output:** "No conflicts detected." Visualizations might show crossing paths, but time separation prevents conflict alerts.

### Scenario 5: Conflict Due to Safety Buffer (Paths Don't Touch)

**Description:** The actual flight paths do not intersect, but their safety zones (buffers) overlap in space and time.

**`buffer_only_conflict_scenario.json`:**
```json
{
  "primary_mission": {
    "drone_id": "Primary_WideBody",
    "waypoints": [
      { "x": 0, "y": 0, "z": 10 },
      { "x": 100, "y": 0, "z": 10 }
    ],
    "start_time": 1000,
    "end_time": 1002
  },
  "simulated_missions": [
    {
      "drone_id": "Sim_NearPass",
      "waypoints": [
        { "x": 0, "y": 15, "z": 10, "timestamp": 1000 }, // Paths 15m apart
        { "x": 100, "y": 15, "z": 10, "timestamp": 1002 }
      ]
    }
  ]
}
```
**To Trigger Conflict (Example):** Run with a safety buffer of `-b 20` (20 meters).
**Expected Output:** A conflict report indicating proximity due to the safety buffer.
---

These scenarios should help in understanding the system's capabilities and for testing its responses to various mission profiles. Remember to adjust coordinates, times, and safety buffer settings to explore further. 