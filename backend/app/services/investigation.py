from datetime import datetime

def build_evidence(events, incident):
    by_id = {e.event_id: e for e in events}
    observed = []
    for eid in incident["event_ids"]:
        e = by_id.get(eid)
        if not e: continue
        if e.event_type == "usb_insert": text = f"USB device {e.device_id or 'unknown'} was inserted."
        elif e.event_type == "process_start": text = f"Process {e.process_name} started (PID {e.pid}){(' with parent PID '+str(e.parent_pid)) if e.parent_pid else ''}."
        elif e.event_type == "network_connection": text = f"PID {e.pid} connected to {e.destination_ip}:{e.destination_port}."
        elif e.event_type == "scheduled_task_create": text = f"Scheduled task persistence was created: {e.metadata.get('task_name','unknown')}."
        elif e.event_type == "remote_logon":
            result = e.metadata.get('result', 'observed')
            text = f"Remote authentication attempt from {e.source_ip or 'unknown source'} — {result}."
        else: text = f"Observed event: {e.event_type}."
        observed.append({"event_id": e.event_id, "timestamp": e.timestamp, "statement": text, "kind": "observed"})
    inferred = []
    if len(observed) >= 2:
        inferred.append({"event_id": observed[-1]["event_id"], "timestamp": observed[-1]["timestamp"], "statement": "The events are potentially related because they occur in a short temporal window and share process/device context.", "kind": "inferred"})
    unknown = [{"event_id": incident["event_ids"][-1] if incident["event_ids"] else "none", "timestamp": incident["end"], "statement": "The available telemetry does not prove malicious intent or identify who initiated the activity.", "kind": "unknown"}]
    return observed, inferred, unknown

def answer(question, incident, events):
    q = question.lower().strip()
    if "usb" in q:
        headline = "The USB insertion was followed by process execution, an outbound connection, and a persistence change in the demo timeline."
    elif "why" in q or "flag" in q:
        headline = "The incident was flagged because multiple individually explainable signals formed a higher-risk sequence."
    elif "away" in q or "happened" in q:
        headline = "The reconstructed timeline shows the meaningful activity observed during the selected incident window."
    else:
        headline = "I found the following evidence-backed activity for the selected incident."
    factors = " + ".join(f"{f['score']} {f['title']}" for f in incident["factors"])
    return {
        "answer": headline,
        "risk": f"Risk score: {incident['risk_score']}/100 ({incident['severity']}). Factors: {factors or 'none'}.",
        "evidence_event_ids": incident["event_ids"],
        "limitations": "This is an evidence-based reconstruction, not proof that an attacker was present.",
    }
