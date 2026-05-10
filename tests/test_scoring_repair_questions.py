"""
ALETHEIA RECOVERY NOTE
Patch 06: scoring repair-question regression tests.

Purpose:
    Ensure the simulation scoring layer introduced in Patch 04 exposes repair
    questions without changing score formulas or turning recommendations into
    commands.

Rollback:
    Remove this test file. No production module should need rollback.
"""

from core.scoring import full_report, repair_prompts_from_report


def risky_simulation_fixture():
    return {
        "stability": 0.20,
        "alignment": 0.20,
        "trust_index": 0.20,
        "ego": 0.90,
        "ego_pressure": 0.90,
        "stability_trace": [0.85, 0.70, 0.50, 0.35, 0.20],
        "alignment_trace": [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.22, 0.20, 0.18, 0.15],
        "collapse_risk": True,
        "tipping_step": 4,
        "safeguard_gap": 0.80,
        "grievance_pressure": 0.80,
        "agent_profiles": [],
        "action_counts": {"exploit": 7, "cooperate": 3},
    }


def test_full_report_exposes_repair_questions():
    report = full_report(risky_simulation_fixture())

    assert "repair_questions" in report
    assert isinstance(report["repair_questions"], list)
    assert report["repair_questions"]
    assert all(question.endswith("?") for question in report["repair_questions"])
    assert any("appeal" in question.lower() or "review" in question.lower() for question in report["repair_questions"])


def test_repair_prompts_are_deduplicated_and_compact():
    sim = risky_simulation_fixture()
    questions = repair_prompts_from_report(
        sim,
        integrity=0.20,
        friction=0.90,
        recommendations=[
            {"priority": "critical", "target": "System"},
            {"priority": "critical", "target": "System"},
            {"priority": "low", "target": "Healthy baseline"},
        ],
    )

    assert 1 <= len(questions) <= 8
    assert len(questions) == len(set(questions))
    assert all(question.endswith("?") for question in questions)
    assert any("Throne" in question or "human-review" in question or "appeal" in question for question in questions)
