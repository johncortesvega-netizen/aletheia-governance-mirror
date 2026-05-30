from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
ARTIFICIAL_PAGE = ROOT / "pages_ui" / "artificial_mind_formation_page.py"


def test_patch_167_protocol_guide_has_original_heading():
    text = APP.read_text(encoding="utf-8")
    section = text[text.index("with tab_doctrine:"):text.index("with tab_about:")]
    assert 'st.subheader("Protocol Guide")' in section
    assert '### ALETHEIA Protocol Guide' in section
    assert 'four side-by-side rows of collapsed panels' in section
    assert 'All panels are collapsed by default' in section


def test_patch_167_protocol_guide_restores_four_rows_eight_collapsed_panels():
    text = APP.read_text(encoding="utf-8")
    section = text[text.index("with tab_doctrine:"):text.index("with tab_about:")]
    assert "patrol_guide_rows = [" in section
    assert 'st.columns(2, gap="large")' in section
    assert 'with st.expander(panel_title, expanded=False):' in section
    assert 'with st.expander("Public trust package", expanded=False):' in section
    for title in [
        "1. Operating boundary",
        "2. Artificial Mind Formation Theory",
        "3. Navigation & module map",
        "4. Shared protocol state",
        "5. Release & continuity",
        "6. Evidence & source rules",
        "7. Review lenses",
        "8. World / taxonomy / limits",
        "Public trust package",
    ]:
        assert title in section


def test_patch_167_artificial_mind_explainer_is_restored_inside_patrol_guide():
    app_text = APP.read_text(encoding="utf-8")
    page_text = ARTIFICIAL_PAGE.read_text(encoding="utf-8")
    assert "from pages_ui.artificial_mind_formation_page import get_artificial_mind_formation_markdown" in app_text
    assert "get_artificial_mind_formation_markdown()" in app_text
    assert "ALETHEIA cannot build the spark. It can inspect the hands reaching for it." in page_text
    assert "Artificial Mind Formation Theory" in page_text
    assert "not judge" in page_text


def test_patch_167_protocol_guide_keeps_non_authority_boundary_language():
    text = APP.read_text(encoding="utf-8")
    section = text[text.index("with tab_doctrine:"):text.index("with tab_about:")]
    assert "mirror, not a throne" in section
    assert "does not judge, certify, enforce" in section
    assert "Human review remains required" in section
    assert "does **not** activate Global ID" in section
    assert "not a sovereign body" in section
