from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ABOUT = ROOT / "pages_ui" / "about_page.py"


def test_patch_168_about_page_uses_compact_panel_helper():
    text = ABOUT.read_text(encoding="utf-8")
    assert "def _render_about_panel_rows" in text
    assert "for row_start in range(0, len(panels), 2)" in text
    assert 'st.columns(2, gap="large")' in text
    assert "with st.expander(title, expanded=False):" in text


def test_patch_168_why_page_has_eight_opt_in_panels():
    text = ABOUT.read_text(encoding="utf-8")
    expected_titles = [
        "1. Identity & visual theme",
        "2. Why it exists",
        "3. What this is / is not",
        "4. Science, philosophy, humility, and review",
        "5. First-use path & navigation",
        "6. Failure modes watched",
        "7. Scope layers & anti-capture posture",
        "8. What the modules do",
        "9. Research caution & developer notes",
    ]
    for title in expected_titles:
        assert title in text


def test_patch_168_about_page_keeps_original_aletheia_boundary_language():
    text = ABOUT.read_text(encoding="utf-8")
    assert "ALETHEIA is a free, open-source governance mirror" in text
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in text
    assert "It is not a judge, enforcer, oracle, certification engine" in text
    assert "mirror, not throne" not in text.lower() or "not a judge" in text.lower()


def test_patch_168_about_page_keeps_module_map_without_authority_claims():
    text = ABOUT.read_text(encoding="utf-8")
    assert "AI Integrity Mirror" in text
    assert "Protocol Guide" in text
    assert "World Lens" in text
    assert "It does not certify systems or vendors." in text
    assert "It is not a real election, government, sovereign body, mandate, Global ID system, or real 9k body." in text
