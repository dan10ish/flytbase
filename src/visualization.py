import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Added for 3D plotting
from matplotlib.animation import FuncAnimation # Added for animation
from typing import List, Optional, Tuple
import re # For parsing conflict details
import math # Added for ceil

# Assuming models.py is accessible
from .models import DroneMission, Waypoint

# Define colors for plotting
PRIMARY_COLOR = 'blue'
SIMULATED_COLOR = 'gray'
CONFLICT_COLOR = 'red'
BUFFER_COLOR = 'lightblue' # For potential buffer visualization

# Helper function to interpolate drone position at a given time for 3D animation
def _interpolate_position_3d(waypoints: List[Waypoint], time_minutes: float) -> Optional[Tuple[float, float, float]]:
    """Calculates a drone's (x,y,z) position at a specific time by interpolating between waypoints.

    Returns (x,y,z) tuple or None if time is outside mission or mission has < 2 waypoints.
    """
    if not waypoints or len(waypoints) < 1:
        return None

    # If only one waypoint, drone is at that waypoint for its entire duration (if time matches)
    # For animation, we'll consider it fixed if time is within its segment (which is just the point itself)
    if len(waypoints) == 1:
        wp = waypoints[0]
        # This logic might need refinement based on how single-waypoint missions are defined time-wise
        # For now, assume it's at this spot if the animation time is its timestamp.
        # A better approach for animation might be to ensure missions always have start/end or segments.
        if math.isclose(wp.timestamp_minutes, time_minutes):
             return wp.x, wp.y, wp.z
        # If not at the exact time, and only one waypoint, it's tricky. 
        # Let's assume it's at its first waypoint if time is before/at its first timestamp
        # and last waypoint if time is after/at its last timestamp.
        if time_minutes <= wp.timestamp_minutes: 
            return wp.x, wp.y, wp.z
        else: # time_minutes > wp.timestamp_minutes (and only one point)
            return wp.x, wp.y, wp.z # Stays at its only point after its time

    # Find the segment where the current time falls
    # Sort waypoints by time just in case, though they should be loaded sorted
    sorted_waypoints = sorted(waypoints, key=lambda wp: wp.timestamp_minutes)

    # If time is before the first waypoint, position at the first waypoint
    if time_minutes < sorted_waypoints[0].timestamp_minutes:
        # For animation, we might want it to be invisible or at start point until its time starts.
        # Returning first point for now to keep it simple.
        return sorted_waypoints[0].x, sorted_waypoints[0].y, sorted_waypoints[0].z

    # If time is after the last waypoint, position at the last waypoint
    if time_minutes > sorted_waypoints[-1].timestamp_minutes:
        return sorted_waypoints[-1].x, sorted_waypoints[-1].y, sorted_waypoints[-1].z

    for i in range(len(sorted_waypoints) - 1):
        wp1 = sorted_waypoints[i]
        wp2 = sorted_waypoints[i+1]

        if wp1.timestamp_minutes <= time_minutes <= wp2.timestamp_minutes:
            # If segment has zero duration, drone is at wp1's position
            if math.isclose(wp1.timestamp_minutes, wp2.timestamp_minutes):
                return wp1.x, wp1.y, wp1.z
            
            # Interpolate position
            time_ratio = (time_minutes - wp1.timestamp_minutes) / (wp2.timestamp_minutes - wp1.timestamp_minutes)
            
            interp_x = wp1.x + time_ratio * (wp2.x - wp1.x)
            interp_y = wp1.y + time_ratio * (wp2.y - wp1.y)
            interp_z = wp1.z + time_ratio * (wp2.z - wp1.z)
            return interp_x, interp_y, interp_z
    
    # Should be covered by checks above, but as a fallback, return last waypoint position
    return sorted_waypoints[-1].x, sorted_waypoints[-1].y, sorted_waypoints[-1].z

def _plot_path(ax, waypoints: List[Waypoint], color: str, label: str, linestyle: str = '-', marker: str = 'o', markersize: int = 5, is_3d: bool = False):
    """Helper function to plot a single drone path (2D or 3D)."""
    if not waypoints:
        return
    x = [wp.x for wp in waypoints]
    y = [wp.y for wp in waypoints]
    if is_3d:
        z = [wp.z for wp in waypoints]
        ax.plot(x, y, z, marker=marker, linestyle=linestyle, color=color, label=label, markersize=markersize)
        # Optionally label waypoints with time in 3D
        # for wp in waypoints:
        #     ax.text(wp.x, wp.y, wp.z, f' {wp.timestamp_minutes}m', fontsize=8, color=color)
    else:
        ax.plot(x, y, marker=marker, linestyle=linestyle, color=color, label=label, markersize=markersize)
        # Optionally label waypoints with time in 2D
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
    """Generates 2D plots: one overview and one for each primary-simulated pair.

    Args:
        primary_mission: The primary DroneMission object.
        simulated_missions: A list of simulated DroneMission objects.
        safety_buffer: The safety buffer distance.
        conflict_details: A list of strings describing conflicts, if any.
    """
    # --- Main Overview Plot (2D) ---
    fig_overview, ax_overview = plt.subplots(figsize=(12, 8))
    ax_overview.set_aspect('equal', adjustable='box')
    ax_overview.set_xlabel("X Coordinate")
    ax_overview.set_ylabel("Y Coordinate")
    ax_overview.set_title(f"Overall Drone Mission Paths (2D - Safety Buffer: {safety_buffer} units)")
    ax_overview.grid(True, linestyle='--', alpha=0.6)

    _plot_path(ax_overview, primary_mission.waypoints, PRIMARY_COLOR, f"Primary ({primary_mission.drone_id})", marker='s', markersize=6, is_3d=False)

    sim_colors_overview = plt.cm.viridis_r([i/len(simulated_missions) for i in range(len(simulated_missions))]) if simulated_missions else []
    sim_missions_dict_overview = {sim.drone_id: sim for sim in simulated_missions}

    for i, sim_mission in enumerate(simulated_missions):
        _plot_path(ax_overview, sim_mission.waypoints, sim_colors_overview[i], f"Sim ({sim_mission.drone_id})", linestyle=':', marker='^', markersize=4, is_3d=False)

    if conflict_details:
        parsed_conflicts_overview = _parse_conflict_details(conflict_details)
        primary_segments_overview = primary_mission.get_path_segments()
        
        # Highlight conflicting primary segments/waypoints on overview
        # (This logic might need refinement if a primary segment conflicts with multiple sims, ensure it's only drawn once red)
        plotted_primary_seg_labels_overview = set()
        for p_idx in parsed_conflicts_overview["primary_segments"]:
            if 0 <= p_idx < len(primary_segments_overview):
                segment = primary_segments_overview[p_idx]
                label_key = f"P_Seg_{p_idx}"
                label_text = f'Conflict Zone (Primary Seg {p_idx})' if label_key not in plotted_primary_seg_labels_overview else ""
                ax_overview.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y],
                                 color=CONFLICT_COLOR, linewidth=3, linestyle='-', marker='',
                                 label=label_text)
                if label_text: plotted_primary_seg_labels_overview.add(label_key)

        plotted_primary_wp_labels_overview = set()
        for p_idx in parsed_conflicts_overview["primary_waypoints"]:
            if 0 <= p_idx < len(primary_mission.waypoints):
                wp = primary_mission.waypoints[p_idx]
                label_key = f"P_WP_{p_idx}"
                label_text = f'Conflict Zone (Primary WP {p_idx})' if label_key not in plotted_primary_wp_labels_overview else ""
                ax_overview.plot(wp.x, wp.y, marker='X', color=CONFLICT_COLOR, markersize=12, linestyle='',
                                 label=label_text)
                if label_text: plotted_primary_wp_labels_overview.add(label_key)
        
        # Highlight conflicting simulated segments/waypoints on overview
        plotted_sim_seg_labels_overview = set()
        for sim_id, s_idx in parsed_conflicts_overview["sim_segments"]:
            if sim_id in sim_missions_dict_overview:
                sim_mission = sim_missions_dict_overview[sim_id]
                sim_segments = sim_mission.get_path_segments()
                if 0 <= s_idx < len(sim_segments):
                    segment = sim_segments[s_idx]
                    label_key = f"Sim_{sim_id}_Seg_{s_idx}"
                    label_text = f'Conflict Zone (Sim {sim_id} Seg {s_idx})' if label_key not in plotted_sim_seg_labels_overview else ""
                    # Find the original color for this sim drone to ensure consistency if not conflicting
                    original_sim_color = SIMULATED_COLOR # Default
                    for i_color, sm_color in enumerate(simulated_missions):
                        # Ensure sim_colors_overview is not empty and index is valid
                        if sm_color.drone_id == sim_id and len(sim_colors_overview) > 0 and i_color < len(sim_colors_overview):
                            original_sim_color = sim_colors_overview[i_color]
                            break
                    ax_overview.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y],
                                     color=CONFLICT_COLOR, linewidth=3, linestyle=':', marker='',
                                     label=label_text)
                    if label_text: plotted_sim_seg_labels_overview.add(label_key)

        plotted_sim_wp_labels_overview = set()
        for sim_id, s_idx in parsed_conflicts_overview["sim_waypoints"]:
            if sim_id in sim_missions_dict_overview:
                sim_mission = sim_missions_dict_overview[sim_id]
                if 0 <= s_idx < len(sim_mission.waypoints):
                    wp = sim_mission.waypoints[s_idx]
                    label_key = f"Sim_{sim_id}_WP_{s_idx}"
                    label_text = f'Conflict Zone (Sim {sim_id} WP {s_idx})' if label_key not in plotted_sim_wp_labels_overview else ""
                    ax_overview.plot(wp.x, wp.y, marker='X', color=CONFLICT_COLOR, markersize=10, linestyle='',
                                     label=label_text)
                    if label_text: plotted_sim_wp_labels_overview.add(label_key)

    handles_overview, labels_overview = ax_overview.get_legend_handles_labels()
    by_label_overview = dict(zip(labels_overview, handles_overview))
    if by_label_overview:
        # Place legend outside to the top right, with smaller font
        ax_overview.legend(by_label_overview.values(), by_label_overview.keys(), loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize='small')
    
    # Adjust layout to make space for legend
    fig_overview.tight_layout(rect=[0.04, 0.03, 0.85, 0.97]) # rect=[left, bottom, right, top]

    # --- Main Overview Plot (3D) ---
    fig_overview_3d = plt.figure(figsize=(12, 8))
    ax_overview_3d = fig_overview_3d.add_subplot(111, projection='3d')
    ax_overview_3d.set_xlabel("X Coordinate")
    ax_overview_3d.set_ylabel("Y Coordinate")
    ax_overview_3d.set_zlabel("Z Coordinate (Altitude)")
    ax_overview_3d.set_title(f"Overall Drone Mission Paths (3D - Safety Buffer: {safety_buffer} units)")
    # ax_overview_3d.grid(True) # Grid not as straightforward for 3D, can be enabled if desired

    _plot_path(ax_overview_3d, primary_mission.waypoints, PRIMARY_COLOR, f"Primary ({primary_mission.drone_id})", marker='s', markersize=6, is_3d=True)

    # Use same colors as 2D overview for consistency
    for i, sim_mission in enumerate(simulated_missions):
        _plot_path(ax_overview_3d, sim_mission.waypoints, sim_colors_overview[i], f"Sim ({sim_mission.drone_id})", linestyle=':', marker='^', markersize=4, is_3d=True)

    if conflict_details:
        parsed_conflicts_3d = _parse_conflict_details(conflict_details) # Same parsing logic
        primary_segments_3d = primary_mission.get_path_segments()
        
        plotted_primary_seg_labels_3d = set()
        for p_idx in parsed_conflicts_3d["primary_segments"]:
            if 0 <= p_idx < len(primary_segments_3d):
                segment = primary_segments_3d[p_idx]
                label_key = f"P_Seg_3D_{p_idx}"
                label_text = f'Conflict Zone (Primary Seg {p_idx})' if label_key not in plotted_primary_seg_labels_3d else ""
                ax_overview_3d.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y], [segment[0].z, segment[1].z],
                                 color=CONFLICT_COLOR, linewidth=3, linestyle='-', marker='',
                                 label=label_text)
                if label_text: plotted_primary_seg_labels_3d.add(label_key)

        plotted_primary_wp_labels_3d = set()
        for p_idx in parsed_conflicts_3d["primary_waypoints"]:
            if 0 <= p_idx < len(primary_mission.waypoints):
                wp = primary_mission.waypoints[p_idx]
                label_key = f"P_WP_3D_{p_idx}"
                label_text = f'Conflict Zone (Primary WP {p_idx})' if label_key not in plotted_primary_wp_labels_3d else ""
                ax_overview_3d.plot([wp.x], [wp.y], [wp.z], marker='X', color=CONFLICT_COLOR, markersize=12, linestyle='',
                                 label=label_text)
                if label_text: plotted_primary_wp_labels_3d.add(label_key)
        
        plotted_sim_seg_labels_3d = set()
        for sim_id, s_idx in parsed_conflicts_3d["sim_segments"]:
            if sim_id in sim_missions_dict_overview: # Reuse dict from 2D overview
                sim_mission = sim_missions_dict_overview[sim_id]
                sim_segments = sim_mission.get_path_segments()
                if 0 <= s_idx < len(sim_segments):
                    segment = sim_segments[s_idx]
                    label_key = f"Sim_3D_{sim_id}_Seg_{s_idx}"
                    label_text = f'Conflict Zone (Sim {sim_id} Seg {s_idx})' if label_key not in plotted_sim_seg_labels_3d else ""
                    ax_overview_3d.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y], [segment[0].z, segment[1].z],
                                     color=CONFLICT_COLOR, linewidth=3, linestyle=':', marker='',
                                     label=label_text)
                    if label_text: plotted_sim_seg_labels_3d.add(label_key)

        plotted_sim_wp_labels_3d = set()
        for sim_id, s_idx in parsed_conflicts_3d["sim_waypoints"]:
            if sim_id in sim_missions_dict_overview:
                sim_mission = sim_missions_dict_overview[sim_id]
                if 0 <= s_idx < len(sim_mission.waypoints):
                    wp = sim_mission.waypoints[s_idx]
                    label_key = f"Sim_3D_{sim_id}_WP_{s_idx}"
                    label_text = f'Conflict Zone (Sim {sim_id} WP {s_idx})' if label_key not in plotted_sim_wp_labels_3d else ""
                    ax_overview_3d.plot([wp.x], [wp.y], [wp.z], marker='X', color=CONFLICT_COLOR, markersize=10, linestyle='',
                                     label=label_text)
                    if label_text: plotted_sim_wp_labels_3d.add(label_key)

    handles_overview_3d, labels_overview_3d = ax_overview_3d.get_legend_handles_labels()
    by_label_overview_3d = dict(zip(labels_overview_3d, handles_overview_3d))
    if by_label_overview_3d:
        ax_overview_3d.legend(by_label_overview_3d.values(), by_label_overview_3d.keys(), loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize='small')
    
    fig_overview_3d.tight_layout(rect=[0.02, 0.02, 0.85, 0.95])

    # --- Individual Plots for Each Simulated Mission vs Primary (2D Grid) ---
    num_sim_missions = len(simulated_missions)
    if num_sim_missions > 0:
        max_subplots_per_grid_fig = 4  # e.g., 2 rows, 2 columns
        ncols_grid = 2  # Number of columns in each grid figure
        
        sim_mission_chunks = [simulated_missions[i:i + max_subplots_per_grid_fig] 
                              for i in range(0, num_sim_missions, max_subplots_per_grid_fig)]
        
        sim_colors_overview = plt.cm.viridis_r([i/len(simulated_missions) for i in range(len(simulated_missions))]) if simulated_missions else []


        for chunk_idx, mission_chunk in enumerate(sim_mission_chunks):
            current_chunk_size = len(mission_chunk)
            if current_chunk_size == 0: continue # Should not happen with the chunking logic

            nrows_grid_chunk = math.ceil(current_chunk_size / ncols_grid)
            
            # Increased figsize for a larger window and to accommodate external legends
            fig_chunk, axes_chunk = plt.subplots(nrows_grid_chunk, ncols_grid, 
                                                 figsize=(ncols_grid * 4.5, nrows_grid_chunk * 4.0), # Increased per-subplot effect
                                                 squeeze=False)
            flat_axes_chunk = axes_chunk.flatten()

            chunk_start_idx = chunk_idx * max_subplots_per_grid_fig

            for i_in_chunk, sim_mission in enumerate(mission_chunk):
                ax_ind = flat_axes_chunk[i_in_chunk]
                global_sim_idx = chunk_start_idx + i_in_chunk # Original index in simulated_missions

                ax_ind.set_aspect('equal', adjustable='box')
                ax_ind.set_xlabel("X", fontsize=7) 
                ax_ind.set_ylabel("Y", fontsize=7) 
                ax_ind.set_title(f"Pri vs Sim ({sim_mission.drone_id.split('_')[-1]}) B:{safety_buffer} (2D)", fontsize=8) 
                ax_ind.grid(True, linestyle='--', alpha=0.6)
                ax_ind.tick_params(axis='both', which='major', labelsize=6)

                _plot_path(ax_ind, primary_mission.waypoints, PRIMARY_COLOR, f"Primary", marker='s', markersize=3, is_3d=False)
                
                current_sim_color_ind = plt.cm.viridis_r(0.5) # Default
                if len(sim_colors_overview) > 0 and global_sim_idx < len(sim_colors_overview):
                    current_sim_color_ind = sim_colors_overview[global_sim_idx]

                _plot_path(ax_ind, sim_mission.waypoints, current_sim_color_ind, f"Sim ({sim_mission.drone_id.split('_')[-1]})", linestyle=':', marker='^', markersize=3, is_3d=False) # Shorter label for sim

                individual_conflict_details_chunk = []
                if conflict_details:
                    for detail in conflict_details:
                        if f"Sim Drone {sim_mission.drone_id}" in detail:
                            individual_conflict_details_chunk.append(detail)
                
                if individual_conflict_details_chunk:
                    parsed_conflicts_chunk = _parse_conflict_details(individual_conflict_details_chunk)
                    primary_segments_chunk = primary_mission.get_path_segments()

                    plotted_primary_seg_labels_chunk = set()
                    for p_idx in parsed_conflicts_chunk["primary_segments"]:
                        if 0 <= p_idx < len(primary_segments_chunk):
                            segment = primary_segments_chunk[p_idx]
                            label_key = f"P_Seg_{p_idx}_sim_{sim_mission.drone_id}_chk{chunk_idx}"
                            label_text = f'Conflict (Pri Seg {p_idx})' if label_key not in plotted_primary_seg_labels_chunk else ""
                            ax_ind.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y],
                                             color=CONFLICT_COLOR, linewidth=2, linestyle='-', marker='',
                                             label=label_text)
                            if label_text: plotted_primary_seg_labels_chunk.add(label_key)
                    
                    plotted_primary_wp_labels_chunk = set()
                    for p_idx in parsed_conflicts_chunk["primary_waypoints"]:
                        if 0 <= p_idx < len(primary_mission.waypoints):
                            wp = primary_mission.waypoints[p_idx]
                            label_key = f"P_WP_{p_idx}_sim_{sim_mission.drone_id}_chk{chunk_idx}"
                            label_text = f'Conflict (Pri WP {p_idx})' if label_key not in plotted_primary_wp_labels_chunk else ""
                            ax_ind.plot(wp.x, wp.y, marker='X', color=CONFLICT_COLOR, markersize=8, linestyle='',
                                             label=label_text)
                            if label_text: plotted_primary_wp_labels_chunk.add(label_key)

                    plotted_sim_seg_labels_chunk = set()
                    for s_sim_id, s_idx in parsed_conflicts_chunk["sim_segments"]:
                        if s_sim_id == sim_mission.drone_id:
                            sim_segments_chunk = sim_mission.get_path_segments()
                            if 0 <= s_idx < len(sim_segments_chunk):
                                segment = sim_segments_chunk[s_idx]
                                label_key = f"Sim_{s_sim_id}_Seg_{s_idx}_chk{chunk_idx}"
                                label_text = f'Conflict (Sim Seg {s_idx})' if label_key not in plotted_sim_seg_labels_chunk else ""
                                ax_ind.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y],
                                                 color=CONFLICT_COLOR, linewidth=2, linestyle=':', marker='',
                                                 label=label_text)
                                if label_text: plotted_sim_seg_labels_chunk.add(label_key)
                    
                    plotted_sim_wp_labels_chunk = set()
                    for s_sim_id, s_wp_idx in parsed_conflicts_chunk["sim_waypoints"]:
                         if s_sim_id == sim_mission.drone_id:
                            if 0 <= s_wp_idx < len(sim_mission.waypoints):
                                wp = sim_mission.waypoints[s_wp_idx]
                                label_key = f"Sim_{s_sim_id}_WP_{s_wp_idx}_chk{chunk_idx}"
                                label_text = f'Conflict (Sim WP {s_wp_idx})' if label_key not in plotted_sim_wp_labels_chunk else ""
                                ax_ind.plot(wp.x, wp.y, marker='X', color=CONFLICT_COLOR, markersize=7, linestyle='',
                                                label=label_text)
                                if label_text: plotted_sim_wp_labels_chunk.add(label_key)

                handles_ind, labels_ind = ax_ind.get_legend_handles_labels()
                by_label_ind = dict(zip(labels_ind, handles_ind))
                if by_label_ind:
                    # Move legend outside the plot area
                    ax_ind.legend(by_label_ind.values(), by_label_ind.keys(), loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize=6)
            
            # Hide any unused subplots in the current chunk figure
            for j in range(current_chunk_size, nrows_grid_chunk * ncols_grid):
                flat_axes_chunk[j].set_visible(False)

            # Adjust layout with rect to make space for suptitle and external legends
            # rect=[left, bottom, right, top]
            fig_chunk.tight_layout(rect=[0.03, 0.03, 0.85, 0.93]) # Leave space on right for legends, top for suptitle
            fig_chunk.suptitle(f"Individual Conflicts (Sim Drones {chunk_start_idx + 1}-{min(chunk_start_idx + max_subplots_per_grid_fig, num_sim_missions)}) (2D)", fontsize=10, y=0.98) # Adjusted y and fontsize slightly

    # --- Individual Plots for Each Simulated Mission vs Primary (3D Grid) ---
    # Similar structure to the 2D individual plots, but using 3D axes
    if num_sim_missions > 0:
        # (Using same chunking logic as for 2D individual plots)
        # max_subplots_per_grid_fig = 4 
        # ncols_grid = 2
        # sim_mission_chunks = ...

        for chunk_idx, mission_chunk in enumerate(sim_mission_chunks):
            current_chunk_size = len(mission_chunk)
            if current_chunk_size == 0: continue

            nrows_grid_chunk = math.ceil(current_chunk_size / ncols_grid)
            
            fig_chunk_3d, axes_chunk_3d = plt.subplots(nrows_grid_chunk, ncols_grid, 
                                                 figsize=(ncols_grid * 5.0, nrows_grid_chunk * 4.5), # Slightly larger for 3D
                                                 squeeze=False,
                                                 subplot_kw={'projection': '3d'}) # Key for 3D subplots
            flat_axes_chunk_3d = axes_chunk_3d.flatten()
            chunk_start_idx = chunk_idx * max_subplots_per_grid_fig

            for i_in_chunk, sim_mission in enumerate(mission_chunk):
                ax_ind_3d = flat_axes_chunk_3d[i_in_chunk]
                global_sim_idx = chunk_start_idx + i_in_chunk

                # ax_ind_3d.set_aspect('auto') # 'equal' not well supported for 3d, use auto or manual limits
                ax_ind_3d.set_xlabel("X", fontsize=7) 
                ax_ind_3d.set_ylabel("Y", fontsize=7) 
                ax_ind_3d.set_zlabel("Z", fontsize=7)
                ax_ind_3d.set_title(f"Pri vs Sim ({sim_mission.drone_id.split('_')[-1]}) B:{safety_buffer} (3D)", fontsize=8) 
                # ax_ind_3d.grid(True)
                ax_ind_3d.tick_params(axis='both', which='major', labelsize=6)

                _plot_path(ax_ind_3d, primary_mission.waypoints, PRIMARY_COLOR, f"Primary", marker='s', markersize=3, is_3d=True)
                
                current_sim_color_ind = plt.cm.viridis_r(0.5) # Default
                if len(sim_colors_overview) > 0 and global_sim_idx < len(sim_colors_overview):
                    current_sim_color_ind = sim_colors_overview[global_sim_idx]

                _plot_path(ax_ind_3d, sim_mission.waypoints, current_sim_color_ind, f"Sim ({sim_mission.drone_id.split('_')[-1]})", linestyle=':', marker='^', markersize=3, is_3d=True)

                individual_conflict_details_chunk = []
                if conflict_details:
                    for detail in conflict_details:
                        if f"Sim Drone {sim_mission.drone_id}" in detail:
                            individual_conflict_details_chunk.append(detail)
                
                if individual_conflict_details_chunk:
                    parsed_conflicts_chunk_3d = _parse_conflict_details(individual_conflict_details_chunk)
                    primary_segments_chunk_3d = primary_mission.get_path_segments()

                    plotted_primary_seg_labels_chunk_3d = set()
                    for p_idx in parsed_conflicts_chunk_3d["primary_segments"]:
                        if 0 <= p_idx < len(primary_segments_chunk_3d):
                            segment = primary_segments_chunk_3d[p_idx]
                            label_key = f"P_Seg_3D_{p_idx}_sim_{sim_mission.drone_id}_chk{chunk_idx}"
                            label_text = f'Conflict (Pri Seg {p_idx})' if label_key not in plotted_primary_seg_labels_chunk_3d else ""
                            ax_ind_3d.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y], [segment[0].z, segment[1].z],
                                             color=CONFLICT_COLOR, linewidth=2, linestyle='-', marker='',
                                             label=label_text)
                            if label_text: plotted_primary_seg_labels_chunk_3d.add(label_key)
                    
                    plotted_primary_wp_labels_chunk_3d = set()
                    for p_idx in parsed_conflicts_chunk_3d["primary_waypoints"]:
                        if 0 <= p_idx < len(primary_mission.waypoints):
                            wp = primary_mission.waypoints[p_idx]
                            label_key = f"P_WP_3D_{p_idx}_sim_{sim_mission.drone_id}_chk{chunk_idx}"
                            label_text = f'Conflict (Pri WP {p_idx})' if label_key not in plotted_primary_wp_labels_chunk_3d else ""
                            ax_ind_3d.plot([wp.x], [wp.y], [wp.z], marker='X', color=CONFLICT_COLOR, markersize=8, linestyle='',
                                             label=label_text)
                            if label_text: plotted_primary_wp_labels_chunk_3d.add(label_key)

                    plotted_sim_seg_labels_chunk_3d = set()
                    for s_sim_id, s_idx in parsed_conflicts_chunk_3d["sim_segments"]:
                        if s_sim_id == sim_mission.drone_id:
                            sim_segments_chunk_3d = sim_mission.get_path_segments()
                            if 0 <= s_idx < len(sim_segments_chunk_3d):
                                segment = sim_segments_chunk_3d[s_idx]
                                label_key = f"Sim_3D_{s_sim_id}_Seg_{s_idx}_chk{chunk_idx}"
                                label_text = f'Conflict (Sim Seg {s_idx})' if label_key not in plotted_sim_seg_labels_chunk_3d else ""
                                ax_ind_3d.plot([segment[0].x, segment[1].x], [segment[0].y, segment[1].y], [segment[0].z, segment[1].z],
                                                 color=CONFLICT_COLOR, linewidth=2, linestyle=':', marker='',
                                                 label=label_text)
                                if label_text: plotted_sim_seg_labels_chunk_3d.add(label_key)
                    
                    plotted_sim_wp_labels_chunk_3d = set()
                    for s_sim_id, s_wp_idx in parsed_conflicts_chunk_3d["sim_waypoints"]:
                         if s_sim_id == sim_mission.drone_id:
                            if 0 <= s_wp_idx < len(sim_mission.waypoints):
                                wp = sim_mission.waypoints[s_wp_idx]
                                label_key = f"Sim_3D_{s_sim_id}_WP_{s_wp_idx}_chk{chunk_idx}"
                                label_text = f'Conflict (Sim WP {s_wp_idx})' if label_key not in plotted_sim_wp_labels_chunk_3d else ""
                                ax_ind_3d.plot([wp.x], [wp.y], [wp.z], marker='X', color=CONFLICT_COLOR, markersize=7, linestyle='',
                                                label=label_text)
                                if label_text: plotted_sim_wp_labels_chunk_3d.add(label_key)

                handles_ind_3d, labels_ind_3d = ax_ind_3d.get_legend_handles_labels()
                by_label_ind_3d = dict(zip(labels_ind_3d, handles_ind_3d))
                if by_label_ind_3d:
                    ax_ind_3d.legend(by_label_ind_3d.values(), by_label_ind_3d.keys(), loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize=6)
            
            for j in range(current_chunk_size, nrows_grid_chunk * ncols_grid):
                flat_axes_chunk_3d[j].set_visible(False)

            fig_chunk_3d.tight_layout(rect=[0.02, 0.02, 0.85, 0.93])
            fig_chunk_3d.suptitle(f"Individual Conflicts (Sim Drones {chunk_start_idx + 1}-{min(chunk_start_idx + max_subplots_per_grid_fig, num_sim_missions)}) (3D)", fontsize=10, y=0.98)

    # --- Generate 4D Animation Plot ---
    if primary_mission and primary_mission.waypoints: # Ensure there is something to animate
        print("\nGenerating 4D (3D + Time) animation...")
        try:
            # Call the new animation function
            # The animation object needs to be held in scope to run.
            # We store it in the global Held_animations list.
            plot_animated_3d_missions(primary_mission, simulated_missions, safety_buffer)
        except Exception as anim_e:
            print(f"Warning: Failed to generate 4D animation. Error: {anim_e}")

    plt.show(block=False) # This ensures all previously created static figures are shown

# --- Animation Function ---
Held_animations = [] # To keep animation objects in scope

def plot_animated_3d_missions(
    primary_mission: DroneMission,
    simulated_missions: List[DroneMission],
    safety_buffer: float # Keep for title consistency, though not directly used in animation logic here
):
    """Generates an animated 3D plot of drone missions over time."""
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_zlabel("Z Coordinate (Altitude)")
    ax.set_title(f"Animated Drone Missions (3D)")

    all_missions = [primary_mission] + simulated_missions
    all_waypoints = [wp for mission in all_missions for wp in mission.waypoints if mission.waypoints]
    if not all_waypoints:
        plt.close(fig) # Close figure if no waypoints to animate
        return None

    min_time = min(wp.timestamp_minutes for wp in all_waypoints)
    max_time = max(wp.timestamp_minutes for wp in all_waypoints)
    if min_time == max_time: max_time +=1 # Ensure duration for animation if all at same time

    time_range = max_time - min_time
    num_frames = 200 # Number of animation frames
    time_step = time_range / num_frames

    # Plot static paths first as a backdrop
    _plot_path(ax, primary_mission.waypoints, PRIMARY_COLOR, f"Primary ({primary_mission.drone_id}) Path", linestyle='--', marker='', is_3d=True)
    sim_colors_anim = plt.cm.viridis_r([i/len(simulated_missions) for i in range(len(simulated_missions))]) if simulated_missions else []
    for i, sim_mission in enumerate(simulated_missions):
        _plot_path(ax, sim_mission.waypoints, sim_colors_anim[i], f"Sim ({sim_mission.drone_id}) Path", linestyle=':', marker='', is_3d=True)

    # Initialize drone markers (scatter plot points) for animation
    drone_markers = []
    # Primary drone marker
    initial_pos_primary = _interpolate_position_3d(primary_mission.waypoints, min_time)
    if initial_pos_primary:
        p_marker = ax.scatter([initial_pos_primary[0]], [initial_pos_primary[1]], [initial_pos_primary[2]], color=PRIMARY_COLOR, s=100, label=f"Primary ({primary_mission.drone_id})", depthshade=True)
        drone_markers.append((p_marker, primary_mission.waypoints))
    
    # Simulated drone markers
    for i, sim_mission in enumerate(simulated_missions):
        initial_pos_sim = _interpolate_position_3d(sim_mission.waypoints, min_time)
        if initial_pos_sim:
            s_marker = ax.scatter([initial_pos_sim[0]], [initial_pos_sim[1]], [initial_pos_sim[2]], color=sim_colors_anim[i], s=70, label=f"Sim ({sim_mission.drone_id})", depthshade=True, marker='^')
            drone_markers.append((s_marker, sim_mission.waypoints))

    # Time display text
    time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes, fontsize=12)

    # Set plot limits to encompass all paths
    all_x = [wp.x for wp in all_waypoints]
    all_y = [wp.y for wp in all_waypoints]
    all_z = [wp.z for wp in all_waypoints]
    if all_x and all_y and all_z:
        ax.set_xlim(min(all_x) - 10, max(all_x) + 10)
        ax.set_ylim(min(all_y) - 10, max(all_y) + 10)
        ax.set_zlim(min(all_z) - 5, max(all_z) + 5)
    
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    fig.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust for legend

    def update(frame_num):
        current_time = min_time + frame_num * time_step
        time_text.set_text(f'Time: {int(current_time // 60):02d}:{int(current_time % 60):02d} (Min: {current_time:.1f})')
        
        new_positions = []
        for marker, waypoints in drone_markers:
            pos = _interpolate_position_3d(waypoints, current_time)
            if pos:
                # For scatter, we need to update _offsets3d, which expects a list of (x,y,z) tuples
                marker._offsets3d = ([pos[0]], [pos[1]], [pos[2]])
                new_positions.append(pos)
            # else: drone is outside its mission time or no valid position, marker remains
        return [m[0] for m in drone_markers] + [time_text]

    # Create animation
    # interval is delay between frames in ms. (e.g. 200 frames, 50ms interval = 10s animation)
    ani = FuncAnimation(fig, update, frames=num_frames + 1, interval=50, blit=False, repeat=True)
    # blit=False is often more robust for 3D, especially with legends/text.
    
    Held_animations.append(ani) # Store to prevent garbage collection
    plt.show(block=False)
    return ani # Though it's stored globally, returning can be good practice

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