import smtplib
from email.message import EmailMessage
from . import config

def send_report(leads):
    if not config.REPORT_TO_EMAIL:
        raise RuntimeError("REPORT_TO_EMAIL is not configured.")

    msg = EmailMessage()
    msg["Subject"] = f"BIM Lead Report - {len(leads)} new leads"
    msg["From"] = config.REPORT_FROM_EMAIL
    msg["To"] = config.REPORT_TO_EMAIL

    lines = ["New BIM / CAD-to-BIM leads found:", "",
             "Company | Service | Email | Location | Score | Website"]
    for x in leads:
        lines.append(
            f"{x['company_name']} | {x['service']} | {x['email']} | "
            f"{x['location']} | {x['lead_score']} | {x['website']}"
        )
    msg.set_content("\n".join(lines))

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as s:
        s.starttls()
        s.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        s.send_message(msg)
