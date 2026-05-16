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

    current_manifest = [name for name in root_artifacts if name.endswith("_MANIFEST.txt")]
    current_recovery = [name for name in root_artifacts if name.endswith("_RECOVERY_NOTE.md")]

    assert len(current_manifest) == 1, root_artifacts
    assert len(current_recovery) == 1, root_artifacts
    assert current_manifest[0].replace("_MANIFEST.txt", "") == current_recovery[0].replace("_RECOVERY_NOTE.md", "")

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

    assert "standing root-hygiene rule" in patch_index
    assert "Latest patch visible at root" in patch_index


def test_patch_147_archive_helper_dry_run_keeps_current_patch() -> None:
    from tools.archive_root_patch_artifacts import discover_patch_artifacts

    root_artifacts = sorted(
        path.name
        for path in ROOT.iterdir()
        if path.is_file()
        and path.name.startswith("PATCH_")
        and (path.name.endswith("_MANIFEST.txt") or path.name.endswith("_RECOVERY_NOTE.md"))
    )
    current_patch = root_artifacts[0].replace("_MANIFEST.txt", "").replace("_RECOVERY_NOTE.md", "").replace("PATCH_", "")
    moves = discover_patch_artifacts(ROOT, current_patch=current_patch, keep_current=True)
    move_sources = {source.name for source, _target in moves}

    assert f"PATCH_{current_patch}_MANIFEST.txt" not in move_sources
    assert f"PATCH_{current_patch}_RECOVERY_NOTE.md" not in move_sources


def test_patch_147_no_authority_or_behavior_change_language() -> None:
    manifest_files = sorted(ROOT.glob("PATCH_*_MANIFEST.txt"))
    recovery_files = sorted(ROOT.glob("PATCH_*_RECOVERY_NOTE.md"))
    assert len(manifest_files) == 1
    assert len(recovery_files) == 1
    manifest = manifest_files[0].read_text(encoding="utf-8")
    recovery = recovery_files[0].read_text(encoding="utf-8")
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
