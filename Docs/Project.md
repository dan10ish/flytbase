## Build Plan 🚀

**Core Principle:** Start simple, get the core 2D functionality working, then iterate and add layers (GUI, 3D) if time permits. Prioritize deliverables. Aim for production-level code quality: modular, well-documented, robust, and adhering to high programming standards. *Constantly use your AI-assisted coding tools!*

### Recommended Python Tech Stack (Focus on Speed & Compatibility)

* **Core Logic & Data:**
    * Python's built-in `math` module (for basic distance calculations, vector math).
    * Python's built-in `datetime` module (for all time-related calculations and comparisons).
    * **Shapely:** For 2D geometric operations like path intersection, distance, and buffer creation. It's relatively straightforward for 2D, which is your primary target.
* **Visualization & Animation:**
    * **Matplotlib:** The workhorse for 2D plotting and can handle basic 3D plots if you reach the extra credit. Crucially, it supports animation and integrates well with GUI libraries.
* **Desktop GUI:**
    * **PySimpleGUI:** This library significantly simplifies creating GUIs by wrapping Tkinter (or other backends). It's designed for rapid development and has good Matplotlib integration, making it ideal for your timeline.

### Workflow & Procedural Steps with Checkpoints

Here's a phased approach. Tick off checkpoints as you complete them.

---

**Phase 1: Core Deconfliction Logic (2D Focus) - (Est. 10-12 hours)**

* **Objective:** Implement the fundamental spatial and temporal conflict detection for 2D drone paths.
* **Steps & Actions:**
    1.  **Understand Input/Output:**
        * Define how you'll represent the primary drone's mission: list of (x,y) waypoints, overall start/end time (provided as integer HHMM, e.g., `1430` for 2:30 PM).
        * Define how you'll represent simulated drone flights: list of (x,y) waypoints, with specific timings provided for *each waypoint* (as integer HHMM).
        * Decide on a simple data structure (using `models.py` with `Waypoint` having `timestamp_minutes` field). Initially, these scenarios will be ingested from JSON files expecting HHMM integer times.
    2.  **Implement Path Segmentation:**
        * Write functions to break down a list of waypoints into line segments (e.g., a segment is between waypoint A and waypoint B).
    3.  **Spatial Check Implementation (2D):**
        * For each segment of the primary drone's path:
            * Iterate through each segment of every simulated drone's path.
            * Use **Shapely** to:
                * Create `LineString` objects for the path segments.
                * Check if the segments intersect.
                * Calculate the minimum distance between segments.
                * Check if this distance is less than a defined safety buffer. This safety buffer should be a configurable parameter (e.g., adjustable in the GUI).
        * Additionally, implement a check to ensure no two drones (primary or simulated) occupy the exact same waypoint coordinates at the exact same time.
        * Log any potential spatial conflicts, including segment proximity/intersections and simultaneous waypoint occupations.
    4.  **Temporal Check Implementation (2D):**
        * **Crucial:** You need to determine *when* each drone is on a particular segment (using the `timestamp_minutes` field from `Waypoint` objects).
            * Assume a constant speed for the primary drone to complete its entire mission within the given time window (calculated in minutes). Distribute this time across its path segments to estimate entry/exit times (in minutes since midnight) for each segment.
            * For simulated drones, their waypoint timings (already in minutes since midnight) allow you to determine their entry/exit times for their segments.
        * If a spatial conflict (or near-miss within buffer) is detected:
            * Compare the time intervals during which the primary drone is on its conflicting segment and the simulated drone is on its conflicting segment.
            * If these time intervals overlap, you have a spatio-temporal conflict.
        * Log confirmed spatio-temporal conflicts.
    5.  **Develop the Query Interface Function:**
        * Create the main Python function that takes the primary drone's mission details.
        * This function will call your spatial and temporal check logic.
        * It should return a status ("clear" or "conflict detected").
    6.  **Conflict Explanation Logic:**
        * If conflicts are found, the query interface should also return details:
            * Location(s) (e.g., coordinates of conflict or involved segments).
            * Time(s) of conflict.
            * Which simulated flight(s) caused the conflict.
* **Checkpoints (from PDF):**
    * [ ] Input: Primary Drone Mission (waypoints x,y; overall time window) defined.
    * [ ] Input: Simulated Flight Schedules (waypoints x,y; associated timings) defined.
    * [ ] Functionality: Spatial Check implemented (path intersection within safety buffer).
    * [ ] Functionality: Temporal Check implemented (overlapping time segments in same spatial area).
    * [ ] Functionality: Query Interface created (accepts mission, returns status & details).
    * [ ] Functionality: Conflict Explanation provides location, time, and conflicting drone ID.
    * [ ] Code: Initial modular structure emerging (e.g., separate functions/classes for checks).

---

**Phase 2: Basic Visualization & Initial Testing (2D) - (Est. 6-8 hours)**

* **Objective:** Visually represent the paths and conflicts to verify your logic.
* **Steps & Actions:**
    1.  **Static 2D Plotting with Matplotlib:**
        * Plot the primary drone's waypoints and path.
        * Plot the trajectories of simulated drones.
        * Visually highlight the safety buffer around the primary drone's path segments.
        * Clearly mark detected conflict locations/segments on the plot.
    2.  **Scenario Generation:**
        * Create a few hardcoded scenarios:
            * One clearly conflict-free mission.
            * One with an obvious spatial and temporal conflict.
            * One with a spatial overlap but no temporal conflict (drones pass the same point at different times safely).
            * One with a near-miss that's caught by the safety buffer.
    3.  **Basic Animation (Optional, but good for video):**
        * Use Matplotlib's animation capabilities to show drones moving along their paths over time. This will make conflict visualization much clearer.
    4.  **Initial Testing & Debugging:**
        * Run your scenarios. Does your logic correctly identify conflicts? Does the visualization match?
        * Refine your conflict detection logic based on visual feedback.
* **Checkpoints (from PDF):**
    * [ ] Sim & Viz: Visual depiction of primary drone's mission.
    * [ ] Sim & Viz: Visual depiction of simulated drone trajectories.
    * [ ] Sim & Viz: Highlighted areas/segments where conflicts occur.
    * [ ] Testing: Conflict-free mission scenario tested.
    * [ ] Testing: Conflict-detected scenarios tested.
    * [ ] QA: Evidence of iterative testing.

---

**Phase 3: GUI Implementation (Desktop App) - (Est. 6-8 hours)**

* **Objective:** Create a simple user interface to run the deconfliction.
* **Steps & Actions:**
    1.  **Design a Simple UI with PySimpleGUI:**
        * Input fields for the primary drone's waypoints (e.g., a text area where user can input comma-separated x,y pairs) and time window.
        * A "Check Mission" button.
        * A display area for the status ("Clear" / "Conflict Detected").
        * A display area for conflict explanation details.
        * An area to embed/show the Matplotlib visualization.
    2.  **Integrate Core Logic:**
        * When the button is clicked, get inputs from the GUI.
        * Call your query interface function from Phase 1.
        * Update the GUI with the results and conflict details.
    3.  **Embed Matplotlib Plot:**
        * Use PySimpleGUI's capabilities to embed the Matplotlib canvas into your GUI window. Update the plot when a new check is run.
* **Checkpoints (from PDF):**
    * [ ] (Implied) System is interactive for demonstration.
    * [ ] Code: Demonstrates structure for a user-facing application.

---

**Phase 4: Documentation & Deliverables Prep - (Est. 6-8 hours)**

* **Objective:** Prepare all required documentation and the demonstration video. *Do not underestimate this phase!*
* **Steps & Actions:**
    1.  **Code Polishing & Commenting:**
        * Ensure your code is clean, well-organized into modules, and has clear comments/docstrings.
    2.  **Write `README.md`:**
        * Clear setup instructions (Python version, libraries to install, how to install them e.g. `pip install -r requirements.txt`).
        * Clear execution instructions (how to run your application/script).
    3.  **Write Reflection & Justification Document (1-2 pages):**
        * Discuss your design decisions (why these libraries, data structures).
        * Explain how spatial and temporal checks were implemented (briefly describe your algorithm/logic).
        * **Crucially, describe your use of AI tools:** Which tools, what prompts, how they helped, how you validated/refined AI output.
        * Testing strategy: Describe the scenarios you created and tested. Discuss any edge cases you considered (e.g., drones starting/ending at the same waypoint, vertical takeoffs if doing 3D).
        * Scalability Discussion: Outline your thoughts on handling tens of thousands of drones (e.g., spatial indexing, distributed processing, optimized data structures, dedicated database – see PDF for prompts).
    4.  **Plan and Record Demonstration Video (3-5 mins WITH VOICEOVER):**
        * Script what you'll show and say.
        * Demonstrate the working system (GUI if you built one).
        * Show conflict-free and conflict-present scenarios using your visualizations/animations.
        * Clearly explain how the system identifies and explains conflicts, pointing to the GUI/output.
* **Checkpoints (from PDF):**
    * [ ] Code: Self-contained Python solution.
    * [ ] Code: Modular and well-documented.
    * [ ] Docs: README with setup/execution instructions.
    * [ ] Docs: Reflection & Justification document written.
        * [ ] Design decisions discussed.
        * [ ] Spatial/temporal checks explained.
        * [ ] AI integration described.
        * [ ] Testing strategy & edge cases discussed.
        * [ ] Scalability discussed.
    * [ ] Video: 3-5 minutes with voiceover.
    * [ ] Video: Demonstrates working system.
    * [ ] Video: Shows simulation graphs/animations for various scenarios.
    * [ ] Video: Clear explanation of conflict identification & explanation.
    * [ ] Evaluation: Coding Standards (clear naming, formatting).
    * [ ] Evaluation: Architectural Decisions Justified.
    * [ ] Evaluation: Readability and Comments.
    * [ ] Evaluation: Test Case Design (various conflict scenarios covered).
    * [ ] Evaluation: Robustness and Error Handling (thought given to potential issues).

---

**Phase 5: Extra Credit - 3D/4D Simulation (If Time Permits - Est. 4-6 hours AFTER core is solid)**

* **Objective:** Extend to 3D spatial coordinates (x,y,z) + time.
* **Steps & Actions:**
    1.  **Adapt Data Structures:** Include 'z' (altitude) in waypoints.
    2.  **Update Spatial Logic:**
        * Distance calculations now in 3D. (Use `math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)`).
        * Line segment intersection/closest point in 3D is more complex. For speed, you might simplify (e.g., project to 2D planes for initial checks or focus on proximity of 3D line segments). AI tools can help find algorithms/snippets for 3D line segment distance.
    3.  **Update Visualization:**
        * Use Matplotlib's `mplot3d` toolkit for 3D scatter and line plots.
        * Animate this 3D plot to represent the 4th dimension (time).
* **Checkpoints (from PDF):**
    * [ ] Input: Altitude (z) included for Primary Drone Mission (if attempted).
    * [ ] Sim & Viz: 4D visualization (3D space + time) to show spatio-temporal evolution (if attempted).
    * [ ] Video: Section showcasing 4D visualization features (if attempted).
    * [ ] Extra Credit: Solution extended into 3D space with altitude.

---

### Final Tips for the 36-Hour Sprint:

* **KISS (Keep It Simple, Stupid):** Don't over-engineer solutions, especially early on.
* **Timebox Ruthlessly:** Allocate time for each phase and stick to it as much as possible. If you get stuck, simplify your approach or use AI tools to find a path forward quickly.
* **Iterate & Test Frequently:** Test small pieces of functionality as you build them.
* **Prioritize Core Requirements:** The 2D version with all deliverables is better than an incomplete 3D version.
* **AI Is Your Co-Pilot:** Use it for boilerplate code, debugging help, explaining concepts, finding library usage examples, and even drafting parts of your documentation. Remember to document *how* you used it.
* **Don't Skip the Reflection Doc & Video:** These are heavily weighted in the evaluation.
* **Get Some Sleep!** A tired brain makes mistakes. Short breaks can also help.

Good luck! You can do this. Focus on one step at a time.