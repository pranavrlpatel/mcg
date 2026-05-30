import React, { useState, useEffect } from 'react';
import GraphView from './components/GraphView';
import { ShockPanel } from './components/ShockPanel';
import { PunchlinePanel } from './components/PunchlinePanel';
import { useLiveState } from './hooks/useLiveState';
import './index.css';

function App() {
  const [chain, setChain] = useState(null);
  const [shockPct, setShockPct] = useState(null);
  const [headlines, setHeadlines] = useState([]);
  
  const liveStateData = useLiveState();
  const liveState = liveStateData.state || liveStateData;
  const baselines = liveStateData.baselines || { delta_margin: 0.071 };

  useEffect(() => {
    if (liveState && liveState.chain) {
      setChain(liveState.chain);
      setShockPct(liveState.shock_pct);
      if (liveState.source_headlines) {
        setHeadlines(liveState.source_headlines);
      }
    }
  }, [liveState]);

  const handleResult = (newChain, newShockPct) => {
    setChain(newChain);
    setShockPct(newShockPct);
  };

  return (
    <div className="app-container">
      <header>
        <h1>Market Causality Graph (MCG)</h1>
        <p>Live Supply Chain Shock Propagation Engine</p>
      </header>
      
      <div className="panels-grid">
        <ShockPanel onResult={handleResult} headlines={headlines} />
        <GraphView chain={chain} />
      </div>
      
      <PunchlinePanel 
        chain={chain} 
        shockPct={shockPct} 
        deltaMargin={baselines.delta_margin} 
      />
    </div>
  );
}

export default App;
