import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "tyago071@gmail.com"
sender_password = "tomq lhvr mwlk nhqg"
recipient_email = "tyago071@gmail.com"
subject = "Hello from Python"
body = "with attachment"

class CustomMail():
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def __enter__(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.login(self.sender_email, self.sender_password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()

    def send_mail(self, recipient_email, subject, body, attach=None):
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_email
        html_part = MIMEText(body)
        message.attach(html_part)

        if attach is not None:
            with attach.open("rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= attachment.png",
                    )
            message.attach(part)

        self.server.sendmail(self.sender_email, recipient_email, message.as_string())

# with open("../out/Alessander Angelo_certificado_gefel.png", "rb") as attachment:
#     # Add the attachment to the message
#     part = MIMEBase("application", "octet-stream")
#     part.set_payload(attachment.read())
#     encoders.encode_base64(part)
#     part.add_header(
#         "Content-Disposition",
#         f"attachment; filename= attachment.png",
#         )
    
#     message = MIMEMultipart()
#     message['Subject'] = subject
#     message['From'] = sender_email
#     message['To'] = recipient_email
#     html_part = MIMEText(body)
#     message.attach(html_part)
#     message.attach(part)
