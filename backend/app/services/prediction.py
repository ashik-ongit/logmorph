"""Experimental next-stage hypothesis layer.

This is deliberately conservative: it predicts a possible next behavior stage
from the currently reconstructed chain. It does not claim that an attack will
occur and it does not execute any response action.
"""

def predict_next(events, incident):
    types = {e.event_type for e in events}
    signals = []
    if "remote_logon" in types:
        signals.append("remote-access activity")
    if "process_start" in types:
        signals.append("process execution")
    if "network_connection" in types:
        signals.append("external network activity")
    if "scheduled_task_create" in types or "startup_change" in types:
        signals.append("persistence activity")

    if {"remote_logon", "process_start", "network_connection"}.issubset(types):
        stage = "Credential or discovery-related activity"
        confidence = 72
        rationale = "Remote access, process execution and network activity form a multi-stage sequence."
    elif {"process_start", "network_connection"}.issubset(types):
        stage = "Persistence or follow-on execution"
        confidence = 58
        rationale = "Execution followed by outbound network activity may precede additional follow-on behavior."
    elif "process_start" in types:
        stage = "Follow-on process activity"
        confidence = 41
        rationale = "Process execution is present, but the available chain is not sufficient for a stronger hypothesis."
    else:
        stage = "No meaningful next-stage hypothesis"
        confidence = 15
        rationale = "Current telemetry does not contain enough correlated signals."

    return {
        "experimental": True,
        "prediction": stage,
        "confidence": confidence,
        "signals": signals,
        "rationale": rationale,
        "disclaimer": "Prediction is a hypothesis from observed telemetry, not proof that an attack will occur."
    }
