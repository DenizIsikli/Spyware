# Built-in modules
import datetime
import os
import time

# External libraries
from dotenv import load_dotenv
from datetime import date, datetime


class LoadEnvironmentVariables:
    @staticmethod
    def load_environment_variables():
        load_dotenv()
        return {
            "gmail_address_sender": os.getenv("GMAIL_ADDRESS_SENDER"),
            "gmail_address_receiver": os.getenv("GMAIL_ADDRESS_RECEIVER"),
            "folder_path_recordings": os.getenv("FOLDER_PATH_RECORDINGS"),
            "folder_path_screenshots": os.getenv("FOLDER_PATH_SCREENSHOTS"),
            "folder_path_soundfile": os.getenv("FOLDER_PATH_SOUNDFILE"),
            "folder_path_sys_info": os.getenv("FOLDER_PATH_SYS_INFO"),
            "folder_path_cmd_prompts": os.getenv("FOLDER_PATH_CMD_PROMPTS")
        }


# Base class for widely used variables
class BaseClass(LoadEnvironmentVariables):
    def __init__(self):
        # Date and time
        self.currentDate = date.today()
        self.currentTime = datetime.now()

        # General time length for timer based functions
        self.duration = 300
        self.end_time = time.time() + self.duration

        # Load config settings - mail and password
        env_vars = LoadEnvironmentVariables.load_environment_variables()
        self.gmail_address_sender = env_vars["gmail_address_sender"]
        self.gmail_address_receiver = env_vars["gmail_address_receiver"]

        # Base definition of folder_path
        self.folder_path_recordings = env_vars["folder_path_recordings"]
        self.folder_path_screenshots = env_vars["folder_path_screenshots"]
        self.folder_path_soundfile = env_vars["folder_path_soundfile"]
        self.folder_path_sys_info = env_vars["folder_path_sys_info"]
        self.folder_path_cmd_prompts = env_vars["folder_path_cmd_prompts"]
