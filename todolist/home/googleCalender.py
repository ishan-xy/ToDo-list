import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def create_event(title, desc, date):
    print(f"Creating event with title: {title}, description: {desc}, date: {date}")
    """Creates an event on the user's calendar."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        print("Service built successfully")
        # Call the Calendar API to create an event
        
        event = {
            'summary': title,
            'description': desc,
            'start': {
                'dateTime': date,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': date,
                'timeZone': 'Asia/Kolkata',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')
        
    except HttpError as error:
        print(f"An error occurred: {error}")