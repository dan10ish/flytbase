import os
import json
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Dict, Any, Optional, Tuple

# Import our modules
from .models import DroneMission, Waypoint
from .utils import load_missions_from_json
from .conflict_checks import find_conflicts
from .visualization import plot_missions
from .deconfliction_system import check_mission_conflicts

# Set theme for the GUI
sg.theme('LightBlue2')  # A clean, professional-looking theme

def convert_waypoints_to_text(waypoints: List[Dict[str, float]]) -> str:
    """Convert a list of waypoint dictionaries to a string format."""
    waypoint_strs = []
    for wp in waypoints:
        waypoint_strs.append(f"{wp['x']},{wp['y']}")
    return ";".join(waypoint_strs)

def parse_waypoints_text(waypoints_text: str) -> List[Dict[str, float]]:
    """Parse waypoints from string format to a list of dictionaries."""
    waypoints = []
    try:
        # Split by semicolons to get individual waypoints
        wp_strings = waypoints_text.strip().split(';')
        for wp_str in wp_strings:
            if wp_str:  # Skip empty strings
                # Split by comma to get x,y coordinates
                coords = wp_str.strip().split(',')
                if len(coords) >= 2:
                    waypoints.append({
                        'x': float(coords[0].strip()),
                        'y': float(coords[1].strip())
                    })
    except ValueError as e:
        sg.popup_error(f"Error parsing waypoints: {e}\nUse format: x1,y1;x2,y2;...")
        return []
    
    return waypoints

def create_json_from_inputs(values: Dict[str, Any]) -> Dict[str, Any]:
    """Create a mission JSON structure from the GUI inputs."""
    try:
        # Parse primary mission data
        primary_waypoints = parse_waypoints_text(values['-PRIMARY_WAYPOINTS-'])
        if not primary_waypoints:
            return None
        
        # Validate start and end times
        try:
            start_time = int(values['-START_TIME-'])
            end_time = int(values['-END_TIME-'])
            
            if not (0 <= start_time <= 2359 and 0 <= end_time <= 2359):
                sg.popup_error("Start and end times must be in HHMM format (0-2359)")
                return None
            
            if start_time >= end_time:
                sg.popup_error("Start time must be before end time")
                return None
        except ValueError:
            sg.popup_error("Start and end times must be integers in HHMM format")
            return None
        
        # Create the JSON structure
        mission_data = {
            "primary_mission": {
                "drone_id": values['-PRIMARY_ID-'],
                "waypoints": primary_waypoints,
                "start_time": start_time,
                "end_time": end_time
            },
            "simulated_missions": []
        }
        
        # Add simulated missions if any are specified
        if values['-SIM_WAYPOINTS-']:
            sim_waypoints_raw = parse_waypoints_text(values['-SIM_WAYPOINTS-'])
            if not sim_waypoints_raw:
                return None
            
            # Parse timestamps if provided
            timestamps_raw = values['-SIM_TIMESTAMPS-'].strip().split(';')
            timestamps = []
            
            for ts_str in timestamps_raw:
                if ts_str.strip():
                    try:
                        ts = int(ts_str.strip())
                        if not (0 <= ts <= 2359):
                            sg.popup_error(f"Invalid timestamp: {ts}. Must be in HHMM format (0-2359)")
                            return None
                        timestamps.append(ts)
                    except ValueError:
                        sg.popup_error(f"Invalid timestamp format: {ts_str}. Must be an integer in HHMM format")
                        return None
            
            # Check if we have timestamps for each waypoint
            if timestamps and len(timestamps) != len(sim_waypoints_raw):
                sg.popup_error(f"Number of timestamps ({len(timestamps)}) must match number of waypoints ({len(sim_waypoints_raw)})")
                return None
            
            # If no timestamps are provided, use the primary start time for all waypoints
            if not timestamps:
                timestamps = [start_time] * len(sim_waypoints_raw)
            
            # Create simulated mission with timestamps
            sim_waypoints = []
            for i, wp in enumerate(sim_waypoints_raw):
                sim_wp = wp.copy()
                sim_wp["timestamp"] = timestamps[i]
                sim_waypoints.append(sim_wp)
            
            mission_data["simulated_missions"].append({
                "drone_id": values['-SIM_ID-'],
                "waypoints": sim_waypoints
            })
        
        return mission_data
    
    except Exception as e:
        sg.popup_error(f"Error creating mission data: {e}")
        return None

def display_results(window, status: str, details: List[str], primary_mission: DroneMission, simulated_missions: List[DroneMission], safety_buffer: float):
    """Display the results in the GUI and update the plot."""
    # Update the status display
    if status == "Clear":
        window['-STATUS-'].update("CLEAR - No conflicts detected", text_color='green')
    elif status == "Conflict Detected":
        window['-STATUS-'].update("CONFLICT DETECTED", text_color='red')
    else:
        window['-STATUS-'].update(f"ERROR: {status}", text_color='orange')
    
    # Update the details display
    window['-DETAILS-'].update('\n'.join(details))
    
    # Create a new figure for the visualization in a separate window
    if primary_mission and simulated_missions:
        # Use the existing plot_missions function which will create a new figure
        plot_missions(primary_mission, simulated_missions, safety_buffer, details if status == "Conflict Detected" else None)

def main_window():
    """Create and run the main application window."""
    # Define the layout for the main window
    layout = [
        [sg.Text('Drone Deconfliction System - GUI', font=('Helvetica', 16))],
        
        # Input Section - Primary Drone Mission
        [sg.Frame('Primary Drone Mission', [
            [sg.Text('Drone ID:'), sg.Input('primary_01', key='-PRIMARY_ID-', size=(15, 1))],
            [sg.Text('Waypoints (x1,y1;x2,y2;...):')],
            [sg.Multiline('0,0;100,0;100,100', key='-PRIMARY_WAYPOINTS-', size=(40, 3))],
            [sg.Text('Start Time (HHMM):'), sg.Input('800', key='-START_TIME-', size=(6, 1)), 
             sg.Text('End Time (HHMM):'), sg.Input('810', key='-END_TIME-', size=(6, 1))],
        ])],
        
        # Input Section - Simulated Drone Mission
        [sg.Frame('Simulated Drone Mission', [
            [sg.Text('Drone ID:'), sg.Input('sim_01', key='-SIM_ID-', size=(15, 1))],
            [sg.Text('Waypoints (x1,y1;x2,y2;...):')],
            [sg.Multiline('50,-10;50,10', key='-SIM_WAYPOINTS-', size=(40, 3))],
            [sg.Text('Timestamps (HHMM;HHMM;... one per waypoint):')],
            [sg.Multiline('803;806', key='-SIM_TIMESTAMPS-', size=(40, 2))],
        ])],
        
        # Safety Settings
        [sg.Frame('Safety Settings', [
            [sg.Text('Safety Buffer:'), sg.Slider(range=(1, 20), default_value=5, orientation='h', size=(20, 15), key='-BUFFER-')]
        ])],
        
        # Load from File or Run from Inputs
        [sg.Button('Check from Inputs', key='-CHECK_INPUTS-'), 
         sg.Button('Load Mission File', key='-LOAD_FILE-'),
         sg.Input('', key='-FILE_PATH-', visible=False, enable_events=True)],
        
        # Results Section
        [sg.Frame('Results', [
            [sg.Text('Status:'), sg.Text('Waiting for check...', key='-STATUS-', size=(30, 1))],
            [sg.Text('Details:')],
            [sg.Multiline('', key='-DETAILS-', size=(60, 10), disabled=True)]
        ])],
        
        # Bottom Controls
        [sg.Button('Exit')]
    ]
    
    # Create the window
    window = sg.Window('Drone Deconfliction System', layout, finalize=True, resizable=True)
    
    # Main event loop
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        elif event == '-CHECK_INPUTS-':
            # Create mission data from inputs
            mission_data = create_json_from_inputs(values)
            if mission_data:
                # Save the mission data to a temporary file
                with open('temp_mission.json', 'w') as f:
                    json.dump(mission_data, f, indent=2)
                
                try:
                    # Run the check
                    safety_buffer = float(values['-BUFFER-'])
                    status, details, primary_mission, simulated_missions = check_mission_conflicts(
                        'temp_mission.json', safety_buffer, False  # We'll handle plotting separately
                    )
                    
                    # Display the results in the GUI
                    display_results(window, status, details, primary_mission, simulated_missions, safety_buffer)
                    
                except Exception as e:
                    sg.popup_error(f"Error running check: {e}")
                
                # Clean up the temporary file
                if os.path.exists('temp_mission.json'):
                    os.remove('temp_mission.json')
        
        elif event == '-LOAD_FILE-':
            # Open a file dialog to select a mission file
            file_path = sg.popup_get_file('Select Mission File', file_types=(("JSON Files", "*.json"),))
            if file_path:
                try:
                    # Run the check with the selected file
                    safety_buffer = float(values['-BUFFER-'])
                    status, details, primary_mission, simulated_missions = check_mission_conflicts(
                        file_path, safety_buffer, False  # We'll handle plotting separately
                    )
                    
                    # Display the results in the GUI
                    display_results(window, status, details, primary_mission, simulated_missions, safety_buffer)
                    
                except Exception as e:
                    sg.popup_error(f"Error running check with file {file_path}: {e}")
    
    window.close()

if __name__ == '__main__':
    main_window() 