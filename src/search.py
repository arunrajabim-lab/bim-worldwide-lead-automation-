import requests
from urllib.parse import urlparse
from . import config

def search_web(query, region=None):
    if not config.SEARCH_API_KEY:
        raise RuntimeError("SEARCH_API_KEY is not configured.")
    q = query if not region else f"{query} {region}"
    params = {
        "engine": "google", "q": q, "api_key": config.SEARCH_API_KEY,
        "num": config.MAX_RESULTS_PER_QUERY
    }
    r = requests.get(config.SEARCH_API_URL, params=params,
                     timeout=config.REQUEST_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return [
        {"title": x.get("title",""), "snippet": x.get("snippet",""),
         "url": x.get("link",""), "source": "web_search"}
        for x in data.get("organic_results", []) if x.get("link")
    ]

def domain(url):
    try:
        return urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""
