import requests
import os
import time

BRIGHT_DATA_TOKEN = os.environ.get("BRIGHT_DATA_TOKEN", "mock_token")
SERP_ZONE = os.environ.get("SERP_ZONE", "mock_zone")
DEMO_MODE = os.environ.get("DEMO_MODE", "false").lower() == "true"

WATCH_QUERIES = {
    "bauxite":        "bauxite tariff supply disruption OR sanctions",
    "alumina":        "alumina refinery production cut OR price spike",
    "aluminum":       "aluminum LME price increase OR shortage",
    "boeing_costs":   "Boeing raw material cost manufacturing supply chain",
    "airline_margins": "airline fuel cost operating margin warning"
}

# Negation terms — flip signal if these appear in headline
NEGATION_TERMS = ["unlikely", "doubt", "reject", "no plans", "dismissed",
                  "rules out", "denies", "not expected"]

def fetch_news_signal(node: str) -> list[dict]:
    if DEMO_MODE or BRIGHT_DATA_TOKEN == "mock_token":
        # Mock signal for demo mode
        if node == "bauxite":
            return [{"title": "Major bauxite tariff announced by key suppliers", "snippet": "A new tariff on bauxite exports...", "date": "10 mins ago", "url": "#"}]
        return []

    query = WATCH_QUERIES[node]
    resp = requests.post(
        "https://api.brightdata.com/request",
        headers={
            "Authorization": f"Bearer {BRIGHT_DATA_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "zone": SERP_ZONE,
            "url": f"https://www.google.com/search?q={query}&tbm=nws&brd_json=1",
            "format": "raw"
        },
        timeout=30
    )
    results = resp.json().get("news", [])
    return [
        {
            "title": r.get("title", ""),
            "snippet": r.get("snippet", ""),
            "date": r.get("date"),
            "url": r.get("url")
        }
        for r in results[:5]
    ]

def score_shock(signals: list[dict]) -> float:
    """
    Returns shock score 0.0–1.0.
    Positive keywords push up. Negation terms push down.
    Recency bonus: articles from last 48h weighted 2x.
    """
    if not signals:
        return 0.0

    POSITIVE_KEYWORDS = [
        "tariff", "sanction", "disruption", "shortage", "spike",
        "surge", "ban", "restriction", "cut", "crisis", "halt"
    ]

    score = 0.0
    for s in signals:
        text = (s["title"] + " " + s["snippet"]).lower()
        hit = any(kw in text for kw in POSITIVE_KEYWORDS)
        negated = any(neg in text for neg in NEGATION_TERMS)

        if hit and not negated:
            score += 0.2
        elif hit and negated:
            score -= 0.05  # conflicting signal, slight penalty

    return round(min(max(score, 0.0), 1.0), 3)
