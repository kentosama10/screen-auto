import cv2
import numpy as np
import mss
import ctypes
import os
import time
import shutil
import subprocess

# Function to check disk space
def check_disk_space(threshold_gb=10):
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)  # Convert bytes to GB
    return free_gb < threshold_gb

# Function to get the output filename based on timestamp
def get_output_filename():
    return "screen_record_" + time.strftime("%Y%m%d_%H%M%S") + ".mp4"

# Hide the console window
kernel32 = ctypes.windll.kernel32
hwnd = kernel32.GetConsoleWindow()
if hwnd:
    ctypes.windll.user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE (completely hide)

# Set screen resolution
with mss.mss() as sct:
    screen_width = sct.monitors[1]["width"]
    screen_height = sct.monitors[1]["height"]

frame_rate = 20  # FPS
segment_time = 10 * 60  # Save every 10 minutes
max_recording_time = 2 * 60 * 60  # 2 hours split

start_time = time.time()
segment_start_time = start_time

output_file = get_output_filename()
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Function to create a new VideoWriter
def create_video_writer(filename):
    return cv2.VideoWriter(filename, fourcc, frame_rate, (screen_width, screen_height))

out = create_video_writer(output_file)

print("Screen recording started. Create a file named 'stop.txt' to stop.")

try:
    with mss.mss() as sct:
        while True:
            # Check if stop file exists
            if os.path.exists("stop.txt"):
                print("Stop file detected. Stopping screen recording.")
                break

            # Check if disk space is low and delete old recordings if necessary
            if check_disk_space(threshold_gb=5):  
                print("Low disk space! Deleting oldest recording...")
                files = sorted([f for f in os.listdir() if f.startswith("screen_record_")], reverse=True)
                if files:
                    os.remove(files[-1])

            # Capture screen even when locked
            screenshot = sct.grab(sct.monitors[1])
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            out.write(frame)

            # Check if it's time to save a segment
            if time.time() - segment_start_time >= segment_time:
                print("Saving segment...")
                out.release()
                output_file = get_output_filename()
                out = create_video_writer(output_file)
                segment_start_time = time.time()

            # Check if 2 hours have passed, then restart new recording
            if time.time() - start_time >= max_recording_time:
                out.release()
                output_file = get_output_filename()
                out = create_video_writer(output_file)
                start_time = time.time()

            # Limit frame rate
            time.sleep(1 / frame_rate)

except Exception as e:
    print(f"Error: {e}")
    print("Script encountered an error. Restarting...")

finally:
    out.release()
    cv2.destroyAllWindows()
    if os.path.exists("stop.txt"):
        os.remove("stop.txt")
    print(f" '{output_file}'.")

# Restart the script only if it failed unexpectedly (not when stop.txt was used)
if "Error" in locals() or "Error" in globals():  
    exe_path = os.path.join(os.getcwd(), "hello-world.exe")  # Update with your .exe name
    subprocess.Popen([exe_path])
    print("Restarting due to an error...")
else:
    print("Stopped normally. Not restarting.")
