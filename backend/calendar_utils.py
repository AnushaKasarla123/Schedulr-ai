from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    token_file = 'token.json'

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def list_events(start_time_str, end_time_str):
    service = get_calendar_service()
    
    # Query events between start_time and end_time
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time_str,
        timeMax=end_time_str,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return events  # Return the list of conflicting events (if any)

def create_event(summary, start_time_str, end_time_str):
    try:
        service = get_calendar_service()
        event = {
            'summary': summary,
            'start': {'dateTime': start_time_str, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_time_str, 'timeZone': 'Asia/Kolkata'},
        }
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print("✅ Event created:", created_event.get("htmlLink"))
        return created_event.get("htmlLink")
    except Exception as e:
        print("❌ Event creation failed:", e)
        return None
def delete_event(start_time, end_time):
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        return False  # Nothing to delete

    for event in events:
        service.events().delete(calendarId='primary', eventId=event['id']).execute()
    return True
