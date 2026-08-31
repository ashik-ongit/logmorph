from dataclasses import dataclass
from datetime import timedelta

@dataclass
class Finding:
    rule_id: str
    title: str
    score: int
    reason: str
    event_ids: list[str]

RULES = [
    ("USB_EXEC_CHAIN", "USB execution chain", 25),
    ("REMOTE_PROCESS", "Remote access followed by process execution", 20),
    ("PERSISTENCE_AFTER_PROCESS", "Persistence change after process execution", 25),
    ("EXTERNAL_NETWORK", "External network connection from suspicious process", 15),
]

def detect(events):
    findings = []
    ordered = sorted(events, key=lambda e: e.timestamp)
    usb = [e for e in ordered if e.event_type == "usb_insert"]
    execs = [e for e in ordered if e.event_type == "process_start"]
    nets = [e for e in ordered if e.event_type == "network_connection"]
    persistence = [e for e in ordered if e.event_type in {"scheduled_task_create", "startup_change", "service_create"}]
    auth = [e for e in ordered if e.event_type in {"remote_logon", "logon"}]

    if usb and execs:
        for u in usb:
            near = [p for p in execs if timedelta(0) <= p.timestamp-u.timestamp <= timedelta(seconds=30)]
            if near:
                ids = [u.event_id] + [p.event_id for p in near]
                findings.append(Finding("USB_EXEC_CHAIN", "USB execution chain", 25, "A process started shortly after a USB device was inserted.", ids))
                break
    if auth and execs:
        for a in auth:
            near = [p for p in execs if timedelta(0) <= p.timestamp-a.timestamp <= timedelta(seconds=30)]
            if near:
                findings.append(Finding("REMOTE_PROCESS", "Remote access followed by process execution", 20, "A process started within 30 seconds of a remote authentication event.", [a.event_id, near[0].event_id]))
                break
    if persistence and execs:
        for p in persistence:
            prior = [x for x in execs if timedelta(0) <= p.timestamp-x.timestamp <= timedelta(seconds=60)]
            if prior:
                findings.append(Finding("PERSISTENCE_AFTER_PROCESS", "Persistence change after process execution", 25, "A persistence mechanism changed soon after process execution.", [prior[-1].event_id, p.event_id]))
                break
    for n in nets:
        if n.destination_ip and not n.destination_ip.startswith(("10.", "192.168.", "172.16.")):
            proc = [p for p in execs if p.pid == n.pid]
            ids = [n.event_id] + ([proc[-1].event_id] if proc else [])
            findings.append(Finding("EXTERNAL_NETWORK", "External network connection", 15, "A process opened an outbound connection to an external address.", ids))
            break
    return findings

def risk_score(findings):
    return min(100, sum(f.score for f in findings))
