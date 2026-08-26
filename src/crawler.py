import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from . import config

EMAIL_RE = re.compile(r'(?i)\b[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}\b')
PATHS = ["/", "/contact", "/contact-us", "/about", "/services",
         "/bim", "/bim-services", "/bim-outsourcing"]

def fetch(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; BIMLeadResearchBot/1.0)"}
    r = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT,
                     allow_redirects=True)
    r.raise_for_status()
    return r.url, r.text

def extract_emails(html):
    return sorted(set(EMAIL_RE.findall(html)))

def text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return " ".join(soup.stripped_strings)

def crawl_company(start_url):
    try:
        final_url, html = fetch(start_url)
    except Exception:
        return {"emails": [], "text": ""}

    soup = BeautifulSoup(html, "html.parser")
    urls = [final_url.rstrip("/") + p for p in PATHS]
    for a in soup.find_all("a", href=True):
        label = a.get_text(" ", strip=True).lower()
        if any(k in label for k in ["contact", "about", "bim", "service"]):
            urls.append(urljoin(final_url, a["href"]))

    seen, emails, texts = set(), set(), []
    for u in urls[:10]:
        if u in seen:
            continue
        seen.add(u)
        try:
            real, body = fetch(u)
            emails.update(extract_emails(body))
            texts.append(text(body))
        except Exception:
            pass

    return {"emails": sorted(emails), "text": "\n".join(texts)[:30000]}
