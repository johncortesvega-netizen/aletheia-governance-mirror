from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_72_16_comparison_export_adds_visible_summary_columns():
    text = app_text()

    required_assignments = [
        'comparison_export["countries_scored_selected_year"]',
        'comparison_export["displayed_rows_selected_year"]',
        'comparison_export["zero_seat_diagnostic_rows_selected_year"]',
        'comparison_export["weighted_friction_selected_year"]',
        'comparison_export["average_empirical_coverage_selected_year"]',
        'comparison_export["raw_trust_survey_coverage_selected_year"]',
        'comparison_export["trust_prior_fallback_coverage_selected_year"]',
        'comparison_export["wgi_coverage_selected_year"]',
        'comparison_export["vdem_coverage_selected_year"]',
        'comparison_export["missing_raw_trust_rows_selected_year"]',
        'comparison_export["missing_wgi_rows_selected_year"]',
        'comparison_export["missing_vdem_rows_selected_year"]',
        'comparison_export["trust_prior_rows_selected_year"]',
        'comparison_export["missing_trust_prior_rows_selected_year"]',
        'comparison_export["verdict_seats_sanctuary_selected_year"]',
        'comparison_export["verdict_seats_threshold_selected_year"]',
        'comparison_export["verdict_seats_asylum_selected_year"]',
        'comparison_export["trust_prior_interpretation_note"]',
    ]
    for assignment in required_assignments:
        assert assignment in text


def test_patch_72_16_comparison_export_download_includes_summary_columns():
    text = app_text()

    export_block_start = text.index("#### Comparison packet export")
    export_block = text[export_block_start:]

    expected_columns = [
        "countries_scored_selected_year",
        "displayed_rows_selected_year",
        "zero_seat_diagnostic_rows_selected_year",
        "weighted_friction_selected_year",
        "average_empirical_coverage_selected_year",
        "raw_trust_survey_coverage_selected_year",
        "trust_prior_fallback_coverage_selected_year",
        "wgi_coverage_selected_year",
        "vdem_coverage_selected_year",
        "missing_raw_trust_rows_selected_year",
        "missing_wgi_rows_selected_year",
        "missing_vdem_rows_selected_year",
        "trust_prior_rows_selected_year",
        "missing_trust_prior_rows_selected_year",
        "verdict_seats_sanctuary_selected_year",
        "verdict_seats_threshold_selected_year",
        "verdict_seats_asylum_selected_year",
        "trust_prior_interpretation_note",
    ]
    for column in expected_columns:
        assert column in export_block


def test_patch_72_16_trust_prior_note_distinguishes_fallback_from_raw_survey():
    text = app_text()

    assert "Trust prior coverage is fallback/model continuity coverage, not observed survey coverage." in text
    assert "Use raw_trust_survey_coverage_selected_year for observed survey availability." in text
    assert "not observed raw survey coverage" in text


def test_patch_72_16_does_not_remove_existing_core_export_columns():
    text = app_text()

    export_block_start = text.index("#### Comparison packet export")
    export_block = text[export_block_start:]

    for column in [
        "_country_name",
        "country",
        "iso3",
        "year",
        "_seats",
        "_integrity",
        "_collapse",
        "_friction",
        "_coverage",
        "_trust_raw",
        "_trust_prior",
        "grid_selected_year",
        "grid_source_state",
        "grid_is_full_9k_allocation",
        "weighted_integrity_selected_year",
        "weighted_collapse_probability_selected_year",
        "seat_total_selected_year",
        "coverage_warning",
        "sydney_protocol_overlay",
        "recommended_interpretation",
    ]:
        assert column in export_block


def test_patch_72_16_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_16_MANIFEST.txt",
        "PATCH_72_16_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_16_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_16_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "World Lens Comparison Packet Summary Columns" in manifest
    assert r"tools\run_patch_checks.bat 72_16" in recovery
    assert "Patch 72.16" in status
    assert "Patch 72.16" in progress
    assert "Comparison Packet Summary Columns" in status + progress
