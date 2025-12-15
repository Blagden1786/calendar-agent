import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .api_stuff.path import PATH

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']  # Changed scope

def edit_event(event_id, summary=None, location=None, description=None, start_datetime=None, end_datetime=None):
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

        # Get the event and then change necessary bits
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        event = change_event(summary, location, description, start_datetime, end_datetime, event)

        service.events().update(
            calendarId="primary",
            eventId=event_id,
            body = event
        ).execute()

        return "Event updated successfully."

    except HttpError as error:
        print('An error occurred: %s' % error)

def change_event(summary, location, description, start_datetime, end_datetime, event):
    # For each argument, either use new one or keep it from old_event
    if summary != None:
        event['summary'] = summary
    if location != None:
            event['location'] = location
    if description != None:
        event['description'] = description
    if start_datetime != None:
        event['start'] = {
            'dateTime': start_datetime,
            'timeZone': 'Europe/London',
        },
    if end_datetime != None:
        event['end'] = {
            'dateTime': end_datetime,
            'timeZone': 'Europe/London',
        },

    return event

edit_event_function = {
    "type": "function",
    "name": "edit_event",
    "description": "Updates a calendar event with the specified details.",
    "parameters": {
        "type": "object",
        "properties": {
            "event_id": {
                "type": "string",
                "description": "The ID of the event to be deleted.",
            },
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
        },
        "required": ["event_id"],
    },
}
