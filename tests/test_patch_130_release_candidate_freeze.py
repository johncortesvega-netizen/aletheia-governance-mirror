from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_130_files_exist():
    required = [
        "docs/release_candidate_freeze_patch_130.md",
        "tests/test_patch_130_release_candidate_freeze.py",
        "PATCH_130_MANIFEST.txt",
        "PATCH_130_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_release_candidate_freeze_language_is_refinement_not_expansion():
    doc = read("docs/release_candidate_freeze_patch_130.md")
    required = [
        "Release Candidate Freeze",
        "release-candidate refinement mode",
        "current app behavior is the surface to preserve",
        "Allowed work is limited to refinement",
        "bug fixes",
        "test hygiene",
        "documentation navigation",
        "small behavior-preserving UI structure cleanup",
        "Human review remains required",
        "ALETHEIA surfaces signals; humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in doc


def test_release_candidate_freeze_forbids_expansion_paths():
    doc = read("docs/release_candidate_freeze_patch_130.md").lower()
    required = [
        "new module",
        "new scoring engine",
        "new risk state",
        "new live model call",
        "agentic review",
        "telemetry",
        "analytics",
        "central storage",
        "global id sync",
        "public ledger sync",
        "certification",
        "compliance approval",
        "privacy guarantee",
        "final-truth claim",
        "receipt schema changes",
    ]
    for phrase in required:
        assert phrase in doc


def test_patch_130_status_docs_updated():
    combined = "\n".join(
        read(rel)
        for rel in [
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
            "docs/release_candidate_freeze_patch_130.md",
        ]
    ).lower()
    required = [
        "patch 130",
        "release candidate freeze",
        "refinement mode",
        "not expansion",
        "no new modules",
        "no new scoring",
        "no live model calls",
        "human review remains required",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_130_boundary_and_encoding_guards():
    changed = "\n".join(
        read(rel)
        for rel in [
            "docs/release_candidate_freeze_patch_130.md",
            "PATCH_130_MANIFEST.txt",
            "PATCH_130_RECOVERY_NOTE.md",
        ]
    ).lower()

    required = [
        "no scoring",
        "no routing",
        "no receipt",
        "no signal",
        "no external calls",
        "no telemetry",
        "no analytics",
        "no storage",
        "privacy guarantee",
        "certification",
        "enforcement",
        "final-truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in changed

    forbidden = [
        "guarantees privacy",
        "privacy guaranteed",
        "certifies privacy",
        "certifies safety",
        "automatic enforcement",
        "final truth guaranteed",
        "todo",
        "fixme",
        "ajustando",
        "afirma",
        "preciso",
        "verwijderen",
        "overmatige",
        "ðÿ",
        "â€”",
        "â€“",
        "â€",
        "â†’",
        "�",
    ]
    for phrase in forbidden:
        assert phrase not in changed
