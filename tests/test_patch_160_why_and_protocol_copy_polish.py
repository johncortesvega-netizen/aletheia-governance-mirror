from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_160_why_aletheia_explains_purpose_without_authority() -> None:
    about = read("pages_ui/about_page.py")
    readme = read("README.md")

    expected = (
        "systems can look orderly while still moving power out of",
        "ALETHEIA's answer is not more command, automation, or institutional control",
        "restrained mirror: make pressure visible, name missing safeguards",
        "reading to human review",
        "compliance is only a floor",
    )
    for phrase in expected:
        assert phrase in about

    assert "Why it exists: many systems can look governed, compliant, neutral, or benevolent" in readme
    assert "restrained mirror: make pressure visible, name missing safeguards" in readme
    assert "ALETHEIA does **not** decide, certify, approve, reject, enforce" in readme


def test_patch_160_protocol_guide_reads_as_operating_boundary_not_command_layer() -> None:
    app = read("app.py")
    guide = read("docs/protocol_guide.md")

    expected_app_phrases = (
        "The Protocol Guide explains the operating boundaries behind the mirror",
        "Use this page to understand the rules, language limits, shared state, and review path. It is guidance, not authority.",
        "what they may reflect, and what they must never claim",
        "not to command, condemn, certify, or become final authority",
        "Plain protocol summary",
    )
    for phrase in expected_app_phrases:
        assert phrase in app

    expected_guide_phrases = (
        "# ALETHEIA v1.0 — Protocol Guide",
        "Function: User-facing operating guide for the v1.0 governance mirror",
        "The guide explains how the mirror should speak",
        "It is not a command layer",
        "No layer creates binding authority, certification, enforcement, or final truth",
    )
    for phrase in expected_guide_phrases:
        assert phrase in guide


def test_patch_160_preserves_copy_only_boundaries() -> None:
    helper_paths = [
        "pages_ui/about_page.py",
        "about_page.py",
        "docs/protocol_guide.md",
    ]
    combined = "\n".join(read(path) for path in helper_paths)
    guide = read("docs/protocol_guide.md")

    assert "full_report(" not in combined
    assert "build_local_witness_receipt" not in combined
    assert "score_country" not in combined
    assert "requests." not in combined
    assert "ALETHEIA does not command, enforce, vote, govern" in guide
