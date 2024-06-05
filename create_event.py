import datetime
import re
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar API settings
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Authenticate with Google Calendar API and return the service object."""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def read_time_slots(filename):
    """Read time slots from a file and return a list of events."""
    pattern = r'(\d{4}-\d{2}-\d{2}): (\d{1,2}:\d{2}[apm]{2})-(\d{1,2}:\d{2}[apm]{2})'
    events = []
    with open(filename, 'r') as file:
        data = file.read()
        matches = re.findall(pattern, data)
        for date, start_time, end_time in matches:
            events.append((date, start_time, end_time))
    return events

def create_event(service, date, start_time, end_time):
    """Create a single Google Calendar event."""
    start_datetime = datetime.datetime.strptime(f'{date} {start_time}', '%Y-%m-%d %I:%M%p')
    end_datetime = datetime.datetime.strptime(f'{date} {end_time}', '%Y-%m-%d %I:%M%p')
    event = {
        'summary': 'Dedicated Python Learning Time',
        'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'UTC'},
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Created event: {created_event.get("htmlLink")}')

def main():
    service = authenticate_google_calendar()
    events = read_time_slots('new.txt')
    for date, start_time, end_time in events:
        create_event(service, date, start_time, end_time)

if __name__ == '__main__':
    main()
