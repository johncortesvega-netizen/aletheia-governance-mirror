from pathlib import Path

from core.ai_integrity_mirror import build_ai_static_scan_protocol_context
from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


ROOT = Path(__file__).resolve().parents[1]
OPAQUE_AI_TEXT = (
    "The agent ranks citizens with proprietary logic and hidden criteria. "
    "The score is not reviewable, users cannot challenge the result, and the workflow "
    "does not disclose how the ranking is produced."
)


def test_patch_173_ai_static_context_is_subordinate_to_mirror_check():
    context = build_ai_static_scan_protocol_context(OPAQUE_AI_TEXT, source_module="Mirror Check")
    assert context["role"] == "subordinate_signal_layer"
    assert context["primary_protocol_path"] == "Mirror Check"
    assert context["ai_static_scan_state"] == "ASYLUM"
    assert context["ai_static_scan_risk"] == "High"
    assert context["human_review_required"] is True
    assert context["authority_claim"] is False
    assert "does not certify" in context["notice"]
    assert "separate AI Integrity verdict" in context["notice"]


def test_patch_173_local_receipt_renders_ai_static_scan_context():
    context = build_ai_static_scan_protocol_context(OPAQUE_AI_TEXT, source_module="Stress Test")
    receipt = build_local_witness_receipt(
        module="Simulation",
        input_text=OPAQUE_AI_TEXT,
        processed_text=OPAQUE_AI_TEXT,
        scan={"scan_mode": "Scan my idea", "ai_static_scan_context": context},
        sim={"stability": 0.5, "trust_index": 0.5, "alignment": 0.5, "ego": 0.2, "collapse_risk": True},
        report={
            "integrity": 0.4,
            "friction": 0.5,
            "collapse_probability": 0.6,
            "trust_friction": 0.4,
            "repair_questions": ["Where is the appeal path?"],
            "ai_static_scan_context": context,
        },
        verdict="ASYLUM",
        risk="High",
        protocol_label="Simulation / Asylum",
        app_version="test",
    )
    rendered = render_local_witness_receipt_text(receipt)
    assert "AI STATIC SCAN CONTEXT" in rendered
    assert "Role: subordinate_signal_layer" in rendered
    assert "Primary protocol path: Stress Test" in rendered
    assert "Static scan state: ASYLUM" in rendered
    assert "Static scan risk: High" in rendered
    assert "No AI static scan context attached" not in rendered


def test_patch_173_app_wires_ai_static_context_into_core_modules():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "build_ai_static_scan_protocol_context" in app
    assert 'source_module="Mirror Check"' in app
    assert 'source_module="Stress Test"' in app
    assert "AI static scan context — subordinate to Mirror Check" in app
    assert "AI static scan context — subordinate to Stress Test" in app


def test_patch_173_no_new_taxonomy_state_or_world_lens_change_marker():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "AI_STATIC_SCAN" not in app
    assert "ai_static_scan_context" in app
