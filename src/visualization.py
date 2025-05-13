import matplotlib.pyplot as plt
from typing import List, Optional, Tuple
import re # For parsing conflict details

# Assuming models.py is accessible
from .models import DroneMission, Waypoint

# Define colors for plotting
PRIMARY_COLOR = 'blue'
SIMULATED_COLOR = 'gray'
CONFLICT_COLOR = 'red'
BUFFER_COLOR = 'lightblue' # For potential buffer visualization

def _plot_path(ax, waypoints: List[Waypoint], color: str, label: str, linestyle: str = '-', marker: str = 'o', markersize: int = 5):
    """Helper function to plot a single drone path."""
    if not waypoints:
        return
    x = [wp.x for wp in waypoints]
    y = [wp.y for wp in waypoints]
    ax.plot(x, y, marker=marker, linestyle=linestyle, color=color, label=label, markersize=markersize)
    # Optionally label waypoints with time
    # for wp in waypoints:
    #     ax.text(wp.x, wp.y, f' {wp.timestamp_minutes}m', fontsize=8, color=color)

def _parse_conflict_details(conflict_details: List[str]) -> dict:
    """Parses conflict detail strings to extract relevant entities (segments, waypoints).
    
    Returns a dictionary containing lists of conflicting entities:
        {
            "primary_segments": [index1, index2, ...],
            "sim_segments": [(drone_id, index1), (drone_id, index2), ...],
            "primary_waypoints": [index1, index2, ...],
            "sim_waypoints": [(drone_id, index1), (drone_id, index2), ...]
        }
    """
    conflicts = {
        "primary_segments": [],
        "sim_segments": [],
        "primary_waypoints": [],
        "sim_waypoints": [],
    }
    
    # Regex patterns to extract indices and IDs - raw strings r'' are safer for regex
    segment_pattern = re.compile(r"Primary Segment (\d+).*Sim Drone (\S+) Segment (\d+)")
    waypoint_pattern = re.compile(r"Primary Waypoint (\d+).*Sim Drone (\S+) Waypoint (\d+)")

    for detail in conflict_details:
        segment_match = segment_pattern.search(detail)
        waypoint_match = waypoint_pattern.search(detail)

        if "Spatio-Temporal Conflict" in detail and segment_match:
            p_idx = int(segment_match.group(1))
            sim_id = segment_match.group(2)
            s_idx = int(segment_match.group(3))
            if p_idx not in conflicts["primary_segments"]:
                conflicts["primary_segments"].append(p_idx)
            sim_segment_tuple = (sim_id, s_idx)
            if sim_segment_tuple not in conflicts["sim_segments"]:
                 conflicts["sim_segments"].append(sim_segment_tuple)

        elif "Waypoint Collision" in detail and waypoint_match:
            p_idx = int(waypoint_match.group(1))
            sim_id = waypoint_match.group(2)
            s_idx = int(waypoint_match.group(3))
            if p_idx not in conflicts["primary_waypoints"]:
                conflicts["primary_waypoints"].append(p_idx)
            sim_waypoint_tuple = (sim_id, s_idx)
            if sim_waypoint_tuple not in conflicts["sim_waypoints"]:
                conflicts["sim_waypoints"].append(sim_waypoint_tuple)

    return conflicts


def plot_missions(
    primary_mission: DroneMission,
    simulated_missions: List[DroneMission],
    safety_buffer: float,
    conflict_details: Optional[List[str]] = None
):
    """Generates a 2D plot visualizing drone missions and detected conflicts.

    Args:
        primary_mission: The primary DroneMission object.
        simulated_missions: A list of simulated DroneMission objects.
        safety_buffer: The safety buffer distance (used for context, plotting actual buffer might be complex).
        conflict_details: A list of strings describing conflicts, if any.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal', adjustable='box') # Ensure correct aspect ratio for distances
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_title(f"Drone Mission Paths (Safety Buffer: {safety_buffer} units)")
    ax.grid(True, linestyle='--', alpha=0.6)

    # Plot primary mission
    _plot_path(ax, primary_mission.waypoints, PRIMARY_COLOR, f"Primary ({primary_mission.drone_id})", marker='s', markersize=6)

    # Plot simulated missions
    sim_colors = plt.cm.viridis_r([i/len(simulated_missions) for i in range(len(simulated_missions))]) if simulated_missions else []
    sim_missions_dict = {sim.drone_id: sim for sim in simulated_missions} # For quick lookup
    
    for i, sim_mission in enumerate(simulated_missions):
        _plot_path(ax, sim_mission.waypoints, sim_colors[i], f"Sim ({sim_mission.drone_id})", linestyle=':', marker='^', markersize=4)

    # Highlight conflicts if details are provided
    if conflict_details:
        parsed_conflicts = _parse_conflict_details(conflict_details)
        
        # Highlight conflicting primary segments/waypoints
        primary_segments = primary_mission.get_path_segments()
        plotted_primary_seg_label = False
        for p_idx in parsed_conflicts["primary_segments"]:
            if 0 <= p_idx < len(primary_segments):
                 segment = primary_segments[p_idx]
                 ax.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y], 
                         color=CONFLICT_COLOR, linewidth=3, linestyle='-', marker='', 
                         label=f'Conflict Zone (Primary Seg {p_idx})' if not plotted_primary_seg_label else "") # Label only once
                 plotted_primary_seg_label = True

        plotted_primary_wp_label = False
        for p_idx in parsed_conflicts["primary_waypoints"]:
             if 0 <= p_idx < len(primary_mission.waypoints):
                 wp = primary_mission.waypoints[p_idx]
                 ax.plot(wp.x, wp.y, marker='X', color=CONFLICT_COLOR, markersize=12, linestyle='',
                         label=f'Conflict Zone (Primary WP {p_idx})' if not plotted_primary_wp_label and not plotted_primary_seg_label else "") # Label only once if no seg conflict label shown
                 plotted_primary_wp_label = True


        # Highlight conflicting simulated segments/waypoints
        plotted_sim_seg_labels = set()
        for sim_id, s_idx in parsed_conflicts["sim_segments"]:
            if sim_id in sim_missions_dict:
                sim_mission = sim_missions_dict[sim_id]
                sim_segments = sim_mission.get_path_segments()
                if 0 <= s_idx < len(sim_segments):
                    segment = sim_segments[s_idx]
                    label_key = f"Sim_{sim_id}_Seg_{s_idx}"
                    label_text = f'Conflict Zone (Sim {sim_id} Seg {s_idx})' if label_key not in plotted_sim_seg_labels else ""
                    ax.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y], 
                             color=CONFLICT_COLOR, linewidth=3, linestyle=':', marker='',
                             label=label_text) 
                    if label_text: plotted_sim_seg_labels.add(label_key)
                             
        plotted_sim_wp_labels = set()
        for sim_id, s_idx in parsed_conflicts["sim_waypoints"]:
            if sim_id in sim_missions_dict:
                sim_mission = sim_missions_dict[sim_id]
                if 0 <= s_idx < len(sim_mission.waypoints):
                    wp = sim_mission.waypoints[s_idx]
                    label_key = f"Sim_{sim_id}_WP_{s_idx}"
                    label_text = f'Conflict Zone (Sim {sim_id} WP {s_idx})' if label_key not in plotted_sim_wp_labels else ""
                    ax.plot(wp.x, wp.y, marker='X', color=CONFLICT_COLOR, markersize=10, linestyle='',
                            label=label_text) 
                    if label_text: plotted_sim_wp_labels.add(label_key)


    # Improve legend handling - avoid duplicate labels
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles)) # Use dict to automatically remove duplicates
    if by_label: # Only show legend if there are labels
      ax.legend(by_label.values(), by_label.keys(), loc='best')

    plt.show() # Display the plot interactively

# Example usage (can be run standalone if needed with dummy data)
if __name__ == '__main__':
    # Create dummy data for testing the plot function
    primary = DroneMission(drone_id="P1", waypoints=[
        Waypoint(x=0, y=0, timestamp_minutes=0),
        Waypoint(x=100, y=100, timestamp_minutes=10),
        Waypoint(x=150, y=80, timestamp_minutes=15),
    ])
    sim1 = DroneMission(drone_id="S1", waypoints=[
        Waypoint(x=10, y=90, timestamp_minutes=5),
        Waypoint(x=90, y=10, timestamp_minutes=12), # Potential conflict area near (100,100)
    ])
    sim2 = DroneMission(drone_id="S2", waypoints=[
        Waypoint(x=140, y=70, timestamp_minutes=14), # Potential conflict near (150,80)
        Waypoint(x=160, y=90, timestamp_minutes=16),
    ])
    
    # Example conflict details matching the dummy data structure (for testing parsing)
    # Example for a segment conflict: Primary Seg 1 vs Sim S2 Seg 0
    # Example for a waypoint collision: Primary WP 2 vs Sim S2 WP 0 (made up for test)
    dummy_conflict_details = [
        "Spatio-Temporal Conflict: Primary Segment 1 (Time 10-15) vs Sim Drone S2 Segment 0 (Time 14-16). Paths cross or breach buffer while time intervals overlap.",
        # "Waypoint Collision: Primary Waypoint 2 (150.0,80.0 at minute 15) vs Sim Drone S2 Waypoint 0 (140.0,70.0 at minute 14)." 
    ]

    print("Plotting example mission without conflicts...")
    plot_missions(primary, [sim1, sim2], safety_buffer=5.0)
    
    print("\nPlotting example mission WITH conflicts...")
    plot_missions(primary, [sim1, sim2], safety_buffer=5.0, conflict_details=dummy_conflict_details) 