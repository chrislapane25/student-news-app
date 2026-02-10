import os
import requests
from datetime import datetime, timedelta

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

CACHE_DURATION = timedelta(minutes=30)
_cache = {
    "timestamp": None,
    "data": {}
}


def get_news(category=None, country="us", limit=10):
    global _cache

    cache_key = category or "general"

    # Use cache if valid
    if (
        cache_key in _cache["data"]
        and _cache["timestamp"]
        and datetime.now() - _cache["timestamp"] < CACHE_DURATION
    ):
        return _cache["data"][cache_key]

    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "pageSize": limit
    }

    if category:
        params["category"] = category

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    articles = response.json().get("articles", [])

    cleaned_articles = [
        {
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "source": a.get("source", {}).get("name"),
            "published_at": a.get("publishedAt"),
            "category": category or "general"
        }
        for a in articles
    ]

    _cache["timestamp"] = datetime.now()
    _cache["data"][cache_key] = cleaned_articles

    return cleaned_articles
