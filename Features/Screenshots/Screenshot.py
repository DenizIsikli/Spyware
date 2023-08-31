# Built-in modules
import os
import sys
import time

# External libraries
from PIL import ImageGrab

# Custom module
import Util.DataClass as Data_Class


class Screenshot(Data_Class):
    def __init__(self):
        self.baseclass = Data_Class.DataClass.__init__(self)  # Call the base class __init__ method

        # Constants for record settings
        self.end_time = self.baseclass.end_time
        self.counter = 0
        self.sleepAmount = 1
        self.image = None

        # Generate a unique filename for the sub-folders
        self.current_time = time.strftime("%Y%m%d-%H%M%S")

        # Folder path and folder name
        self.folder_path = self.baseclass.folder_path_screenshots
        self.folder_name = f"Subfolder{self.current_time}"

    def create_subfolder(self):
        subfolder_path = os.path.join(self.folder_path, self.folder_name)

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
