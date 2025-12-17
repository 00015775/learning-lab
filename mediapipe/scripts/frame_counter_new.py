#!/usr/bin/env python3
"""
Video Frame & FPS Counter
- Accepts any video path from the terminal
- Shows total frames and FPS using OpenCV (cv2) and ffprobe
- Loops until Ctrl+C
"""

import cv2
import subprocess
import sys
import os

# ----------------------------------------------------------------------
def get_info_cv2(video_path):
    """Return (frame_count, fps) using OpenCV, or (None, None) on error."""
    if not os.path.exists(video_path):
        return None, None

    cap = cv2.VideoCapture(video_path) # Replace with your video file
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    # Some codecs report 0 FPS → fallback to None
    fps = fps if fps > 0 else None
    return frame_count, fps


# ----------------------------------------------------------------------
def get_info_ffprobe(video_path):
    """Return (frame_count, fps) using ffprobe, or (None, None) on error."""
    if not os.path.exists(video_path):
        return None, None

    try:
        # ffprobe command for frame count
        cmd_frames = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-count_frames', '-show_entries', 'stream=nb_read_frames',
            '-of', 'csv=p=0', video_path
        ]
        result_frames = subprocess.run(
            cmd_frames, capture_output=True, text=True, check=True
        )
        frame_count = int(result_frames.stdout.strip())

        # ffprobe command for FPS (r_frame_rate)
        cmd_fps = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=r_frame_rate',
            '-of', 'csv=p=0', video_path
        ]
        
        result_fps = subprocess.run(
            cmd_fps, capture_output=True, text=True, check=True
        )
        fps_str = result_fps.stdout.strip()
        if '/' in fps_str:
            num, den = map(int, fps_str.split('/'))
            fps = num / den if den != 0 else None
        else:
            fps = float(fps_str) if fps_str else None

        return frame_count, fps

    except subprocess.CalledProcessError:
        return None, None
    except FileNotFoundError:
        print("Error: ffprobe not found. Install ffmpeg.", file=sys.stderr)
        return None, None
    except Exception:
        return None, None


# ----------------------------------------------------------------------
def format_value(val):
    """Helper to show 'N/A' instead of None."""
    return f"{val:.6f}" if isinstance(val, float) else (val if val is not None else "N/A")


# ----------------------------------------------------------------------
def main():
    print("Video Frame & FPS Counter  (Ctrl+C to exit)\n")
    print("Enter video path below (drag-and-drop works in most terminals):\n")

    while True:
        try:
            video_path = input("Video path: ").strip()
            if not video_path:
                print("Please enter a valid path.\n")
                continue

            if not os.path.isfile(video_path):
                print("File not found. Try again.\n")
                continue

            print("\nAnalyzing...")

            cv2_frames, cv2_fps = get_info_cv2(video_path)
            ff_frames, ff_fps = get_info_ffprobe(video_path)

            print("-" * 60)
            print(f"File: {video_path}")
            print(f"{'Method':<12} {'Frames':<12} {'FPS':<12}")
            print("-" * 60)
            print(f"{'cv2':<12} {format_value(cv2_frames):<12} {format_value(cv2_fps):<12}")
            print(f"{'ffprobe':<12} {format_value(ff_frames):<12} {format_value(ff_fps):<12}")
            print("-" * 60)
            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!\n")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
