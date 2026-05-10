"""
ALETHEIA RECOVERY NOTE
Patch 16: Mirror Check User Baseline + Invisibility Filter

Purpose:
    Verify that Mirror Check follows the same no-hidden-demo baseline as
    Stress Test and applies actor decoupling by default for user input.

Scope:
    Content-level UI contract checks only. This test must not execute Streamlit.

Rollback:
    Remove this test file and revert app.py to Patch 15.
"""

from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
APP_TEXT = APP_PATH.read_text(encoding="utf-8")


def test_mirror_check_starts_empty_not_prefilled_with_demo():
    assert 'st.session_state.audit_chat_query = ""' in APP_TEXT
    assert 'A randomly selected 9k administrative body operates inside demographic-proportional lanes' not in APP_TEXT


def test_mirror_check_demo_must_be_loaded_explicitly():
    assert 'Load Mirror Check demo' in APP_TEXT
    assert 'audit_chat_input_source = "DEMO_INPUT"' in APP_TEXT
    assert 'Demo mode is on. This reading is only an example.' in APP_TEXT
    assert 'they never run by themselves' in APP_TEXT


def test_mirror_check_empty_input_refuses_to_run():
    assert 'audit_input_status = "EMPTY_INPUT"' in APP_TEXT
    assert 'Add your own idea or load a demo before review' in APP_TEXT
    assert 'ALETHEIA does not run examples by itself.' in APP_TEXT


def test_mirror_check_invisibility_filter_defaults_on_for_user_input():
    assert 'key=f"audit_invisibility_filter_{audit_input_status}"' in APP_TEXT
    assert 'value=(audit_input_status == "USER_INPUT")' in APP_TEXT
    assert 'disabled=(audit_input_status == "EMPTY_INPUT")' in APP_TEXT
    assert 'audit_invisibility_report = decouple_actor(st.session_state.audit_chat_query)' in APP_TEXT
    assert 'audit_analysis_query = audit_invisibility_report.get("decoupled_text", st.session_state.audit_chat_query)' in APP_TEXT


def test_mirror_check_preserves_raw_query_for_witness_report():
    assert '"raw_query": raw_text_value' in APP_TEXT
    assert 'latest.get("raw_query", latest["query"])' in APP_TEXT
