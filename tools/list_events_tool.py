import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
from path import PATH
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']  # Changed scope

def list_events(time_from, time_to):
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

        # List next events
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        events = service.events().list(
            calendarId="primary",
            timeMin=time_from,
            timeMax=time_to,
            timeZone = "Europe/London",
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        return events

    except HttpError as error:
        print('An error occurred: %s' % error)

# Define the function declaration for the tool
list_events_function = {
    "name": "list_events",
    "description": "Lists calendar events within the specified time range.",
    "parameters": {
        "type": "object",
        "properties": {
            "time_from": {
                "type": "string",
                "description": "The start date and time of the event in ISO format (e.g., '2024-07-29T15:00:00Z').",
            },
            "time_to": {
                "type": "string",
                "description": "The end date and time of the event in ISO format (e.g., '2024-07-29T16:00:00Z').",
            },
        },
        "required": ["time_from", "time_to"],
    },
}
