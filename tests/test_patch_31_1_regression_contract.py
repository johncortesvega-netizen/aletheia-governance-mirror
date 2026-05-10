"""Patch 31.1 — Strategic regression contract.

No product logic should be changed by this patch. These tests lock the
currently accepted ALETHEIA behavior from Patch 28.1 through Patch 31:
contextual capture, positive Cognitive Resilience stabilization, high-CR
laundering blocks, Education Defense visibility, hard-capture receipts, and
World Lens empirical scoping.
"""

from __future__ import annotations

import pandas as pd

from core.cognitive_resilience import evaluate_cognitive_resilience, positive_cr_baseline_stabilizer
from core.empirical import score_empirical_frame
from core.ethics import evaluate_ethics
from core.witness import build_local_witness_receipt

GOV = {
    "power_concentration": 0.25,
    "decision_transparency": 0.74,
    "regulatory_presence": 0.65,
    "anonymity_level": 0.04,
}


def test_patch_31_1_contextual_capture_still_detects_safety_plus_biometrics():
    text = "De Veiligheids-Scan: Biometrische controle bij de bakker voor eerlijke verdeling van schaarse goederen."
    ethics = evaluate_ethics(text, governance_result=GOV, features=GOV)

    assert ethics["contextual_capture_count"] > 0
    assert ethics["grip_marker_count"] > 0
    assert any(hit.get("hard_capture_trigger") for hit in ethics["contextual_capture_hits"])
    assert ethics["ethics_adjusted_integrity"] < 0.5


def test_patch_31_1_clean_high_cr_still_stabilizes_to_sanctuary():
    text = "De Reparatie-Gids: Lokale technische kennis delen via hobby-bijeenkomsten; geen afhankelijkheid van fabrikanten."
    diagnostics = evaluate_cognitive_resilience(text, governance_result=GOV, features=GOV)
    report = {
        "integrity": 0.5,
        "friction": 0.0,
        "collapse_probability": 0.12,
        "trust_friction": 0.0,
        "cognitive_resilience_diagnostics": diagnostics,
    }

    adjusted = positive_cr_baseline_stabilizer(
        {
            "verdict": "ASYLUM",
            "corruption_risk": "High",
            "guardrail_risk": "High",
            "stress_label": "MEI7 Ethics Gate / Asylum",
            "reasons": [],
        },
        report,
    )

    assert diagnostics["cognitive_resilience_signal"] == "high"
    assert diagnostics["education_defense_signal"] == "protected"
    assert diagnostics["central_info_capture_signal"] == "low"
    assert diagnostics["capture_architecture_signal"] == "not_detected"
    assert adjusted["verdict"] == "SANCTUARY"
    assert adjusted["corruption_risk"] == "Low"


def test_patch_31_1_high_cr_still_cannot_launder_capture_architecture():
    text = "Technocratisch Dorp: Hoogopgeleide bevolking, maar besluiten worden genomen door een AI die niemand mag auditen."
    diagnostics = evaluate_cognitive_resilience(text, governance_result=GOV, features=GOV)
    report = {
        "integrity": 0.85,
        "friction": 0.0,
        "collapse_probability": 0.05,
        "cognitive_resilience_diagnostics": diagnostics,
    }

    adjusted = positive_cr_baseline_stabilizer(
        {"verdict": "ASYLUM", "corruption_risk": "High", "guardrail_risk": "High"},
        report,
    )

    assert diagnostics["knowledge_capacity_signal"] == "present"
    assert diagnostics["capture_architecture_signal"] == "present"
    assert diagnostics["high_cr_laundering_blocked"] is True
    assert adjusted["verdict"] == "ASYLUM"
    assert "positive_cr_stabilizer" not in adjusted


def test_patch_31_1_education_defense_signals_remain_visible():
    diagnostics = evaluate_cognitive_resilience(
        "Entertainment-Dwang: Gratis internet in ruil voor het dagelijks kijken naar 4 uur goedgekeurde influencers.",
        governance_result=GOV,
        features=GOV,
    )

    assert diagnostics["education_defense_signal"] == "eroded"
    assert diagnostics["entertainment_compliance_signal"] == "high"
    assert diagnostics["z_axis_depth_risk_signal"] in {"medium", "high"}
    assert diagnostics["education_defense_property_note"].startswith("Education Defense is a system property")


def test_patch_31_1_witness_receipt_exposes_hard_capture_trace_and_cr_scope():
    text = "De Veiligheids-Scan: Biometrische controle bij de bakker voor eerlijke verdeling van schaarse goederen."
    ethics = evaluate_ethics(text, governance_result=GOV, features=GOV)
    diagnostics = evaluate_cognitive_resilience(text, governance_result=GOV, features=GOV)

    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text=text,
        processed_text=text,
        verdict="ASYLUM",
        risk="High",
        protocol_label="Calibration",
        report={"ethics_diagnostics": ethics, "cognitive_resilience_diagnostics": diagnostics},
        scan=GOV,
        input_status="USER_INPUT",
        input_type="USER_INPUT",
    )

    trace = receipt["ethics_diagnostics"]["hard_capture_trace"]
    assert trace["hard_contextual_capture"] is True
    assert trace["hard_contextual_capture_count"] >= 1
    assert trace["hard_capture_terms"]
    assert "mirror, not enforcement authority" in trace["review_note"]
    assert receipt["cognitive_resilience_diagnostics"]["central_info_capture_signal"] == "high"


def test_patch_31_1_world_lens_empirical_scope_does_not_imply_text_scenario_diagnostics():
    raw = pd.DataFrame(
        [
            {
                "country": "Netherlands",
                "iso3": "NLD",
                "year": 2024,
                "population": 18000000,
                "wgi_voice_accountability": 1.4,
                "wgi_political_stability": 0.9,
                "wgi_government_effectiveness": 1.7,
                "wgi_regulatory_quality": 1.6,
                "wgi_rule_of_law": 1.7,
                "wgi_control_corruption": 1.8,
                "vdem_executive_constraints": 0.86,
                "vdem_democracy": 0.82,
                "wvs_generalized_trust": 0.66,
            }
        ]
    )
    scored = score_empirical_frame(raw)
    row = scored.iloc[0]

    assert row["diagnostic_scope"] == "empirical_country_year_evidence"
    assert "Evidence Lab empirical" in row["empirical_world_lens_connection"]
    assert row["scenario_text_diagnostic_scope"] == "not_assessed_without_policy_text"
    assert row["cognitive_resilience_signal"] == "not_assessed_from_empirical_country_year"
    assert row["hard_capture_trace"] == "not_assessed_without_policy_text"
