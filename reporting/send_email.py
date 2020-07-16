# https://realpython.com/python-send-email/

import smtplib
import ssl
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from reporting.config import credentials


def sending_report_email(email_subject, email_body, plain_or_html, email_sender, email_receiver, email_attachment):
    # Create the email head (sender, receiver, and subject)
    email = MIMEMultipart()
    email["From"] = email_sender
    email["To"] = email_receiver
    email["Subject"] = email_subject
    email.preamble = email_subject

    # Add body and attachment to emailß
    email.attach(MIMEText(email_body, plain_or_html))
    with open(email_attachment, "rb") as attachment:
        report = MIMEApplication(attachment.read())
        report.add_header('Content-Disposition', 'attachment', filename=email_attachment)
        encoders.encode_base64(report)
        email.attach(report)

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, credentials.get('email_pwd'))
        server.sendmail(email_sender, email_receiver, email.as_string())
        print('Mail Sent')

