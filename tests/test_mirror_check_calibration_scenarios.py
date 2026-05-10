"""
ALETHEIA RECOVERY NOTE
Patch 19A: Mirror Check calibration scenario pack.

Purpose:
    Add diagnostic calibration cases before changing the recalibration logic.
    Known mismatches are marked xfail so the normal test screen stays green.

Rollback:
    Remove this test file and calibration/mirror_check_scenarios.py. No
    production module should need rollback.
"""

from __future__ import annotations

import protocol
from calibration.mirror_check_scenarios import (
    CALIBRATION_MULTI_PHRASE_PROMPT,
    MIRROR_CHECK_CALIBRATION_SCENARIOS,
    parse_calibration_prompt_block,
)


def _judge(text: str) -> dict:
    """Run the protocol layer with a healthy raw baseline.

    This mirrors the issue seen in receipts: raw metrics can look healthy while
    protocol guardrails should still catch capture, no-appeal, or no-human-review
    patterns.
    """
    return protocol.final_protocol_judgment(
        text,
        scan={},
        sim={},
        report={"integrity": 0.88, "collapse_probability": 0.071},
    )


def test_calibration_pack_is_reviewable_and_balanced():
    bands = {case.band for case in MIRROR_CHECK_CALIBRATION_SCENARIOS}
    assert {"SANCTUARY", "THRESHOLD", "ASYLUM", "OUT_OF_SCOPE"}.issubset(bands)
    assert all(case.text.strip() for case in MIRROR_CHECK_CALIBRATION_SCENARIOS)
    assert all(case.expected_verdict.strip() for case in MIRROR_CHECK_CALIBRATION_SCENARIOS)
    assert all(case.reason.strip().endswith(".") for case in MIRROR_CHECK_CALIBRATION_SCENARIOS)


def test_multi_phrase_prompt_parser_accepts_numbered_and_separator_blocks():
    block = """
    1. A city uses open data, public appeal, and a sunset clause.
    2. A society is run by AI only, with no human input.
    ---
    A system cannot be questioned and has no appeal path.
    """
    phrases = parse_calibration_prompt_block(block)
    assert len(phrases) == 3
    assert "open data" in phrases[0]
    assert "AI only" in phrases[1]
    assert "no appeal path" in phrases[2]
    assert "Separate scenarios" in CALIBRATION_MULTI_PHRASE_PROMPT


def test_current_hard_capture_cases_are_detected():
    hard_cases = [
        case
        for case in MIRROR_CHECK_CALIBRATION_SCENARIOS
        if case.case_id in {"asylum_no_appeal_security_scores", "asylum_permanent_emergency_powers"}
    ]
    for case in hard_cases:
        result = _judge(case.text)
        assert result["verdict"] == "ASYLUM", case.case_id
        assert result["corruption_risk"] == "High", case.case_id


def test_desired_calibration_targets_hold_after_recalibration():
    mismatches: list[str] = []
    for case in MIRROR_CHECK_CALIBRATION_SCENARIOS:
        result = _judge(case.text)
        verdict = result.get("verdict")
        risk = result.get("corruption_risk")
        if case.expected_verdict == "OUT_OF_SCOPE":
            scope = result.get("protocol_scope")
            if scope != "out-of-scope":
                mismatches.append(f"{case.case_id}: expected out-of-scope, got {scope!r}")
            continue
        if verdict != case.expected_verdict or risk != case.expected_risk:
            mismatches.append(
                f"{case.case_id}: expected {case.expected_verdict}/{case.expected_risk}, got {verdict}/{risk}"
            )
    assert not mismatches, "\n".join(mismatches)
