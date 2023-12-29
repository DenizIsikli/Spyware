import os
import time
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

    currentDate: date = date.today()
    currentTime: datetime = datetime.now()
    duration: int = 5
    end_time: float = None

    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join(self.script_dir, '..', 'config', 'config.env')
        self.create_paths()

        self.end_time = time.time() + self.duration

    def create_paths(self):
        load_dotenv(dotenv_path=self.base_dir, verbose=True)

        # /Features
        features_dir = os.path.join(self.script_dir, '..', 'Features')

        # /Features/...
        self.folder_path_cmdprompts = os.path.join(features_dir, "CmdPrompts")
        self.folder_path_screenshot = os.path.join(features_dir, "Screenshot")
        self.folder_path_soundfile = os.path.join(features_dir, "Soundfile")
        self.folder_path_statusupdate = os.path.join(features_dir, "StatusUpdate")
        self.folder_path_systeminformation = os.path.join(features_dir, "SystemInformation")
        self.folder_path_webcamera = os.path.join(features_dir, "Webcamera")

        # Gmail
        self.gmail_address_sender = os.getenv("GMAIL_ADDRESS_SENDER")
        self.gmail_address_receiver = os.getenv("GMAIL_ADDRESS_RECEIVER")
