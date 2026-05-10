from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
MASCOT = ROOT / "assets" / "aletheia_mascot.png"


def _app_text() -> str:
    return APP.read_text(encoding="utf-8")


def test_patch_32_2_version_is_declared():
    text = _app_text()
    assert 'APP_VERSION = "v9.6.14-patch32-2-mascot-logo"' in text


def test_mascot_asset_is_bundled():
    assert MASCOT.exists()
    assert MASCOT.stat().st_size > 10_000


def test_dove_emoji_logo_is_removed_from_app_shell():
    text = _app_text()
    assert "🕊" not in text


def test_hero_and_sidebar_use_mascot_image():
    text = _app_text()
    assert 'MASCOT_IMAGE = PROJECT_ROOT / "assets" / "aletheia_mascot.png"' in text
    assert 'mascot_uri = _image_data_uri(MASCOT_IMAGE)' in text
    assert 'class="hero-emblem" aria-hidden="true"><img class="mascot-mark"' in text
    assert 'class="sidebar-emblem-mark"><img class="mascot-mark"' in text


def test_mascot_css_keeps_the_round_app_logo_frame():
    text = _app_text()
    assert ".mascot-mark" in text
    assert "object-fit: contain" in text
    assert ".hero-emblem" in text
    assert ".sidebar-emblem-mark" in text
