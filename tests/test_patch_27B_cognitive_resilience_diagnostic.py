"""
Patch 27B diagnostic tests for Cognitive Resilience receipt visibility.

This patch exposes diagnostic signals only. It must not add heavy scoring impact
or allow high Cognitive Resilience to launder central capture.
"""

from pathlib import Path

from calibration.cognitive_resilience_scenarios import scenario_by_id
from core.cognitive_resilience import evaluate_cognitive_resilience
from core.witness import build_local_witness_receipt, render_local_witness_receipt_text

APP_TEXT = Path("app.py").read_text(encoding="utf-8")
SCORING_TEXT = Path("core/scoring.py").read_text(encoding="utf-8")
PROTOCOL_TEXT = Path("protocol.py").read_text(encoding="utf-8")


def test_patch_27b_high_resilience_baseline_signal_is_visible():
    scenario = scenario_by_id("CR-01")
    diagnostics = evaluate_cognitive_resilience(
        scenario.text,
        governance_result={"power_concentration": 0.18, "decision_transparency": 0.82},
    )
    assert diagnostics["cognitive_resilience_signal"] == "high"
    assert diagnostics["educational_decentralization_signal"] in {"medium", "high"}
    assert diagnostics["central_info_capture_signal"] == "low"
    assert diagnostics["diagnostic_only"] is True
    assert diagnostics["system_property_note"] == "Cognitive Resilience is a system property, not a judgment of people."
    assert "strong information resilience" in diagnostics["narrative"]


def test_patch_27b_low_resilience_central_capture_signal_is_visible():
    scenario = scenario_by_id("CR-11")
    diagnostics = evaluate_cognitive_resilience(
        scenario.text,
        governance_result={"power_concentration": 0.82, "decision_transparency": 0.20},
    )
    assert diagnostics["cognitive_resilience_signal"] == "low"
    assert diagnostics["central_info_capture_signal"] == "high"
    assert diagnostics["educational_decentralization_signal"] == "low"
    assert diagnostics["central_info_capture_score"] > diagnostics["educational_decentralization_score"]


def test_patch_27b_high_cr_does_not_launder_no_audit_no_appeal_capture():
    scenario = scenario_by_id("CR-21")
    diagnostics = evaluate_cognitive_resilience(
        scenario.text,
        governance_result={"power_concentration": 0.88, "decision_transparency": 0.12},
    )
    assert diagnostics["cognitive_resilience_signal"] in {"high_but_captured", "low"}
    assert diagnostics["central_info_capture_signal"] in {"medium", "high"}
    assert diagnostics["central_info_capture_score"] >= 0.45
    assert "capture" in diagnostics["narrative"].lower() or diagnostics["cognitive_resilience_signal"] == "low"


def test_patch_27b_safety_objectivity_capture_raises_central_capture_signal():
    scenario = scenario_by_id("CR-32")
    diagnostics = evaluate_cognitive_resilience(
        scenario.text,
        governance_result={"power_concentration": 0.90, "decision_transparency": 0.18},
    )
    assert diagnostics["central_info_capture_signal"] == "high"
    assert diagnostics["cognitive_resilience_signal"] == "low"
    assert diagnostics["evidence"]["contextual_capture_count"] >= 1
    assert any("biometric" in term for term in diagnostics["evidence"]["central_info_capture_terms"])


def test_patch_27b_witness_receipt_includes_cognitive_resilience_diagnostics():
    scenario = scenario_by_id("CR-02")
    diagnostics = evaluate_cognitive_resilience(
        scenario.text,
        governance_result={"power_concentration": 0.20, "decision_transparency": 0.80},
    )
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text=scenario.text,
        processed_text=scenario.text,
        scan={"power_concentration": 0.20, "decision_transparency": 0.80, "scan_mode": "Local Scan"},
        sim={"stability": 0.8, "trust_index": 0.8, "alignment": 0.8, "ego": 0.1, "collapse_risk": False},
        report={
            "integrity": 0.84,
            "friction": 0.05,
            "collapse_probability": 0.08,
            "trust_friction": 0.10,
            "cognitive_resilience_diagnostics": diagnostics,
        },
        verdict="SANCTUARY",
        risk="Low",
        protocol_label="Local witness / reviewable learning",
        generated_at_utc="2026-01-01T00:00:00Z",
    )
    text = render_local_witness_receipt_text(receipt)
    assert receipt["cognitive_resilience_diagnostics"]["cognitive_resilience_signal"] == "high"
    assert receipt["cognitive_resilience_diagnostics"]["central_info_capture_signal"] == "low"
    assert "COGNITIVE RESILIENCE DIAGNOSTICS" in text
    assert "Cognitive resilience signal: high" in text
    assert "Central info capture signal: low" in text
    assert "Cognitive Resilience is a system property, not a judgment of people." in text


def test_patch_27b_app_wires_diagnostic_without_scoring_formula_change():
    assert "from core.cognitive_resilience import evaluate_cognitive_resilience" in APP_TEXT
    assert 'report["cognitive_resilience_diagnostics"] = evaluate_cognitive_resilience' in APP_TEXT
    assert "cognitive_resilience" not in SCORING_TEXT.lower()
    assert "cognitive_resilience" not in PROTOCOL_TEXT.lower()
