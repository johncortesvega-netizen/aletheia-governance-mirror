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
    }


def test_patch_67_1_dutch_crisis_authority_is_threshold():
    text = "Een tijdelijke crisisleider krijgt noodbevoegdheden na een ramp, maar er is geen einddatum of beroepsmogelijkheid gedefinieerd."
    label, needs_review, reason = stress_label_for_phrase(text)
    verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)

    assert verdict == "THRESHOLD"
    assert risk == "Medium"
    assert "Needs Safeguards" in label
    assert "einddatum" in reason or "beroepspad" in reason


def test_patch_67_1_dutch_biometric_basic_services_and_fallback_data_are_caught():
    cases = [
        "Een platform voor openbare diensten vereist biometrische identiteit voordat mensen toegang krijgen tot voedsel, huisvesting of medische hulp.",
        "Een governance-model gebruikt fallback data voor vertrouwen, maar presenteert dit als direct gemeten data.",
        "Een digitale portemonnee voor uitkeringen kan automatisch worden bevroren zonder menselijke tussenkomst.",
        "Een besluitvormingsmodel zegt dat menselijke review beschikbaar is, maar reviewers kunnen de automatische uitkomst niet wijzigen.",
    ]
    for text in cases:
        label, needs_review, _reason = stress_label_for_phrase(text)
        verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
        assert verdict == "THRESHOLD", (text, label)
        assert risk == "Medium"
        assert "Needs Safeguards" in label


def test_patch_67_1_dutch_threshold_outputs_get_repair_and_softened_metrics():
    text = "Een overheidsinstantie verzamelt toestemming via een formulier dat mensen moeten tekenen om essentiële diensten te behouden."
    label, needs_review, _reason = stress_label_for_phrase(text)
    verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
    assert verdict == "THRESHOLD"

    calibrated = calibrate_threshold_safeguard_metrics(
        _base_sim(), text=text, verdict=verdict, risk=risk, protocol_label=label
    )
    assert calibrated["threshold_metric_calibration"]["applied"] is True
    assert calibrated["trust_index"] <= 0.92
    assert calibrated["alignment"] <= 0.92
    assert calibrated["ego"] >= 0.05

    report = ensure_threshold_repair_questions(
        {"repair_questions": []}, verdict=verdict, risk=risk, protocol_label=label
    )
    questions = report["repair_questions"]
    assert len(questions) >= 5
    joined = "\n".join(questions).lower()
    assert "appeal" in joined or "correct" in joined or "safeguard" in joined


def test_patch_67_1_dutch_batch_file_and_docs_exist():
    batch_file = Path("examples/batch_scenarios/stress_test_scenarios_nl_v1.txt")
    assert batch_file.exists()
    lines = [line for line in batch_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 50
    assert Path("docs/stress_test_dutch_lexicon_calibration.md").exists()
