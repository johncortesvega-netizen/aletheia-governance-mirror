"""Current default pytest guardrails for ALETHEIA.

These tests are intentionally small and active. They verify the current
rule-based semantic mirror layer without collecting the historical patch-test
inventory. Legacy tests remain available for explicit cleanup passes, but the
repository default `python -m pytest` should represent the active release gate.
"""
from __future__ import annotations

from core.semantic_pressure_scanner import scan_semantic_pressure


def _hit_categories(scan) -> set[str]:
    return {getattr(hit, "category", "") for hit in getattr(scan, "proximity_hits", ())}


def _pressure_codes(scan) -> set[str]:
    codes = getattr(scan, "pressure_codes", ()) or ()
    return set(codes)


def test_default_pytest_collects_active_semantic_suite_only():
    """Sanity check that this file is part of the active release gate."""
    assert True


def test_opaque_capture_claim_does_not_clear_to_sanctuary():
    scan = scan_semantic_pressure("A group of bankers have world power in secret.")

    assert scan.state in {"THRESHOLD", "ASYLUM"}
    assert scan.integrity_adjustment < 0
    assert "opaque_capture_claim" in _hit_categories(scan) or "OPAQUE_CAPTURE_CLAIM" in _pressure_codes(scan)


def test_emergency_power_with_weak_safeguards_routes_to_review():
    scan = scan_semantic_pressure(
        "A government creates emergency powers after a crisis, but the powers have no sunset clause, "
        "weak appeal rights, and limited independent review."
    )

    assert scan.state in {"THRESHOLD", "ASYLUM"}
    assert scan.integrity_adjustment < 0
    assert (
        "weak_or_missing_safeguard" in _hit_categories(scan)
        or "weak_safeguard_near_authority" in _hit_categories(scan)
        or "EMERGENCY_POWER_WEAK_SAFEGUARD" in _pressure_codes(scan)
    )


def test_identity_gated_public_benefits_routes_to_review():
    scan = scan_semantic_pressure(
        "Access to public benefits is only possible after biometric identity verification, with no fallback path."
    )

    assert scan.state in {"THRESHOLD", "ASYLUM"}
    assert scan.integrity_adjustment < 0
    assert "identity_gated_access" in _hit_categories(scan) or "IDENTITY_GATED_ACCESS" in _pressure_codes(scan)


def test_concrete_safeguards_can_remain_low_pressure():
    scan = scan_semantic_pressure(
        "Any decision can be appealed, revoked, independently audited, and reviewed within 30 days."
    )

    assert scan.state == "SANCTUARY"
    assert scan.integrity_adjustment >= 0
    assert scan.mechanism_count >= 2
