import os
import time
import shutil
import subprocess
from datetime import datetime, timedelta
import ctypes
import sys

# Prevent the PC from sleeping
def prevent_sleep():
    # SetThreadExecutionState flags:
    # ES_CONTINUOUS: Ensures the system continues in this state
    # ES_SYSTEM_REQUIRED: Prevents the system from sleeping
    # ES_DISPLAY_REQUIRED: Prevents the display from turning off
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002 | 0x00000001)

# Restore the PC's sleep settings
def restore_sleep():
    # Revert to the default state
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)

# Function to check disk space
def check_disk_space(threshold_gb=10):
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)  # Convert bytes to GB
    print(f"Free disk space: {free_gb} GB")
    return free_gb < threshold_gb

# Function to get the output filename based on timestamp
def get_output_filename():
    # Determine the base directory (where the script or executable is located)
    if getattr(sys, 'frozen', False):  # If running as a PyInstaller executable
        base_dir = os.path.dirname(sys.executable)
    else:  # If running as a Python script
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Create a subfolder for the current day
    date_folder = time.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
    daily_folder = os.path.join(base_dir, date_folder)
    if not os.path.exists(daily_folder):
        os.makedirs(daily_folder)  # Create the folder if it doesn't exist

    # Generate the output filename with the daily folder
    filename = "screen_record_" + time.strftime("%Y%m%d_%H%M%S") + ".mp4"
    return os.path.join(daily_folder, filename)

# Function to record the screen using ffmpeg
def record_with_ffmpeg(output_file, duration):
    ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")
    print(f"Using ffmpeg at: {ffmpeg_path}")
    command = [
        ffmpeg_path,
        "-f", "gdigrab",
        "-framerate", "10",
        "-i", "desktop",
        "-video_size", "1024x576",
        "-offset_x", "0",
        "-offset_y", "0",
        "-t", str(duration),
        "-vcodec", "libx264",
        "-preset", "ultrafast",
        "-draw_mouse", "0",
        "-an",  # disable audio
        "-vf", "scale=1024:576",
        output_file
    ]
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command, shell=True)

# Recording parameters
segment_time = 10 * 60  # Save every 10 minutes
start_time = time.time()

print("Screen recording started. Create a file named 'stop.txt' to stop.")

# Prevent the PC from sleeping
prevent_sleep()

# Determine the directory of the script or executable
if getattr(sys, 'frozen', False):  # If running as a PyInstaller executable
    base_dir = os.path.dirname(sys.executable)
else:  # If running as a Python script
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the stop.txt file
stop_file_path = os.path.join(base_dir, "stop.txt")

# Main loop
try:
    while True:
        # Check if stop file exists
        if os.path.exists(stop_file_path):
            print("Stop file detected. Stopping screen recording.")
            break

        # Check if disk space is low and delete old recordings if necessary
        if check_disk_space(threshold_gb=5):
            print("Low disk space! Deleting oldest recording...")
            # Find all daily folders
            daily_folders = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
            daily_folders.sort()  # Sort folders by date

            for folder in daily_folders:
                files = sorted([f for f in os.listdir(folder) if f.startswith("screen_record_")], reverse=True)
                if files:
                    oldest_file = os.path.join(folder, files[-1])
                    os.remove(oldest_file)
                    print(f"Deleted oldest recording: {oldest_file}")
                    break

        # Record a segment
        output_file = get_output_filename()
        print(f"Output file will be saved as: {output_file}")
        print(f"Recording segment: {output_file}")
        record_with_ffmpeg(output_file, segment_time)

except Exception as e:
    print(f"Error: {e}")
    print("Script encountered an error. Exiting...")

finally:
    # Restore the PC's sleep settings
    restore_sleep()
    
    # Remove the stop file if it exists
    if os.path.exists(stop_file_path):
        os.remove(stop_file_path)
    
    print("Screen recording stopped.")
