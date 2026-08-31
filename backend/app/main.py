from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.db import get_db, Base, engine
from app.models.schemas import Event, AskRequest
from app.services.correlation import reconstruct
from app.services.investigation import build_evidence, answer
from app.seed import load_events
from app.services.prediction import predict_next

app = FastAPI(title="Endpoint Security Intelligence API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    load_events()

def current_incident():
    events = load_events()
    raw = reconstruct(events)
    observed, inferred, unknown = build_evidence(events, raw)
    return {**raw, "observed": observed, "inferred": inferred, "unknown": unknown, "factors": [{"rule_id": f.rule_id, "title": f.title, "score": f.score, "reason": f.reason} for f in raw["findings"]], "prediction": predict_next(events, raw)}

@app.get("/api/health")
def health(): return {"status":"ok","service":"endpoint-security-intelligence"}

@app.get("/api/events")
def events():
    return [e.model_dump(mode="json") for e in load_events()]

@app.get("/api/incidents")
def incidents():
    return [current_incident()]

@app.get("/api/incidents/{incident_id}")
def incident(incident_id: str):
    if incident_id != "INC-001": raise HTTPException(404, "Incident not found")
    return current_incident()

@app.post("/api/investigate")
def investigate(req: AskRequest):
    inc = current_incident()
    if req.incident_id and req.incident_id != inc["incident_id"]: raise HTTPException(404, "Incident not found")
    return answer(req.question, inc, load_events())
