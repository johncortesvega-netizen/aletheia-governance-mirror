from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
ABOUT = ROOT / "pages_ui" / "about_page.py"
EVIDENCE = ROOT / "pages_ui" / "evidence_lab_page.py"


def test_patch_182_version_marks_second_visual_pass():
    text = APP.read_text(encoding="utf-8")
    assert 'APP_VERSION = "v1.0-ai-patrol-sky-theme-p2"' in text


def test_patch_182_sky_gold_alignment_css_tokens_present():
    text = APP.read_text(encoding="utf-8")
    assert "Patch 182: AI Patrol sky/gold module alignment pass" in text
    assert ".sky-gold-page-anchor" in text
    assert ".pillar-pair" in text
    assert "border-left: 6px solid var(--gold)" in text
    assert "linear-gradient(90deg, var(--gold), rgba(127,188,232,0.62))" in text
    assert 'div[data-testid="stExpander"] blockquote' in text
    assert 'div[data-testid="stExpander"] th' in text


def test_patch_182_target_pages_have_visual_anchor_without_logic_hooks():
    app_text = APP.read_text(encoding="utf-8")
    about_text = ABOUT.read_text(encoding="utf-8")
    evidence_text = EVIDENCE.read_text(encoding="utf-8")

    assert "visual-only sky/gold alignment anchor for the Patrol Guide surface" in app_text
    assert "Patrol Guide</strong>" in app_text
    assert "visual-only sky/gold alignment anchor for the public Why page" in about_text
    assert "Why AI Patrol</strong>" in about_text
    assert "visual-only sky/gold alignment anchor for Evidence Lab" in evidence_text
    assert "Evidence Lab</strong>" in evidence_text

    assert "unsafe_allow_html=True" in app_text
    assert "unsafe_allow_html=True" in about_text
    assert "unsafe_allow_html=True" in evidence_text


def test_patch_182_ai_static_scan_context_remains_subordinate():
    text = APP.read_text(encoding="utf-8")
    assert "AI static scan expanders inherit sky/gold expander and table styling; context remains subordinate" in text
    assert "AI static scan context uses the same sky/gold expander treatment" in text
    assert 'with st.expander("AI static scan context — subordinate to Stress Test", expanded=False):' in text
    assert 'with st.expander("AI static scan context — subordinate to Mirror Check", expanded=False):' in text
    assert "audit_ai_integrity_artifact(" not in text or "ai_static_scan_context" in text


def test_patch_182_status_and_recovery_artifacts_present():
    for path in [
        "PATCH_182_MANIFEST.txt",
        "PATCH_182_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert (ROOT / path).exists(), path
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    assert "Patch 182 — AI Patrol Sky/Gold Module Alignment" in status
    assert "Patch 182 — AI Patrol Sky/Gold Module Alignment" in progress
