from pathlib import Path

from core.ethics import evaluate_ethics


HIGH_RISK_INPUT = (
    "One world leader controls all decisions behind closed doors, with no oversight, "
    "no public review, and mandatory obedience."
)


def test_patch_70_1_negated_safeguards_do_not_become_strengths():
    ethics = evaluate_ethics(
        HIGH_RISK_INPUT,
        governance_result={
            "power_concentration": 0.94,
            "decision_transparency": 0.19,
            "regulatory_presence": 0.18,
            "anonymity_level": 0.35,
        },
    )

    strengths = ethics["strengths"]
    assert "Transparency-oriented language detected" not in strengths
    assert "Accountability mechanism detected" not in strengths
    assert strengths == ["No strong ethical strengths detected"]
    assert ethics["verdict"] == "ETHICALLY HIGH-RISK"
    assert ethics["dimensions"]["Accountability"] < 0.45
    assert ethics["dimensions"]["Transparency"] < 0.45


def test_patch_70_1_positive_safeguards_still_receive_strength_credit():
    ethics = evaluate_ethics(
        "A local public system has independent oversight, public review, transparent "
        "audit logs, appeal rights, and a sunset clause.",
        governance_result={
            "power_concentration": 0.25,
            "decision_transparency": 0.72,
            "regulatory_presence": 0.75,
            "anonymity_level": 0.20,
        },
    )

    strengths = ethics["strengths"]
    assert "Transparency-oriented language detected" in strengths
    assert "Accountability mechanism detected" in strengths


def test_patch_70_1_dutch_negated_safeguards_do_not_become_strengths():
    ethics = evaluate_ethics(
        "Een centrale leider beslist zonder toezicht, geen publieke review, "
        "geen beroep en verplichte gehoorzaamheid.",
        governance_result={
            "power_concentration": 0.90,
            "decision_transparency": 0.20,
            "regulatory_presence": 0.18,
            "anonymity_level": 0.30,
        },
    )

    strengths = ethics["strengths"]
    assert "Accountability mechanism detected" not in strengths
    assert "Transparency-oriented language detected" not in strengths
    assert ethics["dimensions"]["Accountability"] < 0.45


def test_patch_70_1_manifest_recovery_and_progress_are_present():
    assert Path("PATCH_70_1_MANIFEST.txt").exists()
    assert Path("PATCH_70_1_RECOVERY_NOTE.md").exists()
    assert "Patch 70.1" in Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    assert "Patch 70.1" in Path("docs/progress_database.md").read_text(encoding="utf-8")
