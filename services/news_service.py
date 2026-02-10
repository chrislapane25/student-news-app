import os
import requests
from datetime import datetime, timedelta

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

CACHE_DURATION = timedelta(minutes=30)
_cache = {
    "timestamp": None,
    "data": None
}


def fetch_news(category=None, country="us"):
    global _cache

    # Use cache if valid
    if _cache["timestamp"] and datetime.now() - _cache["timestamp"] < CACHE_DURATION:
        return _cache["data"]

    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "pageSize": 10
    }

    if category:
        params["category"] = category

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    articles = response.json().get("articles", [])

    cleaned_articles = [
        {
            "title": a["title"],
            "description": a["description"],
            "url": a["url"],
            "source": a["source"]["name"],
            "published_at": a["publishedAt"]
        }
        for a in articles
    ]

    _cache["timestamp"] = datetime.now()
    _cache["data"] = cleaned_articles

    return cleaned_articles
