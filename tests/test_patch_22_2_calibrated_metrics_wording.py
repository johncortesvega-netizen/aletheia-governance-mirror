from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mirror_check_no_longer_calls_calibrated_integrity_raw():
    app_text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "Raw simulation integrity" not in app_text
    assert "Protocol friction" not in app_text
    assert 'metric("Integrity"' in app_text or 'metric_card("Integrity"' in app_text
    assert "ethics-calibrated reading metrics" in app_text
    assert "Raw pre-ethics values stay in the local witness receipt" in app_text


def test_protocol_summary_uses_integrity_reading_language():
    protocol_text = (ROOT / "protocol.py").read_text(encoding="utf-8")
    assert "Raw simulation integrity is" not in protocol_text
    assert "Integrity reading is" in protocol_text
