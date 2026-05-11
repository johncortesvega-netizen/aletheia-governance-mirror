from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def empirical_text() -> str:
    return Path("core/empirical.py").read_text(encoding="utf-8")


def fallback_empirical_text() -> str:
    return Path("core_empirical.py").read_text(encoding="utf-8")


def test_patch_72_19_evidence_tables_add_humble_display_fields():
    text = app_text()

    assert "def _empirical_humility_display_df" in text
    assert "empirical_pattern_display" in text
    assert "internal_taxonomy_label" in text
    assert "humility_note" in text
    assert "Low-risk internal reading" in text
    assert "not a final safety, final Sanctuary, or authority claim" in text


def test_patch_72_19_evidence_checks_use_internal_taxonomy_wording():
    text = app_text()

    assert "Group averages by internal taxonomy" in text
    assert "These are internal taxonomy groupings for model diagnostics, not final Sanctuary or authority claims." in text
    assert "Technical tables preserve raw/internal taxonomy fields for traceability" in text
    assert "_empirical_humility_display_df(group_df)" in text
    assert "_empirical_humility_display_df(scored[overlay_cols])" in text
    assert "_empirical_humility_display_df(scored)" in text


def test_patch_72_19_protocol_detail_includes_final_interpretation_for_sanitizing():
    text = app_text()

    assert '"final_audit_interpretation"' in text
    assert "Low-risk evidence pattern: strong public-data baseline, still subject to protocol guardrails." in text
    assert "Internal taxonomy label: SANCTUARY; ALETHEIA does not claim final safety, final Sanctuary, or final authority." in text


def test_patch_72_19_methodology_explains_internal_taxonomy_not_final_sanctuary():
    for text in [empirical_text(), fallback_empirical_text()]:
        assert "ALETHEIA uses the raw internal taxonomy labels `SANCTUARY`, `THRESHOLD`, and `ASYLUM`" in text
        assert "SANCTUARY: low-risk internal reading" in text
        assert "This does not mean final safety, final Sanctuary, or authority." in text
        assert "Display layers should describe SANCTUARY as a low-risk internal pattern" in text


def test_patch_72_19_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_19_MANIFEST.txt",
        "PATCH_72_19_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_19_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_19_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Evidence Lab Humility Alignment" in manifest
    assert r"tools\run_patch_checks.bat 72_19" in recovery
    assert "Patch 72.19" in status
    assert "Patch 72.19" in progress
    assert "Evidence Lab Humility Alignment" in status + progress
