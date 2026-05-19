from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def protocol_guide_source() -> str:
    app = read("app.py")
    start = app.index("with tab_doctrine:")
    end = app.index("\nwith tab_about:")
    return app[start:end]


def test_patch_165_protocol_guide_uses_four_side_by_side_opt_in_rows():
    source = protocol_guide_source()

    assert "Protocol Guide sections are grouped into four side-by-side rows" in source
    assert "Each panel is collapsed by default" in source
    assert "protocol_panel_rows = [" in source
    assert "for row_start in range(0, len(protocol_panel_rows), 2):" in source
    assert "columns = st.columns(2)" in source
    assert "with st.expander(panel_title, expanded=False):" in source
    assert "expanded=True" not in source


def test_patch_165_protocol_guide_panel_set_covers_existing_sections():
    source = protocol_guide_source()
    required_panels = [
        "Operating boundary",
        "Artificial Mind Formation Theory",
        "Navigation & module map",
        "Shared protocol state",
        "Release & continuity",
        "Evidence & source rules",
        "Review lenses",
        "World / taxonomy / limits",
    ]
    for panel in required_panels:
        assert panel in source

    required_existing_sections = [
        "Plain doctrine summary",
        "Do not worship the tool",
        "Final operating rule",
        "App navigation map",
        "Current app path",
        "Protocol Guide Consolidation",
        "Shared Protocol State",
        "Progress Database + Patch Status Hardening",
        "Public Release Limits",
        "Sample Reports / Example Audits",
        "Module checks and safe failure",
        "Evidence Lab + Extraordinary Claim Protocol",
        "Evidence rule",
        "Trust evidence rule",
        "Coverage and confidence",
        "Mirror Effect",
        "V-Axis Compass",
        "Failure Classification",
        "Mechanism-vs-Claim Scanner",
        "Self-Audit Mode",
        "Internal taxonomy labels",
        "Humility Protocol / Z-axis boundary",
        "9k representation rule",
        "World Lens interpretation",
        "Data correction and research ethics",
        "Source match overview",
        "Visual source cards",
    ]
    for section in required_existing_sections:
        assert section in source


def test_patch_165_artificial_mind_theory_is_included_in_panel_layout_without_extra_scoring_hooks():
    source = protocol_guide_source()
    app = read("app.py")
    scoring = read("core/scoring.py")
    world_lens = read("core/world_lens.py")

    assert "get_artificial_mind_formation_markdown()" in source
    assert "render_artificial_mind_formation_page(st)" not in source
    assert "from pages_ui.artificial_mind_formation_page import get_artificial_mind_formation_markdown" in app
    assert "ARTIFICIAL_MIND" not in scoring
    assert "ARTIFICIAL_MIND" not in world_lens
