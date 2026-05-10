from pathlib import Path

APP_TEXT = Path("app.py").read_text(encoding="utf-8")


def test_batch_upload_is_staged_not_copied_into_text_area_state():
    assert "audit_batch_upload_signature" in APP_TEXT
    assert "uploaded_batch_bytes = batch_upload.getvalue()" in APP_TEXT
    assert "batch_upload_text = uploaded_batch_bytes.decode" in APP_TEXT
    assert "st.session_state.audit_batch_input = uploaded_batch_text" not in APP_TEXT


def test_batch_text_area_uses_manual_input_only():
    assert 'key="audit_batch_manual_input"' in APP_TEXT
    assert 'key="audit_batch_input"' not in APP_TEXT
    assert 'Paste batch phrases or questions' in APP_TEXT


def test_run_batch_button_uses_stable_batch_ready_flag_and_primary_style():
    assert "batch_ready = bool(batch_items)" in APP_TEXT
    assert 'disabled=not batch_ready' in APP_TEXT
    assert 'type="primary"' in APP_TEXT


def test_new_upload_clears_stale_batch_results():
    assert "st.session_state.audit_batch_summary = []" in APP_TEXT
    assert "st.session_state.audit_batch_archive_bytes = None" in APP_TEXT
    assert "st.session_state.audit_batch_index = None" in APP_TEXT
