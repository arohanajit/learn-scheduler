from __future__ import print_function
import os
import pickle
import datetime
import csv
import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Saves the start and name of all events on the user's calendars within the next two weeks in ascending order by time to a CSV file."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            flow.run_local_server(port=63633)
            creds = flow.credentials
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

    # List all calendars
    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])

    if not calendars:
        print('No calendars found.')
        return

    all_events = []

    for calendar in calendars:
        calendar_id = calendar['id']
        calendar_name = calendar['summary']
        print(f'Fetching events for calendar: {calendar_name} (ID: {calendar_id})')

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        two_weeks_from_now = (datetime.datetime.utcnow() + datetime.timedelta(weeks=2)).isoformat() + 'Z'

        events_result = service.events().list(calendarId=calendar_id, timeMin=now, timeMax=two_weeks_from_now,
                                              singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if events:
            for event in events:
                event['calendarName'] = calendar_name
                all_events.append(event)

    # Sort all events by start time
    all_events.sort(key=lambda x: x['start'].get('dateTime', x['start'].get('date')))

    # Save events to CSV
    with open('events.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Start', 'Summary', 'Calendar'])

        for event in all_events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event['summary']
            calendar_name = event['calendarName']
            writer.writerow([start, summary, calendar_name])

    print('Events saved to events.csv')

if __name__ == '__main__':
    main()