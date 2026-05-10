from core.cognitive_resilience import (
    apply_cognitive_resilience_to_metrics,
    evaluate_cognitive_resilience,
    positive_cr_baseline_stabilizer,
)
from core.witness import build_local_witness_receipt

GOV = {
    "power_concentration": 0.25,
    "decision_transparency": 0.74,
    "regulatory_presence": 0.65,
    "anonymity_level": 0.04,
}


def _positive_report(text: str) -> dict:
    diagnostics = evaluate_cognitive_resilience(text, governance_result=GOV, features=GOV)
    report = {
        "integrity": 0.70,
        "friction": 0.05,
        "collapse_probability": 0.08,
        "trust_friction": 0.03,
        "cognitive_resilience_diagnostics": diagnostics,
    }
    return apply_cognitive_resilience_to_metrics(report, diagnostics)


def test_patch_30_2_positive_cr_can_stabilize_overhard_asylum_to_sanctuary():
    text = "De Reparatie-Gids: Lokale technische kennis delen via hobby-bijeenkomsten; geen afhankelijkheid van fabrikanten."
    report = _positive_report(text)
    judgment = {
        "verdict": "ASYLUM",
        "corruption_risk": "High",
        "guardrail_risk": "High",
        "stress_label": "Generic Local Scan",
        "reasons": [],
        "questions": ["What appeal path exists?"],
    }

    adjusted = positive_cr_baseline_stabilizer(judgment, report)

    assert adjusted["verdict"] == "SANCTUARY"
    assert adjusted["corruption_risk"] == "Low"
    assert adjusted["positive_cr_stabilizer"]["applied"] is True
    assert "high CR" in adjusted["positive_cr_stabilizer"]["reason"] or "High CR" in adjusted["positive_cr_stabilizer"]["reason"]


def test_patch_30_2_positive_cr_stabilizer_blocks_capture_architecture():
    text = "Technocratisch Dorp: Hoogopgeleide bevolking, maar besluiten worden genomen door een AI die niemand mag auditen."
    diagnostics = evaluate_cognitive_resilience(text, governance_result=GOV, features=GOV)
    report = {
        "integrity": 0.70,
        "friction": 0.05,
        "collapse_probability": 0.08,
        "trust_friction": 0.03,
        "cognitive_resilience_diagnostics": diagnostics,
    }
    judgment = {"verdict": "ASYLUM", "corruption_risk": "High", "guardrail_risk": "High", "reasons": []}

    adjusted = positive_cr_baseline_stabilizer(judgment, report)

    assert adjusted["verdict"] == "ASYLUM"
    assert "positive_cr_stabilizer" not in adjusted
    assert diagnostics["capture_architecture_signal"] == "present"
    assert diagnostics["high_cr_laundering_blocked"] is True


def test_patch_30_2_positive_cr_stabilizer_does_not_override_safety_capture():
    text = "De Veiligheids-Scan: Biometrische controle bij de bakker voor eerlijke verdeling van schaarse goederen."
    diagnostics = evaluate_cognitive_resilience(text, governance_result=GOV, features=GOV)
    report = {
        "integrity": 0.70,
        "friction": 0.05,
        "collapse_probability": 0.08,
        "trust_friction": 0.03,
        "cognitive_resilience_diagnostics": diagnostics,
    }
    judgment = {"verdict": "ASYLUM", "corruption_risk": "High", "guardrail_risk": "High", "reasons": []}

    adjusted = positive_cr_baseline_stabilizer(judgment, report)

    assert adjusted["verdict"] == "ASYLUM"
    assert "positive_cr_stabilizer" not in adjusted
    assert diagnostics["central_info_capture_signal"] in {"medium", "high"}


def test_patch_30_2_witness_receipt_keeps_edd_diagnostics_visible():
    text = "Entertainment-Dwang: Gratis internet in ruil voor het dagelijks kijken naar 4 uur goedgekeurde influencers."
    diagnostics = evaluate_cognitive_resilience(text, governance_result=GOV, features=GOV)
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text=text,
        processed_text=text,
        input_status="USER_INPUT",
        input_type="USER_INPUT",
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Calibration",
        scan=GOV,
        report={"cognitive_resilience_diagnostics": diagnostics},
    )

    cr = receipt["cognitive_resilience_diagnostics"]
    assert cr["education_defense_signal"] in {"eroded", "pressured"}
    assert cr["entertainment_compliance_signal"] in {"medium", "high"}
    assert cr["evidence"]["entertainment_compliance_terms"]
