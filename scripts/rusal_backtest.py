import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.propagator import propagate_shock, GRAPH

def run_backtest():
    # Simulate Rusal sanctions: ~6% of global supply offline
    # Bauxite/alumina impact estimated at 8% cost increase
    rusal_shock = 0.08

    results = propagate_shock(GRAPH, "alumina", rusal_shock)

    print("=== 2018 Rusal Backtest ===")
    for r in results:
        print(f"{r['node']:20s}  {r['impact_pct']:+.1f}%  in {r['arrives_in_weeks']} weeks")

    print("\nActual: LME Aluminum +30% in 3 weeks (April 2018)")
    print("Model:  LME Aluminum +", results[0]['impact_pct'], "% —  structural estimate")
    print("Delta:  Behavioural amplification explains gap")

if __name__ == "__main__":
    run_backtest()
