from math import e
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
from .api_stuff.path import PATH
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']  # Changed scope

def delete_event(event_id):
    creds = None
    if os.path.exists(PATH + 'token.json'):
        creds = Credentials.from_authorized_user_file(PATH + 'token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                PATH + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(PATH + 'token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        events = service.events().delete(
            calendarId="primary",
            eventId=event_id,
        ).execute()

        return "Event deleted successfully."

    except HttpError as error:
        print('An error occurred: %s' % error)

# Define the function declaration for the tool
delete_event_function = {
    "name": "delete_event",
    "description": "Deletes a calendar event with the specified event ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "event_id": {
                "type": "string",
                "description": "The ID of the event to be deleted.",
            },
        },
        "required": ["event_id"],
    },
}
