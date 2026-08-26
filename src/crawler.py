import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from . import config

EMAIL_RE = re.compile(
    r'(?i)\b[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}\b'
)

PATHS = [
    "/",
    "/contact",
    "/contact-us",
    "/about",
    "/services",
    "/bim",
    "/bim-services",
    "/bim-outsourcing",
    "/scan-to-bim",
    "/cad-to-bim",
]


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(compatible; BIMLeadResearchBot/1.0)"
    )
}


def fetch(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=config.REQUEST_TIMEOUT,
            allow_redirects=True
        )

        response.raise_for_status()

        return response.url, response.text

    except Exception as e:

        print(f"  Website fetch failed: {url} | {e}")

        return "", ""


def extract_emails(html):

    if not html:
        return []

    emails = EMAIL_RE.findall(html)

    # Remove obvious non-contact / technical emails
    excluded = [
        "example.com",
        "yourdomain.com",
        "domain.com",
        "sentry.io",
    ]

    clean = []

    for email in emails:

        email = email.lower().strip()

        if any(x in email for x in excluded):
            continue

        clean.append(email)

    return sorted(set(clean))


def extract_text(html):

    if not html:
        return ""

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for tag in soup(
        ["script", "style", "noscript", "svg"]
    ):
        tag.decompose()

    return " ".join(
        soup.stripped_strings
    )


def same_domain(url1, url2):

    try:

        d1 = urlparse(url1).netloc.lower()
        d2 = urlparse(url2).netloc.lower()

        return (
            d1.replace("www.", "")
            == d2.replace("www.", "")
        )

    except Exception:

        return False


def crawl_company(start_url):

    final_url, html = fetch(start_url)

    if not html:
        return {
            "emails": [],
            "text": ""
        }

    base_url = final_url.rstrip("/")

    # -----------------------------------------
    # Start with important known pages
    # -----------------------------------------

    urls = []

    for path in PATHS:

        urls.append(
            urljoin(base_url + "/", path.lstrip("/"))
        )

    # -----------------------------------------
    # Discover useful links from homepage
    # -----------------------------------------

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for a in soup.find_all(
        "a",
        href=True
    ):

        label = a.get_text(
            " ",
            strip=True
        ).lower()

        href = a.get("href", "")

        if not href:
            continue

        # Only useful business pages
        if any(
            keyword in label
            for keyword in [
                "contact",
                "about",
                "service",
                "bim",
                "scan",
                "cad",
                "revit",
            ]
        ):

            full_url = urljoin(
                final_url,
                href
            )

            if same_domain(
                final_url,
                full_url
            ):
                urls.append(full_url)

    # -----------------------------------------
    # Remove duplicates
    # -----------------------------------------

    unique_urls = []

    seen_urls = set()

    for url in urls:

        normalized = url.rstrip("/")

        if normalized in seen_urls:
            continue

        seen_urls.add(normalized)

        unique_urls.append(normalized)

    # -----------------------------------------
    # Crawl relevant pages
    # -----------------------------------------

    emails = set()
    texts = []

    for url in unique_urls:

        try:

            real_url, body = fetch(url)

            if not body:
                continue

            page_emails = extract_emails(body)

            emails.update(page_emails)

            page_text = extract_text(body)

            if page_text:
                texts.append(page_text)

        except Exception as e:

            print(
                f"  Page skipped: {url} | {e}"
            )

    # -----------------------------------------
    # Return combined company information
    # -----------------------------------------

    return {
        "emails": sorted(emails),
        "text": "\n".join(texts)[:30000]
    }
