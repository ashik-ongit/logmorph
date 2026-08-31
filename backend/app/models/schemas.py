from datetime import datetime
from pydantic import BaseModel, Field

class Event(BaseModel):
    event_id: str
    timestamp: datetime
    event_type: str
    host: str = "desktop-01"
    user: str | None = None
    session_id: str | None = None
    process_name: str | None = None
    pid: int | None = None
    parent_pid: int | None = None
    file_path: str | None = None
    device_id: str | None = None
    source_ip: str | None = None
    destination_ip: str | None = None
    destination_port: int | None = None
    command_line: str | None = None
    metadata: dict = Field(default_factory=dict)

class Evidence(BaseModel):
    event_id: str
    timestamp: datetime
    statement: str
    kind: str

class Incident(BaseModel):
    incident_id: str
    title: str
    severity: str
    risk_score: int
    status: str
    start: datetime
    end: datetime
    event_ids: list[str]
    observed: list[Evidence]
    inferred: list[Evidence]
    unknown: list[Evidence]
    factors: list[dict]

class AskRequest(BaseModel):
    question: str
    incident_id: str | None = None
