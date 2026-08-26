# Worldwide BIM / CAD-to-BIM Lead Automation

Searches public web results, checks public company pages for business emails, qualifies leads, deduplicates them, keeps a CSV backup, and appends new leads to Google Sheets.

Google Sheet columns:
Company Name | Service | Email ID | Location | Website | Lead Score | Reason | Source | Date Found

Required GitHub Secrets:
SEARCH_API_KEY
SEARCH_API_URL
OPENAI_API_KEY (optional)
AI_MODEL (optional)
GOOGLE_SERVICE_ACCOUNT_JSON
GOOGLE_SHEET_ID

SMTP/email secrets are not required.

Google setup:
1. Enable Google Sheets API and Google Drive API.
2. Create a service account.
3. Share the Google Sheet with the service-account email as Editor.
4. Create a JSON key.
5. Put the complete JSON content in GOOGLE_SERVICE_ACCOUNT_JSON.
6. Put the spreadsheet ID in GOOGLE_SHEET_ID.

Run manually from GitHub Actions -> Daily BIM Lead Search -> Run workflow.

The workflow also runs daily at 09:00 UTC (14:30 IST).

Use only public business information and permitted search/API access. Do not automate LinkedIn login or bypass restrictions. Follow applicable privacy, website terms, and anti-spam rules.
