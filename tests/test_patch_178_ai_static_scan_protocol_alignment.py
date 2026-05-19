from core.ai_integrity_mirror import build_ai_static_scan_protocol_context
from core.witness import build_local_witness_receipt, render_local_witness_receipt_text
from ui.receipt_reader import parse_receipt_standard_view


LOW_AI_TEXT = "This is a short neutral note with no AI-specific deployment claims."


def test_patch_178_context_records_primary_protocol_when_stronger_than_raw_scan():
    context = build_ai_static_scan_protocol_context(
        LOW_AI_TEXT,
        source_module="Mirror Check",
        primary_state="ASYLUM",
        primary_risk="High",
        primary_protocol_label="MEI7 Ethics Gate / Asylum",
    )

    assert context["ai_static_scan_state"] == "SANCTUARY"
    assert context["ai_static_scan_risk"] == "Low"
    assert context["protocol_context_state"] == "ASYLUM"
    assert context["protocol_context_risk"] == "High"
    assert context["protocol_context_label"] == "MEI7 Ethics Gate / Asylum"
    assert context["protocol_alignment"] == "primary_protocol_stronger"
    assert "primary" in context["alignment_note"].lower()


def test_patch_178_local_receipt_renders_protocol_aligned_static_scan_context():
    context = build_ai_static_scan_protocol_context(
        LOW_AI_TEXT,
        source_module="Mirror Check",
        primary_state="ASYLUM",
        primary_risk="High",
        primary_protocol_label="MEI7 Ethics Gate / Asylum",
    )
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text=LOW_AI_TEXT,
        processed_text=LOW_AI_TEXT,
        scan={"scan_mode": "Scan my idea", "ai_static_scan_context": context},
        sim={"stability": 0.5, "trust_index": 0.8, "alignment": 0.78, "ego": 0.15, "collapse_risk": True},
        report={
            "integrity": 0.4162,
            "friction": 0.1086,
            "collapse_probability": 0.24,
            "trust_friction": 0.2,
            "repair_questions": ["Where is the appeal path?"],
            "ai_static_scan_context": context,
        },
        verdict="ASYLUM",
        risk="High",
        protocol_label="MEI7 Ethics Gate / Asylum",
        app_version="test",
    )
    rendered = render_local_witness_receipt_text(receipt)

    assert "AI STATIC SCAN CONTEXT" in rendered
    assert "Primary protocol state: ASYLUM" in rendered
    assert "Protocol context state: ASYLUM" in rendered
    assert "Effective receipt-context state: ASYLUM" in rendered
    assert "Static scan state: SANCTUARY" in rendered
    assert "Protocol alignment: primary_protocol_stronger" in rendered


def test_patch_178_receipt_reader_parses_aligned_and_raw_static_scan_values():
    receipt_text = """LOCAL WITNESS RECEIPT
Module: Mirror Check
Protocol-adjusted state: ASYLUM
Risk: High
Protocol label: MEI7 Ethics Gate / Asylum
Integrity: 0.4162
Trust index: 0.8000
Alignment: 0.7806
Ego: 0.1549

AI STATIC SCAN CONTEXT
Role: subordinate_signal_layer
Primary protocol path: Mirror Check
Primary protocol state: ASYLUM
Primary protocol risk: High
Primary protocol label: MEI7 Ethics Gate / Asylum
Protocol context state: ASYLUM
Protocol context risk: High
Protocol context label: MEI7 Ethics Gate / Asylum
Effective receipt-context state: ASYLUM
Effective receipt-context risk: High
Effective receipt-context label: MEI7 Ethics Gate / Asylum
Protocol alignment: primary_protocol_stronger
Alignment note: Primary protocol reading is stronger than the raw AI static scan; the primary receipt values control this reading.
Static scan state: SANCTUARY
Static scan risk: Low
Static scan label: AI Integrity Patrol / Low-Risk Internal Reading
Risk pressure: 0.0000
Finding count: 0
Notice: AI static scan is attached as protocol context only.
Findings:
- None recorded
Repair questions:
- None recorded

SCANNER FEATURES
scan_mode: Scan my idea
"""
    view = parse_receipt_standard_view(receipt_text)
    context = view["ai_static_scan_context"]

    assert view["module_family"] == "Mirror Check"
    assert view["native_state"] == "ASYLUM"
    assert context["protocol_context_state"] == "ASYLUM"
    assert context["protocol_context_risk"] == "High"
    assert context["static_scan_state"] == "SANCTUARY"
    assert context["static_scan_risk"] == "Low"
    assert context["protocol_alignment"] == "primary_protocol_stronger"


def test_patch_178_receipt_reader_render_mentions_primary_values_control():
    source = open("ui/receipt_reader.py", encoding="utf-8").read()
    assert "Protocol context state" in source
    assert "Raw AI static scan only" in source
    assert "the primary receipt values control this reading" in source
