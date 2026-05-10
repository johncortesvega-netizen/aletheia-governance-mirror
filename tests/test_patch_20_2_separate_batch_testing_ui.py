from pathlib import Path

APP_TEXT = Path("app.py").read_text(encoding="utf-8")


def test_batch_testing_is_hidden_behind_button_and_separate_from_tree_scanner():
    assert "Batch Testing — 50 phrases max" in APP_TEXT
    assert "audit_batch_testing_open" in APP_TEXT
    assert "This stays separate from the tree scanner" in APP_TEXT
    assert "with st.container(border=True)" in APP_TEXT


def test_batch_testing_supports_txt_upload_and_full_zip_download():
    assert "st.file_uploader(" in APP_TEXT
    assert 'type=["txt"]' in APP_TEXT
    assert "Upload .txt list" in APP_TEXT
    assert "Download full batch archive (.zip)" in APP_TEXT


def test_batch_testing_uses_local_only_review_path():
    assert "force_local: bool = False" in APP_TEXT
    assert "governance_scan(text_value, force_local=force_local)" in APP_TEXT
    assert 'judgment, source = local_governance_judgment(text_value, scan, sim, report), "Local batch scan"' in APP_TEXT
    assert "force_local=True" in APP_TEXT


def test_single_mirror_check_no_longer_auto_converts_lists_to_batch():
    assert "Detected a list" not in APP_TEXT
    assert "possible_batch_items" not in APP_TEXT
    assert "is_witness_batch_input" not in APP_TEXT
