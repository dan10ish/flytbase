# UAV Strategic Deconfliction in Shared Airspace

## Objective
Design and implement a strategic deconfliction system that serves as the final authority for verifying whether a drone's planned waypoint mission is safe to execute in shared airspace. [cite: 1] The system must check for conflicts in both space and time against the simulated flight paths of multiple other drones. [cite: 2] The primary mission is defined by a series of waypoints that must be completed within an overall time window. [cite: 3] **Extra Credit:** Extend your solution to a 4D simulation (3D spatial coordinates + time). [cite: 4] We expect you to use AI-assisted tools (Claude Code, Cursor AI, Windsurf, Lovable, Replit, etc.) to aid your development process and document how these tools helped expedite your work. [cite: 5] The assignment is designed to be challenging yet achievable within the time limit when leveraging the latest AI tools and practices. [cite: 6]

## Scenario
A drone is scheduled to execute a waypoint mission within a specified overall time window (e.g., complete mission between T_start and T_end). [cite: 7] The mission is represented by a series of waypoints (with spatial coordinates, and optionally altitude for 3D) that define the drone's intended route. [cite: 8] Before takeoff, the drone queries a central deconfliction service that maintains the flight schedules of several other drones operating in the same airspace. [cite: 9] These simulated drones have their own flight paths that may intersect with the primary drone's mission in both space and time. [cite: 10]

## Requirements

### Input
1.  **Primary Drone Mission:**
    * A series of waypoints defining the drone's route.
    * Each waypoint includes spatial coordinates (x, y). [cite: 11] For extra credit (3D), include altitude (z). [cite: 12]
    * One overall time window (start time, end time) during which the entire mission must be completed.
2.  **Simulated Flight Schedules:**
    * A dataset (hardcoded or provided via a file) representing the flight paths of other drones. [cite: 13]
    * Each simulated flight includes its own set of waypoints and associated timings so that trajectories may overlap in the spatiotemporal domain. [cite: 14]

### Functionality
* **Spatial Check:**
    * Validate that the primary mission's path does not intersect with any other drone's trajectory within a defined safety buffer (minimum distance threshold). [cite: 15]
* **Temporal Check:**
    * Ensure that, within the overall mission window, no other drone is present in the same spatial area during overlapping time segments. [cite: 16]
* **Conflict Explanation:**
    * When conflicts are detected, return a detailed explanation indicating:
        * The location(s) and time(s) of conflict. [cite: 17]
        * Which simulated flight(s) caused the conflict? [cite: 18]
* **Query Interface:**
    * Provide a simple interface (e.g., a Python function) that accepts the primary drone's mission and returns a status (e.g., "clear" or "conflict detected") along with conflict details. [cite: 18]
* **Simulation & Visualization:**
    * Generate simulation graphs or animations that visually depict:
        * The primary drone's waypoint mission. [cite: 19]
        * Trajectories of the simulated drones. [cite: 20]
        * Highlighted areas and time segments where conflicts occur. [cite: 20]
    * Produce videos or a series of plotted graphs to demonstrate multiple scenarios:
        * A conflict-free mission. [cite: 21]
        * Cases where conflicts are detected and explained. [cite: 22]
        * **Extra Credit:** Include 4D visualization (3D space + time) to show the spatio-temporal evolution of conflicts. [cite: 22]
* **Scalability Discussion:**
    * In your reflection document, explain what it would take for such a system to handle real data from tens of thousands of commercial drones. [cite: 23] Outline the architectural changes and enhancements (e.g., distributed computing, real-time data ingestion pipelines, fault tolerance, scalability of conflict resolution algorithms) that would be necessary to support a large-scale deployment. [cite: 24]

## Deliverables
1.  **Code Repository:**
    * A self-contained Python (or any other language) solution implementing the deconfliction system and simulation of multiple drone trajectories. [cite: 25]
    * The code should be modular and well-documented. [cite: 26]
2.  **Documentation:**
    * **README:** Clear setup and execution instructions. [cite: 27]
    * **Reflection & Justification Document (1-2 pages):** [cite: 27]
        * Discuss your design decisions and architectural choices. [cite: 27]
        * Explain how spatial and temporal checks were implemented. [cite: 28]
        * Describe any AI integration, if applicable. [cite: 28]
        * Provide a testing strategy and discuss edge cases. [cite: 29]
        * Explain what would be required to scale the system to handle real-world data from tens of thousands of drones. [cite: 29]
3.  **Demonstration Video:**
    * A 3-5 minute video WITH VOICEOVER that demonstrates: [cite: 30]
        * The working system in action. [cite: 30]
        * Simulation graphs/animations of various scenarios (both conflict-free and conflict-present). [cite: 31]
        * Clear explanations of how the deconfliction system identifies, resolves, and explains conflicts. [cite: 31]
        * **Extra Credit:** A section showcasing any 4D (3D space + time) visualization features. [cite: 32]

## Evaluation Rubric

**A. Code Quality and Architecture (35 points)**
* **Modularity and Structure (10 points):**
    * Code is logically organized into modules (e.g., data ingestion, spatial check, temporal check, visualization). [cite: 33]
* **Coding Standards (10 points):**
    * Adheres to industry standards with clear naming, formatting, and maintainability. [cite: 34]
* **Architectural Decisions (10 points):**
    * Design choices are well-justified, emphasizing scalability and robustness. [cite: 35]
* **Readability and Comments (5 points):**
    * Inline documentation that aids in understanding complex logic. [cite: 36]

**B. Testability and Quality Assurance (25 points)**
* **Test Case Design (10 points):**
    * Comprehensive tests covering various conflict scenarios. [cite: 37]
* **Test Automation (5 points):**
    * Use of automated testing scripts where applicable. [cite: 38]
* **Robustness and Error Handling (5 points):**
    * Proactive handling of potential failure modes and edge cases. [cite: 39]
* **QA Thoughtfulness (5 points):**
    * Evidence of iterative testing and quality assurance practices. [cite: 40]

**C. Effective Use of Al and Resourcefulness (20 points)**
* **Innovative Use of Al (10 points):**
    * If Al is used, it is integrated meaningfully to enhance the solution. [cite: 41]
* **Critical Evaluation of Al Output (5 points):**
    * Clear explanation of how Al contributions were validated and refined. [cite: 42]
* **Self-Driven Learning (5 points):**
    * Demonstrates rapid assimilation of new tools or concepts in solving challenges. [cite: 43]

**D. Documentation, Reflection, and Communication (20 points)**
* **Solution Demonstration Video (10 points):**
    * Quality and clarity in presenting the system, emphasizing design choices and simulation outcomes. [cite: 44]
* **Reflection and Justification Document (10 points):**
    * Thoughtful explanation of design decisions, Al usage, scalability discussion, and handling of edge cases. [cite: 45]
* **Extra Credit for 4D Visualization:**
    * Additional points will be awarded for solutions that successfully extend the simulation into 3D space with altitude as an extra dimension. [cite: 46]