from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"


def test_patch_181_app_version_marks_sky_theme():
    text = APP.read_text(encoding="utf-8")
    assert 'APP_VERSION = "v1.0-ai-patrol-sky-theme"' in text


def test_patch_181_sky_gold_theme_tokens_present():
    text = APP.read_text(encoding="utf-8")
    assert "Patch 181: AI Patrol sky-blue / gold / white-pillars visual theme override" in text
    assert "--sky: #d8f0ff" in text
    assert "--gold: #d4af37" in text
    assert "--pillar: #ffffff" in text
    assert "linear-gradient(180deg, #dff3ff 0%, #eef9ff 38%, #ffffff 100%)" in text


def test_patch_181_white_pillar_motif_overrides_botanical_symbols():
    text = APP.read_text(encoding="utf-8")
    assert ".botanical-frame::before," in text
    assert ".botanical-frame::after" in text
    assert 'content: "";' in text
    assert "width: 18px;" in text
    assert "border: 1px solid rgba(212,175,55,0.36);" in text
    assert "font-size: 0;" in text


def test_patch_181_gold_buttons_and_panel_accents_present():
    text = APP.read_text(encoding="utf-8")
    assert 'div[data-testid="stExpander"]' in text
    assert "border: 1px solid rgba(212,175,55,0.32)" in text
    assert 'button[kind="primary"]' in text
    assert "background: linear-gradient(180deg, #d8b648 0%, #b98c14 100%)" in text
