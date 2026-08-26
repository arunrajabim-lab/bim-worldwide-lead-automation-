import os, json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
HEADERS = ["Company Name","Service","Email ID","Location","Website","Lead Score","Reason","Source","Date Found"]

def append_leads(leads):
    if not leads:
        return
    raw = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    creds = Credentials.from_service_account_info(json.loads(raw), scopes=SCOPES)
    client = gspread.authorize(creds)
    ws = client.open_by_key(sheet_id).sheet1
    if not ws.row_values(1):
        ws.append_row(HEADERS, value_input_option="USER_ENTERED")
    from datetime import datetime, timezone
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rows = [[x.get("company_name",""), x.get("service",""), x.get("email",""),
             x.get("location",""), x.get("website",""), x.get("lead_score",""),
             x.get("reason",""), x.get("source",""), date] for x in leads]
    ws.append_rows(rows, value_input_option="USER_ENTERED")
