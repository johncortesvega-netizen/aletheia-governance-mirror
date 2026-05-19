from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_patch_185_main_app_shell_uses_exact_requested_brand_label():
    text = (ROOT / "ui" / "app_shell.py").read_text(encoding="utf-8")
    assert 'PUBLIC_V1_LABEL = "Aletheia: AI PATROL"' in text
    assert '<div class="hero-kicker">Aletheia: AI PATROL</div>' in text
    assert '<span class="hero-title-main">Aletheia:</span><span class="hero-title-subline">AI PATROL</span>' in text
    assert '<span class="sidebar-brand-main">Aletheia:</span><span class="sidebar-brand-subline">AI PATROL</span>' in text


def test_patch_185_preview_unit_uses_exact_requested_brand_label():
    text = (ROOT / "ui" / "unit_preview.py").read_text(encoding="utf-8")
    assert 'unit-preview-brand-title' in text
    assert 'Proceed to Aletheia: AI PATROL' in text
    assert 'before entering Aletheia: AI PATROL' in text
    assert 'after entering Aletheia: AI PATROL' in text


def test_patch_185_preview_unit_flips_entry_logo_only():
    text = (ROOT / "ui" / "unit_preview.py").read_text(encoding="utf-8")
    assert '/* Patch 185: Preview Unit only; face the entry logo the other way. */' in text
    assert '.hero-emblem .aletheia-mascot-logo' in text
    assert 'transform: scaleX(-1);' in text


def test_patch_185_is_branding_visual_only_documented():
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    assert "Patch 185 — Aletheia AI Patrol Branding Alignment" in status
    assert "Patch 185 — Aletheia AI Patrol Branding Alignment" in progress
    assert "No scoring, routing, taxonomy, receipt" in status
