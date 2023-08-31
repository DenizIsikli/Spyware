# Built-in modules
import datetime
import os
import time

# External libraries
from datetime import date, datetime
from dataclasses import dataclass


@dataclass()
class DataClass:
    base_dir: str = None
    folder_path_cmd_prompts: str = ""
    folder_path_recordings: str = ""
    folder_path_screenshots: str = ""
    folder_path_soundfile: str = ""
    folder_path_sys_info: str = ""

    gmail_address_sender: str = ""
    gmail_address_receiver: str = ""

    currentDate = None
    currentTime = None
    duration = None
    end_time = None

    def __init__(self):
        self.create_paths()

    def create_paths(self):
        self.folder_path_cmd_prompts = os.getenv("FOLDER_PATH_CMD_PROMPTS")
        self.folder_path_recordings = os.getenv("FOLDER_PATH_RECORDINGS")
        self.folder_path_screenshots = os.getenv("FOLDER_PATH_SCREENSHOTS")
        self.folder_path_soundfile = os.getenv("FOLDER_PATH_SOUNDFILE")
        self.folder_path_sys_info = os.getenv("FOLDER_PATH_SYS_INFO")
        self.gmail_address_sender = os.getenv("GMAIL_ADDRESS_SENDER")
        self.gmail_address_receiver = os.getenv("GMAIL_ADDRESS_RECEIVER")

        self.currentDate = date.today()
        self.currentTime = datetime.now()
        self.duration = 300
        self.end_time = time.time() + self.duration
