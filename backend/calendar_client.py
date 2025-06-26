import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        creds = pickle.load(open('token.pickle','rb'))
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.getenv('GOOGLE_CREDENTIALS'), SCOPES)
        creds = flow.run_local_server(port=0)
        pickle.dump(creds, open('token.pickle','wb'))
    return build('calendar', 'v3', credentials=creds)

def list_free_slots(start, end):
    svc = get_service()
    body = {
      "timeMin": start.isoformat(),
      "timeMax": end.isoformat(),
      "timeZone": "UTC",
      "items": [{"id": os.getenv('CALENDAR_ID')}]
    }
    freebusy = svc.freebusy().query(body=body).execute()
    busy = freebusy['calendars'][os.getenv('CALENDAR_ID')]['busy']
    # compute gaps, return suggested slots
    # ...
    return gaps

def book_event(start, end, summary):
    svc = get_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
        'end':   {'dateTime': end.isoformat(),   'timeZone': 'UTC'},
    }
    return svc.events().insert(calendarId=os.getenv('CALENDAR_ID'), body=event).execute()
