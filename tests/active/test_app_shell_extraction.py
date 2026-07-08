from pathlib import Path

from ui.app_shell import ALETHEIA_GLOBAL_CSS, apply_app_page_config_and_theme


ROOT = Path(__file__).resolve().parents[2]


def test_global_css_lives_in_app_shell_not_app_py():
    app_text = (ROOT / "app.py").read_text(encoding="utf-8")
    shell_text = (ROOT / "ui" / "app_shell.py").read_text(encoding="utf-8")

    assert "apply_app_page_config_and_theme(st)" in app_text
    assert "st.set_page_config(page_title=\"ALETHEIA\"" not in app_text
    assert "ALETHEIA_GLOBAL_CSS" in shell_text
    assert ".hero" in ALETHEIA_GLOBAL_CSS
    assert ".footer-banner" in ALETHEIA_GLOBAL_CSS


def test_app_shell_config_helper_is_importable():
    assert callable(apply_app_page_config_and_theme)
