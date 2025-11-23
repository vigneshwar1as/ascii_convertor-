import cv2
import os
import shutil
import time
import subprocess
import sys
ASCII_CHARS = " :. @%#*+= "
def frame_to_ascii(frame, new_width=40):
    cols, rows = shutil.get_terminal_size(fallback=(100, 80))
    height, width = frame.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 corrects aspect ratio for text
    if new_height > rows - 2:   # leave margin
        new_height = rows - 2
    resized = cv2.resize(frame, (new_width, new_height))
    ascii_frame = ""
    for row in resized:
        for pixel in row:
            index = int(pixel) * len(ASCII_CHARS) // 256
            # Ensure index is within bounds
            index = max(0, min(index, len(ASCII_CHARS) - 1))
            ascii_frame += ASCII_CHARS[index]
        ascii_frame += "\n"

    return ascii_frame


def play_video(video_path="C:\\Users\\sarun\\Pictures\\Screenshots\\Screenshot 2025-10-30 212949.png", width=100):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print(f"Error: Could not open {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps if fps > 0 else 0.03

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Convert frame → ASCII
            ascii_frame = frame_to_ascii(gray, width)

            # Clear screen & print
            os.system("cls" if os.name == "nt" else "clear")
            print(ascii_frame)

            # Control playback speed
            time.sleep(delay)
    finally:
        cap.release()


def open_terminal_and_play():
    """
    Opens a new terminal window and runs the video in it
    """
    script_path = os.path.abspath(__file__)
    
    if os.name == 'nt':  # Windows
        # Create a command that will run this script with a flag to play directly
        cmd = f'start cmd /k python "{script_path}" --play'
        subprocess.Popen(cmd, shell=True)
    else:  # Linux/Mac
        cmd = f'gnome-terminal -- python "{script_path}" --play'
        subprocess.Popen(cmd, shell=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--play":
        # Direct play mode (called from the new terminal)
        play_video(width=100)
    else:
        # Open a new terminal and play there
        open_terminal_and_play()