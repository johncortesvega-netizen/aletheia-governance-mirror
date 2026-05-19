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
        "4. First-use path & navigation",
        "5. Failure modes watched",
        "6. Scope layers & anti-capture posture",
        "7. What the modules do",
        "8. Research caution & developer notes",
    ]
    for title in expected_titles:
        assert title in text


def test_patch_168_about_page_keeps_ai_patrol_boundary_language():
    text = ABOUT.read_text(encoding="utf-8")
    assert "AI Patrol is the friendlier public face of ALETHEIA" in text
    assert "AI Patrol signals. Humans review. Power stays accountable." in text
    assert "It is not a judge, enforcer, oracle, certification engine" in text
    assert "mirror, not throne" not in text.lower() or "not a judge" in text.lower()


def test_patch_168_about_page_keeps_module_map_without_authority_claims():
    text = ABOUT.read_text(encoding="utf-8")
    assert "AI Integrity Patrol" in text
    assert "Patrol Guide" in text
    assert "World Lens" in text
    assert "It does not certify systems or vendors." in text
    assert "It is not a real election, government, sovereign body, mandate, Global ID system, or real 9k body." in text
