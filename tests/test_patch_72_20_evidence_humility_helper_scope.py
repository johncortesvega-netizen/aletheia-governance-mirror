from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_72_20_helper_is_defined_before_evidence_lab_call():
    text = app_text()

    helper_idx = text.index("def _empirical_humility_display_df")
    call_idx = text.index("_empirical_humility_display_df(group_df)")
    assert helper_idx < call_idx


def test_patch_72_20_helper_is_top_level_not_nested_inside_world_lens():
    text = app_text()

    helper_line = next(line for line in text.splitlines() if line.startswith("def _empirical_humility_display_df"))
    assert helper_line == "def _empirical_humility_display_df(df: pd.DataFrame) -> pd.DataFrame:"
    assert text.count("def _empirical_humility_display_df") == 1


def test_patch_72_20_evidence_lab_calls_still_present():
    text = app_text()

    assert "_empirical_humility_display_df(group_df)" in text
    assert "_empirical_humility_display_df(scored[overlay_cols])" in text
    assert "_empirical_humility_display_df(scored)" in text
    assert "Group averages by internal taxonomy" in text


def test_patch_72_20_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_20_MANIFEST.txt",
        "PATCH_72_20_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_20_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_20_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Evidence Humility Helper Scope Fix" in manifest
    assert r"tools\run_patch_checks.bat 72_20" in recovery
    assert "Patch 72.20" in status
    assert "Patch 72.20" in progress
    assert "Evidence Humility Helper Scope Fix" in status + progress
