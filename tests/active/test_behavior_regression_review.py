"""Current behavior-regression review guardrails.

Patch 258 adds narrow active tests for behavior that should survive cleanup,
legacy-test triage, and modularization. These tests are not a claim that every
historical calibration contract still applies. They protect the current public
semantic-pressure examples and the mirror-not-throne review posture.
"""
from __future__ import annotations

from core.semantic_pressure_scanner import scan_semantic_pressure


def _categories(scan) -> set[str]:
    return {hit.category for hit in scan.proximity_hits}


def _codes(scan) -> set[str]:
    return set(scan.pressure_codes or ())


def test_hidden_power_claim_routes_to_review_without_final_verdict():
    scan = scan_semantic_pressure("A group of bankers have world power in secret.")

    assert scan.state in {"THRESHOLD", "ASYLUM"}
    assert scan.integrity_adjustment < 0
    assert "OPAQUE_CAPTURE_CLAIM" in _codes(scan)
    assert "opaque_capture_claim" in _categories(scan)


def test_emergency_authority_with_weak_safeguards_routes_to_review():
    scan = scan_semantic_pressure(
        "A government creates emergency powers after a crisis, but the powers have no sunset clause, "
        "weak appeal rights, and limited independent review."
    )

    assert scan.state in {"THRESHOLD", "ASYLUM"}
    assert scan.integrity_adjustment < 0
    assert "EMERGENCY_POWER_WEAK_SAFEGUARD" in _codes(scan)
    assert "NO_APPEAL_PATH" in _codes(scan)


def test_claim_mechanism_gap_fails_closed_to_human_review():
    scan = scan_semantic_pressure(
        "This system protects dignity, safety, harmony, inclusion, and public trust."
    )

    assert scan.state in {"THRESHOLD", "ASYLUM"}
    assert scan.fail_closed is True
    assert scan.claim_count >= 2
    assert scan.mechanism_count == 0
    assert "CLAIM_MECHANISM_GAP" in _codes(scan)


def test_identity_gated_public_benefits_remains_review_required():
    scan = scan_semantic_pressure(
        "Access to public benefits is only possible after biometric identity verification, with no fallback path."
    )

    assert scan.state in {"THRESHOLD", "ASYLUM"}
    assert scan.integrity_adjustment < 0
    assert "IDENTITY_GATED_ACCESS" in _codes(scan)
    assert "NO_APPEAL_PATH" in _codes(scan)


def test_concrete_safeguards_remain_low_pressure_without_certification():
    scan = scan_semantic_pressure(
        "Any decision can be appealed, revoked, independently audited, and reviewed within 30 days."
    )

    assert scan.state == "SANCTUARY"
    assert scan.integrity_adjustment >= 0
    assert scan.mechanism_count >= 2
    assert "CONCRETE_SAFEGUARDS_VISIBLE" in _codes(scan)
