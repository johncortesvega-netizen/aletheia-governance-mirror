from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"


def _text() -> str:
    return APP.read_text(encoding="utf-8")


def test_patch32_updates_app_version():
    text = _text()
    assert 'APP_VERSION = "v9.6.12-patch32-plain-language-ui"' in text


def test_patch32_adds_plain_language_glossary_note():
    text = _text()
    assert "Plain words:" in text
    assert "Sanctuary means safer. Threshold means check it. Asylum means high risk." in text
    assert "A receipt is your local proof" in text


def test_patch32_uses_simpler_main_navigation_copy():
    text = _text()
    assert "Stress Test — Try an Idea" in text
    assert "Evidence Lab — Data Check" in text
    assert "What should World Lens use?" in text
    assert "Complete World Lens receipt" in text


def test_patch32_keeps_mirror_boundary_plain():
    text = _text()
    assert "Paste an idea. ALETHEIA looks for power, pressure, appeal, and risk." in text
    assert "You keep the final say." in text
    assert "ALETHEIA asks questions here. It gives no orders and no final judgment." in text
    assert "Creates a receipt you hold. It is not published, synced, or treated as authority." in text


def test_patch32_retains_hard_boundaries():
    text = _text()
    assert "mirror, not a throne" in text.lower()
    assert "People decide" in text
    assert "never rules, votes, commands, or replaces people" in text
