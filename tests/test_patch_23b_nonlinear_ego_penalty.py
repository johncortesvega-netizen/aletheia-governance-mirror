"""
Patch 23B: nonlinear ego penalty calibration.

This keeps the change narrow: scoring.py receives the tipping-point ego curve,
while protocol hard overrides, witness hashing, and UI behavior remain unchanged.
"""

from core.scoring import compute_scores, collapse_probability, nonlinear_ego_penalty, trust_friction


def _sim(ep, *, stability=0.82, alignment=0.88, trust_index=0.90, ego=0.10):
    return {
        "stability": stability,
        "alignment": alignment,
        "trust_index": trust_index,
        "ego": ego,
        "ego_pressure": ep,
        "stability_trace": [stability] * 12,
        "collapse_risk": False,
    }


def test_patch_23b_nonlinear_penalty_is_bounded_and_tipping_point_shaped():
    low = nonlinear_ego_penalty(0.10)
    mid = nonlinear_ego_penalty(0.50)
    high = nonlinear_ego_penalty(0.90)

    assert 0.0 <= low < mid < high <= 1.0
    assert high - mid > mid - low


def test_patch_23b_integrity_degrades_sharply_at_high_ego_pressure():
    low_integrity, low_friction = compute_scores(_sim(0.10))
    high_integrity, high_friction = compute_scores(_sim(0.90))

    assert high_integrity < low_integrity - 0.30
    assert high_friction > low_friction + 0.30


def test_patch_23b_collapse_probability_uses_nonlinear_ego_pressure():
    low = collapse_probability(_sim(0.10))
    high = collapse_probability(_sim(0.90))

    assert high > low + 0.35
    assert high >= 0.50


def test_patch_23b_trust_friction_rises_with_high_ego_pressure():
    assert trust_friction(_sim(0.90)) > trust_friction(_sim(0.10)) + 0.25
