from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


SAMPLE_MIRROR_RECEIPT = """
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

SILENT OPERATOR REPAIR QUESTIONS
- What appeal path exists for people affected by this proposal?

MACHINE-READABLE RECEIPT JSON
{
  "active_modules": ["Mirror Check"],
  "module": "Mirror Check",
  "metrics": {
    "integrity": 0.7311,
    "friction": 0.0,
    "collapse_probability": 0.073,
    "trust_index": 0.98,
    "alignment": 0.95,
    "ego": 0.0009
  },
  "repair_questions": ["What appeal path exists for people affected by this proposal?"],
  "verdict": {
    "protocol_adjusted_state": "SANCTUARY",
    "risk": "Low",
    "protocol_label": "Generic Local Scan"
  }
}
"""


def test_patch_142_4_receipt_reader_uses_narrative_system_status_shape():
    from ui.receipt_reader import parse_receipt_standard_view

    view = parse_receipt_standard_view(SAMPLE_MIRROR_RECEIPT)

    assert view["system_status"] == "SANCTUARY"
    assert view["native_state"] == "SANCTUARY"
    assert view["standard_band"] == "Low (Standard Band)"
    assert view["module_family"] == "Mirror Check"
    assert view["core_logic_title"] == "Core Logic (The Mirror Check)"
    assert "verbal translation of the uploaded receipt" in view["core_logic_text"]
    assert "without generating a new verdict" in view["core_logic_text"]
    assert "Trust Index" in [row["Metric"] for row in view["metric_rows"]]
    assert any(row["Value"] == "0.9800" for row in view["metric_rows"])
    assert any(row["Interpretation"] == "Near-total reliability." for row in view["metric_rows"])
    assert "low" in view["summary"].lower()
    assert "What appeal path exists" in view["repair_questions"][0]


def test_patch_142_4_receipt_reader_is_upload_only_and_uploaded_language_only():
    helper = read("ui/receipt_reader.py")
    assert "file_uploader" in helper
    assert "Upload an ALETHEIA receipt file to read it in Standard View." in helper
    assert "Not found in uploaded receipt" in helper
    assert "Paste an ALETHEIA receipt" not in helper
    assert "pasted receipt" not in helper.lower()
    assert "text_area" not in helper


def test_patch_142_4_no_rescore_or_authority_claims_added():
    helper = read("ui/receipt_reader.py")
    forbidden_runtime = [
        "full_report(",
        "simulate(",
        "audit_ai_integrity_artifact(",
        "scan_privacy_boundary_static(",
        "build_local_witness_receipt(",
        "requests.",
        "httpx",
        "openai",
        "ollama",
        "embedding",
        "telemetry",
        "analytics",
        "database",
    ]
    lowered = helper.lower()
    for phrase in forbidden_runtime:
        assert phrase.lower() not in lowered
    assert "does not rescore, certify, approve, reject, enforce, or override" in helper
    assert "not certification, approval, rejection, enforcement, or final truth" in helper


def test_patch_142_4_docs_and_manifest_exist():
    required = [
        "PATCH_142_4_MANIFEST.txt",
        "PATCH_142_4_RECOVERY_NOTE.md",
        "tests/test_patch_142_4_receipt_reader_narrative_output.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel
