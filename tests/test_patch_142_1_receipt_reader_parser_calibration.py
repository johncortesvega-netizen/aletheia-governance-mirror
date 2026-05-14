from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


RECEIPT_WITH_JSON = """
ALETHEIA LOCAL WITNESS RECEIPT
Module: Mirror Check
VERDICT SIGNAL
Protocol-adjusted state: SANCTUARY
Risk: Low
Protocol label: Generic Local Scan
CORE METRICS
Integrity: 0.7311
Friction: 0.0000
Collapse probability: 0.0730
Trust index: 0.9800
Alignment: 0.9500
Ego: 0.0009
THRESHOLD MAPPING LAYER
Component readings:
- Power balance: Threshold +

SILENT OPERATOR REPAIR QUESTIONS
- What appeal path exists for people affected by this proposal?
- Who can pause, correct, or review the executive power in this design?

MACHINE-READABLE RECEIPT JSON
{
  "module": "Mirror Check",
  "verdict": {
    "protocol_adjusted_state": "SANCTUARY",
    "risk": "Low",
    "protocol_label": "Generic Local Scan"
  },
  "metrics": {
    "integrity": 0.7311,
    "friction": 0.0,
    "collapse_probability": 0.073,
    "trust_index": 0.98,
    "alignment": 0.95,
    "ego": 0.0009
  },
  "repair_questions": [
    "What appeal path exists for people affected by this proposal?",
    "Who can pause, correct, or review the executive power in this design?"
  ]
}
"""


def test_receipt_reader_prefers_machine_readable_json_and_reads_current_receipt_keys():
    reader = importlib.import_module("ui.receipt_reader")
    parsed = reader.parse_receipt_standard_view(RECEIPT_WITH_JSON)
    fields = parsed["fields"]

    assert parsed["native_state"] == "SANCTUARY"
    assert parsed["standard_band"] == "Low (Standard Band)"
    assert fields["module_source"] == "Mirror Check"
    assert fields["risk_state"] == "Low"
    assert fields["protocol_adjusted_state"] == "SANCTUARY"
    assert fields["protocol_label"] == "Generic Local Scan"
    assert fields["integrity"] == "0.7311"
    assert fields["friction"] == "0.0000"
    assert fields["collapse_probability"] == "0.0730"
    assert fields["trust"] == "0.9800"
    assert fields["alignment"] == "0.9500"
    assert fields["ego"] == "0.0009"
    assert "What appeal path exists" in parsed["repair_questions"][0]
    assert any("Who can pause" in question for question in parsed["repair_questions"])
    assert not any("Power balance" in question for question in parsed["repair_questions"])


def test_receipt_reader_text_fallback_accepts_risk_and_trust_index_without_component_leakage():
    reader = importlib.import_module("ui.receipt_reader")
    text_only = """
Module: AI Integrity Mirror
Protocol-adjusted state: THRESHOLD
Risk: Elevated
Protocol label: AI Integrity Artifact Review
Integrity: 0.6421
Friction: 0.1100
Collapse probability: 0.2100
Trust index: 0.7700
Alignment: 0.8300
Ego: 0.0900
Component readings:
- Power balance: Threshold +
SILENT OPERATOR REPAIR QUESTIONS
- Which claim needs evidence before human reliance?
- What appeal path exists for affected people?
"""
    parsed = reader.parse_receipt_standard_view(text_only)
    fields = parsed["fields"]

    assert parsed["native_state"] == "THRESHOLD"
    assert fields["module_source"] == "AI Integrity Mirror"
    assert fields["risk_state"] == "Elevated"
    assert fields["trust"] == "0.7700"
    assert "Which claim needs evidence" in parsed["repair_questions"][0]
    assert not any("Power balance" in question for question in parsed["repair_questions"])


def test_receipt_reader_is_shared_utility_and_does_not_change_module_receipts_or_scoring():
    app = read("app.py")
    helper = read("ui/receipt_reader.py")
    assert app.count("render_receipt_reader_standard_view") == 2
    assert "with st.expander(\"Receipt Reader — Standard View\"" in app
    assert "tab_receipt_reader" not in app

    forbidden = [
        "full_report(",
        "simulate(",
        "build_local_witness_receipt",
        "render_local_witness_receipt_text",
        "audit_ai_integrity",
        "scan_privacy_boundary_static",
        "requests.",
        "httpx.",
        "openai",
        "embedding",
        "telemetry",
        "analytics",
        "download_button",
    ]
    lower_helper = helper.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lower_helper


def test_receipt_reader_ui_uses_uploaded_language_only_and_standard_metric_rows():
    helper = read("ui/receipt_reader.py")
    assert "Performance & Risk Metrics" in helper
    assert "Trust Index" in helper
    assert "Not found in uploaded receipt" in helper
    assert "risk_state" in helper
    assert "pasted receipt" not in helper.lower()
    assert "file_uploader" in helper


def test_patch_142_1_docs_capture_parser_calibration_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_142_1_MANIFEST.txt",
            "PATCH_142_1_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
        ]
    ).lower()
    for phrase in [
        "patch 142.1",
        "receipt reader parser calibration",
        "machine-readable receipt json",
        "risk:",
        "trust index:",
        "silent operator repair questions",
        "no scoring",
        "no verdict routing",
        "no receipt schema",
        "no receipt generation",
        "no ai integrity scan behavior",
        "no privacy audit scan behavior",
        "no world lens math",
        "no external calls",
        "no telemetry",
        "no analytics",
        "no certification",
        "human review remains required",
    ]:
        assert phrase in combined
