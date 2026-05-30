from pathlib import Path


def test_main_app_brand_titles_remove_colon_after_aletheia() -> None:
    text = Path("ui/app_shell.py").read_text(encoding="utf-8")
    assert 'PUBLIC_V1_LABEL = "ALETHEIA Governance Mirror"' in text
    assert '<div class="hero-kicker">Free · Open Source · Human Review Required</div>' in text
    assert '<span class="hero-title-main">ALETHEIA</span><span class="hero-title-subline">GOVERNANCE MIRROR</span>' in text
    assert '<span class="sidebar-brand-main">ALETHEIA</span><span class="sidebar-brand-subline">Governance Mirror</span>' in text
    assert '<span class="hero-title-main">Aletheia:</span>' not in text
    assert '<span class="sidebar-brand-main">Aletheia:</span>' not in text


def test_preview_unit_brand_title_removes_colon_after_aletheia() -> None:
    text = Path("ui/unit_preview.py").read_text(encoding="utf-8")
    assert '<span class="unit-preview-brand-main">ALETHEIA</span>' in text
    assert '<span class="unit-preview-brand-main">Aletheia:</span>' not in text
    assert 'Proceed to ALETHEIA' in text
    assert 'before entering ALETHEIA' in text


def test_tree_canopy_is_raised_for_module_tree_visuals() -> None:
    text = Path("app.py").read_text(encoding="utf-8")
    assert 'canopy_y_offset = -8 if state == "SANCTUARY" else (-4 if state == "THRESHOLD" else 1)' in text
    assert 'canopy_sag = 2 if state == "SANCTUARY" else (6 if state == "THRESHOLD" else 11)' in text
    assert 'Patch 189 raises the visual-only canopy again' in text

def test_app_version_marks_second_robot_officer_visual_patch() -> None:
    text = Path("app.py").read_text(encoding="utf-8")
    assert 'APP_VERSION = "v1.0-original-governance-mirror-p1"' in text
