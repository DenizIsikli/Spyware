# Built-in modules
import datetime
import os
import time

# External libraries
from datetime import date, datetime
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass()
class DataClass:
    folder_path_cmdprompts: str = ""
    folder_path_screenshot: str = ""
    folder_path_soundfile: str = ""
    folder_path_statusupdate: str = ""
    folder_path_systeminformation: str = ""
    folder_path_webcamera: str = ""

    gmail_address_sender: str = ""
    gmail_address_receiver: str = ""

    currentDate = None
    currentTime = None
    duration = None
    end_time = None

    def __init__(self):
        self.create_paths()
        self.base_dir = "/config/config.env"

    def create_paths(self):
        load_dotenv(dotenv_path=self.base_dir, verbose=True)

        # Base directory
        self.folder_path_cmdprompts = os.getenv("FOLDER_PATH_CMDPROMPTS")
        self.folder_path_screenshot = os.getenv("FOLDER_PATH_SCREENSHOTS")
        self.folder_path_soundfile = os.getenv("FOLDER_PATH_SOUNDFILE")
        self.folder_path_statusupdate = os.getenv("FOLDER_PATH_STATUSUPDATE")
        self.folder_path_systeminformation = os.getenv("FOLDER_PATH_SYS_INFO")
        self.folder_path_webcamera = os.getenv("FOLDER_PATH_RECORDINGS")

        # Gmail
        self.gmail_address_sender = os.getenv("GMAIL_ADDRESS_SENDER")
        self.gmail_address_receiver = os.getenv("GMAIL_ADDRESS_RECEIVER")

        # Config
        self.currentDate = date.today()
        self.currentTime = datetime.now()
        self.duration = 300
        self.end_time = time.time() + self.duration
