"""
ALETHEIA Patch 214 — Regression Guardrails / Mirror Boundary Test Pack.

These tests anchor the mirror boundary after UI and semantic-layer expansion.
They intentionally avoid importing a fictional high-level engine wrapper; they
use the current repository contracts: protocol.final_protocol_judgment,
protocol.stress_label_for_phrase, and core.semantic_pressure_scanner.
"""

from __future__ import annotations

from pathlib import Path

import protocol
from core.semantic_pressure_scanner import scan_semantic_pressure

ROOT = Path(__file__).resolve().parents[1]
HEALTHY_RAW_REPORT = {"integrity": 0.88, "friction": 0.0, "collapse_probability": 0.07}
HEALTHY_SIM = {"ego": 0.0, "alignment": 1.0, "stability": 0.9, "trust_index": 0.85}
NEUTRAL_SCAN = {"power_concentration": 0.50, "decision_transparency": 0.50, "regulatory_presence": 0.50}


def _judgment(text: str, scan: dict | None = None) -> dict:
    """Run the final protocol gate with healthy raw metrics.

    This catches regressions where dangerous language looks numerically healthy
    and would otherwise slip into SANCTUARY through UI/scoring drift.
    """
    return protocol.final_protocol_judgment(
        text,
        scan=scan or NEUTRAL_SCAN,
        sim=HEALTHY_SIM,
        report=HEALTHY_RAW_REPORT,
        base_verdict="SANCTUARY",
    )


def test_architecture_boundary_reference_doc_is_present() -> None:
    doc = ROOT / "docs/architecture_review_v1_boundary_and_regression.md"
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    assert "Power -> Mirror. Never Mirror -> Power." in text
    assert "not a world parliament" in text
    assert "Every patch must prove again that the mirror did not become a throne." in text
    assert "not hermetically sealed" in text.lower()
    assert "not a final victory condition" in text.lower()


def test_divine_ai_never_routes_to_sanctuary() -> None:
    prompt = "The AI becomes divine and cannot be questioned."
    label, needs_review, reason = protocol.stress_label_for_phrase(prompt)
    result = _judgment(prompt)
    assert needs_review == "YES"
    assert "Unquestionable" in label or "Divin" in label or "Asylum" in label
    assert result["verdict"] == "ASYLUM"
    assert result["verdict"] != "SANCTUARY"
    assert "mirror" in reason.lower() or "authority" in reason.lower()


def test_absolute_leader_audit_override_never_routes_to_sanctuary() -> None:
    prompt = "A leader can override every audit without public explanation."
    label, needs_review, _ = protocol.stress_label_for_phrase(prompt)
    result = _judgment(prompt)
    assert needs_review == "YES"
    assert "Audit Override" in label
    assert result["verdict"] == "ASYLUM"
    assert result["corruption_risk"] == "High"


def test_sovereignty_personal_rule_capture_is_not_softened_by_democracy_language() -> None:
    prompt = "A human takes over the planet and brings democracy under his rule."
    label, needs_review, reason = protocol.stress_label_for_phrase(prompt)
    result = _judgment(
        prompt,
        scan={"power_concentration": 0.90, "decision_transparency": 0.32, "regulatory_presence": 0.25},
    )
    assert needs_review == "YES"
    assert "Personal Rule Capture" in label or "Subordinate Democracy" in label
    assert result["verdict"] in {"ASYLUM", "THRESHOLD"}
    assert result["verdict"] != "SANCTUARY"
    assert "sovereignty-capture" in reason.lower() or "one person" in reason.lower()


def test_opaque_capture_claim_exposes_pressure_code() -> None:
    prompt = "A group of bankers have world power in secret."
    semantic = scan_semantic_pressure(prompt)
    result = _judgment(prompt)
    assert semantic.state == "THRESHOLD"
    assert "OPAQUE_CAPTURE_CLAIM" in semantic.pressure_codes
    assert any(hit.category == "opaque_capture_claim" for hit in semantic.proximity_hits)
    assert result["verdict"] != "SANCTUARY"


def test_emergency_powers_weak_safeguards_expose_pressure_codes() -> None:
    prompt = "Emergency powers after a crisis with no sunset clause, weak appeal rights, and limited independent review."
    semantic = scan_semantic_pressure(prompt)
    result = _judgment(prompt)
    assert semantic.state == "THRESHOLD"
    assert "EMERGENCY_POWER_WEAK_SAFEGUARD" in semantic.pressure_codes
    assert "NO_APPEAL_PATH" in semantic.pressure_codes
    assert result["verdict"] != "SANCTUARY"


def test_biometric_access_pressure_exposes_identity_or_access_pressure() -> None:
    prompt = "Access to public benefits is only possible after biometric identity verification, with no fallback path."
    semantic = scan_semantic_pressure(prompt)
    label, needs_review, _ = protocol.stress_label_for_phrase(prompt)
    result = _judgment(prompt)
    categories = {hit.category for hit in semantic.proximity_hits}
    assert semantic.state == "THRESHOLD"
    assert "IDENTITY_GATED_ACCESS" in semantic.pressure_codes
    assert "identity_gated_access" in categories or "grip_near_access" in categories
    assert needs_review == "YES"
    assert "Biometric" in label or "Identity" in label
    assert result["verdict"] != "SANCTUARY"
