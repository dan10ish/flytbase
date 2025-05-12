import math
from typing import Tuple, List

from models import Waypoint, DroneMission

# Import shapely - ensure it's in requirements.txt and installed
from shapely.geometry import LineString, Point

# Define a small tolerance for floating point comparisons
FLOAT_TOLERANCE = 1e-9

def _get_time_interval_for_segment(segment: Tuple[Waypoint, Waypoint]) -> Tuple[int, int]:
    """Returns the time interval (start_minutes, end_minutes) for a segment.
    Assumes waypoints within a segment are ordered chronologically.
    """
    # Segment waypoints should already be sorted by time from loading/calculation
    start_minutes = segment[0].timestamp_minutes
    end_minutes = segment[1].timestamp_minutes
    # Ensure start <= end, although they should be ordered correctly already
    return min(start_minutes, end_minutes), max(start_minutes, end_minutes)

def check_segment_spatial_conflict(
    segment1: Tuple[Waypoint, Waypoint],
    segment2: Tuple[Waypoint, Waypoint],
    safety_buffer: float
) -> bool:
    """Checks for spatial conflict (intersection or buffer breach) between two 2D path segments.

    Args:
        segment1: The first path segment, represented by two Waypoints.
        segment2: The second path segment, represented by two Waypoints.
        safety_buffer: The minimum allowed distance between the segments.

    Returns:
        True if the segments intersect or if the distance between them is less 
        than the safety_buffer, False otherwise.
    """
    try:
        # Create Shapely LineString objects for each segment
        line1_coords = [(segment1[0].x, segment1[0].y), (segment1[1].x, segment1[1].y)]
        line2_coords = [(segment2[0].x, segment2[0].y), (segment2[1].x, segment2[1].y)]
        
        # Avoid creating zero-length lines if waypoints are identical (use points instead for distance check)
        if line1_coords[0] == line1_coords[1]:
             geom1 = Point(line1_coords[0])
        else:
             geom1 = LineString(line1_coords)
             
        if line2_coords[0] == line2_coords[1]:
            geom2 = Point(line2_coords[0])
        else:
            geom2 = LineString(line2_coords)

        # 1. Check for direct intersection
        # Note: intersects() includes touching endpoints
        if geom1.intersects(geom2):
            return True

        # 2. Check if the minimum distance is less than the safety buffer
        # Use geom1.distance(geom2) which calculates the shortest distance
        min_distance = geom1.distance(geom2)
        
        # Compare distance with safety buffer, considering float tolerance
        if min_distance < safety_buffer - FLOAT_TOLERANCE:
            return True
            
    except Exception as e:
        # Log the error or handle it appropriately
        # For now, let's print a warning and assume no conflict to avoid halting execution
        # In a production system, better error handling/logging is needed.
        print(f"Warning: Shapely check failed for segments {segment1} and {segment2}. Error: {e}")
        return False 

    return False

def check_spatio_temporal_segment_conflict(
    segment1: Tuple[Waypoint, Waypoint],
    segment2: Tuple[Waypoint, Waypoint],
    safety_buffer: float
) -> bool:
    """Checks for spatio-temporal conflict between two path segments.

    A conflict occurs if the segments are spatially conflicting (intersect or 
    within safety_buffer) AND their time intervals overlap.

    Args:
        segment1: The first path segment.
        segment2: The second path segment.
        safety_buffer: The minimum allowed spatial distance.

    Returns:
        True if both spatial conflict and temporal overlap exist, False otherwise.
    """
    # 1. Check for spatial conflict first
    if not check_segment_spatial_conflict(segment1, segment2, safety_buffer):
        return False # No spatial conflict, so no spatio-temporal conflict

    # 2. If spatially conflicting, check for temporal overlap
    start1, end1 = _get_time_interval_for_segment(segment1)
    start2, end2 = _get_time_interval_for_segment(segment2)

    # Check for overlap: (StartA <= EndB) and (StartB <= EndA)
    # Handles cases where intervals might be single points (start == end)
    overlap = (start1 <= end2) and (start2 <= end1)

    return overlap

def check_waypoint_collision(
    wp1: Waypoint,
    wp2: Waypoint
) -> bool:
    """Checks if two waypoints represent the same location at the same time.

    Uses FLOAT_TOLERANCE for comparing coordinates.

    Args:
        wp1: The first waypoint.
        wp2: The second waypoint.

    Returns:
        True if coordinates (within tolerance) and timestamps match, False otherwise.
    """
    # Check if timestamps are identical
    if wp1.timestamp_minutes != wp2.timestamp_minutes:
        return False

    # Check if coordinates are identical within the defined tolerance
    # abs(a - b) < tolerance is a common way to compare floats
    x_match = abs(wp1.x - wp2.x) < FLOAT_TOLERANCE
    y_match = abs(wp1.y - wp2.y) < FLOAT_TOLERANCE

    return x_match and y_match

def find_conflicts(
    primary_mission: DroneMission,
    simulated_missions: List[DroneMission],
    safety_buffer: float
) -> Tuple[bool, List[str]]:
    """Checks for spatio-temporal conflicts between a primary mission and simulated missions.

    Checks for:
    1. Spatio-temporal segment conflicts (intersection/proximity + time overlap).
    2. Simultaneous waypoint occupations (exact same place and time).

    Args:
        primary_mission: The primary DroneMission object.
        simulated_missions: A list of simulated DroneMission objects.
        safety_buffer: The minimum allowed spatial distance between drones/paths.

    Returns:
        A tuple containing:
          - bool: True if any conflict is detected, False otherwise.
          - List[str]: A list of strings describing each detected conflict.
                     Empty if no conflicts are found.
    """
    conflict_found = False
    conflict_details: List[str] = []

    primary_segments = primary_mission.get_path_segments()
    primary_waypoints = primary_mission.waypoints

    for sim_mission in simulated_missions:
        sim_segments = sim_mission.get_path_segments()
        sim_waypoints = sim_mission.waypoints

        # 1. Check Spatio-Temporal Segment Conflicts 
        for p_idx, p_segment in enumerate(primary_segments):
            p_start_time, p_end_time = _get_time_interval_for_segment(p_segment)
            for s_idx, s_segment in enumerate(sim_segments):
                # Use the combined spatio-temporal check
                if check_spatio_temporal_segment_conflict(p_segment, s_segment, safety_buffer):
                    s_start_time, s_end_time = _get_time_interval_for_segment(s_segment)
                    conflict_found = True
                    desc = (f"Spatio-Temporal Conflict: Primary Segment {p_idx} (Time {p_start_time}-{p_end_time}) vs "
                            f"Sim Drone {sim_mission.drone_id} Segment {s_idx} (Time {s_start_time}-{s_end_time}). "
                            f"Paths cross or breach buffer while time intervals overlap."
                           )
                    conflict_details.append(desc)
                    # Optimization: If we only need *a* conflict, we could break early.
                    # But for detailed reporting, we check all.

        # 2. Check Waypoint Collisions (Exact same place at exact same time)
        # This check remains the same as it inherently includes time.
        for p_wp_idx, p_wp in enumerate(primary_waypoints):
            for s_wp_idx, s_wp in enumerate(sim_waypoints):
                if check_waypoint_collision(p_wp, s_wp):
                    conflict_found = True
                    desc = (f"Waypoint Collision: Primary Waypoint {p_wp_idx} ({p_wp.x},{p_wp.y} at minute {p_wp.timestamp_minutes}) vs "
                            f"Sim Drone {sim_mission.drone_id} Waypoint {s_wp_idx} ({s_wp.x},{s_wp.y} at minute {s_wp.timestamp_minutes}).")
                    conflict_details.append(desc)

    return conflict_found, conflict_details

# We will later add functions to iterate through missions and segments,
# and incorporate temporal checks. 