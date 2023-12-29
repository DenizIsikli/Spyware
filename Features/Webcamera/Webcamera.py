import os
import time
import cv2
import numpy as np
from PIL import ImageGrab
from screeninfo import get_monitors
from Util.DataClass import DataClass


class Webcamera(DataClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Constants
        self.end_time = self.end_time

        # Generate a unique filename for the recording
        self.current_time = time.strftime("%Y%m%d-%H%M%S")

        # Folder path and filename
        self.folder_path = self.folder_path_webcamera
        os.makedirs(self.folder_path, exist_ok=True)
        self.output_file_name = f"Recording{self.current_time}.mp4"

    @staticmethod
    def get_screen_size():
        try:
            monitors = get_monitors()
            main_monitor = monitors[0]
            return main_monitor.width, main_monitor.height
        except Exception as e:
            print(f"Error occurred while getting screen size: {e}")
            return None

    def record_screen(self):
        screen_size = self.get_screen_size()
        if screen_size is None:
            print("Unable to determine screen size")
            return 2

        file_path = os.path.join(self.folder_path, self.output_file_name)

        codec = cv2.VideoWriter_fourcc(*"mp4v")
        output = cv2.VideoWriter(file_path, codec, 30.0, screen_size)

        # While recording is true and the recording time is below the duration
        while time.time() < self.end_time:
            # Capture the screen time
            frame = ImageGrab.grab()
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

            # Write the frame to the output video file
            output.write(frame)

        output.release()
