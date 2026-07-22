import logging
import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from the_disaster_response_agent.tools.agents.agent import DisasterResponseAgent

# --- Logging setup ---
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logger = logging.getLogger("disaster_agent")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_DIR / "agent_queries.jsonl")
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)

app = FastAPI(title="NDMA Disaster Response Agent", version="0.1.0")

# One agent session per (simple, in-memory) session_id — resets on server restart
sessions: dict[str, DisasterResponseAgent] = {}


class QueryRequest(BaseModel):
    session_id: str
    message: str


class QueryResponse(BaseModel):
    session_id: str
    response: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if request.session_id not in sessions:
        sessions[request.session_id] = DisasterResponseAgent()

    agent = sessions[request.session_id]
    response_text = agent.ask(request.message)

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": request.session_id,
        "message": request.message,
        "response": response_text,
    }
    logger.info(json.dumps(log_entry))

    return QueryResponse(session_id=request.session_id, response=response_text)


@app.post("/reset/{session_id}")
def reset_session(session_id: str):
    if session_id in sessions:
        sessions[session_id].reset()
        return {"status": "reset", "session_id": session_id}
    return {"status": "no_active_session", "session_id": session_id}