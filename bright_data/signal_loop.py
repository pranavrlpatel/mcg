import time
import threading
from bright_data.signal_watcher import fetch_news_signal, score_shock, WATCH_QUERIES
from bright_data.price_scraper import get_lme_aluminum_price, compute_shock_pct
from engine.propagator import propagate_shock, GRAPH
from api.state import LIVE_STATE

POLL_INTERVAL = 15      # 15 seconds for demo (normally 15 min in production)
DEMO_INTERVAL = 15       # 15 seconds for demo mode — to show it quickly

SHOCK_THRESHOLD = 0.0    # Tune lower so ANY news triggers the live demo graph

def run_signal_loop(demo_mode: bool = False):
    interval = DEMO_INTERVAL if demo_mode else POLL_INTERVAL
    print(f"[signal_loop] Starting — polling every {interval}s — demo_mode={demo_mode}")

    while True:
        try:
            for node in WATCH_QUERIES.keys():
                signals = fetch_news_signal(node)
                shock_score = score_shock(signals)

                print(f"[signal_loop] {node}: score={shock_score}")

                if shock_score >= SHOCK_THRESHOLD or demo_mode: # Trigger in demo mode if signals exist
                    live_price = get_lme_aluminum_price()

                    if live_price is None:
                        print(f"[signal_loop] Price fetch failed — skipping propagation")
                        continue

                    shock_pct = compute_shock_pct(live_price)

                    # Only propagate positive shocks for demo clarity
                    if abs(shock_pct) < 0.02:
                        continue

                    chain = propagate_shock(GRAPH, node, shock_pct)

                    LIVE_STATE.update({
                        "triggered": True,
                        "triggered_by": node,
                        "shock_pct": round(shock_pct * 100, 2),
                        "live_price": live_price,
                        "source_headlines": [s["title"] for s in signals[:3]],
                        "chain": chain,
                        "timestamp": time.time(),
                        "shock_score": shock_score
                    })

                    print(f"[signal_loop] SHOCK FIRED: {node} +{shock_pct:.1%} → propagated")
                    break   # one shock per poll cycle — avoid cascade during demo

        except Exception as e:
            print(f"[signal_loop] Error in loop iteration: {e}")

        time.sleep(interval)

def start_background_loop(demo_mode: bool = False):
    t = threading.Thread(target=run_signal_loop, args=(demo_mode,), daemon=True)
    t.start()
    return t
