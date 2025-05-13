# Drone Deconfliction System: Comprehensive Explanation

This document provides a detailed explanation of the Drone Deconfliction System project, covering every file, its purpose, the functions within it, their logic, naming conventions, and illustrative examples.

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
4.  [Naming Conventions](#naming-conventions)
    - [File Naming](#file-naming)
    - [Function and Variable Naming](#function-and-variable-naming)
    - [Drone IDs](#drone-ids)
5.  [Example Test Cases and Scenarios](#example-test-cases-and-scenarios)

---

## 1. Project Overview

The Drone Deconfliction System is a Python application designed to detect and report potential spatio-temporal conflicts between a primary drone's mission and one or more simulated drone flights. It operates in a 2D environment and considers both spatial proximity (including a safety buffer) and temporal overlaps.

The system can be run via a command-line interface (CLI) or a graphical user interface (GUI). It loads mission data from JSON files, performs conflict analysis, and can visualize the drone paths and any detected conflicts using Matplotlib.

**Key Functionalities:**

- Loading mission data from JSON files.
- Calculating timestamps for the primary drone's path based on constant speed.
- Checking for spatial conflicts (path intersections or buffer breaches) using the Shapely library.
- Checking for temporal overlaps between drones on potentially conflicting path segments.
- Identifying exact waypoint collisions (same location, same time).
- Providing detailed conflict reports.
- Visualizing missions and conflicts.
- Offering a GUI for easier interaction and mission input.

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
│   ├── conflict_checks.py    # Core spatio-temporal conflict logic
│   ├── deconfliction_system.py # Main execution script and CLI for core logic
│   ├── gui.py                  # GUI implementation using PySimpleGUI
│   ├── models.py               # Data models (Waypoint, DroneMission)
│   ├── utils.py                # Utility functions (JSON loading, time conversion)
│   └── visualization.py        # Mission plotting using Matplotlib
├── .gitignore                # Specifies intentionally untracked files that Git should ignore
├── app.py                    # Main GUI application entry point
├── Explained.md              # This file: Detailed explanation of the project
├── missions.json             # Default/example mission file
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

- **Purpose:** This is the main entry point for launching the Graphical User Interface (GUI) of the Drone Deconfliction System.
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
  - Calling `main_window()` initializes and displays the GUI.
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
  shapely>=1.7 # Or specify a compatible version
  matplotlib>=3.0 # For visualization
  PySimpleGUI>=4.60.0 # For GUI implementation
  ```
- **Logic:**
  - `shapely`: Used for advanced 2D geometric operations (line intersections, distances).
  - `matplotlib`: Used for plotting drone paths and conflicts.
  - `PySimpleGUI`: Used to create the graphical user interface.
  - The `>=` specifies the minimum version required, ensuring compatibility.
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

- **Purpose:** An example JSON file that defines a set of drone missions, including one primary mission and several simulated missions. This file is used by default by the CLI if no other file is specified, and can be loaded via the GUI.
- **Content Snippet:**
  ```json
  {
    "primary_mission": {
      "drone_id": "primary_01",
      "waypoints": [
        { "x": 0, "y": 0 },
        { "x": 100, "y": 0 },
        { "x": 100, "y": 100 }
      ],
      "start_time": 800,
      "end_time": 810
    },
    "simulated_missions": [
      {
        "drone_id": "sim_A_conflict",
        "waypoints": [
          { "x": 50, "y": -10, "timestamp": 803 },
          { "x": 50, "y": 10, "timestamp": 806 }
        ]
      }
      // ... more simulated missions
    ]
  }
  ```
- **Logic:**
  - `primary_mission`:
    - `drone_id`: A unique identifier for the primary drone.
    - `waypoints`: A list of `{"x": x_coord, "y": y_coord}` dictionaries. Timestamps are _not_ provided here; they are calculated based on `start_time` and `end_time`.
    - `start_time`: The overall mission start time in HHMM format (e.g., `800` for 08:00).
    - `end_time`: The overall mission end time in HHMM format (e.g., `810` for 08:10).
  - `simulated_missions`: A list of mission objects for simulated drones.
    - `drone_id`: A unique identifier for the simulated drone.
    - `waypoints`: A list of `{"x": x_coord, "y": y_coord, "timestamp": hhmm_time}` dictionaries. Each waypoint has an explicit timestamp in HHMM format.
- **How it Works:** This file is read by `src.utils.load_missions_from_json()` to create `DroneMission` objects.
- **Naming Conventions:** `missions.json` clearly indicates its purpose. Drone IDs like "primary_01", "sim_A_conflict" are descriptive.

### `src/__init__.py`

- **Purpose:** This empty file tells Python that the `src` directory should be treated as a package. This allows for relative imports between modules within the `src` directory.
- **Content:** It is typically empty.
- **How it Works:** When Python encounters an `__init__.py` file in a directory, it recognizes that directory as a package, enabling structured organization of modules. For example, `from .models import Waypoint` works because `src` is a package.
- **Naming Conventions:** `__init__.py` is a special, required name for this purpose.

### `src/models.py`

- **Purpose:** Defines the core data structures (data classes) used throughout the application to represent waypoints and drone missions.
- **Content:**

  - `Waypoint` data class:
    - `x: float`: The x-coordinate of the waypoint.
    - `y: float`: The y-coordinate of the waypoint.
    - `timestamp_minutes: int`: The time at which the drone is at this waypoint, represented as minutes since midnight (0-1439).
  - `DroneMission` data class:
    - `drone_id: str`: A unique identifier for the drone.
    - `waypoints: List[Waypoint]`: A list of `Waypoint` objects defining the drone's path and timing.
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

- **Purpose:** Contains utility functions used across different parts of the project, primarily for data loading, parsing, and time/distance calculations.
- **Key Functions:**

  - **`_parse_hhmm_to_minutes(hhmm: int) -> int`:**

    - **Logic:** Converts an integer time in HHMM format (e.g., `800` for 08:00, `1430` for 14:30) into total minutes since midnight (0-1439).
    - **Input:** `hhmm` (integer between 0 and 2359).
    - **Output:** Total minutes (integer).
    - **Error Handling:** Raises `ValueError` for invalid HHMM format or values (e.g., `2500`, `870`).
    - **Example:** `_parse_hhmm_to_minutes(800)` returns `480`. `_parse_hhmm_to_minutes(1430)` returns `870`.

  - **`_calculate_distance(p1: Dict[str, float], p2: Dict[str, float]) -> float`:**

    - **Logic:** Calculates the Euclidean distance between two 2D points. Points are expected as dictionaries `{'x': float, 'y': float}`.
    - **Input:** `p1`, `p2` (dictionaries).
    - **Output:** Distance (float).
    - **Error Handling:** Raises `ValueError` if points have missing keys or non-numeric coordinates.
    - **Example:** `_calculate_distance({'x': 0, 'y': 0}, {'x': 3, 'y': 4})` returns `5.0`.

  - **`load_missions_from_json(filepath: str) -> Tuple[DroneMission, List[DroneMission]]`:**
    - **Logic:** This is a crucial function for loading and processing mission data from a JSON file.
      1.  Reads the JSON file specified by `filepath`.
      2.  **Parses Simulated Missions:**
          - Iterates through each mission in the `"simulated_missions"` list.
          - For each waypoint, it parses the `x`, `y` coordinates and the `timestamp` (HHMM format) using `_parse_hhmm_to_minutes`.
          - Creates `Waypoint` objects and then a `DroneMission` object for each simulated drone.
          - Sorts waypoints by their `timestamp_minutes`.
      3.  **Parses Primary Mission:**
          - Retrieves data from the `"primary_mission"` object.
          - Parses `start_time` and `end_time` (HHMM) into minutes since midnight.
          - Validates that `start_time` is before `end_time`.
          - **Calculates Primary Drone Timestamps:** This is a key piece of logic.
            - If only one waypoint, its timestamp is `start_time_minutes`.
            - If multiple waypoints:
              - Calculates the total path distance by summing distances between consecutive waypoints using `_calculate_distance`.
              - Calculates the total mission duration (`end_time_minutes - start_time_minutes`).
              - If `total_distance` is 0 (all waypoints at the same spot), all waypoints get `start_time_minutes`.
              - Otherwise, calculates a constant `speed` (distance units per minute).
              - The first waypoint is assigned `start_time_minutes`.
              - For subsequent waypoints, it calculates the time taken to travel the segment (`segment_distance / speed`) and adds it to the previous waypoint's time.
              - Timestamps are rounded and clamped to ensure the last waypoint does not exceed `end_time_minutes`. The final waypoint's time is adjusted to be exactly `end_time_minutes` if the calculated value is very close (within 1 minute tolerance).
          - Creates `Waypoint` objects with these calculated timestamps and then the primary `DroneMission` object.
    - **Input:** `filepath` (string path to JSON).
    - **Output:** A tuple `(primary_mission_object, list_of_simulated_mission_objects)`.
    - **Error Handling:** Raises `FileNotFoundError`, `json.JSONDecodeError`, `ValueError` (for data format issues, invalid times), or `KeyError` (for missing JSON keys).
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
  - Primary mission: waypoints `(0,0), (100,0)`, start_time `800`, end_time `810`.
    - Total distance = 100. Total duration = 10 minutes. Speed = 10 units/min.
    - Waypoint 1 `(0,0)`: timestamp `480` (08:00).
    - Waypoint 2 `(100,0)`: time for segment = 100/10 = 10 mins. Timestamp = 480 + 10 = `490` (08:10).

### `src/conflict_checks.py`

- **Purpose:** Contains the core logic for detecting spatio-temporal conflicts between drone missions.
- **Key Constants:**

  - `FLOAT_TOLERANCE = 1e-9`: A small value used for comparing floating-point numbers to account for precision issues. For example, instead of `a == b`, use `abs(a - b) < FLOAT_TOLERANCE`.

- **Key Functions:**

  - **`_get_time_interval_for_segment(segment: Tuple[Waypoint, Waypoint]) -> Tuple[int, int]`:**

    - **Logic:** Extracts the start and end timestamps (in minutes since midnight) from the two `Waypoint` objects that define a path segment. Assumes waypoints in a segment are chronologically ordered.
    - **Input:** `segment` (a tuple of two `Waypoint` objects).
    - **Output:** A tuple `(start_minutes, end_minutes)`.

  - **`check_segment_spatial_conflict(segment1: Tuple[Waypoint, Waypoint], segment2: Tuple[Waypoint, Waypoint], safety_buffer: float) -> bool`:**

    - **Logic:** Uses the Shapely library to check for spatial conflicts between two path segments.
      1.  Converts each segment (defined by two `Waypoint` objects) into Shapely `LineString` objects. If a segment's start and end waypoints are identical, it's treated as a Shapely `Point`.
      2.  **Intersection Check:** Checks if `geom1.intersects(geom2)`. This returns `True` if the lines cross or touch (including endpoints).
      3.  **Buffer Check:** Calculates the minimum distance between the two geometries using `geom1.distance(geom2)`. If this distance is less than `safety_buffer` (minus `FLOAT_TOLERANCE` for robust comparison), a buffer breach is detected.
    - **Input:** `segment1`, `segment2`, `safety_buffer`.
    - **Output:** `True` if a spatial conflict (intersection or buffer breach) exists, `False` otherwise.
    - **Error Handling:** Includes a `try-except` block to catch errors from Shapely operations, printing a warning and returning `False` (assuming no conflict to prevent halting). In a production system, this might need more sophisticated logging or error handling.

  - **`check_spatio_temporal_segment_conflict(segment1: Tuple[Waypoint, Waypoint], segment2: Tuple[Waypoint, Waypoint], safety_buffer: float) -> bool`:**

    - **Logic:** Determines if a spatio-temporal conflict exists between two segments.
      1.  First, calls `check_segment_spatial_conflict`. If there's no spatial conflict, returns `False` immediately.
      2.  If there _is_ a spatial conflict, it retrieves the time intervals for each segment using `_get_time_interval_for_segment`.
      3.  Checks if these time intervals overlap. The condition for overlap is `(startA <= endB) and (startB <= endA)`.
    - **Input:** `segment1`, `segment2`, `safety_buffer`.
    - **Output:** `True` if both spatial conflict and temporal overlap exist, `False` otherwise.
    - **Example:**
      - SegA: (0,0)@T=0 to (10,0)@T=10. SegB: (5,-1)@T=4 to (5,1)@T=6. Buffer=0.5.
      - Spatial: Segments are close (`distance < 0.5`).
      - Temporal: Interval A [0, 10], Interval B [4, 6]. They overlap. -> Conflict.
      - SegC: (0,0)@T=0 to (10,0)@T=10. SegD: (5,-1)@T=12 to (5,1)@T=14. Buffer=0.5.
      - Spatial: Segments are close.
      - Temporal: Interval C [0, 10], Interval D [12, 14]. No overlap. -> No Conflict.

  - **`check_waypoint_collision(wp1: Waypoint, wp2: Waypoint) -> bool`:**

    - **Logic:** Checks if two waypoints represent the exact same location at the exact same time.
      1.  Compares `wp1.timestamp_minutes` and `wp2.timestamp_minutes`. If different, returns `False`.
      2.  Compares `x` coordinates and `y` coordinates using `abs(coord1 - coord2) < FLOAT_TOLERANCE`.
    - **Input:** `wp1`, `wp2` (two `Waypoint` objects).
    - **Output:** `True` if timestamps and coordinates (within tolerance) match, `False` otherwise.

  - **`find_conflicts(primary_mission: DroneMission, simulated_missions: List[DroneMission], safety_buffer: float) -> Tuple[bool, List[str]]`:**
    - **Logic:** This is the main orchestrator for conflict detection.
      1.  Retrieves path segments and waypoints for the primary mission.
      2.  Iterates through each `sim_mission` in `simulated_missions`.
      3.  For each `sim_mission`:
          - Retrieves its path segments and waypoints.
          - **Segment Conflicts:** Iterates through each `p_segment` of the primary mission and each `s_segment` of the simulated mission.
            - Calls `check_spatio_temporal_segment_conflict(p_segment, s_segment, safety_buffer)`.
            - If a conflict is found, sets `conflict_found = True` and appends a descriptive string to `conflict_details`.
          - **Waypoint Collisions:** Iterates through each `p_wp` (primary waypoint) and `s_wp` (simulated waypoint).
            - Calls `check_waypoint_collision(p_wp, s_wp)`.
            - If a collision is found, sets `conflict_found = True` and appends a descriptive string to `conflict_details`.
    - **Input:** `primary_mission` (DroneMission), `simulated_missions` (List of DroneMission), `safety_buffer` (float).
    - **Output:** A tuple `(conflict_found_boolean, list_of_conflict_description_strings)`.
    - **Naming Conventions:**
      - Function names are descriptive verbs (e.g., `check_...`, `find_...`).
      - Parameters like `segment1`, `wp1`, `safety_buffer` are clear.
      - Variables like `p_segment` (primary segment), `s_wp` (simulated waypoint) use prefixes for clarity.
      - `conflict_details` stores human-readable descriptions.

- **How it Works:** Systematically compares the primary mission against each simulated mission, checking for both types of conflicts (segment-based spatio-temporal and exact waypoint collisions).
- **Test Case (Conceptual for `find_conflicts`):**
  - **Scenario:** Primary drone flies (0,0)@08:00 -> (100,0)@08:10. Sim drone flies (50,-2)@08:03 -> (50,2)@08:07. Safety buffer = 5.
  - **Expected Output:** `find_conflicts` should identify a spatio-temporal conflict. The primary path is y=0 from t=08:00 to 08:10. The sim path crosses x=50 from y=-2 to y=2 between t=08:03 and t=08:07. The paths are spatially close (within buffer 5 around y=0 for the primary drone). The time intervals [08:00, 08:10] and [08:03, 08:07] overlap.

### `src/visualization.py`

- **Purpose:** Handles the generation of 2D plots to visualize drone mission paths and highlight any detected conflicts using Matplotlib.
- **Key Constants (Colors):**

  - `PRIMARY_COLOR = 'blue'`
  - `SIMULATED_COLOR = 'gray'` (though a colormap `plt.cm.viridis_r` is used for multiple sim drones)
  - `CONFLICT_COLOR = 'red'`
  - `BUFFER_COLOR = 'lightblue'` (defined but not explicitly used to draw buffer areas in the current implementation, buffer value is in the title).

- **Key Functions:**

  - **`_plot_path(ax, waypoints: List[Waypoint], color: str, label: str, linestyle: str = '-', marker: str = 'o', markersize: int = 5)`:**

    - **Logic:** A helper function to plot a single drone's path on a given Matplotlib `Axes` object (`ax`). Extracts x and y coordinates from the `waypoints` and uses `ax.plot()`.
    - **Input:** Matplotlib axes `ax`, list of `Waypoint` objects, color, label, linestyle, marker style, and marker size.
    - **Output:** None (modifies the `ax` object).

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

  - **`plot_missions(primary_mission: DroneMission, simulated_missions: List[DroneMission], safety_buffer: float, conflict_details: Optional[List[str]] = None)`:**
    - **Logic:**
      1.  Creates a new Matplotlib figure and axes (`fig, ax = plt.subplots(...)`). Sets up title, labels, grid, and aspect ratio (`ax.set_aspect('equal')` is important for correct visual representation of distances).
      2.  Plots the primary mission's path using `_plot_path` with `PRIMARY_COLOR`.
      3.  Plots each simulated mission's path using `_plot_path`, cycling through colors from `plt.cm.viridis_r` for visual distinction.
      4.  **Highlight Conflicts (if `conflict_details` is provided):**
          - Calls `_parse_conflict_details` to get structured conflict data.
          - Iterates through the parsed conflicting primary segments and waypoints, replotting them with `CONFLICT_COLOR` and thicker lines or larger markers.
          - Iterates through the parsed conflicting simulated drone segments and waypoints, also highlighting them in `CONFLICT_COLOR`.
          - Manages labels to avoid redundancy in the legend (e.g., "Conflict Zone" label appears only once per type).
      5.  **Legend:** Gathers all unique handles and labels from the plot and displays a legend using `ax.legend()`.
      6.  Displays the plot using `plt.show(block=False)`. `block=False` allows the plot to open in a new window without blocking the execution of the main program (especially important for the GUI).
    - **Input:** `primary_mission`, `simulated_missions`, `safety_buffer`, and optional `conflict_details`.
    - **Output:** None (displays a plot).
    - **Naming Conventions:**
      - `_plot_path`, `_parse_conflict_details` are helper functions.
      - `plot_missions` is the main public function of this module.
      - Variables are descriptive (e.g., `sim_colors`, `parsed_conflicts`).

- **How it Works:** Provides a visual representation of the mission scenario, making it easier to understand the paths and the nature of any detected conflicts. The conflict highlighting is driven by parsing the text descriptions, which is a practical approach for this system.
- **Test Case (Conceptual):**
  - Given a primary mission, a simulated mission that conflicts with it, and the corresponding `conflict_details` string.
  - `plot_missions` should display both paths, and the specific segment(s) or waypoint(s) mentioned in `conflict_details` should be drawn in red. The legend should correctly label the drones and conflict markers.

### `src/deconfliction_system.py`

- **Purpose:** This script serves as the main entry point for the command-line interface (CLI) of the deconfliction system. It orchestrates the loading of missions, conflict checking, and result display (including optional plotting).
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

- **Purpose:** Implements the graphical user interface (GUI) for the Drone Deconfliction System using the PySimpleGUI library. It allows users to input mission data manually, load missions from files, trigger conflict checks, and view results including visualizations.
- **Key UI Elements & Layout:**

  - Input fields for Primary Drone Mission (ID, Waypoints `x1,y1;x2,y2;...`, Start Time HHMM, End Time HHMM).
  - Input fields for a (single) Simulated Drone Mission (ID, Waypoints, Timestamps `HHMM;HHMM;...`).
  - Slider for adjusting the Safety Buffer.
  - Buttons: "Check from Inputs", "Load Mission File".
  - Display areas for Status ("Clear", "Conflict Detected") and detailed conflict messages.
  - The Matplotlib plot is shown in a separate, new window generated by `visualization.plot_missions`.

- **Key Functions:**

  - **`convert_waypoints_to_text(waypoints: List[Dict[str, float]]) -> str` (Not directly used in the final flow but good utility):**

    - **Logic:** Converts a list of waypoint dictionaries (e.g., `[{'x':0,'y':0}, {'x':10,'y':10}]`) into a semicolon-separated string (e.g., `"0,0;10,10"`).

  - **`parse_waypoints_text(waypoints_text: str) -> List[Dict[str, float]]`:**

    - **Logic:** Parses a string of waypoints (format: `x1,y1;x2,y2;...`) into a list of dictionaries `[{'x': float, 'y': float}, ...]`. Handles splitting by semicolon and then comma, and converts coordinates to floats.
    - **Error Handling:** Shows a `sg.popup_error` if parsing fails (e.g., non-numeric values).

  - **`create_json_from_inputs(values: Dict[str, Any]) -> Optional[Dict[str, Any]]`:**

    - **Logic:**
      1.  Retrieves all input values from the PySimpleGUI `values` dictionary (which holds the current state of all input elements).
      2.  Parses primary mission waypoints using `parse_waypoints_text`.
      3.  Validates primary mission start/end times (HHMM format, start < end).
      4.  Constructs the `primary_mission` part of a JSON-like dictionary.
      5.  If simulated mission waypoints are provided:
          - Parses them using `parse_waypoints_text`.
          - Parses timestamps (semicolon-separated HHMM strings). Validates format and range.
          - Ensures the number of timestamps matches the number of waypoints. If no timestamps are provided, it defaults to using the primary mission's start time for all simulated waypoints (this might be a simplification or specific requirement).
          - Constructs the `simulated_missions` list in the JSON-like dictionary.
    - **Output:** A dictionary representing the mission data in the same format as `missions.json`, or `None` if there's an input error.
    - **Error Handling:** Uses `sg.popup_error` to display errors related to input format or validation.

  - **`display_results(window, status: str, details: List[str], primary_mission: DroneMission, simulated_missions: List[DroneMission], safety_buffer: float)`:**

    - **Logic:**
      1.  Updates the GUI's status text element (`window['-STATUS-']`) with the result ("CLEAR", "CONFLICT DETECTED", "ERROR") and appropriate text color.
      2.  Updates the GUI's details multiline element (`window['-DETAILS-']`) with the conflict descriptions.
      3.  If `primary_mission` and `simulated_missions` data is available, it calls `visualization.plot_missions(...)` to generate and show the plot in a new, separate Matplotlib window. The `conflict_details` are passed to `plot_missions` for highlighting.

  - **`main_window()`:**
    - **Logic:**
      1.  **Set Theme:** `sg.theme('LightBlue2')`.
      2.  **Define Layout:** Defines the PySimpleGUI layout, a list of lists where each inner list is a row in the GUI. Uses elements like `sg.Text`, `sg.Input`, `sg.Multiline`, `sg.Slider`, `sg.Button`, `sg.Frame`. Keys (e.g., `'-PRIMARY_ID-'`, `'-CHECK_INPUTS-'`) are assigned to input elements to retrieve their values.
      3.  **Create Window:** `window = sg.Window(...)`. `finalize=True` is important for some integrations.
      4.  **Event Loop:** `while True: event, values = window.read()`. This is the heart of a PySimpleGUI app.
          - Handles window close/exit events.
          - **`'-CHECK_INPUTS-'` event:**
            - Calls `create_json_from_inputs(values)` to get mission data from the GUI fields.
            - If successful, saves this data to a temporary file (`temp_mission.json`). This is done because `check_mission_conflicts` expects a file path.
            - Calls `deconfliction_system.check_mission_conflicts` with `temp_mission.json`, the safety buffer from the slider, and `show_plot=False` (because `display_results` will handle calling `plot_missions` directly).
            - Calls `display_results` to update the GUI.
            - Deletes `temp_mission.json`.
          - **`'-LOAD_FILE-'` event:**
            - Opens a file dialog (`sg.popup_get_file`) to let the user select a mission JSON file.
            - If a file is selected, calls `deconfliction_system.check_mission_conflicts` with the selected file path.
            - Calls `display_results`.
      5.  **Close Window:** `window.close()` when the loop exits.

- **How it Works:** Provides an interactive way to define/load missions and see results. It leverages the core logic from `deconfliction_system.py` (which in turn uses `utils.py`, `conflict_checks.py`, and `visualization.py`). The GUI acts as a frontend to this existing backend logic.
- **Naming Conventions:**
  - PySimpleGUI element keys are typically uppercase strings enclosed in hyphens (e.g., `'-PRIMARY_WAYPOINTS-'`).
  - Event names match button keys.
  - Functions follow standard Python naming.
- **Test Case (Manual):**
  1.  Run `python app.py`.
  2.  Leave default values. Click "Check from Inputs".
      - Expected: Status "Conflict Detected" (based on default values in `missions.json` which often model a conflict). Details will list the conflict. A plot window will appear showing the paths and highlighted conflict.
  3.  Change primary waypoints to `0,0;10,0`, start `900`, end `905`.
  4.  Change simulated waypoints to `0,50;10,50`, timestamps `900;905`.
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

### Spatial Checks

Performed by `check_segment_spatial_conflict` in `src/conflict_checks.py` using the Shapely library.
For any two path segments (one from primary, one from a simulated drone):

1.  **LineString Creation:** Each segment (defined by two (x,y) waypoints) is converted into a `shapely.geometry.LineString` object. If a segment's start and end points are identical, it's treated as a `shapely.geometry.Point`.
2.  **Intersection:** It checks if `line1.intersects(line2)`. This is true if the segments cross or touch.
3.  **Proximity/Buffer Breach:** It calculates the shortest distance between the two geometric objects: `line1.distance(line2)`. If this `distance < safety_buffer`, a conflict is flagged.
    - `safety_buffer` is a configurable parameter (e.g., 5 units).

### Temporal Checks

If a spatial conflict (intersection or buffer breach) is detected between two segments, a temporal check is performed by `check_spatio_temporal_segment_conflict`:

1.  **Time Intervals:** For each of the two spatially conflicting segments, the time interval during which the respective drone traverses that segment is determined.
    - `segmentA_interval = [waypoint_A1.timestamp_minutes, waypoint_A2.timestamp_minutes]`
    - `segmentB_interval = [waypoint_B1.timestamp_minutes, waypoint_B2.timestamp_minutes]`
      (Timestamps are already in minutes since midnight).
2.  **Overlap Check:** The function checks if these two time intervals overlap. Two intervals `[s1, e1]` and `[s2, e2]` overlap if `s1 <= e2` AND `s2 <= e1`.

### Spatio-Temporal Conflict

A spatio-temporal conflict between two path segments is declared **if and only if**:

1.  The segments are in **spatial conflict** (they intersect OR the distance between them is less than the `safety_buffer`).
    AND
2.  Their **time intervals overlap**.

This is the core logic of `check_spatio_temporal_segment_conflict`.

### Safety Buffer

- **Concept:** A configurable minimum distance that must be maintained between any part of the primary drone's path and any part of a simulated drone's path at any overlapping time.
- **Implementation:** Used in `check_segment_spatial_conflict`. If `line1.distance(line2) < safety_buffer`, it's considered a spatial conflict.
- **Configuration:**
  - CLI: `-b BUFFER` or `--buffer BUFFER` argument.
  - GUI: Adjustable via a slider.

### Waypoint Collision

- **Concept:** A more specific type of conflict where two drones (primary and a simulated one, or two simulated ones if the logic were extended) are at the _exact same coordinates at the exact same time_.
- **Implementation:** Handled by `check_waypoint_collision` in `src/conflict_checks.py`.
  1.  Checks if `waypoint1.timestamp_minutes == waypoint2.timestamp_minutes`.
  2.  Checks if `abs(waypoint1.x - waypoint2.x) < FLOAT_TOLERANCE` AND `abs(waypoint1.y - waypoint2.y) < FLOAT_TOLERANCE`.
- Both conditions must be true for a waypoint collision.

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

The `data/` directory contains several JSON files that serve as excellent test cases.

- **`data/scenario_clear.json`**

  - **Description:** Primary drone flies `(0,0)` to `(100,0)` from 10:00 to 10:10. Simulated drone "S_Far" flies `(0,100)` to `(100,100)` (far north) in the same timeframe. "S_Later" flies `(0,10)` to `(100,10)` but much later (11:00-11:10).
  - **Expected:** "Clear". No spatial or temporal overlap that constitutes a conflict.
  - **To Run (CLI):** `python -m src.deconfliction_system data/scenario_clear.json -b 5`

- **`data/scenario_conflict_buffer.json`**

  - **Description:** Primary "P_Buffer" flies `(0,0)` to `(100,0)` from 12:00 to 12:10. Simulated "S_CloseCall" flies `(50,2)` to `(50,20)` from 12:04 to 12:08.
  - **Logic:** The primary drone is on y=0. The sim drone passes x=50, with y-coordinates from 2 to 20. The closest point on the primary path is (50,0). The distance to the sim path's point (50,2) is 2 units.
  - **Expected (with `safety_buffer = 5`):** "Conflict Detected". The paths don't intersect, but the sim drone comes within 2 units of the primary path, which is less than the buffer of 5. The time intervals [12:00, 12:10] and [12:04, 12:08] overlap.
  - **To Run (CLI):** `python -m src.deconfliction_system data/scenario_conflict_buffer.json -b 5`
  - **Expected (with `safety_buffer = 1`):** "Clear". The 2-unit proximity is now outside the 1-unit buffer.

- **`data/scenario_conflict_spatial_only.json`**

  - **Description:** Primary "P_SpatialOnly" flies `(0,0)` to `(100,100)` from 14:00 to 14:10. Simulated "S_Crosses_Later" flies `(0,100)` to `(100,0)` from 15:00 to 15:10. These paths form an 'X' and clearly intersect spatially (around (50,50)).
  - **Logic:** Spatial conflict exists. However, the primary mission's time interval [14:00, 14:10] does _not_ overlap with the simulated mission's interval [15:00, 15:10].
  - **Expected:** "Clear".
  - **To Run (CLI):** `python -m src.deconfliction_system data/scenario_conflict_spatial_only.json -b 5`

- **`data/scenario_conflict_st.json`**

  - **Description:** Primary "P_Conflict" flies `(0,0)` to `(100,100)` from 09:00 to 09:10. Simulated "S_Crosses" flies `(0,100)` to `(100,0)` from 09:04 to 09:08. Paths intersect spatially.
  - **Logic:** Spatial conflict exists. The primary mission's time interval [09:00, 09:10] _does_ overlap with the simulated mission's interval [09:04, 09:08].
  - **Expected:** "Conflict Detected".
  - **To Run (CLI):** `python -m src.deconfliction_system data/scenario_conflict_st.json -b 5`

- **Waypoint Collision Test (Manual Setup in GUI or Custom JSON):**
  - **Primary Mission:** ID "P_WP", Waypoints `0,0;10,0`, Start Time `1000`, End Time `1002`.
    - This would mean (0,0) at 10:00 (600 min), (10,0) at 10:02 (602 min).
    - Midpoint (5,0) would be at 10:01 (601 min).
  - **Simulated Mission:** ID "S_WP_Clash", Waypoints `5,0`, Timestamps `1001`.
  - **Expected (with any buffer):** "Conflict Detected". A specific "Waypoint Collision" message for P_WP waypoint (interpolated or actual, depending on how primary waypoints align with its calculated times) and S_WP_Clash waypoint (5,0) at minute 601.
  - **Note on `missions.json` Example:** The `missions.json` file has a "sim_C_waypoint_clash" example:
    ```json
    {
      "drone_id": "sim_C_waypoint_clash",
      "waypoints": [{ "x": 100, "y": 0, "timestamp": 805 }]
    }
    ```
    The primary mission in `missions.json` is:
    `{"x": 0, "y": 0}, {"x": 100, "y": 0}, {"x": 100, "y": 100}` from 800 to 810.
    Path: (0,0) -> (100,0) -> (100,100).
    Calculated times for primary:
    (0,0) @ 800 (480 min)
    (100,0) @ 805 (485 min) - Assuming distance (0,0) to (100,0) is 100, and (100,0) to (100,100) is 100. Total distance 200. Total time 10 min. Speed 20 units/min. Time for first segment = 100/20 = 5 min.
    (100,100) @ 810 (490 min)
    The simulated drone `sim_C_waypoint_clash` is at `(100,0)` at `805` (485 min).
    The primary drone is also at `(100,0)` at `805` (485 min).
    This should result in a "Waypoint Collision" detail.

This comprehensive explanation should provide a solid understanding of the entire Drone Deconfliction System.
