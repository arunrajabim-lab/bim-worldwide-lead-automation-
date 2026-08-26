from pathlib import Path
from . import config
from .search import search_web, domain
from .crawler import crawl_company
from .qualify import ai_score
from .storage import existing_emails, append
from .sheets import append_leads as append_to_sheet

OUT = Path("data/leads.csv")

def run():
    results, seen = [], set()
    for query in config.SEARCH_QUERIES:
        for region in config.REGIONS:
            try:
                batch = search_web(query, region)
            except Exception as e:
                print("Search failed:", e)
                continue
            for r in batch:
                d = domain(r["url"])
                if d and d not in seen:
                    seen.add(d)
                    results.append((r, region))
            if len(results) >= config.MAX_COMPANIES:
                break
        if len(results) >= config.MAX_COMPANIES:
            break

    old = existing_emails(OUT)
    leads = []
    for r, region in results:
        try:
            crawled = crawl_company(r["url"])
            if not crawled["emails"]:
                continue
            name = (r.get("title") or domain(r["url"])).split("|")[0].split("-")[0].strip()
            q = ai_score(name, r["url"], crawled["text"])
            if int(q.get("lead_score", 0)) < 55:
                continue
            for email in crawled["emails"]:
                email = email.lower()
                if email in old:
                    continue
                leads.append({
                    "company_name": name,
                    "service": q.get("service", "BIM / CAD services"),
                    "email": email,
                    "location": region,
                    "website": r["url"],
                    "source": r.get("source", "web_search"),
                    "lead_score": q.get("lead_score", 0),
                    "reason": q.get("reason", "")
                })
                old.add(email)
        except Exception as e:
            print("Company processing failed:", r.get("url"), e)

    leads.sort(key=lambda x: int(x["lead_score"]), reverse=True)
    append(OUT, leads)
    if leads:
        append_to_sheet(leads)
    print(f"New qualified leads added: {len(leads)}")

if __name__ == "__main__":
    run()
