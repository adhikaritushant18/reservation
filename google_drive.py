import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io

# Google credentials file
SERVICE_ACCOUNT_FILE = "credentials.json"

# File ID from GitHub Secret or local environment
FILE_ID = os.getenv("GOOGLE_DRIVE_FILE_ID")

# Local file name
LOCAL_FILE = "booking.xlsx"


def get_drive_service():
    """Create Google Drive service."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive"]
    )

    service = build("drive", "v3", credentials=credentials)
    return service


def download_excel():
    """Download booking.xlsx from Google Drive."""

    service = get_drive_service()

    request = service.files().get_media(fileId=FILE_ID)

    file = io.BytesIO()

    downloader = MediaIoBaseDownload(file, request)

    done = False

    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloading... {int(status.progress() * 100)}%")

    with open(LOCAL_FILE, "wb") as f:
        f.write(file.getvalue())

    print("Downloaded booking.xlsx")


def upload_excel():
    """Upload updated booking.xlsx back to Google Drive."""

    service = get_drive_service()

    media = MediaFileUpload(
        LOCAL_FILE,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    service.files().update(
        fileId=FILE_ID,
        media_body=media
    ).execute()

    print("Uploaded updated booking.xlsx")