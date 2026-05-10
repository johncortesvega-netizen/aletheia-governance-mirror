from pathlib import Path

APP_TEXT = Path("app.py").read_text(encoding="utf-8")


def test_batch_testing_is_side_by_side_with_normal_questionnaire():
    assert "normal_review_col, batch_testing_col = st.columns([0.62, 0.38], gap=\"large\")" in APP_TEXT
    assert "with normal_review_col:" in APP_TEXT
    assert "with batch_testing_col:" in APP_TEXT
    assert "Use this side for one proposal or scenario. The tree scanner only runs here." in APP_TEXT
    assert "A separate local test bench for lists. This stays separate from the tree scanner and does not run it." in APP_TEXT


def test_txt_upload_is_limited_to_batch_panel_copy():
    assert "Upload .txt list for batch only" in APP_TEXT
    assert "Upload .txt list\"," not in APP_TEXT
    assert "Open Batch Testing here when you want to upload or paste a list." in APP_TEXT


def test_batch_panel_still_hidden_behind_button():
    assert "audit_batch_testing_open" in APP_TEXT
    assert "Batch Testing — 50 phrases max" in APP_TEXT
    assert "st.session_state.audit_batch_testing_open = not st.session_state.audit_batch_testing_open" in APP_TEXT


def test_single_review_and_batch_review_remain_separate_actions():
    assert "Review idea" in APP_TEXT
    assert "Run Batch Testing" in APP_TEXT
    assert "possible_batch_items" not in APP_TEXT
    assert "Detected a list" not in APP_TEXT
