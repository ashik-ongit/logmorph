from datetime import datetime, timedelta, timezone
from app.models.schemas import Event

DEMO_START = datetime(2026, 8, 31, 12, 15, 3, tzinfo=timezone.utc)


def demo_events():
    t = DEMO_START
    events = [
        Event(event_id="evt-001", timestamp=t, event_type="usb_insert", user="alice", device_id="USB-7A91", metadata={"vendor":"Demo Storage","serial":"7A91"}),
        Event(event_id="evt-002", timestamp=t+timedelta(seconds=5), event_type="process_start", user="alice", process_name="update-helper.exe", pid=4821, parent_pid=4312, file_path=r"C:\Users\alice\AppData\Local\Temp\update-helper.exe", metadata={"signed":False}),
        Event(event_id="evt-003", timestamp=t+timedelta(seconds=6), event_type="process_start", user="alice", process_name="cmd.exe", pid=4890, parent_pid=4821, command_line="cmd.exe /c updater.cmd"),
        Event(event_id="evt-004", timestamp=t+timedelta(seconds=9), event_type="network_connection", user="alice", process_name="update-helper.exe", pid=4821, destination_ip="203.0.113.45", destination_port=443),
        Event(event_id="evt-005", timestamp=t+timedelta(seconds=12), event_type="scheduled_task_create", user="alice", process_name="schtasks.exe", pid=4932, metadata={"task_name":"System Update Check"}),
        Event(event_id="evt-006", timestamp=t+timedelta(seconds=18), event_type="file_modify", user="alice", file_path=r"C:\Users\alice\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\update.lnk"),
        Event(event_id="evt-007", timestamp=t+timedelta(seconds=25), event_type="usb_remove", user="alice", device_id="USB-7A91"),
        Event(event_id="evt-008", timestamp=t+timedelta(hours=3, minutes=2), event_type="remote_logon", user="alice", source_ip="198.51.100.24", session_id="remote-demo", metadata={"result":"failed","attempt":1}),
        Event(event_id="evt-009", timestamp=t+timedelta(hours=3, minutes=2, seconds=3), event_type="remote_logon", user="alice", source_ip="198.51.100.24", session_id="remote-demo", metadata={"result":"failed","attempt":2}),
        Event(event_id="evt-010", timestamp=t+timedelta(hours=3, minutes=2, seconds=6), event_type="remote_logon", user="alice", source_ip="198.51.100.24", session_id="remote-demo", metadata={"result":"failed","attempt":3}),
        Event(event_id="evt-011", timestamp=t+timedelta(hours=3, minutes=2, seconds=9), event_type="remote_logon", user="alice", source_ip="198.51.100.24", session_id="remote-demo", metadata={"result":"failed","attempt":4}),
    ]
    return events


def load_events():
    return demo_events()

if __name__ == "__main__":
    for e in demo_events():
        print(e.model_dump_json())
