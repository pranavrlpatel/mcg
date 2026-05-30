import React, { useMemo } from 'react';
import ReactFlow, { Background, Controls, MiniMap } from 'reactflow';
import 'reactflow/dist/style.css';

export default function GraphView({ chain }) {
  const NODE_POSITIONS = [
    { id: 'bauxite', label: 'Bauxite', x: 300, y: 0 },
    { id: 'alumina', label: 'Alumina', x: 300, y: 120 },
    { id: 'aluminum', label: 'Aluminum', x: 300, y: 240 },
    { id: 'boeing_costs', label: 'Boeing', x: 300, y: 360 },
    { id: 'airline_margins', label: 'Airlines', x: 300, y: 480 }
  ];

  const nodes = useMemo(() => {
    return NODE_POSITIONS.map(pos => {
      let bgColor = '#6b7280'; // default gray
      if (chain) {
        const chainNode = chain.find(c => c.node === pos.id);
        if (chainNode) {
          if (chainNode.impact_pct < 0) bgColor = '#ef4444'; // red
          else if (chainNode.impact_pct > 0) bgColor = '#22c55e'; // green
        }
      }
      return {
        id: pos.id,
        position: { x: pos.x, y: pos.y },
        data: { label: pos.label },
        style: {
          background: bgColor,
          color: '#fff',
          border: 'none',
          borderRadius: '8px',
          padding: '10px',
          textAlign: 'center',
          fontWeight: 'bold',
          width: 150
        }
      };
    });
  }, [chain]);

  const edges = useMemo(() => {
    const edgeList = [
      { id: 'e1', source: 'bauxite', target: 'alumina' },
      { id: 'e2', source: 'alumina', target: 'aluminum' },
      { id: 'e3', source: 'aluminum', target: 'boeing_costs' },
      { id: 'e4', source: 'boeing_costs', target: 'airline_margins' },
    ];
    
    return edgeList.map(edge => ({
      ...edge,
      animated: chain !== null,
      style: { stroke: chain !== null ? '#3b82f6' : '#555', strokeWidth: 2 }
    }));
  }, [chain]);

  return (
    <div className="glass-panel" style={{ width: '100%', height: '500px', display: 'flex', flexDirection: 'column' }}>
      <h2 style={{ marginBottom: '16px' }}>📊 Causal Chain Propagation</h2>
      <div style={{ flex: 1, width: '100%', minHeight: '400px', height: '100%' }}>
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background color="#58a6ff" gap={16} />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
}
