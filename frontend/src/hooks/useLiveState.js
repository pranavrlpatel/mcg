import { useEffect, useState } from "react";

export function useLiveState() {
  const [state, setState] = useState(null);
  const [edges, setEdges] = useState(null);
  const [baselines, setBaselines] = useState(null);

  useEffect(() => {
    const fetchEdges = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
        const resp = await fetch(`${apiUrl}/edges`);
        const data = await resp.json();
        setEdges(data.edges);
      } catch(e) {
        console.error("Failed to fetch edges", e);
      }
    };

    const fetchBaselines = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
        const resp = await fetch(`${apiUrl}/baselines`);
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
        const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
        const resp = await fetch(`${apiUrl}/live-state`);
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
