from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_patch_147_current_patch_visible_and_historical_artifacts_archived() -> None:
    root_artifacts = sorted(
        path.name
        for path in ROOT.iterdir()
        if path.is_file()
        and path.name.startswith("PATCH_")
        and (
            path.name.endswith("_MANIFEST.txt")
            or path.name.endswith("_RECOVERY_NOTE.md")
            or path.name.startswith("PATCH_README")
        )
    )

    assert "PATCH_147_MANIFEST.txt" in root_artifacts
    assert "PATCH_147_RECOVERY_NOTE.md" in root_artifacts
    assert all(name.startswith("PATCH_147_") for name in root_artifacts), root_artifacts

    assert (ROOT / "docs" / "patch_archive" / "manifests").is_dir()
    assert (ROOT / "docs" / "patch_archive" / "recovery_notes").is_dir()
    assert (ROOT / "docs" / "patch_archive" / "manifests" / "PATCH_146_1_MANIFEST.txt").exists()
    assert (ROOT / "docs" / "patch_archive" / "recovery_notes" / "PATCH_146_1_RECOVERY_NOTE.md").exists()


def test_patch_147_archive_docs_define_latest_patch_rule() -> None:
    archive_readme = (ROOT / "docs" / "patch_archive" / "README.md").read_text(encoding="utf-8")
    patch_index = (ROOT / "docs" / "patch_index.md").read_text(encoding="utf-8")

    expected_phrases = [
        "Only the latest/current patch manifest and recovery note stay visible",
        "The audit trail is archived, indexed, and preserved",
        "--current-patch",
    ]
    for phrase in expected_phrases:
        assert phrase in archive_readme

    assert "Patch 147 establishes the standing root-hygiene rule" in patch_index
    assert "Latest patch visible at root" in patch_index


def test_patch_147_archive_helper_dry_run_keeps_current_patch() -> None:
    from tools.archive_root_patch_artifacts import discover_patch_artifacts

    moves = discover_patch_artifacts(ROOT, current_patch="147", keep_current=True)
    move_sources = {source.name for source, _target in moves}

    assert "PATCH_147_MANIFEST.txt" not in move_sources
    assert "PATCH_147_RECOVERY_NOTE.md" not in move_sources


def test_patch_147_no_authority_or_behavior_change_language() -> None:
    manifest = (ROOT / "PATCH_147_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = (ROOT / "PATCH_147_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    combined = manifest + "\n" + recovery

    required_boundaries = [
        "No app behavior change",
        "No scoring change",
        "No verdict routing change",
        "No receipt schema or receipt generation change",
        "No signal regex or signal weight change",
        "No AI Integrity",
        "Human review remains required",
    ]
    for phrase in required_boundaries:
        assert phrase in combined

    forbidden_positive_claims = [
        "certifies ALETHEIA",
        "proves integrity",
        "guarantees privacy",
        "guarantees security",
    ]
    lowered = combined.lower()
    for phrase in forbidden_positive_claims:
        assert phrase.lower() not in lowered
