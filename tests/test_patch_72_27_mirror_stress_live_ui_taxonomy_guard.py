from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_72_27_generic_protocol_ui_helper_exists():
    text = app_text()

    assert "def _protocol_taxonomy_ui_table_df" in text
    assert "def _protocol_public_label" in text
    assert "def _protocol_humility_note" in text
    assert "Low-risk internal reading" in text
    assert "Review / threshold reading" in text
    assert "High-risk internal reading" in text
    assert "Internal taxonomy label only; not final safety, final Sanctuary, or authority." in text


def test_patch_72_27_sydney_guard_and_batch_tables_are_display_guarded():
    text = app_text()

    assert "_protocol_taxonomy_ui_table_df(pd.DataFrame(check[\"results\"]))" in text
    assert "_protocol_taxonomy_ui_table_df(pd.DataFrame(check.get(\"results\", [])))" in text
    assert "_protocol_taxonomy_ui_table_df(pd.DataFrame(st.session_state.stress_batch_summary))" in text
    assert "st.session_state.audit_batch_summary = summaries" in text


def test_patch_72_27_stress_metric_uses_public_label_not_raw_state_heading():
    text = app_text()

    assert 'metric_card("Protocol reading", result_display, result_helper)' in text
    assert "_protocol_metric_display(verdict)" in text
    assert "Internal taxonomy:" in text
    assert "_protocol_humility_note(verdict)" in text
    assert 'metric_card("Result state", result_display, result_helper)' not in text


def test_patch_72_27_mirror_judgment_card_uses_public_label_and_humility_note():
    text = app_text()

    start = text.index("def render_chat_judgment")
    block = text[start:text.index("with st.expander(\"Observed reasons\"", start)]

    assert "_protocol_metric_display(verdict)" in block
    assert "Internal taxonomy:" in block
    assert "Humility note:" in block
    assert "_protocol_humility_note(verdict)" in block


def test_patch_72_27_self_check_case_copy_avoids_final_sanctuary_language():
    text = app_text()

    assert "Safeguarded public system should remain low-risk eligible" in text
    assert "Safeguarded public system must remain eligible for Sanctuary" not in text


def test_patch_72_27_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_27_MANIFEST.txt",
        "PATCH_72_27_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_27_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_27_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Mirror Stress Live UI Taxonomy Guard" in manifest
    assert r"tools\run_patch_checks.bat 72_27" in recovery
    assert "Patch 72.27" in status
    assert "Patch 72.27" in progress
    assert "Mirror Stress Live UI Taxonomy Guard" in status + progress
