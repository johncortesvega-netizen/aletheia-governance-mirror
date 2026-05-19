from core.ai_integrity_mirror import build_ai_static_scan_protocol_context
from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


LOW_AI_TEXT = "This is a short neutral note with no AI deployment claims."


def _stress_receipt_with_protocol_override():
    context = build_ai_static_scan_protocol_context(
        LOW_AI_TEXT,
        source_module="Stress Test",
        primary_state="ASYLUM",
        primary_risk="High",
        primary_protocol_label="Predictive Sentencing Capture / Asylum",
    )
    return build_local_witness_receipt(
        module="Simulation",
        input_text="A predictive sentencing system uses hidden ranking and blocks appeal.",
        processed_text="A predictive sentencing system uses hidden ranking and blocks appeal.",
        scan={"scan_mode": "Scan my idea", "ai_static_scan_context": context},
        sim={
            "stability": 0.7583,
            "trust_index": 0.8,
            "alignment": 0.85,
            "ego": 0.1,
            "collapse_risk": True,
        },
        report={
            "integrity": 0.7301,
            "friction": 0.1042,
            "collapse_probability": 0.165,
            "trust_friction": 0.174,
            "protocol_capture_risk": True,
            "repair_questions": ["Where is the appeal path?"],
            "ai_static_scan_context": context,
        },
        verdict="ASYLUM",
        risk="High",
        protocol_label="Predictive Sentencing Capture / Asylum",
        app_version="test",
    )


def test_patch_180_plain_summary_labels_stress_metrics_as_diagnostics():
    text = render_local_witness_receipt_text(_stress_receipt_with_protocol_override())

    assert "PLAIN-ENGLISH RECEIPT SUMMARY" in text
    assert "Protocol-adjusted state: ASYLUM" in text
    assert "Risk: High" in text
    assert "Protocol capture risk: True" in text
    assert "Integrity (Stress Test diagnostic metric): 0.7301" in text
    assert "Friction (Stress Test diagnostic metric): 0.1042" in text
    assert "Collapse probability (Stress Test diagnostic metric): 0.1650" in text
    assert "Protocol guardrails may route the receipt to THRESHOLD or ASYLUM" in text


def test_patch_180_ai_static_scan_context_no_longer_overwrites_raw_static_values():
    text = render_local_witness_receipt_text(_stress_receipt_with_protocol_override())

    assert "Effective receipt-context state: ASYLUM" in text
    assert "Effective receipt-context risk: High" in text
    assert "Effective receipt-context label: Predictive Sentencing Capture / Asylum" in text
    assert "Static scan state: SANCTUARY" in text
    assert "Static scan risk: Low" in text
    assert "Static scan label: AI Integrity Patrol / Low-Risk Internal Reading" in text
    assert "Raw static scan state:" not in text
