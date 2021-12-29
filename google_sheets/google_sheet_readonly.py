from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.  ### READONLY
#operation = "read"
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# If modifying these scopes, delete the file token.json. ### UPDATE
operation = "update"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']



def main():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(f'token_{operation}.json'):
        creds = Credentials.from_authorized_user_file(f'token_{operation}.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f'token_{operation}.json', 'w') as token:
            token.write(creds.to_json())

if __name__ == '__main__':
    main()