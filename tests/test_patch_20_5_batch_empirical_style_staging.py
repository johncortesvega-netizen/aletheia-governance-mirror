from pathlib import Path

APP_TEXT = Path("app.py").read_text(encoding="utf-8")


def test_batch_upload_follows_empirical_style_stage_then_run_flow():
    assert "Batch input source" in APP_TEXT
    assert "Like Evidence Lab, uploaded files are staged first" in APP_TEXT
    assert "Press Run Batch Testing to process it" in APP_TEXT
    assert "run_batch = st.button(" in APP_TEXT


def test_upload_and_paste_are_separate_sources():
    assert '["Upload .txt", "Paste list"]' in APP_TEXT
    assert 'batch_text = batch_upload_text if batch_source == "Upload .txt" else batch_manual_text' in APP_TEXT
    assert 'Uploaded text preview' in APP_TEXT
    assert 'Paste batch phrases or questions' in APP_TEXT


def test_uploaded_text_preview_is_disabled_and_does_not_become_source_widget():
    assert 'key="audit_batch_upload_preview"' in APP_TEXT
    assert 'disabled=True' in APP_TEXT
    assert 'key="audit_batch_manual_input"' in APP_TEXT
    assert 'key="audit_batch_input"' not in APP_TEXT


def test_batch_panel_remains_separate_from_tree_scanner():
    assert "This bench stays separate from the tree scanner" in APP_TEXT
    assert "Use this side for one proposal or scenario. The tree scanner only runs here." in APP_TEXT
