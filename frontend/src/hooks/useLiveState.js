import { useEffect, useState } from "react";

export function useLiveState() {
  const [state, setState] = useState(null);
  const [edges, setEdges] = useState(null);
  const [baselines, setBaselines] = useState(null);

  useEffect(() => {
    const fetchEdges = async () => {
      try {
        const resp = await fetch("http://localhost:8000/edges");
        const data = await resp.json();
        setEdges(data.edges);
      } catch(e) {
        console.error("Failed to fetch edges", e);
      }
    };

    const fetchBaselines = async () => {
      try {
        const resp = await fetch("http://localhost:8000/baselines");
        const data = await resp.json();
        setBaselines(data);
      } catch(e) {
        console.error("Failed to fetch baselines", e);
      }
    };

    fetchEdges();
    fetchBaselines();

    const poll = async () => {
      try {
        const resp = await fetch("http://localhost:8000/live-state");
        const data = await resp.json();
        if (data.triggered) setState(data);
      } catch(e) {
        console.error("Failed to poll live state", e);
      }
    };

    poll();
    const interval = setInterval(poll, 5000); // poll every 5s
    return () => clearInterval(interval);
  }, []);

  return { state, edges, baselines, setState };
}
