import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from path import PATH
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']  # Changed scope


def create_event(summary,  start_datetime, end_datetime, location="", description=""):
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

        # Create an event
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'Europe/London',
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': 'Europe/London',
            },
            'reminders': {
                'useDefault': False,
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event.get('htmlLink')}"

    except HttpError as error:
        print('An error occurred: %s' % error)

# Define the function declaration for the tool
create_event_function = {
    "name": "create_event",
    "description": "Creates a calendar event with the specified details.",
    "parameters": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "The summary or title of the event.",
            },
            "location": {
                "type": "string",
                "description": "The location of the event.",
            },
            "description": {
                "type": "string",
                "description": "A description of the event.",
            },
            "start_datetime": {
                "type": "string",
                "description": "The start date and time of the event in ISO format (e.g., '2024-07-29T15:00:00Z'). When no time given just use the date part (eg '2025-12-25)",
            },
            "end_datetime": {
                "type": "string",
                "description": "The end date and time of the event in ISO format (e.g., '2024-07-29T16:00:00Z'). When no time given just use the date part (eg '2025-12-25)",
            },
        },
        "required": ["summary", "start_datetime", "end_datetime"],
    },
}
