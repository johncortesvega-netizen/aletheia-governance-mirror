"""
ALETHEIA RECOVERY NOTE
Patch 08: User Input Baseline Contract + Invisibility Filter UI

Purpose:
    Verify that the Simulation tab no longer analyzes built-in example data by
    default and that user-submitted input is the baseline for Scenario Scan.

Scope:
    Content-level UI contract checks only. This test must not execute Streamlit.

Rollback:
    Remove this test file and revert app.py to Patch 07.
"""

from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
APP_TEXT = APP_PATH.read_text(encoding="utf-8")


def test_simulation_scenario_starts_empty_not_example_loaded():
    assert 'st.session_state.simulation_scenario_text = ""' in APP_TEXT
    assert 'st.session_state.simulation_scenario_text = SCENARIOS["Healthcare as a shared human right"]' not in APP_TEXT


def test_demo_scenarios_are_explicitly_loaded_and_labeled():
    assert 'Demo examples' in APP_TEXT
    assert 'Load demo' in APP_TEXT
    assert 'Demo mode is on. These results are only an example.' in APP_TEXT
    assert 'never run by themselves' in APP_TEXT


def test_empty_scenario_scan_refuses_to_run():
    assert 'input_status = "EMPTY_INPUT"' in APP_TEXT
    assert 'Add your own scenario or load a demo before running Scenario Scan' in APP_TEXT
    assert 'ALETHEIA does not run examples by itself.' in APP_TEXT
    assert 'if run or "last_report" not in st.session_state' not in APP_TEXT


def test_invisibility_filter_defaults_on_for_user_input():
    assert 'from core.parser import parse_scenario_llm, decouple_actor' in APP_TEXT
    assert '"Invisibility Filter"' in APP_TEXT
    assert 'value=(input_status == "USER_INPUT")' in APP_TEXT
    assert 'disabled=(input_status == "EMPTY_INPUT")' in APP_TEXT
    assert 'analysis_query = invisibility_report.get("decoupled_text", query)' in APP_TEXT


def test_default_language_replaced_with_starting_preset_language():
    assert '"default": "Starting preset"' in APP_TEXT
    assert 'Reset starting preset' in APP_TEXT
    assert 'This is only a starting lens. ALETHEIA waits for your input.' in APP_TEXT
