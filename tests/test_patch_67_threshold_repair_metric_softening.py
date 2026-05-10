from pathlib import Path

from protocol import (
    apply_guardrail_verdict,
    calibrate_threshold_safeguard_metrics,
    ensure_threshold_repair_questions,
    stress_label_for_phrase,
)


def _base_sim():
    return {
        "stability": 0.96,
        "trust_index": 1.0,
        "alignment": 1.0,
        "ego": 0.0,
        "ego_pressure": 0.0,
        "Ep": 0.0,
        "trust_trace": [1.0, 1.0],
        "alignment_trace": [1.0, 1.0],
        "ego_trace": [0.0, 0.0],
    }


def test_patch_67_threshold_metrics_are_not_perfect_for_needs_safeguards():
    text = "A decision model says human review is available, but reviewers cannot change the automated outcome."
    label, needs_review, _reason = stress_label_for_phrase(text)
    verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
    assert verdict == "THRESHOLD"
    assert "Needs Safeguards" in label

    calibrated = calibrate_threshold_safeguard_metrics(
        _base_sim(), text=text, verdict=verdict, risk=risk, protocol_label=label
    )
    assert calibrated["threshold_metric_calibration"]["applied"] is True
    assert calibrated["trust_index"] <= 0.92
    assert calibrated["alignment"] <= 0.92
    assert calibrated["ego"] >= 0.05
    assert calibrated["ego_pressure"] >= 0.05


def test_patch_67_threshold_outputs_receive_repair_questions():
    report = {"repair_questions": []}
    patched = ensure_threshold_repair_questions(
        report,
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Consent Under Pressure / Needs Safeguards",
    )
    questions = patched.get("repair_questions") or []
    joined = "\n".join(questions).lower()
    assert len(questions) >= 5
    assert "safeguard" in joined
    assert "appeal" in joined or "correct" in joined
    assert "aletheia becoming the authority" in joined


def test_patch_67_asylum_is_not_downgraded_by_threshold_softening():
    text = "An evil dictator takes permanent power with no appeal."
    label, needs_review, _reason = stress_label_for_phrase(text)
    verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
    assert verdict == "ASYLUM"

    calibrated = calibrate_threshold_safeguard_metrics(
        _base_sim(), text=text, verdict=verdict, risk=risk, protocol_label=label
    )
    assert calibrated["threshold_metric_calibration"]["applied"] is False
    assert calibrated["trust_index"] == 1.0
    assert calibrated["alignment"] == 1.0


def test_patch_67_app_wires_threshold_helpers_and_docs_exist():
    app_text = Path("app.py").read_text(encoding="utf-8")
    assert "calibrate_threshold_safeguard_metrics" in app_text
    assert "ensure_threshold_repair_questions" in app_text
    assert Path("docs/stress_test_threshold_repair_calibration.md").exists()
