from collections import defaultdict
from .detection import detect, risk_score

def reconstruct(events):
    findings = detect(events)
    score = risk_score(findings)
    ordered = sorted(events, key=lambda e: e.timestamp)
    if score >= 81: severity = "CRITICAL"
    elif score >= 61: severity = "HIGH"
    elif score >= 41: severity = "MEDIUM"
    elif score >= 21: severity = "LOW"
    else: severity = "BENIGN"

    ids = []
    for f in findings:
        for eid in f.event_ids:
            if eid not in ids: ids.append(eid)
    for e in ordered:
        if e.event_id not in ids and e.event_type in {"usb_insert","process_start","network_connection","scheduled_task_create","remote_logon"}:
            ids.append(e.event_id)

    return {
        "incident_id": "INC-001",
        "title": "Potentially Suspicious USB Activity",
        "severity": severity,
        "risk_score": score,
        "status": "OPEN",
        "start": ordered[0].timestamp,
        "end": ordered[-1].timestamp,
        "event_ids": ids,
        "findings": findings,
    }
