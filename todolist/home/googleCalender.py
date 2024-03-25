import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    # Initialize credentials to None
    creds = None

    # If token.json exists, load the credentials from the file
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds

def get_service():
    # Get the credentials
    creds = get_credentials()

    # Build the service
    service = build("calendar", "v3", credentials=creds)
    
    return service

def create_event(title, desc, date):
    print(f"Creating event with title: {title}, description: {desc}, date: {date}")

    # Get the service
    service = get_service()

    # Define the event
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

    # Call the Calendar API to create the event
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')
    
    #return the event id
    return event['id']

def update_event(event_id, title, desc, date):
    print(f"Updating event with id: {event_id}, title: {title}, description: {desc}, date: {date}")

    # Get the service
    service = get_service()

    # Define the updated event
    event = service.events().get(calendarId='primary', eventId=event_id).execute()

    event['summary'] = title
    event['description'] = desc
    event['start']['dateTime'] = date
    event['end']['dateTime'] = date

    # Call the Calendar API to update the event
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    print(f'Event updated: {updated_event.get("htmlLink")}')

def delete_event(event_id):
    print(f"Deleting event with id: {event_id}")

    # Get the service
    service = get_service()
    try:
        # Call the Calendar API to delete the event
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print('Event deleted')
    except HttpError as error:
        print(f"An error occurred: {error}")