

import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


credentials_path = os.path.join('credentials', 'credentials.json')

load_dotenv()

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

RANGE_NAME_BILLING = 'Billing!A1:G'
RANGE_NAME_ATTENDANCE = 'Attendance!A1:D'
RANGE_NAME_STUDENT_INFO = 'StudentInformation!A1:I'

def get_sheets_service():
    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

def get_sheet_data(range_name):
    service = get_sheets_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    return values

def update_sheet_data(range_name, values):
    service = get_sheets_service()
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption="RAW", body=body).execute()
    return result



