# External libraries
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Custom module
import Features.DataClass as Data_Class


class SendMail(Data_Class):
    def __init__(self):
        self.baseclass = Data_Class.BaseClass.__init__(self)  # Call the base class __init__ method

        self.mail_subject = "Data"
        self.mail_body = None

        # Load config settings - sender and receiver
        self.gmail_address_sender = self.baseclass.gmail_address_sender
        self.gmail_address_receiver = self.baseclass.gmail_address_receiver

    def send_mail(self, zip_file_path):
        message = MIMEMultipart("alternative")
        message["Subject"] = self.mail_subject
        message["From"] = self.gmail_address_sender
        message["To"] = self.gmail_address_receiver

        # Attach the ZIP file
        with open(zip_file_path, "rb") as file:
            attachment = MIMEBase("application", "zip")
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename="Encrypted_Folders.zip")
            message.attach(attachment)

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.gmail_address_sender, self.gmail_address_receiver)
            server.send_message(message)
