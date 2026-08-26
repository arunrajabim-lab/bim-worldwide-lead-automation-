from pathlib import Path
from . import config
from .search import search_web, domain
from .crawler import crawl_company
from .qualify import ai_score
from .storage import existing_emails, append
from .sheets import append_leads as append_to_sheet

OUT = Path("data/leads.csv")

DAILY_TARGET = 20
MIN_LEAD_SCORE = 55


def run():
    print("======================================")
    print("WORLDWIDE BIM LEAD AUTOMATION")
    print("Priority 1: SCAN TO BIM")
    print("Priority 2: CAD TO BIM")
    print("Daily target: 20 qualified companies")
    print("======================================")

    results = []
    seen_domains = set()

    # --------------------------------------------------
    # SEARCH
    # SEARCH_QUERIES is already ordered:
    # Scan to BIM first, CAD to BIM second
    # --------------------------------------------------

    for query in config.SEARCH_QUERIES:

        print(f"\nSearching: {query}")

        for region in config.REGIONS:

            print(f"  Region: {region}")

            try:
                batch = search_web(query, region)
            except Exception as e:
                print(f"  Search failed: {e}")
                continue

            for r in batch:

                url = r.get("url", "")
                d = domain(url)

                if not d:
                    continue

                # Avoid same company/domain repeatedly
                if d in seen_domains:
                    continue

                seen_domains.add(d)

                results.append((r, region))

            # Stop collecting candidates once we have enough
            # to find 20 qualified companies
            if len(results) >= 60:
                break

        if len(results) >= 60:
            break

    print(f"\nCandidates collected: {len(results)}")

    # --------------------------------------------------
    # EXISTING LEADS
    # --------------------------------------------------

    old_emails = existing_emails(OUT)

    leads = []
    seen_emails = set(old_emails)

    # --------------------------------------------------
    # PROCESS COMPANIES
    # --------------------------------------------------

    for index, (r, region) in enumerate(results, start=1):

        # Stop after 20 qualified companies
        if len(leads) >= DAILY_TARGET:
            break

        url = r.get("url", "")

        print(
            f"\n[{index}/{len(results)}] "
            f"Checking: {url}"
        )

        try:

            # ------------------------------------------
            # CRAWL COMPANY WEBSITE
            # ------------------------------------------

            crawled = crawl_company(url)

            emails = crawled.get("emails", [])

            if not emails:
                print("  No public business email found.")
                continue

            # ------------------------------------------
            # COMPANY NAME
            # ------------------------------------------

            name = (
                r.get("title")
                or domain(url)
                or "Unknown Company"
            )

            name = (
                name
                .split("|")[0]
                .split("-")[0]
                .strip()
            )

            # ------------------------------------------
            # AI / KEYWORD QUALIFICATION
            # ------------------------------------------

            q = ai_score(
                name,
                url,
                crawled.get("text", "")
            )

            score = int(
                q.get("lead_score", 0)
            )

            if score < MIN_LEAD_SCORE:
                print(
                    f"  Rejected — Lead score: {score}"
                )
                continue

            # ------------------------------------------
            # SERVICE
            # ------------------------------------------

            service = q.get(
                "service",
                "BIM / CAD services"
            )

            # ------------------------------------------
            # EMAILS
            # ------------------------------------------

            added_this_company = False

            for email in emails:

                email = email.strip().lower()

                if not email:
                    continue

                # Duplicate email protection
                if email in seen_emails:
                    continue

                # Add only one main business email
                leads.append({
                    "company_name": name,
                    "service": service,
                    "email": email,
                    "location": region,
                    "website": url,
                    "source": r.get(
                        "source",
                        "web_search"
                    ),
                    "lead_score": score,
                    "reason": q.get(
                        "reason",
                        ""
                    )
                })

                seen_emails.add(email)
                added_this_company = True

                # Only one email per company
                break

            if added_this_company:
                print(
                    f"  QUALIFIED ✓ "
                    f"{name} | Score: {score}"
                )

        except Exception as e:

            print(
                f"  Company processing failed: {e}"
            )

    # --------------------------------------------------
    # SORT BY LEAD SCORE
    # --------------------------------------------------

    leads.sort(
        key=lambda x: int(
            x.get("lead_score", 0)
        ),
        reverse=True
    )

    # --------------------------------------------------
    # FINAL LIMIT = 20
    # --------------------------------------------------

    leads = leads[:DAILY_TARGET]

    print("\n======================================")
    print(
        f"Qualified leads found: {len(leads)}"
    )
    print("======================================")

    # --------------------------------------------------
    # SAVE CSV BACKUP
    # --------------------------------------------------

    if leads:
        append(
            OUT,
            leads
        )

        # ------------------------------------------------
        # SAVE TO GOOGLE SHEET
        # ------------------------------------------------

        append_to_sheet(leads)

        print(
            f"{len(leads)} leads added to Google Sheet."
        )

    else:

        print(
            "No new qualified leads found today."
        )


if __name__ == "__main__":
    run()
