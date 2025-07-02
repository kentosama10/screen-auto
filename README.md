# Screen Auto - Automated Screen Recording Tool

## Overview
Screen Spy is a Python-based screen recording utility that captures your screen continuously while running in the background. It features automatic segmentation, disk space management, and error recovery capabilities.

## Features
- **Silent Operation**: Runs in the background with no visible console window
- **Continuous Recording**: Captures screen content even when the system is locked
- **Automatic Segmentation**: Creates new video segments every 10 minutes
- **Disk Space Management**: Monitors available disk space and automatically removes older recordings when space is low
- **Error Recovery**: Automatically restarts in case of unexpected errors
- **Graceful Shutdown**: Can be stopped by creating a 'stop.txt' file

## Requirements
- Python 3.6+
- `ffmpeg` executable in the same directory as the script

## Installation
1. Clone this repository or download the script
2. Download the `ffmpeg` executable and place it in the same directory as the script

## Usage
1. Run the script:
```bash
python screen-spy.py
```

2. The script will:
   - Start recording immediately
   - Hide the console window
   - Create MP4 video files named `screen_record_YYYYMMDD_HHMMSS.mp4`

3. To stop recording:
   - Create a file named `stop.txt` in the same directory as the script
   - The script will detect this file and stop gracefully

## Configuration
You can modify these variables in the script to adjust behavior:
- `segment_time = 10 * 60` - Time in seconds before creating a new segment (default: 10 minutes)
- `threshold_gb = 5` - Minimum required free disk space in GB
- `-framerate 10` - Frame rate for recording (default: 10 FPS)
- `-video_size 1024x576` - Video resolution (default: 1024x576)

## Output
- Video files are saved in MP4 format
- Naming convention: `screen_record_YYYYMMDD_HHMMSS.mp4`
- Videos are recorded at 1024x576 resolution
- Files are automatically segmented every 10 minutes

## Error Handling
- Monitors available disk space
- Automatically deletes oldest recordings when space is low
- Restarts automatically if an error occurs
- Creates new recording segments periodically to prevent file corruption

## Security Note
This tool captures all screen content, including sensitive information. Use responsibly and ensure compliance with privacy policies and regulations.

## Limitations
- Currently optimized for Windows systems
- Requires sufficient disk space for continuous recording
- Requires `ffmpeg` executable for screen recording
