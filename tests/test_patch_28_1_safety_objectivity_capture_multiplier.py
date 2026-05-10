from core.ethics import apply_ethics_to_metrics, contextual_capture_hits, evaluate_ethics


BASE_SIM = {
    "stability": 0.82,
    "trust_index": 0.78,
    "alignment": 0.80,
    "ego": 0.20,
    "collapse_risk": False,
}

BASE_REPORT = {
    "integrity": 0.74,
    "friction": 0.18,
    "collapse_probability": 0.20,
    "trust_friction": 0.20,
}


def test_patch_28_1_objectivity_filter_with_no_appeal_gets_multiplier():
    text = (
        "For objectivity and public safety, every post must receive automated approval "
        "before posting through a central truth gate, with no appeal."
    )

    hits = contextual_capture_hits(text)
    result = evaluate_ethics(
        text,
        governance_result={"power_concentration": 0.78, "decision_transparency": 0.25, "regulatory_presence": 0.25},
    )

    assert hits
    assert hits[0]["severity_multiplier"] > 1.0
    assert hits[0]["hard_capture_trigger"] is True
    assert result["verdict"] == "ETHICALLY HIGH-RISK"
    assert result["ethics_score"] <= 0.46
    assert result["dimensions"]["Micro Sovereignty"] <= 0.28


def test_patch_28_1_biometric_food_gate_is_hard_capture():
    text = (
        "For fair distribution and public health, bakery access requires biometric ID; "
        "food access is conditioned on compliance."
    )

    result = evaluate_ethics(
        text,
        governance_result={"power_concentration": 0.82, "decision_transparency": 0.30, "regulatory_presence": 0.30},
    )
    hit = result["contextual_capture_hits"][0]

    assert hit["hard_capture_trigger"] is True
    assert "biometric id" in hit["hard_capture_terms"] or "access to food" in hit["hard_capture_terms"]
    assert result["ethics_score"] <= 0.46
    assert any("Hard safety/objectivity capture trigger" in risk for risk in result["risks"])


def test_patch_28_1_private_conversation_surveillance_to_police_is_hard_capture():
    text = (
        "For mental-health safety and inclusion, private conversations are monitored "
        "and sent to police for early intervention."
    )

    result = evaluate_ethics(
        text,
        governance_result={"power_concentration": 0.80, "decision_transparency": 0.20, "regulatory_presence": 0.20},
    )

    assert result["contextual_capture_count"] == 1
    assert result["contextual_capture_hits"][0]["hard_capture_trigger"] is True
    assert result["verdict"] == "ETHICALLY HIGH-RISK"
    assert result["dimensions"]["Consent"] <= 0.30


def test_patch_28_1_multiplier_increases_visible_ethics_pressure():
    text = (
        "For safety and fairness, all residents must use mandatory digital ID and biometric control; "
        "mobility access is conditioned on compliance and there is no appeal."
    )
    ethics = evaluate_ethics(
        text,
        governance_result={"power_concentration": 0.84, "decision_transparency": 0.22, "regulatory_presence": 0.20},
    )

    adjusted_sim, adjusted_report = apply_ethics_to_metrics(BASE_SIM, BASE_REPORT, ethics)
    reason = adjusted_report["ethics_adjustment_reason"]

    assert adjusted_report["ethics_adjustment_applied"] is True
    assert reason["contextual_capture_multiplier"] > 1.0
    assert reason["hard_contextual_capture"] is True
    assert reason["total_ethics_pressure"] >= 0.28
    assert adjusted_report["friction"] > BASE_REPORT["friction"]
    assert adjusted_report["collapse_probability"] > BASE_REPORT["collapse_probability"]
    assert adjusted_sim["alignment"] < BASE_SIM["alignment"]


def test_patch_28_1_safeguarded_public_health_language_is_not_capture_by_itself():
    text = (
        "A local opt-in public health notice board publishes open data with independent audit, "
        "appeal, review, transparency, and a sunset clause; participation remains voluntary."
    )

    result = evaluate_ethics(
        text,
        governance_result={"power_concentration": 0.22, "decision_transparency": 0.85, "regulatory_presence": 0.75},
    )

    assert contextual_capture_hits(text) == []
    assert result["contextual_capture_count"] == 0
    assert result["dimensions"]["Micro Sovereignty"] >= 0.65
    assert result["verdict"] != "ETHICALLY HIGH-RISK"
