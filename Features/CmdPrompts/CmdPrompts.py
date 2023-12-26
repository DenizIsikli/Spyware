# Built-in modules
import os
import platform
import subprocess

# Custom module
from Util.DataClass import DataClass


class CmdPrompts(DataClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Folder path and filename
        self.folder_path = self.folder_path_cmdprompts
        self.ipconfigall_output_file_name = "Ipconfig.txt"
        self.netstat_output_file_name = "Netstat.txt"

        # Default value
        self.ipconfig_data = None
        self.netstat_data = None

    def ipconfig_all(self):
        platform_switch = {
            # ipconfig
            'Windows': lambda: subprocess.check_output(['ipconfig', '/all'], text=True),
            # ifconfig
            'Darwin': lambda: subprocess.check_output(['ifconfig', '-a'], text=True),
            # ifconfig
            'Linux': lambda: subprocess.check_output(['ifconfig', '-a'], text=True)
        }

        try:
            # Get hosts platform system and the matching keys in the dictionary
            platform_name = platform.system()
            get_os = platform_switch.get(platform_name)

            if get_os:
                self.ipconfig_data = get_os()  # Call the lambda function
            else:
                raise Exception("Unsupported platform")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Open/Create file path
        file_path = os.path.join(self.folder_path, self.ipconfigall_output_file_name)
        with open(file_path, "a") as f:
            f.write("-----------------------------BEGIN-----------------------------\n")

            f.write(f"{self.ipconfig_data}\n\n\n")

            f.write(f"Current date: {self.currentDate} || Current time: {self.currentTime}\n\n")

            f.write("------------------------------END------------------------------\n\n\n")

    def netstat_ano(self):
        platform_switch = {
            # netstat -ano
            'Windows': lambda: subprocess.check_output(['netstat', '-ano'], text=True),
            # netstat -anp
            'Darwin': lambda: subprocess.check_output(['netstat', '-anp'], text=True),
            # netstat -anp
            'Linux': lambda: subprocess.check_output(['netstat', '-anp'], text=True)
        }

        try:
            # Get hosts platform system and the matching keys in the dictionary
            platform_name = platform.system()
            get_os = platform_switch.get(platform_name)

            if get_os:
                netstat_output = get_os()  # Call the lambda function

                listening_lines = [line for line in netstat_output.split('\n') if 'LISTENING' in line]
                self.netstat_data = '\n'.join(listening_lines)
            else:
                raise Exception("Unsupported platform")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Create the folder path if it doesn't exist
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        # Open/Create file path
        file_path = os.path.join(self.folder_path, self.netstat_output_file_name)
        with open(file_path, "a") as f:
            f.write("-----------------------------BEGIN-----------------------------\n\n")

            f.write(f"{self.netstat_data}\n\n\n")

            f.write(f"Current date: {self.currentDate} || Current time: {self.currentTime}\n\n")

            f.write("------------------------------END------------------------------\n\n\n")
