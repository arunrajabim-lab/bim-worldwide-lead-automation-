import requests
from urllib.parse import urlparse
from . import config


def search_web(query, region=None):

    if not config.SEARCH_API_KEY:
        raise RuntimeError(
            "SEARCH_API_KEY is not configured."
        )

    # Region is added to the Google search query
    q = query

    if region:
        q = f"{query} {region}"

    params = {
        "engine": "google",
        "q": q,
        "api_key": config.SEARCH_API_KEY,
        "num": config.MAX_RESULTS_PER_QUERY,
    }

    try:

        response = requests.get(
            config.SEARCH_API_URL,
            params=params,
            timeout=config.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.Timeout:

        print(
            f"Search timeout: {query} | {region}"
        )

        return []

    except requests.exceptions.RequestException as e:

        print(
            f"Search API error: {e}"
        )

        return []

    # -----------------------------------------
    # Extract organic Google results
    # -----------------------------------------

    results = []

    for item in data.get(
        "organic_results",
        []
    ):

        url = item.get(
            "link",
            ""
        )

        if not url:
            continue

        results.append({

            "title": item.get(
                "title",
                ""
            ),

            "snippet": item.get(
                "snippet",
                ""
            ),

            "url": url,

            "source": "SerpAPI / Google"
        })

    return results


def domain(url):

    try:

        parsed = urlparse(url)

        hostname = parsed.netloc.lower()

        if hostname.startswith("www."):
            hostname = hostname[4:]

        return hostname

    except Exception:

        return ""
