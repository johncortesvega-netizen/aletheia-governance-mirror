from pathlib import Path

from calibration.cognitive_resilience_scenarios import scenario_by_id
from core.cognitive_resilience import (
    apply_cognitive_resilience_to_metrics,
    evaluate_cognitive_resilience,
)


BASE_REPORT = {
    "integrity": 0.70,
    "friction": 0.20,
    "collapse_probability": 0.20,
    "trust_friction": 0.20,
}


def _diagnostics(scenario_id: str, *, power: float = 0.30, transparency: float = 0.82):
    scenario = scenario_by_id(scenario_id)
    return evaluate_cognitive_resilience(
        scenario.text,
        governance_result={
            "power_concentration": power,
            "decision_transparency": transparency,
        },
        features={"centralization": power, "transparency": transparency},
    )


def test_patch_28_high_decentralized_education_lightly_stabilizes_metrics():
    diagnostics = _diagnostics("CR-02", power=0.24, transparency=0.90)
    adjusted = apply_cognitive_resilience_to_metrics(BASE_REPORT, diagnostics)

    assert diagnostics["cognitive_resilience_signal"] == "high"
    assert diagnostics["educational_decentralization_signal"] == "high"
    assert diagnostics["central_info_capture_signal"] == "low"
    assert adjusted["integrity"] > BASE_REPORT["integrity"]
    assert adjusted["friction"] < BASE_REPORT["friction"]
    assert adjusted["collapse_probability"] < BASE_REPORT["collapse_probability"]
    assert adjusted["trust_friction"] < BASE_REPORT["trust_friction"]
    scoring = adjusted["cognitive_resilience_diagnostics"]["scoring_adjustment"]
    assert scoring["patch"] == "28"
    assert scoring["applied"] is True
    assert scoring["lightweight"] is True


def test_patch_28_low_cr_central_information_capture_raises_friction_and_collapse():
    diagnostics = _diagnostics("CR-11", power=0.76, transparency=0.30)
    adjusted = apply_cognitive_resilience_to_metrics(BASE_REPORT, diagnostics)

    assert diagnostics["central_info_capture_signal"] == "high"
    assert adjusted["integrity"] < BASE_REPORT["integrity"]
    assert adjusted["friction"] > BASE_REPORT["friction"]
    assert adjusted["collapse_probability"] > BASE_REPORT["collapse_probability"]
    assert adjusted["trust_friction"] > BASE_REPORT["trust_friction"]


def test_patch_28_high_cr_does_not_launder_unauditable_central_power():
    diagnostics = _diagnostics("CR-21", power=0.88, transparency=0.22)
    adjusted = apply_cognitive_resilience_to_metrics(BASE_REPORT, diagnostics)
    scoring = adjusted["cognitive_resilience_diagnostics"]["scoring_adjustment"]

    assert diagnostics["cognitive_resilience_signal"] in {"high_but_captured", "low"}
    assert scoring["hard_capture_blocks_stabilization"] is True
    assert adjusted["integrity"] <= BASE_REPORT["integrity"]
    assert adjusted["friction"] >= BASE_REPORT["friction"]
    assert adjusted["collapse_probability"] >= BASE_REPORT["collapse_probability"]


def test_patch_28_safety_objectivity_capture_overrides_resilience_language():
    diagnostics = _diagnostics("CR-33", power=0.82, transparency=0.24)
    adjusted = apply_cognitive_resilience_to_metrics(BASE_REPORT, diagnostics)
    scoring = adjusted["cognitive_resilience_diagnostics"]["scoring_adjustment"]

    assert diagnostics["central_info_capture_signal"] == "high"
    assert diagnostics["evidence"]["contextual_capture_count"] > 0
    assert scoring["hard_capture_blocks_stabilization"] is True
    assert adjusted["integrity"] < BASE_REPORT["integrity"]
    assert adjusted["friction"] > BASE_REPORT["friction"]


def test_patch_28_no_change_when_diagnostics_are_missing():
    assert apply_cognitive_resilience_to_metrics(BASE_REPORT, None) == BASE_REPORT


def test_patch_28_app_wires_cr_scoring_after_diagnostics():
    text = Path("app.py").read_text(encoding="utf-8")
    assert "apply_cognitive_resilience_to_metrics" in text
    assert 'report = apply_cognitive_resilience_to_metrics(' in text
