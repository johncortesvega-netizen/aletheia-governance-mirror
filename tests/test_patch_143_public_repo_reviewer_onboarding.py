from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_reviewer_start_path_exists_and_is_linked_from_readme():
    readme = read("README.md")
    reviewer = read("docs/reviewer_start_here.md")

    assert "## Start here for reviewers" in readme
    assert "docs/reviewer_start_here.md" in readme
    assert "docs/glossary.md" in readme
    assert "docs/how_to_review_aletheia_without_trusting_it.md" in readme
    assert "docs/validation_and_precision.md" in readme
    assert "Aletheia Unit Preview" in reviewer
    assert "Receipt Reader" in reviewer
    assert "World Lens" in reviewer
    assert "It does not decide, certify, approve, reject, enforce" in reviewer


def test_glossary_explains_project_specific_terms_and_boundaries():
    glossary = read("docs/glossary.md")
    required_terms = [
        "## 9k",
        "## Sydney Protocol",
        "## V-Axis",
        "## World Lens",
        "## Receipt Reader",
        "## Standard View",
        "## Aletheia Unit Preview",
        "## QUESTION_PROMPT",
        "## Z-axis / Asymptote note",
    ]
    for term in required_terms:
        assert term in glossary

    assert "What it does not claim" in glossary
    assert "not a country certification" in glossary
    assert "does not rescore, override, regenerate, certify, or merge verdicts" in glossary
    assert "not a fourth risk state" in glossary


def test_validation_doc_addresses_false_precision_and_external_validation():
    validation = read("docs/validation_and_precision.md")

    assert "Numerical values are review aids" in validation
    assert "not independent validation" in validation
    assert "Decimal precision" in validation
    assert "`Z=1.0000` is outside ALETHEIA's claim" in validation
    assert "External validation roadmap" in validation
    assert "false positives and false negatives" in validation
    assert "Trust-prior coverage must not be presented as observed public trust" in validation


def test_self_audit_invitation_contains_review_without_trust_steps():
    guide = read("docs/how_to_review_aletheia_without_trusting_it.md")

    expected = [
        "Clone and run locally",
        "Inspect telemetry, storage, and network claims",
        "Run the protocol baseline self-audit",
        "Compare local receipts across repeated runs",
        "Inspect receipt boundaries",
        "Review signal rules and heuristic maps directly",
        "Upload known test scenarios",
        "Check that outputs avoid authority claims",
        "Review World Lens source and coverage notes",
    ]
    for phrase in expected:
        assert phrase in guide

    assert "ALETHEIA reflects. Humans review. Power stays accountable." in guide


def test_patch_archive_navigation_and_helper_exist_without_deleting_audit_trail():
    archive_readme = read("docs/patch_archive/README.md")
    archive_index = read("docs/patch_archive/root_patch_artifact_index.md")
    helper = read("tools/archive_root_patch_artifacts.py")

    assert "archive navigation layer" in archive_readme
    assert "does not delete them" in archive_readme
    assert "PATCH_142_16_MANIFEST.txt" in archive_index
    assert "docs/patch_archive/manifests/PATCH_142_16_MANIFEST.txt" in archive_index
    assert "def archive_patch_artifacts" in helper
    assert "--dry-run" in helper


def test_contributing_points_to_reviewer_readiness_docs():
    contributing = read("CONTRIBUTING.md")

    assert "## Reviewer-readiness path" in contributing
    assert "docs/reviewer_start_here.md" in contributing
    assert "docs/glossary.md" in contributing
    assert "docs/how_to_review_aletheia_without_trusting_it.md" in contributing
    assert "docs/validation_and_precision.md" in contributing


def test_patch_143_introduces_no_forbidden_authority_claims():
    combined = "\n".join([
        read("README.md"),
        read("docs/reviewer_start_here.md"),
        read("docs/glossary.md"),
        read("docs/validation_and_precision.md"),
        read("docs/how_to_review_aletheia_without_trusting_it.md"),
        read("docs/patch_archive/README.md"),
    ]).lower()

    forbidden_positive_claims = [
        "aletheia certifies",
        "aletheia approves",
        "aletheia rejects",
        "aletheia enforces",
        "aletheia governs",
        "aletheia is a final truth system",
        "aletheia has legal authority",
        "aletheia has official authority",
    ]
    for phrase in forbidden_positive_claims:
        assert phrase not in combined

    # Negated boundary language remains required.
    assert "not certification" in combined or "does not certify" in combined
    assert "not final truth" in combined or "final truth" in combined
