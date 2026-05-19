from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"


def test_patch_177_mirror_check_has_plain_language_panel_layout():
    text = APP.read_text(encoding="utf-8")
    assert 'st.markdown("### Mirror Check review summary")' in text
    assert 'with st.expander("What is this reading?", expanded=False):' in text
    assert 'with st.expander("The main results", expanded=False):' in text
    assert 'with st.expander("How power and control are distributed", expanded=False):' in text
    assert 'with st.expander("Signal analysis and conclusion", expanded=False):' in text


def test_patch_177_mirror_check_panels_are_opt_in_not_expanded_by_default():
    text = APP.read_text(encoding="utf-8")
    assert 'with st.expander("Threshold mapping review", expanded=False):' in text
    assert 'with st.expander("Observed reasons", expanded=False):' in text
    assert 'with st.expander("Safeguard questions for human review", expanded=False):' in text
    assert 'with st.expander("Questions before relying on this reading", expanded=False):' in text
    assert 'with st.expander("Threshold mapping preview", expanded=(verdict == "THRESHOLD")):' not in text
    assert 'with st.expander("Observed reasons", expanded=True):' not in text


def test_patch_177_mirror_check_keeps_values_as_review_values_not_rescored():
    text = APP.read_text(encoding="utf-8")
    assert "Plain-language panels for human review" in text
    assert "These panels do not rescore the receipt" in text
    assert "does not give official permission" in text
    assert "does not prove that something is safe, good, or true" in text


def test_patch_177_support_context_is_side_by_side_and_subordinate():
    text = APP.read_text(encoding="utf-8")
    assert 'st.markdown("### Mirror Check support context")' in text
    assert 'support_columns = st.columns(2, gap="large")' in text
    assert 'with st.expander("Source match hits", expanded=False):' in text
    assert 'with st.expander("AI static scan context — subordinate to Mirror Check", expanded=False):' in text
