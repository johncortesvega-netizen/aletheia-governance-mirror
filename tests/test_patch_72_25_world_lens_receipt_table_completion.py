from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_72_25_public_display_helper_detects_internal_taxonomy_labels():
    text = app_text()

    assert '"internal_taxonomy_label"' in text
    assert '"raw_aletheia_verdict"' in text
    assert '"raw_verdict"' in text
    assert 'if verdict_col_name == "empirical_pattern_display":' in text
    assert 'for candidate in ["internal_taxonomy_label", "raw_aletheia_verdict", "raw_verdict", "aletheia_verdict", "verdict", "Verdict", "result"]' in text


def test_patch_72_25_threshold_and_asylum_final_interpretations_are_sanitized():
    text = app_text()

    assert "Review / threshold evidence pattern: unresolved safeguards or friction." in text
    assert "Review / threshold reading · Internal taxonomy label: THRESHOLD;" in text
    assert "High-risk evidence pattern: high capture/collapse concern." in text
    assert "High-risk internal reading · Internal taxonomy label: ASYLUM;" in text
    assert 'text_value.startswith("THRESHOLD · THRESHOLD evidence pattern")' in text
    assert 'text_value.startswith("ASYLUM · ASYLUM evidence pattern")' in text


def test_patch_72_25_receipt_distribution_filename_uses_taxonomy_not_verdict():
    text = app_text()

    assert "aletheia_world_lens_receipt_{int(selected_year)}_taxonomy_distribution.csv" in text
    assert "aletheia_world_lens_receipt_{int(selected_year)}_verdict_distribution.csv" not in text


def test_patch_72_25_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_25_MANIFEST.txt",
        "PATCH_72_25_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_25_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_25_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "World Lens Receipt Table Completion" in manifest
    assert r"tools\run_patch_checks.bat 72_25" in recovery
    assert "Patch 72.25" in status
    assert "Patch 72.25" in progress
    assert "World Lens Receipt Table Completion" in status + progress
