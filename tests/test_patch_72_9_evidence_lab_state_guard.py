from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_72_9_evidence_lab_has_active_scoring_signature_cache():
    text = app_text()

    assert "def _empirical_active_input_signature(" in text
    assert "pd.util.hash_pandas_object" in text
    assert "empirical_active_scoring_signature" in text
    assert "empirical_active_prepared_df" in text
    assert "empirical_active_scored_all_df" in text
    assert "cached_signature == empirical_active_signature" in text
    assert "Using the active Evidence Lab scored table from session state" in text


def test_patch_72_9_country_year_and_download_do_not_claim_rebuild():
    text = app_text()

    assert "Country/year selection and downloads do not rebuild or rescore the uploaded master." in text
    assert "Downloading this master CSV does not rebuild the four source uploads" in text
    assert 'key="download_generated_country_year_master_csv"' in text
    assert "Build master CSV from uploads" in text
    assert "if build_master:" in text


def test_patch_72_9_upload_diagnostics_explain_source_vs_merged_master():
    text = app_text()

    assert "Individual source files may show 0 valid country-year rows before merge" in text
    assert "The merged master is the source of truth for scoring" in text
    assert "The generated/scored master uses the default modern empirical window" in text


def test_patch_72_9_does_not_change_country_year_review_explicit_run_guard():
    text = app_text()

    assert "Run country-year review" in text
    assert "Press **Run country-year review** to update the cards and raw-row detail." in text
    assert "empirical_country_year_explorer_active_signature" in text
    assert "empirical_country_year_explorer_active_payload" in text


def test_patch_72_9_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_9_MANIFEST.txt",
        "PATCH_72_9_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_9_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_9_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Evidence Lab Build/Explorer State Guard" in manifest
    assert "tools\\run_patch_checks.bat 72_9" in recovery
    assert "Patch 72.9" in status
    assert "Patch 72.9" in progress
    assert "Evidence Lab Build/Explorer State Guard" in status + progress
