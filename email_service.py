import smtplib
from email.mime.text import MIMEText
from config import *


def send_email(subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    server.starttls()

    server.login(EMAIL, PASSWORD)

    server.send_message(msg)

    server.quit()