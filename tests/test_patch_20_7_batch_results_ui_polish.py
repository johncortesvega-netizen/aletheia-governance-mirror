from pathlib import Path

APP_TEXT = Path("app.py").read_text(encoding="utf-8")


def test_batch_summary_uses_user_facing_column_names():
    assert '"State": "Type"' in APP_TEXT
    assert '"Risk": "Role"' in APP_TEXT
    assert '"Label": "Reading"' in APP_TEXT
    assert 'st.column_config.TextColumn("Reading", width="large")' in APP_TEXT


def test_question_prompt_display_is_cleaned_for_ui():
    assert '"QUESTION_PROMPT": "Question"' in APP_TEXT
    assert '"Review Tool": "Review"' in APP_TEXT
    assert '"Audit Question / Review Tool": "Audit question"' in APP_TEXT


def test_machine_values_are_only_display_mapped_not_changed_in_summary_storage():
    assert 'st.session_state.audit_batch_summary = summaries' in APP_TEXT
    assert 'batch_summary_df = pd.DataFrame(st.session_state.audit_batch_summary)' in APP_TEXT
    assert 'batch_display_df = batch_summary_df.rename' in APP_TEXT
