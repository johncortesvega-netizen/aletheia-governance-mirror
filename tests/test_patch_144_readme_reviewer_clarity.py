from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_readme_has_60_second_entry_and_reviewer_path():
    readme = read("README.md")

    assert "## ALETHEIA in 60 Seconds" in readme
    assert "ALETHEIA is a mirror, not a throne" in readme
    assert "governance-risk signals for human review" in readme
    assert "does **not** decide, certify, approve, reject, enforce, govern, vote" in readme
    assert "## New reviewer path" in readme
    assert "Aletheia Unit Preview" in readme
    assert "docs/for-reviewers/quick_start.md" in readme
    assert "docs/validation_and_precision.md" in readme
    assert "docs/how_to_review_aletheia_without_trusting_it.md" in readme


def test_readme_includes_typical_use_cases_and_current_v1_surfaces():
    readme = read("README.md")

    assert "## Typical use cases" in readme
    assert "Review an AI company's public safety policy" in readme
    assert "Stress-test a proposed governance system" in readme
    assert "Upload a local witness receipt" in readme

    for module in [
        "Mirror Check",
        "Stress Test",
        "AI Integrity Mirror",
        "Evidence Lab",
        "World Lens",
        "Receipt Reader",
        "Boundary Cases",
    ]:
        assert module in readme


def test_for_reviewers_quick_start_exists_and_is_bounded():
    quick = read("docs/for-reviewers/quick_start.md")
    index = read("docs/for-reviewers/README.md")

    assert "5-minute path" in quick
    assert "Aletheia Unit Preview" in quick
    assert "Run locally" in quick or "run locally" in quick
    assert "Receipt Reader" in quick
    assert "docs/how_to_review_aletheia_without_trusting_it.md" in quick
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in quick
    assert "This folder is a doorway" in index


def test_glossary_has_examples_and_dutch_equivalents():
    glossary = read("docs/glossary.md")

    assert "## Quick examples and Dutch equivalents" in glossary
    assert "Dutch / Nederlands" in glossary
    assert "Spiegel, geen troon" in glossary
    assert "Menselijke beoordeling vereist" in glossary
    assert "Standaardweergave" in glossary
    assert "Wereldlens" in glossary
    assert "Vraagprompt / review-toolmodus" in glossary
    assert "A World Lens allocation scaffold, not a parliament or authority" in glossary


def test_validation_doc_names_validation_gap_and_precision_limits():
    validation = read("docs/validation_and_precision.md")

    assert "## Validation gap and current credibility boundary" in validation
    assert "structured heuristic readings with interpretive value" in validation
    assert "independent comparison against external datasets" in validation
    assert "Reader guidance for numerical outputs" in validation
    assert "not a claim of scientific certainty" in validation
    assert "Typical validation questions reviewers should ask" in validation


def test_contributing_is_philosophy_first_and_links_quick_start():
    contributing = read("CONTRIBUTING.md")

    assert "## Philosophy first, code second" in contributing
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in contributing
    assert "docs/for-reviewers/quick_start.md" in contributing
    assert "should not make ALETHEIA more authoritative" in contributing


def test_patch_144_clarity_docs_introduce_no_positive_authority_claims():
    combined = "\n".join(
        [
            read("README.md"),
            read("docs/for-reviewers/quick_start.md"),
            read("docs/for-reviewers/README.md"),
            read("docs/glossary.md"),
            read("docs/validation_and_precision.md"),
            read("CONTRIBUTING.md"),
        ]
    ).lower()

    forbidden_positive_claims = [
        "aletheia certifies",
        "aletheia approves",
        "aletheia rejects",
        "aletheia enforces",
        "aletheia governs",
        "aletheia votes",
        "aletheia is a final truth system",
        "aletheia has legal authority",
        "aletheia has official authority",
    ]
    for phrase in forbidden_positive_claims:
        assert phrase not in combined

    assert "does **not** decide".lower() in combined or "does not decide" in combined
    assert "mirror, not throne" in combined
