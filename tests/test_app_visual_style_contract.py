from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"
TEXT = APP.read_text(encoding="utf-8")


def test_patch_12_botanical_dashboard_shell_is_present():
    assert "botanical-frame" in TEXT
    assert "sidebar-emblem-card" in TEXT
    assert "civic-ribbon" in TEXT
    assert "footer-banner" in TEXT


def test_patch_12_keeps_mirror_boundary_visible():
    assert "A mirror, not a throne." in TEXT
    assert "ALETHEIA asks. People decide." in TEXT
    assert "ALETHEIA reflects." in TEXT


def test_patch_12_uses_warm_civic_style_tokens():
    assert "Dignity first" in TEXT
    assert "Keep appeal visible" in TEXT
    assert "Baseline controls" in TEXT
