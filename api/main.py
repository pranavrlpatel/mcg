import os
from dotenv import load_dotenv
load_dotenv()

import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine.propagator import propagate_shock, GRAPH
from bright_data.sec_scraper import get_all_baselines
from bright_data.signal_loop import start_background_loop
from api.state import LIVE_STATE
import os

app = FastAPI(title="Market Causality Graph API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    demo_mode = os.environ.get("DEMO_MODE", "false").lower() == "true"
    start_background_loop(demo_mode=demo_mode)
    print("[startup] Signal loop started")

from pydantic import BaseModel

class PropagateRequest(BaseModel):
    shock_pct: float
    start_node: str

@app.get("/propagate")
def propagate(shock_pct: float = 0.15, start_node: str = "bauxite"):
    """Manual trigger — used by frontend slider"""
    chain = propagate_shock(GRAPH, start_node, shock_pct)
    
    LIVE_STATE.update({
        "triggered": True,
        "triggered_by": start_node,
        "shock_pct": round(shock_pct * 100, 2),
        "chain": chain,
        "timestamp": 123456789,
        "source_headlines": ["Manual override trigger"]
    })
    
    return {"chain": chain, "shock_input_pct": shock_pct * 100, "start_node": start_node}

@app.post("/propagate")
def propagate_post(req: PropagateRequest):
    chain = propagate_shock(GRAPH, req.start_node, req.shock_pct)
    
    LIVE_STATE.update({
        "triggered": True,
        "triggered_by": req.start_node,
        "shock_pct": round(req.shock_pct * 100, 2),
        "chain": chain,
        "timestamp": 123456789,
        "source_headlines": ["Manual override trigger"]
    })
    
    return {"chain": chain, "shock_input_pct": req.shock_pct * 100, "start_node": req.start_node}


@app.get("/live-state")
def live_state():
    """Polled by frontend every 10s — returns latest auto-detected shock"""
    return LIVE_STATE

@app.get("/edges")
def get_edges():
    """Returns all calibrated edges for graph visualization"""
    return {
        "edges": [
            {"from": k[0], "to": k[1], **v}
            for k, v in GRAPH.items()
        ]
    }

@app.get("/baselines")
def baselines():
    """Returns live-scraped Boeing and Delta margin baselines"""
    return get_all_baselines()

@app.get("/health")
def health():
    return {"status": "ok", "bright_data": "connected"}
