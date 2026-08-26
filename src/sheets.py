import os
import json
import gspread

from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


HEADERS = [
    "Company Name",
    "Service",
    "Email ID",
    "Location",
    "Website",
    "Lead Score",
    "Reason",
    "Source",
    "Date Found",
]


def append_leads(leads):

    if not leads:
        print("No leads to save to Google Sheet.")
        return

    # -----------------------------------------
    # Check required GitHub Secrets
    # -----------------------------------------

    raw = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_JSON",
        ""
    )

    sheet_id = os.getenv(
        "GOOGLE_SHEET_ID",
        ""
    )

    if not raw:
        raise RuntimeError(
            "GOOGLE_SERVICE_ACCOUNT_JSON is not configured."
        )

    if not sheet_id:
        raise RuntimeError(
            "GOOGLE_SHEET_ID is not configured."
        )

    # -----------------------------------------
    # Authenticate Google Service Account
    # -----------------------------------------

    try:

        service_account_info = json.loads(raw)

        credentials = (
            Credentials
            .from_service_account_info(
                service_account_info,
                scopes=SCOPES
            )
        )

        client = gspread.authorize(
            credentials
        )

    except Exception as e:

        raise RuntimeError(
            f"Google authentication failed: {e}"
        )

    # -----------------------------------------
    # Open Google Sheet
    # -----------------------------------------

    try:

        spreadsheet = client.open_by_key(
            sheet_id
        )

        worksheet = spreadsheet.sheet1

    except Exception as e:

        raise RuntimeError(
            f"Could not open Google Sheet: {e}"
        )

    # -----------------------------------------
    # Create header row if empty
    # -----------------------------------------

    try:

        if not worksheet.row_values(1):

            worksheet.append_row(
                HEADERS,
                value_input_option="USER_ENTERED"
            )

    except Exception as e:

        raise RuntimeError(
            f"Could not create Google Sheet headers: {e}"
        )

    # -----------------------------------------
    # Prepare rows
    # -----------------------------------------

    from datetime import datetime, timezone

    date_found = (
        datetime.now(timezone.utc)
        .strftime("%Y-%m-%d")
    )

    rows = []

    for lead in leads:

        rows.append([
            lead.get(
                "company_name",
                ""
            ),

            lead.get(
                "service",
                ""
            ),

            lead.get(
                "email",
                ""
            ),

            lead.get(
                "location",
                ""
            ),

            lead.get(
                "website",
                ""
            ),

            lead.get(
                "lead_score",
                ""
            ),

            lead.get(
                "reason",
                ""
            ),

            lead.get(
                "source",
                ""
            ),

            date_found,
        ])

    # -----------------------------------------
    # Append to Google Sheet
    # -----------------------------------------

    try:

        worksheet.append_rows(
            rows,
            value_input_option="USER_ENTERED"
        )

        print(
            f"SUCCESS: {len(rows)} leads "
            "saved to Google Sheet."
        )

    except Exception as e:

        raise RuntimeError(
            f"Could not write to Google Sheet: {e}"
        )
