import math
from typing import Tuple, List, Dict

from .models import Waypoint, DroneMission

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

# --- 3D Geometry Helper Functions ---

def _subtract_vectors(v1: Waypoint, v2: Waypoint) -> Dict[str, float]:
    return {'x': v1.x - v2.x, 'y': v1.y - v2.y, 'z': v1.z - v2.z}

def _dot_product(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    return vec1['x'] * vec2['x'] + vec1['y'] * vec2['y'] + vec1['z'] * vec2['z']

def _vector_norm_sq(vec: Dict[str, float]) -> float:
    return vec['x']**2 + vec['y']**2 + vec['z']**2

def distance_point_to_segment_3d(point: Waypoint, seg_start: Waypoint, seg_end: Waypoint) -> float:
    """Calculates the minimum distance from a 3D point to a 3D line segment."""
    segment_vec = _subtract_vectors(seg_end, seg_start)
    point_to_start_vec = _subtract_vectors(point, seg_start)

    seg_len_sq = _vector_norm_sq(segment_vec)
    if seg_len_sq < FLOAT_TOLERANCE: # Segment is essentially a point
        return math.sqrt(_vector_norm_sq(point_to_start_vec))

    # Project point_to_start_vec onto segment_vec
    # t = dot(point_to_start_vec, segment_vec) / segment_length_squared
    t = _dot_product(point_to_start_vec, segment_vec) / seg_len_sq

    if t < 0.0: # Closest point is seg_start
        return math.sqrt(_vector_norm_sq(point_to_start_vec))
    elif t > 1.0: # Closest point is seg_end
        point_to_end_vec = _subtract_vectors(point, seg_end)
        return math.sqrt(_vector_norm_sq(point_to_end_vec))
    else: # Closest point is on the segment
        closest_point_on_line = {
            'x': seg_start.x + t * segment_vec['x'],
            'y': seg_start.y + t * segment_vec['y'],
            'z': seg_start.z + t * segment_vec['z']
        }
        distance_vec = {
            'x': point.x - closest_point_on_line['x'],
            'y': point.y - closest_point_on_line['y'],
            'z': point.z - closest_point_on_line['z']
        }
        return math.sqrt(_vector_norm_sq(distance_vec))

# --- End of 3D Geometry Helper Functions ---

def check_segment_spatial_conflict(
    segment1: Tuple[Waypoint, Waypoint],
    segment2: Tuple[Waypoint, Waypoint],
    safety_buffer: float
) -> bool:
    """Checks for spatial conflict (buffer breach) between two 3D path segments.

    For 3D, this simplifies to checking if the minimum distance between the segments
    is less than the safety_buffer. Direct intersection is harder with Shapely (2D).
    This implementation will use a simplified proximity check:
    Calculate distance from each endpoint of segment1 to segment2,
    and from each endpoint of segment2 to segment1.
    If any of these distances are less than safety_buffer, consider it a conflict.
    This is an approximation, a full segment-to-segment distance is more complex.
    """
    # Unpack waypoints
    p1_start, p1_end = segment1
    p2_start, p2_end = segment2

    # Check distance from p1_start to segment2
    if distance_point_to_segment_3d(p1_start, p2_start, p2_end) < safety_buffer - FLOAT_TOLERANCE:
        return True
    # Check distance from p1_end to segment2
    if distance_point_to_segment_3d(p1_end, p2_start, p2_end) < safety_buffer - FLOAT_TOLERANCE:
        return True
    # Check distance from p2_start to segment1
    if distance_point_to_segment_3d(p2_start, p1_start, p1_end) < safety_buffer - FLOAT_TOLERANCE:
        return True
    # Check distance from p2_end to segment1
    if distance_point_to_segment_3d(p2_end, p1_start, p1_end) < safety_buffer - FLOAT_TOLERANCE:
        return True

    # A more robust check would involve finding the actual closest points between the two segments.
    # For now, this endpoint-to-segment check provides a basic level of proximity detection.
    # If waypoints themselves are very close (within buffer), that should also be caught.
    # Consider distance between segment midpoints as another heuristic?
    # For now, sticking to point-to-segment for simplicity as discussed.

    return False # No conflict detected by this simplified check

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
    """Checks if two waypoints represent the same location (3D) at the same time.

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

    # Check if coordinates are identical within the defined tolerance (now includes Z)
    x_match = abs(wp1.x - wp2.x) < FLOAT_TOLERANCE
    y_match = abs(wp1.y - wp2.y) < FLOAT_TOLERANCE
    z_match = abs(wp1.z - wp2.z) < FLOAT_TOLERANCE

    return x_match and y_match and z_match

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
                    desc = (f"Waypoint Collision: Primary Waypoint {p_wp_idx} ({p_wp.x},{p_wp.y},{p_wp.z} at minute {p_wp.timestamp_minutes}) vs "
                            f"Sim Drone {sim_mission.drone_id} Waypoint {s_wp_idx} ({s_wp.x},{s_wp.y},{s_wp.z} at minute {s_wp.timestamp_minutes}).")
                    conflict_details.append(desc)

    return conflict_found, conflict_details

# We will later add functions to iterate through missions and segments,
# and incorporate temporal checks. 