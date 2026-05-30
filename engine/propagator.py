# Pre-computed from Granger analysis — normally run granger.py offline, paste results here
GRAPH = {
    ("bauxite",       "alumina"):        {"lag_months": 3, "elasticity": 0.74, "p_value": 0.021, "std_error": 0.08},
    ("alumina",       "aluminum"):       {"lag_months": 2, "elasticity": 0.81, "p_value": 0.011, "std_error": 0.06},
    ("aluminum",      "boeing_costs"):   {"lag_months": 8, "elasticity": 0.43, "p_value": 0.033, "std_error": 0.11},
    ("boeing_costs",  "airline_margins"):{"lag_months": 6, "elasticity": 0.38, "p_value": 0.041, "std_error": 0.13},
}

CHAIN_ORDER = [
    ("bauxite",      "alumina"),
    ("alumina",      "aluminum"),
    ("aluminum",     "boeing_costs"),
    ("boeing_costs", "airline_margins"),
]

def propagate_shock(graph: dict, start_node: str, shock_pct: float) -> list[dict]:
    """
    Propagates a shock from start_node downstream through the chain.

    Args:
        graph:      GRAPH dict with edge weights
        start_node: which node the shock hits (e.g. "bauxite")
        shock_pct:  fractional shock magnitude (e.g. 0.15 for 15%)

    Returns:
        List of impact dicts per downstream node, with confidence intervals.
    """
    results = []
    current_shock = shock_pct
    cumulative_lag = 0

    # Find the position of start_node in the chain
    start_idx = next(
        (i for i, (src, _) in enumerate(CHAIN_ORDER) if src == start_node),
        0
    )

    for source, target in CHAIN_ORDER[start_idx:]:
        if (source, target) not in graph:
            break

        edge = graph[(source, target)]
        propagated = current_shock * edge["elasticity"]
        cumulative_lag += edge["lag_months"]

        # 95% confidence interval
        margin = 1.96 * edge["std_error"] * abs(current_shock)

        results.append({
            "node":             target,
            "impact_pct":       round(propagated * 100, 2),
            "impact_ci_low":    round((propagated - margin) * 100, 2),
            "impact_ci_high":   round((propagated + margin) * 100, 2),
            "cumulative_lag_months": cumulative_lag,
            "arrives_in_weeks": cumulative_lag * 4,
            "edge_p_value":     edge["p_value"],
            "edge_elasticity":  edge["elasticity"],
        })

        current_shock = propagated  # attenuate for next hop

    return results
