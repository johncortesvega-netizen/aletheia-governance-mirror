from core.ethics import (
    contextual_capture_hits,
    evaluate_ethics,
    grip_marker_hits,
    micro_sovereignty_signal,
)


def test_positive_rights_language_with_enforcement_is_penalized():
    safe = evaluate_ethics(
        "A local community review board protects rights through opt-in appeal, public audit, and a sunset clause.",
        governance_result={"power_concentration": 0.25, "decision_transparency": 0.8, "regulatory_presence": 0.8},
    )
    captured = evaluate_ethics(
        "For fairness and rights, all people must comply with mandatory enforcement through a central grid.",
        governance_result={"power_concentration": 0.65, "decision_transparency": 0.45, "regulatory_presence": 0.35},
    )

    assert contextual_capture_hits("fairness and rights require mandatory enforcement through a central grid")
    assert captured["ethics_score"] < safe["ethics_score"]
    assert captured["dimensions"]["Micro Sovereignty"] < safe["dimensions"]["Micro Sovereignty"]
    assert any("mandatory power" in risk or "enforcement" in risk for risk in captured["risks"])


def test_grip_markers_force_high_risk_ethics_review():
    result = evaluate_ethics(
        "The authority has permanent control, no appeal, and cannot be questioned.",
        governance_result={"power_concentration": 0.70, "decision_transparency": 0.30, "regulatory_presence": 0.20},
    )

    assert grip_marker_hits("permanent control and no appeal cannot be questioned")
    assert result["verdict"] == "ETHICALLY HIGH-RISK"
    assert result["ethics_score"] <= 0.42
    assert result["dimensions"]["Consent"] <= 0.30
    assert result["dimensions"]["Accountability"] <= 0.30


def test_micro_sovereignty_favors_local_revocable_review_over_global_identity_grid():
    local = micro_sovereignty_signal(
        "A local household and community review process uses consent, appeal, rollback, privacy, and a sunset clause.",
        governance_result={"power_concentration": 0.20},
    )
    central = micro_sovereignty_signal(
        "A central grid with universal ID and biometric authority enables remote enforcement and constant surveillance.",
        governance_result={"power_concentration": 0.75},
    )

    assert local > 0.65
    assert central < 0.35
    assert local > central


def test_public_good_lift_does_not_override_contextual_capture():
    result = evaluate_ethics(
        "Water is a shared human right, but access is controlled by mandatory identity enforcement through a central grid.",
        governance_result={"power_concentration": 0.72, "decision_transparency": 0.40, "regulatory_presence": 0.30},
    )

    assert result["ethics_score"] < 0.60
    assert result["verdict"] != "ETHICALLY STRONG"
    assert result["contextual_capture_hits"]
