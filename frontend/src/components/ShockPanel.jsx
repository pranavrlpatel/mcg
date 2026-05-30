import React, { useState } from 'react';
import axios from 'axios';

export function ShockPanel({ onResult, headlines = [] }) {
  const [sliderValue, setSliderValue] = useState(15);

  const handlePropagate = async () => {
    try {
      const response = await axios.post('http://localhost:8000/propagate', {
        shock_pct: sliderValue / 100, // sending as fraction to match logic
        start_node: 'bauxite'
      });
      onResult(response.data.chain, sliderValue);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="shock-panel glass-panel">
      <h2>🌐 Live Bright Data SERP API Feed</h2>
      <div className="signal-feed">
        {headlines.length > 0 ? (
          headlines.map((headline, i) => (
            <div key={i} className="signal-item">
              <span className="live-badge">LIVE</span>
              {headline}
            </div>
          ))
        ) : (
          <div className="signal-item muted">Watching for supply chain shocks...</div>
        )}
      </div>

      <div className="manual-controls">
        <h3>Manual Override (Demo)</h3>
        <div className="control-group">
          <label>Shock Magnitude: {sliderValue}%</label>
          <input 
            type="range" 
            min="1" 
            max="100" 
            value={sliderValue} 
            onChange={e => setSliderValue(Number(e.target.value))} 
          />
        </div>
        <button className="primary-btn" onClick={handlePropagate}>
          Propagate
        </button>
      </div>
    </div>
  );
}
