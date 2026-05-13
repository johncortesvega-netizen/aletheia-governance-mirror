import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_126_files_exist():
    required = [
        "docs/final_structural_simplification_freeze.md",
        "tests/test_patch_126_final_structural_simplification_freeze.py",
        "PATCH_126_MANIFEST.txt",
        "PATCH_126_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_freeze_doc_records_refinement_not_expansion():
    doc = read("docs/final_structural_simplification_freeze.md")
    required = [
        "ALETHEIA is not in expansion mode. It is in refinement mode.",
        "move existing UI code into clearer files",
        "remove duplication",
        "consolidate repeated copy",
        "improve documentation navigation",
        "tighten regression tests",
        "lock existing behavior",
        "new modules",
        "new scoring",
        "new panels",
        "new analysis modes",
        "new intelligence",
        "release-candidate surface",
        "Human review remains required",
        "ALETHEIA surfaces signals; humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in doc


def test_patch_126_updates_public_status_docs():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
            "README.md",
        ]
    ).lower()
    required = [
        "patch 126",
        "final structural simplification freeze",
        "refinement mode",
        "not in expansion mode",
        "release-candidate surface",
        "no app runtime behavior change",
        "no new scoring",
        "no new panel",
        "no new analysis mode",
        "no external calls",
        "human review remains required",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_126_does_not_edit_app_py_or_add_runtime_helper():
    manifest = read("PATCH_126_MANIFEST.txt")
    assert "- app.py" not in manifest
    assert "ui/" not in manifest
    assert "pages_ui/" not in manifest


def test_patch_126_boundary_language_is_non_authoritative():
    changed = "\n".join(
        read(rel)
        for rel in [
            "docs/final_structural_simplification_freeze.md",
            "PATCH_126_MANIFEST.txt",
            "PATCH_126_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "does not certify",
        "privacy guarantee",
        "certification",
        "enforcement",
        "final truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in changed

    forbidden = [
        "guarantees privacy",
        "privacy guaranteed",
        "certifies privacy",
        "certifies safety",
        "final truth guaranteed",
        "automatic enforcement",
        "todo",
        "fixme",
        "ajustando",
        "afirma",
        "preciso",
        "verwijderen",
        "overmatige",
    ]
    for phrase in forbidden:
        assert phrase not in changed


def test_patch_126_manifest_tracks_freeze_files_after_later_patches():
    manifest = json.loads(read("data/protocol_baseline_manifest.json"))
    assert int(str(manifest["created_for_patch"])) >= 126
    assert "ALETHEIA v1.0 AI Integrity Preview" in manifest["baseline_id"]
    assert "docs/final_structural_simplification_freeze.md" in manifest["files"]
    assert "tests/test_patch_126_final_structural_simplification_freeze.py" in manifest["files"]
    assert "PATCH_126_MANIFEST.txt" in manifest["files"]
    assert "PATCH_126_RECOVERY_NOTE.md" in manifest["files"]
