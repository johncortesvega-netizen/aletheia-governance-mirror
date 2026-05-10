from pathlib import Path

APP_TEXT = Path("app.py").read_text(encoding="utf-8")


def test_batch_table_folds_role_into_reading_for_narrow_panel():
    assert "fold Role into Reading" in APP_TEXT
    assert "batch_display_df = batch_display_df[[\"#\", \"Type\", \"Reading\"]]" in APP_TEXT
    assert 'st.column_config.TextColumn("Role"' not in APP_TEXT
