"""
ALETHEIA RECOVERY NOTE
Patch 11: Tab Name Cleanup

Purpose:
    Verify that the top-level module tabs use the clearer public names while
    preserving clear public names and keeping reference modules behind the main work modules.

Scope:
    Content-level UI contract checks only. This test must not execute Streamlit.

Rollback:
    Remove this test file and revert the tab-label strings in app.py.
"""

from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
APP_TEXT = APP_PATH.read_text(encoding="utf-8")


def test_top_level_tabs_use_public_friendly_names():
    expected = [
        "🪞 Mirror Check",
        "🚀 Stress Test",
        "🤖 AI Integrity Mirror",
        "📊 Evidence Lab",
        "🌐 World Lens",
        "🧭 Boundary Cases",
        "📜 Protocol Guide",
        "ℹ️ Why ALETHEIA",
    ]
    positions = [APP_TEXT.index(label) for label in expected]
    assert positions == sorted(positions)
    assert '"💬 Audit", "🚀 Simulation", "📊 Empirical Study", "🌐 Global Grid", "📜 Doctrine", "ℹ️ About"' not in APP_TEXT


def test_main_module_headers_match_tab_names():
    assert 'Mirror Check — Gentle Risk Review' in APP_TEXT
    assert 'Stress Test — Try an Idea' in APP_TEXT
    assert 'st.subheader("World Lens")' in APP_TEXT
    assert 'st.subheader("Protocol Guide")' in APP_TEXT
    assert 'st.subheader("Why ALETHEIA")' in APP_TEXT


def test_about_page_preserves_module_definitions_under_new_names():
    assert 'with st.expander("Mirror Check", expanded=True):' in APP_TEXT
    assert 'with st.expander("Stress Test", expanded=True):' in APP_TEXT
    assert 'AI Integrity Mirror — Static Artifact Review' in APP_TEXT
    assert 'with st.expander("Evidence Lab", expanded=True):' in APP_TEXT
    assert 'with st.expander("World Lens", expanded=True):' in APP_TEXT
    assert 'with st.expander("Protocol Guide", expanded=True):' in APP_TEXT
