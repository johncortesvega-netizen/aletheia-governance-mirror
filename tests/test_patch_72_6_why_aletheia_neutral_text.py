from pathlib import Path


def about_text() -> str:
    return Path("about_page.py").read_text(encoding="utf-8")


def test_patch_72_6_why_aletheia_intro_is_neutral_and_current():
    text = about_text()

    assert "does not decide, enforce, validate final truth, or replace human judgment" in text
    assert "governance-risk research prototype with a gentle, practical tone" in text
    assert "validate extraordinary authority claims" in text
    assert "Humility Protocol keeps the Z-axis bounded" in text
    assert "not a perfection score" in text


def test_patch_72_6_why_aletheia_module_copy_matches_patch_72_language():
    text = about_text()

    assert "internal review label: SANCTUARY, THRESHOLD, or ASYLUM" in text
    assert "These labels are model signals for human review, not final verdicts" in text
    assert "calibrate the review model; they do not create authority, enforcement, or final decisions" in text
    assert "non-authority impact mirror" in text
    assert "select a real 9k" in text


def test_patch_72_6_why_aletheia_9k_and_z_axis_boundaries_are_friendly():
    text = about_text()

    assert "9k is framed as a human anti-tyranny scaffold / threshold steward" in text
    assert "not a final safety claim, not a source of final legitimacy, and not an authority claim" in text
    assert "Z=0.9999 is the highest human/system review boundary shown by ALETHEIA" in text
    assert "Z=1.0000 remains outside ALETHEIA's claim" in text


def test_patch_72_6_why_aletheia_avoids_older_validation_wording():
    text = about_text()

    assert "validate spiritual authority" not in text
    assert "validates spiritual authority" not in text
    assert "religious validation, or final judgments" not in text
    assert "a sovereign system" not in text
    assert "sovereign authority, a political mandate" not in text


def test_patch_72_6_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_6_MANIFEST.txt",
        "PATCH_72_6_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_6_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_6_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Why ALETHEIA Neutral Text Refresh" in manifest
    assert "tools\\run_patch_checks.bat 72_6" in recovery
    assert "Patch 72.6" in status
    assert "Patch 72.6" in progress
    assert "Why ALETHEIA Neutral Text Refresh" in status + progress
