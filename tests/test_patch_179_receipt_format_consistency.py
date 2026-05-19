from pathlib import Path

from core.witness import render_local_witness_batch_index_text, render_local_witness_receipt_text


ROOT = Path(__file__).resolve().parents[1]


def _minimal_receipt(module="Mirror Check"):
    return {
        "receipt_type": "local_witness_receipt",
        "receipt_version": "local-witness-v2",
        "generated_at_utc": "2026-05-19T00:00:00Z",
        "app_version": "test",
        "rubric_version": "v0.1",
        "prompt_version": "v0.1",
        "active_modules": [module],
        "module": module,
        "input_status": "USER_INPUT",
        "input_type": "USER_INPUT",
        "invisibility_filter_applied": False,
        "notice": "test notice",
        "dataflow": "Power -> Mirror, never Mirror -> Power",
        "hashes": {
            "scenario_sha256": "scenario-hash",
            "processed_scenario_sha256": "processed-scenario-hash",
            "document_fingerprint_sha256": "document-hash",
            "processed_document_fingerprint_sha256": "processed-document-hash",
            "report_fingerprint_sha256": "report-hash",
            "audit_receipt_sha256": "audit-hash",
        },
        "authority_boundary": {
            "stored_locally": True,
            "public_ledger": False,
            "global_id_sync": False,
            "central_storage": False,
            "authority_claim": False,
            "human_review_required": True,
        },
        "verdict": {
            "protocol_adjusted_state": "ASYLUM",
            "risk": "High",
            "protocol_label": "Test / Asylum",
        },
        "metrics": {
            "integrity": 0.27,
            "friction": 0.34,
            "collapse_probability": 0.83,
            "trust_index": 0.62,
            "alignment": 0.53,
            "ego": 0.36,
        },
        "report": {},
        "repair_questions": ["Who can challenge this?", "What evidence is missing?"],
    }


def test_patch_179_local_receipts_have_plain_english_sections_and_preserve_values():
    text = render_local_witness_receipt_text(_minimal_receipt())
    assert "PLAIN-ENGLISH RECEIPT SUMMARY" in text
    assert "What is this document?" in text
    assert "The main results" in text
    assert "How power and control are distributed" in text
    assert "Next steps and questions" in text
    assert "Protocol-adjusted state: ASYLUM" in text
    assert "Risk: High" in text
    assert "Protocol label: Test / Asylum" in text
    assert "Integrity (Diagnostic metric): 0.2700" in text
    assert "MACHINE-READABLE RECEIPT JSON" in text


def test_patch_179_stress_receipts_use_stress_test_display_name_in_summary():
    text = render_local_witness_receipt_text(_minimal_receipt(module="Simulation"))
    assert "local Stress Test receipt" in text
    assert "Module: Simulation" in text


def test_patch_179_batch_index_has_plain_english_batch_summary():
    index = {
        "receipt_type": "local_witness_batch_index",
        "generated_at_utc": "2026-05-19T00:00:00Z",
        "app_version": "test",
        "module": "Simulation",
        "receipt_count": 1,
        "hashes": {"batch_index_sha256": "batch-hash"},
        "notice": "test notice",
        "dataflow": "Power -> Mirror, never Mirror -> Power",
        "items": [{"item": 1, "protocol_adjusted_state": "ASYLUM", "risk": "High", "protocol_label": "Test / Asylum", "audit_receipt_sha256": "audit-hash"}],
    }
    text = render_local_witness_batch_index_text(index)
    assert "PLAIN-ENGLISH BATCH SUMMARY" in text
    assert "01: ASYLUM / High / Test / Asylum" in text
    assert "The batch index summarizes the readings; it does not merge them into one final verdict." in text
    assert "MACHINE-READABLE BATCH INDEX JSON" in text


def test_patch_179_world_lens_markdown_receipt_uses_plain_english_summary():
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "## Plain-English receipt summary" in app_source
    assert "This is a World Lens selected-year evidence receipt." in app_source
    assert "### How power and control are distributed" in app_source
    assert "The 9k view is an analytical anti-tyranny scaffold only." in app_source


def test_patch_179_evidence_lab_receipt_examples_use_same_section_names():
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "Plain-English receipt summary" in app_source
    assert "This is an Evidence Lab review note." in app_source
    assert "How power and control are distributed" in app_source
    assert "This receipt keeps control with the user" in app_source
