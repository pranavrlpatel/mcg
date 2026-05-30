import React from 'react';

export function PunchlinePanel({ chain, shockPct, deltaMargin }) {
  if (!chain || chain.length === 0) return null;

  const airlineImpact = chain.find(n => n.node === "airline_margins");
  if (!airlineImpact) return null;

  // Impact is negative to margin, so if cost rises (impact_pct > 0), margin goes down
  const marginDelta = -1 * (airlineImpact.impact_pct / 100);
  const projectedMargin = (deltaMargin + marginDelta) * 100;
  
  // CI also inverted logic:
  const marginCiLow = (deltaMargin - (airlineImpact.impact_ci_high / 100)) * 100;
  const marginCiHigh = (deltaMargin - (airlineImpact.impact_ci_low / 100)) * 100;

  return (
    <div className="punchline-panel glass-panel highlight-border">
      <div className="alert-header">
        ⚠️ <span className="highlight-text">{shockPct.toFixed(1)}%</span> upstream shock detected via Bright Data
      </div>
      <div className="chain-summary">
        {chain.map((node, i) => (
          <div key={node.node} className="chain-row fade-in" style={{ animationDelay: `${i * 0.2}s` }}>
            <span className="arrow">→</span>
            <span className="node-name">{node.node.replace("_", " ")}</span>
            <span className={`impact ${node.impact_pct < 0 ? "positive-text" : "negative-text"}`}>
              {node.impact_pct > 0 ? "+" : ""}{node.impact_pct.toFixed(1)}%
            </span>
            <span className="lag">realises in {node.arrives_in_weeks} weeks</span>
            <span className="ci muted">
              [{node.impact_ci_low.toFixed(1)}%, {node.impact_ci_high.toFixed(1)}%]
            </span>
          </div>
        ))}
      </div>
      <div className="margin-projection">
        <div className="company">Delta Air Lines</div>
        <div className="current">
          Current operating margin (live SEC EDGAR via <b>Bright Data Crawl API</b>): <span className="stat">{(deltaMargin * 100).toFixed(1)}%</span>
        </div>
        <div className="projected">
          Projected post-shock margin: <span className="stat big-stat">{projectedMargin.toFixed(1)}%</span>
        </div>
        <div className="confidence muted">
          95% CI: [{marginCiLow.toFixed(1)}%, {marginCiHigh.toFixed(1)}%]
          &nbsp;(p={airlineImpact.edge_p_value})
        </div>
      </div>
    </div>
  );
}
