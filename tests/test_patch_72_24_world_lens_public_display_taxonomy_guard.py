from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_72_24_world_lens_public_display_helper_exists():
    text = app_text()

    assert "def _world_lens_public_display_df" in text
    assert "def _world_lens_taxonomy_label" in text
    assert "Low-risk internal reading" in text
    assert "Review / threshold reading" in text
    assert "High-risk internal reading" in text
    assert "not a final safety, final Sanctuary, or authority claim" in text


def test_patch_72_24_comparison_tables_use_internal_taxonomy_label_not_plain_verdict():
    text = app_text()

    start = text.index("def _comparison_display")
    block = text[start:text.index("def _safe_receipt_table", start)]

    assert 'verdict_col: "internal_taxonomy_label"' in block
    assert "return _world_lens_public_display_df(out)" in block
    assert 'verdict_col: "verdict"' not in block


def test_patch_72_24_result_distribution_uses_public_taxonomy_display():
    text = app_text()

    assert 'st.markdown("### Internal taxonomy distribution")' in text
    assert 'title="Seat distribution by internal taxonomy"' in text
    assert 'verdict_df["empirical_pattern_display"] = verdict_df["internal_taxonomy_label"].apply(_world_lens_taxonomy_label)' in text
    assert "Seat distribution by verdict" not in text
    assert 'st.markdown("### Result distribution")' not in text


def test_patch_72_24_report_distribution_and_receipt_exports_are_display_guarded():
    text = app_text()

    assert 'st.markdown("#### Internal taxonomy distribution for reports")' in text
    assert "verdict_report = _world_lens_public_display_df(verdict_report)" in text
    assert "verdict_receipt = _world_lens_public_display_df(verdict_summary_df.copy())" in text
    assert "all_rows_receipt = _world_lens_public_display_df(comparison_export.copy())" in text
    assert "Result distribution for reports" not in text


def test_patch_72_24_world_lens_naming_replaces_old_global_grid_public_text():
    text = app_text()

    assert "Download selected-year World Lens CSV" in text
    assert "aletheia_world_lens_{selected_year}.csv" in text
    assert "Evidence Lab and World Lens year controls match" in text
    assert "Focus country is available in World Lens year" in text

    assert "Download selected-year Global Grid CSV" not in text
    assert "Empirical and Global Grid year controls match" not in text
    assert "Focus country is available in Global Grid year" not in text


def test_patch_72_24_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_24_MANIFEST.txt",
        "PATCH_72_24_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_24_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_24_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "World Lens Public Display Taxonomy Guard" in manifest
    assert r"tools\run_patch_checks.bat 72_24" in recovery
    assert "Patch 72.24" in status
    assert "Patch 72.24" in progress
    assert "World Lens Public Display Taxonomy Guard" in status + progress
