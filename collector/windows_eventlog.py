"""Optional Windows Event Log adapter.

This adapter is intentionally small: acquisition is separate from the analysis engine.
Install pywin32 on Windows and map selected Event IDs into the universal event model.
"""

import json
import platform


def collect_recent(limit=50):
    if platform.system() != "Windows":
        raise RuntimeError("Windows Event Log collection must run on Windows")
    try:
        import win32evtlog
    except ImportError as exc:
        raise RuntimeError("Install pywin32 on Windows to use this collector") from exc

    handle = win32evtlog.OpenEventLog(None, "Security")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    rows = []
    while len(rows) < limit:
        batch = win32evtlog.ReadEventLog(handle, flags, 0)
        if not batch: break
        for item in batch:
            rows.append({
                "event_id": f"win-{item.RecordNumber}",
                "source": "windows-security",
                "event_type": f"windows_event_{item.EventID & 0xFFFF}",
                "timestamp": item.TimeGenerated.isoformat(),
                "metadata": {"record_number": item.RecordNumber, "strings": item.StringInserts or []},
            })
            if len(rows) >= limit: break
    win32evtlog.CloseEventLog(handle)
    return rows

if __name__ == "__main__":
    print(json.dumps(collect_recent(), indent=2, default=str))
