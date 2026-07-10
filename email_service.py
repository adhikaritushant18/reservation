import smtplib
from email.mime.text import MIMEText
from config import *


def send_email(subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = ", ".join(TO_EMAIL)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    server.starttls()

    server.login(EMAIL, PASSWORD)

    # Send to all recipients
    server.sendmail(
        EMAIL,
        TO_EMAIL,
        msg.as_string()
    )

    server.quit()