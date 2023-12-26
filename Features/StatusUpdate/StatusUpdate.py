# Built-in modules
import os
from datetime import datetime

# Custom module
from Util.DataClass import DataClass


class StatusUpdate(DataClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Folder path and filename
        self.folder_path = self.folder_path_statusupdate
        self.status_filename = "StatusUpdate.txt"

    def status_update(self, status: str):
        file_path = os.path.join(self.folder_path, self.status_filename)
        with open(file_path, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}]: {status}\n")
