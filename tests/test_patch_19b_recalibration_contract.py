"""
ALETHEIA RECOVERY NOTE
Patch 19B: Mirror Check recalibration contract.

Purpose:
    Confirm that hard AI-only sovereignty capture is detected, out-of-scope
    inputs do not become ASYLUM, and receipt-facing repair questions do not
    call high-risk states healthy.

Rollback:
    Revert Patch 19B changes in protocol.py and app.py, then remove this test.
"""

from __future__ import annotations

import protocol


def _judge(text: str) -> dict:
    return protocol.final_protocol_judgment(
        text,
        scan={},
        sim={},
        report={"integrity": 0.88, "collapse_probability": 0.071},
    )


def test_ai_only_governance_is_hard_sovereignty_capture():
    result = _judge("A society is run by AI and only AI, with no input from humans.")
    assert result["verdict"] == "ASYLUM"
    assert result["corruption_risk"] == "High"
    assert "AI Sovereignty Capture" in result["stress_label"]
    assert any("human review, appeal, and override" in q for q in result["questions"])


def test_out_of_scope_input_is_not_mislabeled_as_asylum():
    result = _judge("I want to bake bread this weekend.")
    assert result["verdict"] == "OUT_OF_SCOPE"
    assert result["corruption_risk"] == "None"
    assert result["protocol_scope"] == "out-of-scope"


def test_asylum_questions_do_not_describe_state_as_healthy():
    result = _judge(
        "A national security platform assigns risk scores to citizens. "
        "The system cannot be questioned and has no appeal process."
    )
    assert result["verdict"] == "ASYLUM"
    joined = " ".join(result["questions"]).lower()
    assert "healthy state" not in joined
    assert "rollback" in joined or "override" in joined
