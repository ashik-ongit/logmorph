from app.seed import demo_events
from app.services.detection import detect, risk_score
from app.services.correlation import reconstruct

def test_demo_has_findings():
    findings = detect(demo_events())
    assert len(findings) >= 3
    assert risk_score(findings) >= 65

def test_reconstruction_is_explainable():
    inc = reconstruct(demo_events())
    assert inc["incident_id"] == "INC-001"
    assert inc["risk_score"] >= 65
    assert "evt-001" in inc["event_ids"]
