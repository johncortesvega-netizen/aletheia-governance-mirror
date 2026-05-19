from pathlib import Path

from ui.receipt_reader import parse_receipt_standard_view


ROOT = Path(__file__).resolve().parents[1]


SAMPLE_RECEIPT = """LOCAL WITNESS RECEIPT
Module: Mirror Check
Protocol-adjusted state: SANCTUARY
Risk: Low
Protocol label: Mirror Check / Sanctuary
Integrity: 0.807
Friction: 0.000
Collapse probability: 0.050
Trust index: 0.738
Alignment: 0.900
Ego: 0.010

Repair questions:
- Where can people object, pause, or request human review if something goes wrong?
- What prevents this system from becoming centralized over time?
"""


def test_patch_176_parse_keeps_native_values_unchanged():
    view = parse_receipt_standard_view(SAMPLE_RECEIPT)

    assert view["native_state"] == "SANCTUARY"
    assert view["standard_band"] == "Low (Standard Band)"
    assert view["fields"]["integrity"] == "0.807"
    assert view["fields"]["friction"] == "0.000"
    assert view["fields"]["collapse_probability"] == "0.050"
    assert view["fields"]["trust"] == "0.738"
    assert view["fields"]["alignment"] == "0.900"


def test_patch_176_receipt_reader_contains_plain_english_sections():
    source = (ROOT / "ui" / "receipt_reader.py").read_text(encoding="utf-8")

    assert "Plain-English receipt summary" in source
    assert "What is this document?" in source
    assert "The main results" in source
    assert "How is power distributed?" in source
    assert "Next steps and questions" in source
    assert "This is a record of an ALETHEIA review, a kind of digital mirror." in source


def test_patch_176_plain_tone_preserves_non_authority_boundary():
    source = (ROOT / "ui" / "receipt_reader.py").read_text(encoding="utf-8")

    assert "The computer does not decide anything here." in source
    assert "does not give official permission" in source
    assert "does not prove that something is truly safe, good, or true" in source
    assert "Human review remains required" in source
    assert "Receipt Reader does not change or rescore them" in source


def test_patch_176_power_distribution_uses_plain_review_areas():
    source = (ROOT / "ui" / "receipt_reader.py").read_text(encoding="utf-8")

    assert '"Review area": "Power"' in source
    assert '"Review area": "Correction"' in source
    assert '"Review area": "Access"' in source
    assert "Missing fields are not inferred" in source
