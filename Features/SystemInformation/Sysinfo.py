# Built-in modules
import os
import platform
import socket

# External libraries
from requests import get
from getmac import get_mac_address

# Custom module
import Util.DataClass as Data_Class


class SysInfo(Data_Class):
    def __init__(self):
        self.baseclass = Data_Class.DataClass.__init__(self)  # Call the base class __init__ method

        # Folder path and filename
        self.folder_path = self.baseclass.folder_path_sys_info
        self.output_file_name = "SystemInformation.txt"

        # Public IP website link
        self.public_ip_link = "https://api.ipify.org"

        # Mac address
        self.mac_address = get_mac_address()

        # Default value
        self.os_info = None

    def system_information(self):
        platform_switch = {
            # platform.win32_ver(release='', version='', csd='', ptype='')
            'Windows': lambda: platform.win32_ver(),
            # platform.mac_ver(release='', versioninfo=('', '', ''), machine='')
            'Darwin': lambda: platform.mac_ver(),
            # platform.libc_ver(executable=sys.executable, lib='', version='', chunksize=16384)
            'Linux': lambda: platform.libc_ver()
        }

        try:
            # Get hosts platform system and the matching keys in the dictionary
            platform_name = platform.system()
            get_os = platform_switch.get(platform_name)

            if get_os:
                self.os_info = get_os()  # Call the lambda function
            else:
                raise Exception("Unsupported platform")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Open/Create file path
        file_path = os.path.join(self.folder_path, self.output_file_name)
        with open(file_path, "a") as f:
            hostname = socket.gethostname()
            ipaddr = socket.gethostbyname(hostname)

            f.write("-----------------------------BEGIN-----------------------------\n\n")

            try:
                public_ip = get(self.public_ip_link).text
                f.write(f"Public IP Address: {public_ip}\n")
            except Exception as e:
                f.write(f"Couldn't get Public IP Address (May be due to max query): {e}\n")

            f.write(f"Processor Info: {platform.processor()}\n")
            f.write(f"OS Info: {platform.system()}\n")
            f.write(f"Detailed OS Info: {self.os_info}\n")
            f.write(f"Machine Info: {platform.machine()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP Address: {ipaddr}\n")
            f.write(f"Mac Address: {self.mac_address}\n\n\n")

            f.write(f"Current date: {self.currentDate} || Current time: {self.currentTime}\n\n")

            f.write("------------------------------END-----------------------------\n\n\n")
