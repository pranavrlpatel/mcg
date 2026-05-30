# Shared mutable state between signal loop and API
# In production: replace with Redis
LIVE_STATE = {
    "triggered": False,
    "triggered_by": None,
    "shock_pct": 0.0,
    "live_price": None,
    "source_headlines": [],
    "chain": [],
    "timestamp": None,
    "shock_score": 0.0
}
