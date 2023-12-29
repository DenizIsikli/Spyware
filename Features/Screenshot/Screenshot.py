import os
import sys
import time
from PIL import ImageGrab
from Util.DataClass import DataClass


class Screenshot(DataClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Constants for record settings
        self.end_time = self.end_time
        self.counter = 0
        self.sleepAmount = 1
        self.image = ImageGrab.grab()

        # Generate a unique filename for the sub-folders
        self.current_time = time.strftime("%Y%m%d-%H%M%S")

        # Folder path and folder name
        self.folder_path = self.folder_path_screenshot
        os.makedirs(self.folder_path, exist_ok=True)
        self.subfolder_name = f"Subfolder{self.current_time}"

    def create_subfolder(self):
        subfolder_path = os.path.join(self.folder_path, self.subfolder_name)

        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        return subfolder_path

    def screenshot(self):
        subfolder_path = self.create_subfolder()

        while time.time() < self.end_time:
            try:
                self.image = ImageGrab.grab()
            except Exception as e:
                print(f"Error while grabbing the image: {e}")
                break

            self.counter += 1

            # Save captured screenshots to the file path
            output_file_name = f"Screenshot{self.counter}.png"
            file_path = os.path.join(subfolder_path, output_file_name)
            self.image.save(file_path)

            # Flush the output to display immediately
            sys.stdout.flush()

            time.sleep(self.sleepAmount)
