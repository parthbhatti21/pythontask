import os
import requests
import datetime
from datetime import datetime
import json
import e1
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from requests.structures import CaseInsensitiveDict

data=[]
scopes=['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar.events.readonly']
allevents=[]
def main():
    creds=None
    if(os.path.exists('token.json')):
        creds=Credentials.from_authorized_user_file('token.json',scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('client_secret.json',scopes)
            creds=flow.run_local_server(port=0)
        with open('token.json','w') as token:
            token.write(creds.to_json())
    service= build('calendar','v3',credentials=creds)
    now=datetime.utcnow().isoformat()+'z'
    event=service.events().list(calendarId='primary',timeMin=now,singleEvents=True,orderBy='startTime').execute()
    allevents=event.get('items',[])
    if(not allevents):
        print("No events")
        return
    else:
        j=0
        for i in allevents:
            start=i['start'].get('dateTime',i['start'].get('date'))
            print("Task",j+1,":",i['summary'],",Time:",start)
            j+=1
        addevent(creds)

def addevent(creds):
    start=(input("Enter Time in (dd/mm/yy 00:00) format:"))
    datetime_object = datetime.strptime(start, '%d/%m/%y %H:%M')
    end=(input("Enter Finishing Time in (dd/mm/yy 00:00) format:"))
    datetime_object1 = datetime.strptime(end, '%d/%m/%y %H:%M')
    start_form=datetime_object.isoformat()+'+05:30'
    end_form=datetime_object1.isoformat()+'+05:30'
    print(end_form)
    des=input("Enter title:")
    # start_form=datetime.isoformat(datetime_object)+'Z'
    # end_form=datetime.isoformat(datetime_object1)+'Z'
    event={
        'summary':des,
        'start': {'dateTime': start_form, 'timeZone': 'Asia/Kolkata'},
          'end': {'dateTime': end_form, 'timeZone': 'Asia/Kolkata'},
    }
    service= build('calendar','v3',credentials=creds)
    event1=service.events().insert(calendarId='primary',body=event).execute()
    print("Event created")

    

if __name__ == '__main__':
    main()