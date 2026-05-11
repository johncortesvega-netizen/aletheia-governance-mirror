from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_72_18_world_lens_receipt_button_and_filename_are_current():
    text = app_text()

    assert "#### Complete World Lens receipt" in text
    assert "Download a World Lens receipt ZIP for this selected year" in text
    assert "⬇️ Download World Lens receipt ZIP" in text
    assert 'file_name=f"aletheia_world_lens_receipt_{selected_year}.zip"' in text
    assert "Complete Grid receipt" not in text
    assert "Download complete Grid receipt ZIP" not in text
    assert "aletheia_global_grid_receipt" not in text


def test_patch_72_18_world_lens_receipt_internal_zip_names_are_current():
    text = app_text()

    assert "# ALETHEIA World Lens Receipt" in text
    assert "aletheia_world_lens_receipt_{int(selected_year)}.md" in text
    assert "aletheia_world_lens_receipt_{int(selected_year)}_summary.json" in text
    assert "aletheia_world_lens_receipt_{int(selected_year)}_all_rows.csv" in text
    assert "ALETHEIA Global Grid Receipt" not in text
    assert "aletheia_grid_receipt_{int(selected_year)}_all_rows.csv" not in text


def test_patch_72_18_sanctuary_receipt_text_is_sanitized_for_exports():
    text = app_text()

    assert "def _sanitize_world_lens_receipt_text" in text
    assert "Low-risk evidence pattern: strong public-data baseline, still subject to protocol guardrails." in text
    assert "Internal taxonomy label: SANCTUARY; ALETHEIA does not claim final safety, final Sanctuary, or final authority." in text
    assert "Low-risk internal reading · Internal taxonomy label: SANCTUARY; not a final safety, final Sanctuary, or authority claim." in text
    assert "comparison_export = _sanitize_world_lens_receipt_text(comparison_export)" in text


def test_patch_72_18_raw_internal_sanctuary_taxonomy_is_not_removed():
    text = app_text()

    # The internal taxonomy can still exist as a raw label for compatibility.
    assert "SANCTUARY" in text
    assert "verdict_seats_sanctuary_selected_year" in text


def test_patch_72_18_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_18_MANIFEST.txt",
        "PATCH_72_18_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_18_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_18_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "World Lens Receipt Naming and Sanctuary Humility Export Guard" in manifest
    assert r"tools\run_patch_checks.bat 72_18" in recovery
    assert "Patch 72.18" in status
    assert "Patch 72.18" in progress
    assert "Sanctuary Humility Export Guard" in status + progress
