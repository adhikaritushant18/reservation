import pandas as pd
from datetime import datetime, timedelta
from google_drive import download_excel, upload_excel
from email_service import send_email
from config import *

download_excel()

df = pd.read_excel(
    BOOKING_FILE,
    sheet_name=SHEET_NAME
)

tomorrow = datetime.today().date() + timedelta(days=1)

for index, row in df.iterrows():

    arrival = pd.to_datetime(row["Arrival Kathmandu"]).date()

    reminder = str(row["Reminder Sent"]).strip().lower()

    if arrival == tomorrow and reminder != "yes":

        subject = f"Arrival Tomorrow - {row['Group Name']}"

        body = f"""
Dear Reservation Team,

This is an automated reminder from the Reservation Management System.

The following group is scheduled to arrive tomorrow. Please ensure that all necessary arrangements have been completed.

--------------------------------------------------
Booking ID   : {row['Booking ID']}
Group Name   : {row['Group Name']}
Arrival Date : {arrival}
Hotel        : {row['Hotel']}
Guide        : {row['Guide']}
--------------------------------------------------

Please verify the following:
• Hotel reservation has been confirmed.
• Guide has been informed.
• Airport pickup (if applicable) has been arranged.
• Any special requests have been addressed.

This is an automated email. Please do not reply to this message.

Best Regards,

Reservation Management System
Makalu Adventure Travel & Tours Pvt. Ltd.
"""
        send_email(subject, body)

        df.at[index, "Reminder Sent"] = "Yes"

df.to_excel(
    BOOKING_FILE,
    sheet_name=SHEET_NAME,
    index=False
)

upload_excel()

print("Done!")