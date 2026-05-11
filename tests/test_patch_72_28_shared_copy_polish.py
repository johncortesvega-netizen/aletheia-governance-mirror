from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def empirical_text() -> str:
    return Path("core/empirical.py").read_text(encoding="utf-8")


def fallback_empirical_text() -> str:
    return Path("core_empirical.py").read_text(encoding="utf-8")


def test_patch_72_28_shared_state_labels_are_module_neutral():
    text = app_text()

    assert "Selected case / scenario" in text
    assert "Evidence basis" in text
    assert "Selected country / scenario" not in text
    assert "Grid basis" not in text


def test_patch_72_28_mirror_copy_uses_humility_language():
    text = app_text()

    assert "Near low-risk boundary" in text
    assert "Questions before relying on this reading" in text
    assert "Protocol audit result" not in text
    assert "final label" not in text
    assert "Near Sanctuary" not in text
    assert "Questions before trusting this model" not in text
    assert "A low-risk internal reading requires stronger consent, accountability, non-harm, and dignity." in text or "Sanctuary requires stronger consent" not in text


def test_patch_72_28_evidence_lab_schema_help_is_clearer():
    text = app_text()

    assert "Helpful empirical columns" in text
    assert 'helpful_empirical_columns = [c for c in EMPIRICAL_COLUMNS if c != "population"]' in text
    assert "Scale expectations:" in text
    assert "Helpful data columns" not in text
    assert "or enforcement authority" in text
    assert "or enforcement mechanism" not in text


def test_patch_72_28_method_note_uses_current_authority_boundary_framing():
    for text in [empirical_text(), fallback_empirical_text()]:
        assert "This layer adds an empirical evidence-audit workflow to ALETHEIA's symbolic and protocol-guided governance-risk mirror." in text
        assert "internal authority-boundary review model" in text
        assert "internal readings correspond to observed governance-stability indicators" in text
        assert "These datasets are optional empirical sources." in text
        assert "purely symbolic governance-risk prototype" not in text
        assert "V-Axis-inspired model" not in text
        assert "classifications correspond" not in text


def test_patch_72_28_evidence_source_and_field_mapping_copy_is_cleaner():
    for text in [empirical_text(), fallback_empirical_text()]:
        assert "Transparency International / CPI-style corruption indices" in text
        assert "corruption / capture risk" in text
        assert '"ALETHEIA variable": "corruption / capture"' in text
        assert "vulnerable groups" in text
        assert "Transparency International / corruption indices" not in text
        assert "corruption/capture" not in text
        assert "vulnerable beings" not in text


def test_patch_72_28_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_28_MANIFEST.txt",
        "PATCH_72_28_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_28_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_28_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Shared Copy Humility Polish" in manifest
    assert r"tools\run_patch_checks.bat 72_28" in recovery
    assert "Patch 72.28" in status
    assert "Patch 72.28" in progress
    assert "Shared Copy Humility Polish" in status + progress
