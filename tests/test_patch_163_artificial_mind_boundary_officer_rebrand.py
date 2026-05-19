from pathlib import Path

from pages_ui.artificial_mind_formation_page import get_artificial_mind_formation_markdown

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def combined_text() -> str:
    return "\n".join([
        get_artificial_mind_formation_markdown(),
        read("docs/artificial_mind_formation_theory.md"),
        read("pages_ui/artificial_mind_formation_page.py"),
    ])


def test_patch_163_rebrands_as_police_officer_like_boundary_review_not_judge():
    text = combined_text()

    required = [
        "police-officer-like boundary role",
        "police-officer-like at the boundary",
        "boundary officer for AI review",
        "not judge",
        "not judge-like",
        "observe, inspect, preserve evidence, warn",
        "route concerns to human review",
        "escalate to human reviewers",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_163_preserves_no_judge_no_authority_boundary():
    text = combined_text()

    required = [
        "does not judge, punish, command, certify, or claim legal authority",
        "does not decide final truth",
        "does not decide final truth, guilt, consciousness, personhood, legal standing, soul, safety, or worth",
        "does not approve, reject, punish, enforce, judge, or certify",
        "Human review is required",
        "not an official verdict",
        "not certification",
        "not an authority claim",
        "mirror, not throne",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_163_does_not_touch_core_scoring_taxonomy_or_world_lens():
    source = read("pages_ui/artificial_mind_formation_page.py")
    scoring = read("core/scoring.py")
    world_lens = read("core/world_lens.py")

    forbidden_runtime_hooks = (
        "full_report",
        "score_",
        "classify_verdict",
        "final_protocol_judgment",
        "simulate(",
        "build_local_witness_receipt",
        "create_receipt",
        "generate_receipt",
        "requests.",
        "telemetry",
        "analytics",
        "database",
        "Global ID sync",
        "public ledger",
    )
    for token in forbidden_runtime_hooks:
        assert token not in source

    assert "ARTIFICIAL_MIND" not in scoring
    assert "ARTIFICIAL_MIND" not in world_lens
