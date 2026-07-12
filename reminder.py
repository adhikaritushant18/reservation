import pandas as pd
from datetime import datetime, timedelta

from google_drive import download_excel, upload_excel
from email_service import send_email
from config import *
from openpyxl import load_workbook

# Download latest Excel from Google Drive
download_excel()

# Read Arrival Dates sheet
df = pd.read_excel(
    BOOKING_FILE,
    sheet_name="Arrival Dates"
)
df["Reminder sent at"] = df["Reminder sent at"].astype("object")

tomorrow = datetime.today().date() + timedelta(days=1)

for index, row in df.iterrows():

    arrival = pd.to_datetime(row["Arrival Date"]).date()

    reminder = str(row["Reminder Sent"]).strip().lower()

    if arrival == tomorrow and reminder != "yes":

        subject = (
            f"Automated Arrival Reminder | "
            f"{row['Group Name']} | {arrival.strftime('%d-%b-%Y')}"
        )

        body = f"""
Dear Reservation Team,

This is an automated reminder from the Reservation Management System.

The following guest is arriving tomorrow.

------------------------------------------------------------

Booking ID      : {row['Booking ID']}

Trip Name       : {row['Trip Name']}

Group Name      : {row['Group Name']}

Agency          : {row['Agency']}

Guest Name      : {row['Guest name']}

Pax             : {row['Pax']}

Arrival Date    : {row['Arrival Date']}

Arrival Time    : {row['Arrival Time']}

Flight No       : {row['Flight no']}

Hotel           : {row['Hotel']}

Airport Pickup  : {row['Airport pickup']}

------------------------------------------------------------

Please verify:

✓ Hotel reservation confirmed

✓ Airport pickup arranged

✓ Guide informed

✓ Guest arrival prepared

This is an automated email.

Reservation Management System
Makalu Adventure Travel & Tours Pvt. Ltd.
"""

        send_email(subject, body)

        df.at[index, "Reminder Sent"] = "Yes"
        df.at[index, "Reminder sent at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

# Save updated workbook
book = load_workbook(BOOKING_FILE)

with pd.ExcelWriter(
    BOOKING_FILE,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:
    df.to_excel(
        writer,
        sheet_name="Arrival Dates",
        index=False
    )

# Upload updated workbook
upload_excel()

print("Reminder process completed successfully.")