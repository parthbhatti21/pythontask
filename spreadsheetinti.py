import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID="1AVjiOZpQ-2BkywYXVFfv955FAvDGX8I7dJQBX6hDcak"

def main():
  creds = None
  mo=input("Enter mobile:")
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    creds=None
    if(os.path.exists('token.json')):
        creds=Credentials.from_authorized_user_file('token.json',SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
            creds=flow.run_local_server(port=0)
        with open('token.json','w') as token:
            token.write(creds.to_json())
  try:
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:E")
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    for row in values:
      if(row[3]=="Phone"):
         continue
      if(row[3]==mo):
         print("Exist")
         break
    else:
      print("Doesn't found!")
  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()