# Market Causality Graph (MCG)

A live, Bright-Data-powered supply chain shock propagation engine. It computes in real-time which companies get hurt when an upstream commodity event fires, by how much, and how many weeks before it appears in any analyst report or equity price.

## Overview

The system is built in three tightly integrated layers:
1. **Bright Data signal layer**: Uses SERP API for news shocks, Web Unlocker for live LME prices, and Web Scraper API for live SEC EDGAR margins.
2. **Causal engine**: Uses Granger causality analysis (with ADF stationarity pre-checks) to compute calibrated edges for lag, elasticity, and p-value.
3. **React Frontend**: Visualizes the shock propagation using React Flow.

## Why Bright Data Is Unremovable — The Exact Dependency Chain

The MCG engine relies entirely on Bright Data to function. Pull the plug on Bright Data and the engine goes completely silent:

1. **Tool 1 — SERP API (The Trip Wire)**: Runs in the background and fires Google News searches. It bypasses blocks and returns JSON. If the keyword-filtered shock score crosses 0.6, it triggers the engine.
2. **Tool 2 — Web Unlocker (The Quantifier)**: Only fires when Tool 1 trips. Fetches live LME aluminum spot price from metals-api.com. Without a real price number, there is no `shock_pct`, and the propagator has nothing to run.
3. **Tool 3 — Web Scraper API (The Anchor)**: Runs at startup to scrape SEC EDGAR for Boeing and Delta's latest margins. This ensures the baseline margins in the UI are real, not hardcoded.

In code:
```python
if shock_score >= SHOCK_THRESHOLD:         # Tool 1 must fire
    live_price = get_lme_aluminum_price()  # Tool 2 must return a number
    shock_pct = compute_shock_pct(live_price)
    chain = propagate_shock(GRAPH, node, shock_pct)  # Engine runs
```
Every step depends on the previous one, making Bright Data the true nervous system of the app.

## Setup Instructions

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
3. Run the backend:
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```
4. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
