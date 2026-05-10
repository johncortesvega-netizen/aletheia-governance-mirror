from core.ethics import evaluate_ethics, apply_ethics_to_metrics
from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


def test_ethics_integrity_gap_applies_visible_integrity_adjustment():
    text = "This policy protects fairness and rights through mandatory enforcement, a central grid, and universal ID."
    ethics = evaluate_ethics(text)
    sim = {"stability": 0.80, "trust_index": 1.0, "alignment": 1.0, "ego": 0.0, "collapse_risk": False}
    report = {"integrity": 0.88, "friction": 0.0, "collapse_probability": 0.07, "trust_friction": 0.0}

    adjusted_sim, adjusted_report = apply_ethics_to_metrics(sim, report, ethics)

    assert adjusted_report["ethics_adjustment_applied"] is True
    assert adjusted_report["integrity"] <= ethics["ethics_score"] + 0.0001
    assert "raw_metrics_before_ethics" in adjusted_report
    assert adjusted_report["raw_metrics_before_ethics"]["integrity"] == 0.88


def test_local_witness_receipt_records_ethics_adjustment_block():
    ethics = {
        "ethics_score": 0.5,
        "ethics_adjusted_integrity": 0.5,
        "micro_sovereignty": 0.22,
        "contextual_capture_count": 1,
        "grip_marker_count": 0,
        "ethics_verdict": "ETHICALLY AMBIGUOUS",
        "risks": ["Positive language is coupled to mandatory power"],
        "strengths": [],
    }
    sim = {"stability": 0.75, "trust_index": 0.8, "alignment": 0.82, "ego": 0.12, "collapse_risk": False}
    report = {
        "integrity": 0.5,
        "friction": 0.1,
        "collapse_probability": 0.2,
        "trust_friction": 0.05,
        "raw_metrics_before_ethics": {"integrity": 0.88},
        "ethics_diagnostics": ethics,
        "ethics_adjustment_applied": True,
        "ethics_adjustment_reason": {"contextual_capture_count": 1, "total_ethics_pressure": 0.1},
    }
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text="fairness through mandatory enforcement",
        processed_text="fairness through mandatory enforcement",
        input_status="USER_INPUT",
        scan={},
        sim=sim,
        report=report,
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Needs Safeguards",
        app_version="test",
    )
    text = render_local_witness_receipt_text(receipt)
    assert receipt["ethics_adjustment"]["applied"] is True
    assert "ETHICS ADJUSTMENT" in text
    assert "Applied: True" in text
