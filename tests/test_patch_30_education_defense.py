from core.cognitive_resilience import (
    apply_cognitive_resilience_to_metrics,
    evaluate_cognitive_resilience,
)
from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


BASE_REPORT = {
    "integrity": 0.70,
    "friction": 0.20,
    "collapse_probability": 0.20,
    "trust_friction": 0.20,
}

BASE_SIM = {
    "stability": 0.80,
    "trust_index": 0.82,
    "alignment": 0.86,
    "ego": 0.08,
    "collapse_risk": False,
}

PROTECTED_EDUCATION_TEXT = (
    "A local community uses open-source education, repair guides, books, craft workshops, "
    "source checking, question circles, elders, mentors, and master-apprentice practice. "
    "Participation is voluntary, appealable, revocable, and there is no central editor or truth gatekeeper."
)

ERODED_EDUCATION_TEXT = (
    "For efficient public safety, hobbies are banned unless approved. A mandatory entertainment "
    "compliance system uses an algorithmic feed, obedience profile, attention scoring, infinite scroll, "
    "licensed speech, and archive rewriting so reading is replaced and dissent is filtered."
)

CAPTURE_WITH_EDUCATION_TEXT = (
    "The city teaches advanced open-source lessons and question circles, but a central AI with one private "
    "server keyholder controls the official feed, uses mandatory entertainment compliance, and provides no appeal."
)


def _diagnostics(text: str, *, power: float, transparency: float):
    return evaluate_cognitive_resilience(
        text,
        governance_result={"power_concentration": power, "decision_transparency": transparency},
        features={"centralization": power, "transparency": transparency},
    )


def test_patch_30_protected_education_defense_is_system_property_not_people_judgment():
    diagnostics = _diagnostics(PROTECTED_EDUCATION_TEXT, power=0.20, transparency=0.90)

    assert diagnostics["education_defense_signal"] == "protected"
    assert diagnostics["entertainment_compliance_signal"] == "low"
    assert diagnostics["algorithmic_erosion_signal"] == "low"
    assert diagnostics["z_axis_depth_risk_signal"] == "low"
    assert "system propert" in diagnostics["education_defense_property_note"].lower()
    assert "judgment of people" in diagnostics["education_defense_property_note"].lower()


def test_patch_30_entertainment_compliance_and_algorithmic_erosion_raise_pressure():
    diagnostics = _diagnostics(ERODED_EDUCATION_TEXT, power=0.78, transparency=0.28)
    adjusted = apply_cognitive_resilience_to_metrics(BASE_REPORT, diagnostics)
    edd = adjusted["cognitive_resilience_diagnostics"]["scoring_adjustment"]["education_defense_adjustment"]

    assert diagnostics["education_defense_signal"] == "eroded"
    assert diagnostics["entertainment_compliance_signal"] == "high"
    assert diagnostics["algorithmic_erosion_signal"] == "high"
    assert edd["patch"] == "30"
    assert edd["applied"] is True
    assert edd["lightweight"] is True
    assert adjusted["integrity"] < BASE_REPORT["integrity"]
    assert adjusted["friction"] > BASE_REPORT["friction"]
    assert adjusted["collapse_probability"] > BASE_REPORT["collapse_probability"]
    assert adjusted["trust_friction"] > BASE_REPORT["trust_friction"]


def test_patch_30_high_education_still_does_not_launder_capture():
    diagnostics = _diagnostics(CAPTURE_WITH_EDUCATION_TEXT, power=0.86, transparency=0.25)
    adjusted = apply_cognitive_resilience_to_metrics(BASE_REPORT, diagnostics)
    scoring = adjusted["cognitive_resilience_diagnostics"]["scoring_adjustment"]

    assert diagnostics["central_info_capture_signal"] == "high"
    assert diagnostics["education_defense_signal"] in {"eroded", "pressured"}
    assert scoring["hard_capture_blocks_stabilization"] is True
    assert adjusted["integrity"] <= BASE_REPORT["integrity"]
    assert adjusted["friction"] >= BASE_REPORT["friction"]


def test_patch_30_receipt_renders_education_defense_trace():
    diagnostics = _diagnostics(ERODED_EDUCATION_TEXT, power=0.78, transparency=0.28)
    report = apply_cognitive_resilience_to_metrics(dict(BASE_REPORT), diagnostics)
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text=ERODED_EDUCATION_TEXT,
        processed_text=ERODED_EDUCATION_TEXT,
        scan={"power_concentration": 0.78, "decision_transparency": 0.28},
        sim=BASE_SIM,
        report=report,
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Education Defense Review",
        app_version="patch-30-test",
    )
    rendered = render_local_witness_receipt_text(receipt)

    assert receipt["cognitive_resilience_diagnostics"]["education_defense_signal"] == "eroded"
    assert "Education defense signal: eroded" in rendered
    assert "Entertainment compliance signal: high" in rendered
    assert "Algorithmic erosion signal: high" in rendered
    assert "Entertainment compliance evidence:" in rendered
    assert "Algorithmic erosion evidence:" in rendered
