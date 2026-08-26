import csv
from pathlib import Path

FIELDS = ["company_name","service","email","location","website",
          "source","lead_score","reason"]

def existing_emails(path):
    if not path.exists():
        return set()
    with path.open(encoding="utf-8", newline="") as f:
        return {r["email"].lower() for r in csv.DictReader(f) if r.get("email")}

def append(path, leads):
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerows({k:x.get(k,"") for k in FIELDS} for x in leads)
