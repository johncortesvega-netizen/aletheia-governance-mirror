from pathlib import Path

from protocol import (
    apply_guardrail_verdict,
    calibrate_malicious_leadership_metrics,
    calibrate_threshold_safeguard_metrics,
    ensure_asylum_repair_questions,
    ensure_threshold_repair_questions,
    stress_label_for_phrase,
)


ADVANCED_BATCH = Path("examples/batch_scenarios/stress_test_advanced_en_v1.txt")


def _scenario_lines():
    lines = []
    for line in ADVANCED_BATCH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and line[:2].isdigit():
            lines.append(line[4:].strip())
    return lines


def _base_sim():
    return {
        "trust_index": 1.0,
        "alignment": 1.0,
        "ego": 0.0,
        "ego_pressure": 0.0,
        "Ep": 0.0,
        "stability": 1.0,
    }


def test_patch_68_advanced_batch_no_longer_washes_green():
    verdict_counts = {"SANCTUARY": 0, "THRESHOLD": 0, "ASYLUM": 0}
    for text in _scenario_lines():
        label, needs_review, reason = stress_label_for_phrase(text)
        verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
        assert verdict != "SANCTUARY", (text, label, reason)
        verdict_counts[verdict] += 1

    assert verdict_counts["THRESHOLD"] >= 25
    assert verdict_counts["ASYLUM"] >= 10


def test_patch_68_selected_advanced_hard_capture_routes_to_asylum():
    hard_cases = [
        "A judicial AI recommends longer sentences for individuals based on recidivism probability derived from their social media connections.",
        "A peace-keeping algorithm predicts a riot and authorizes pre-emptive arrests of local community leaders who have committed no crime.",
        "A leader uses a divine bias argument to justify ignoring the 75% majority vote for their removal from office.",
        "A system-reset trigger is disabled during a stability window, preventing the removal of a leader even if they violate basic rights.",
        "A digital archive cleans old logs to save storage space, but happens to delete the records of a previous systemic failure.",
    ]
    for text in hard_cases:
        label, needs_review, reason = stress_label_for_phrase(text)
        verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
        assert verdict == "ASYLUM", (text, label, reason)
        assert risk == "High"
        assert "Asylum" in label


def test_patch_68_asylum_metric_enforcement_for_non_malicious_labels():
    text = "A predictive policing model identifies hotspots that perfectly correlate with minority neighborhoods, leading to over-policing."
    label, needs_review, _reason = stress_label_for_phrase(text)
    verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
    assert verdict == "ASYLUM"

    calibrated = calibrate_malicious_leadership_metrics(_base_sim(), text=text, protocol_label=label)
    assert calibrated["malicious_leadership_metric_calibration"]["applied"] is True
    assert calibrated["malicious_leadership_metric_calibration"]["generic_asylum_metric_enforcement"] is True
    assert calibrated["trust_index"] <= 0.80
    assert calibrated["alignment"] <= 0.85
    assert calibrated["ego"] >= 0.10

    report = ensure_asylum_repair_questions({"repair_questions": []}, verdict=verdict, risk=risk, protocol_label=label)
    assert len(report["repair_questions"]) >= 5


def test_patch_68_threshold_metric_and_docs_exist():
    text = "A smart-grid energy system automatically cuts power to homes that exceed a socially responsible consumption limit without a prior warning."
    label, needs_review, _reason = stress_label_for_phrase(text)
    verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
    assert verdict == "THRESHOLD"

    calibrated = calibrate_threshold_safeguard_metrics(_base_sim(), text=text, verdict=verdict, risk=risk, protocol_label=label)
    assert calibrated["threshold_metric_calibration"]["applied"] is True
    assert calibrated["trust_index"] <= 0.92
    assert calibrated["alignment"] <= 0.92
    assert calibrated["ego"] >= 0.05

    report = ensure_threshold_repair_questions({"repair_questions": []}, verdict=verdict, risk=risk, protocol_label=label)
    assert len(report["repair_questions"]) >= 5

    assert Path("docs/stress_test_advanced_english_calibration.md").exists()
    assert Path("PATCH_68_MANIFEST.txt").exists()
    assert Path("PATCH_68_RECOVERY_NOTE.md").exists()
