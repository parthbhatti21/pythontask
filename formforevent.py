import tkinter as tk
from tkinter import ttk
from ttkbootstrap import * 
from tkinter import messagebox
from datetime import datetime
import os
import requests
import datetime
import p4
import e1
from datetime import datetime
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from requests.structures import CaseInsensitiveDict


def submit_form():
    scopes=['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar.events.readonly']
    allevents=[]
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
    des = title_entry.get()
    start_datetime = start_datetime_entry.get()
    end_datetime = end_datetime_entry.get()
    email=email_entry.get()
    
    if not des:
        messagebox.showerror("Error", "Please enter the event title.")
        return
    if not email:
        messagebox.showerror("Error", "Please enter the email.")
        return
    try:
        start_datetime = datetime.strptime(start_datetime, "%d/%m/%y %H:%M")
        end_datetime = datetime.strptime(end_datetime, "%d/%m/%y %H:%M")
        if start_datetime >= end_datetime:
            messagebox.showerror("Error", "Ending datetime should be after starting datetime.")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid datetime format. Please use DD/MM/YY HH:MM.")
        return
    
    
    print("Event Title:", des)
    print("Starting Datetime:", start_datetime)
    print("Ending Datetime:", end_datetime)
    print(email)
    start_form=start_datetime.isoformat()+'+05:30'
    end_form=end_datetime.isoformat()+'+05:30'
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
    e1.email(start_datetime,end_datetime,email,des)
    title_entry.delete(0, tk.END)
    start_datetime_entry.delete(0, tk.END)
    end_datetime_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

root=Window(themename="darkly")  
root.geometry("500x500")
root.title("Event Form")
title_label = ttk.Label(root, text="Event Title:")
title_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
title_entry = ttk.Entry(root)
title_entry.grid(row=0, column=1, padx=5, pady=5)
start_datetime_label = ttk.Label(root, text="Starting Datetime (DD/MM/YY HH:MM):")
start_datetime_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
start_datetime_entry = ttk.Entry(root)
start_datetime_entry.grid(row=1, column=1, padx=5, pady=5)
end_datetime_label = ttk.Label(root, text="Ending Datetime (DD/MM/YY HH:MM):")
end_datetime_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
end_datetime_entry = ttk.Entry(root)
end_datetime_entry.grid(row=2, column=1, padx=5, pady=5)
email_label = ttk.Label(root, text="Email")
email_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
email_entry = ttk.Entry(root)
email_entry.grid(row=3, column=1, padx=5, pady=5)
submit_button = ttk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
