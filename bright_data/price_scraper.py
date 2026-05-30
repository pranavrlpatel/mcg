import requests
import os

BRIGHT_DATA_TOKEN = os.environ.get("BRIGHT_DATA_TOKEN", "mock_token")
UNLOCKER_ZONE = os.environ.get("UNLOCKER_ZONE", "mock_zone")
METALS_API_KEY = os.environ.get("METALS_API_KEY", "mock_key")
DEMO_MODE = os.environ.get("DEMO_MODE", "false").lower() == "true"

BASELINE_ALUMINUM = 2237.0  # USD/tonne — recalibrate from your data download

def get_lme_aluminum_price() -> float | None:
    """
    Fetches live aluminum spot price directly from metals-api.
    Returns price in USD/tonne or None on failure.
    """
    if DEMO_MODE or METALS_API_KEY == "mock_key":
        # Return a mocked spike for demo
        return BASELINE_ALUMINUM * 1.112 # 11.2% spike

    return _direct_metals_api_call()

def _direct_metals_api_call() -> float | None:
    try:
        resp = requests.get(
            f"https://metals-api.com/api/latest",
            params={"access_key": METALS_API_KEY, "base": "USD", "symbols": "ALU"},
            timeout=15
        )
        data = resp.json()
        alu_per_oz = data["rates"]["ALU"]
        return round(1 / alu_per_oz * 32150.7, 2)
    except Exception as e:
        print(f"[price_scraper] Direct API also failed: {e}")
        return None

def compute_shock_pct(live_price: float) -> float:
    return round((live_price - BASELINE_ALUMINUM) / BASELINE_ALUMINUM, 4)
