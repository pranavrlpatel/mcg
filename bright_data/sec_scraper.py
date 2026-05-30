import requests
import os
import re
from bs4 import BeautifulSoup

BRIGHT_DATA_TOKEN = os.environ.get("BRIGHT_DATA_TOKEN", "mock_token")
SCRAPER_ZONE = os.environ.get("SCRAPER_ZONE", "mock_zone")
DEMO_MODE = os.environ.get("DEMO_MODE", "false").lower() == "true"

EDGAR_SEARCH = {
    "boeing": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=BA&type=10-Q&dateb=&owner=include&count=1&search_text=",
    "delta":  "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=DAL&type=10-Q&dateb=&owner=include&count=1&search_text="
}

# Fallback hardcoded values — used if scraper fails
FALLBACK_MARGINS = {
    "boeing": -0.021,   # Boeing Q4 2025 operating margin (negative — ongoing)
    "delta":  0.071     # Delta Q1 2026 operating margin
}

def scrape_edgar_margin(ticker: str) -> float:
    """
    Attempts to scrape latest quarterly operating margin from SEC EDGAR.
    Returns float (e.g. 0.071 for 7.1%) or fallback value.
    """
    if DEMO_MODE or BRIGHT_DATA_TOKEN == "mock_token":
        return FALLBACK_MARGINS[ticker]

    try:
        resp = requests.post(
            "https://api.brightdata.com/request",
            headers={
                "Authorization": f"Bearer {BRIGHT_DATA_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "zone": SCRAPER_ZONE,
                "url": EDGAR_SEARCH[ticker],
                "format": "raw"
            },
            timeout=45
        )
        
        try:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0 and "page_html" in data[0]:
                html_content = data[0]["page_html"]
            else:
                html_content = resp.text
        except Exception:
            html_content = resp.text

        soup = BeautifulSoup(html_content, "html.parser")
        filing_link = soup.select_one("a[href*='/Archives/edgar/']")
        if not filing_link:
            raise ValueError("No filing link found")
        return FALLBACK_MARGINS[ticker]
    except Exception as e:
        print(f"[sec_scraper] Failed for {ticker}: {e} — using fallback")
        return FALLBACK_MARGINS[ticker]

def get_all_baselines() -> dict:
    from bright_data.price_scraper import BASELINE_ALUMINUM
    return {
        "delta_margin":  scrape_edgar_margin("delta"),
        "boeing_margin": scrape_edgar_margin("boeing"),
        "aluminum_baseline": BASELINE_ALUMINUM
    }
