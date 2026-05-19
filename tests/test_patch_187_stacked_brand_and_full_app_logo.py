from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_patch_187_main_app_shell_stacks_ai_patrol_under_aletheia():
    text = (ROOT / "ui" / "app_shell.py").read_text(encoding="utf-8")
    assert '<div class="hero-title"><span class="hero-title-main">Aletheia:</span><span class="hero-title-subline">AI PATROL</span></div>' in text
    assert '<div class="sidebar-brand"><span class="sidebar-brand-main">Aletheia:</span><span class="sidebar-brand-subline">AI PATROL</span></div>' in text
    assert "Aletheia: AI PATROL" in text


def test_patch_187_app_css_supports_stacked_title_and_readable_hero_logo():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert ".hero-title-main" in text
    assert ".hero-title-subline" in text
    assert ".sidebar-brand-main" in text
    assert ".sidebar-brand-subline" in text
    assert ".hero-emblem .aletheia-mascot-logo" in text
    assert "transform: none;" in text


def test_patch_187_preview_unit_stacks_brand_title():
    text = (ROOT / "ui" / "unit_preview.py").read_text(encoding="utf-8")
    assert "unit-preview-brand-title" in text
    assert 'unit-preview-brand-main">Aletheia:</span>' in text
    assert 'unit-preview-brand-subline">AI PATROL</span>' in text
    assert "Proceed to Aletheia: AI PATROL" in text
    assert "before entering Aletheia: AI PATROL" in text


def test_patch_187_is_visual_branding_only_documented():
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    assert "Patch 187 — Stacked Brand and Full-App Logo Direction" in status
    assert "Patch 187 — Stacked Brand and Full-App Logo Direction" in progress
    assert "No scoring, routing, taxonomy, receipt" in status
