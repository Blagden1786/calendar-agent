import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .api_stuff.path import PATH
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']  # Changed scope


def create_event(summary,  start_datetime, end_datetime, location="", description="", colour=''):
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
            'colorId' : colour,
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
        return f"Event created successfully"

    except HttpError as error:
        print('An error occurred: %s' % error)

# Define the function declaration for the tool
create_event_function = {
    "type": "function",
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
                "description": "The start date and time of the event in ISO format (e.g., '2024-07-29T15:00:00Z')",
            },
            "end_datetime": {
                "type": "string",
                "description": "The end date and time of the event in ISO format (e.g., '2024-07-29T16:00:00Z')",
            },
            'colour' : {
                'type': 'string',
                'description': 'The colour of the event. To assign a colour follow this logic: If it is sport related give it "8", if it is work related give it "3". Otherwise, pass no argument'
            }
        },
        "required": ["summary", "start_datetime", "end_datetime"],
    },
}

def create_allday_event(summary,  start_date, end_date, location="", description="", colour=''):
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
            'colorId' : colour,
            'start': {
                'date': start_date,
                'timeZone': 'Europe/London',
            },
            'end': {
                'date': end_date,
                'timeZone': 'Europe/London',
            },
            'reminders': {
                'useDefault': False,
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created successfully"

    except HttpError as error:
        print('An error occurred: %s' % error)

# Define the function declaration for the tool
create_allday_event_function = {
    "type": "function",
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
                "description": "The start date and time of the event in the format yyyy-mm-dd (e.g., '2024-07-29')",
            },
            "end_datetime": {
                "type": "string",
                "description": "The end date and time of the event in the format yyyy-mm-dd (e.g., '2024-07-29')",
            },
            'colour' : {
                'type': 'string',
                'description': 'The colour of the event. To assign a colour follow this logic: If it is sport related give it "8", if it is work related give it "3". Otherwise, pass no argument'
            }
        },
        "required": ["summary", "start_datetime", "end_datetime"],
    },
}
