from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def test_patch_188_robot_officer_assets_are_packaged():
    expected = [
        "assets/ai_patrol_officer_stop_go.png",
        "assets/ai_patrol_officer_preview.png",
        "assets/ai_patrol_officer_character_sheet.png",
    ]
    for name in expected:
        path = ROOT / name
        assert path.exists(), f"Missing robot officer asset: {name}"
        assert path.suffix.lower() == ".png"
        with Image.open(path) as img:
            assert img.size[0] >= 512
            assert img.size[1] >= 512


def test_patch_188_main_app_uses_robot_officer_logo_with_readable_stop_go():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'MASCOT_LOGO_IMAGE = PROJECT_ROOT / "assets" / "ai_patrol_officer_stop_go.png"' in text
    assert 'APP_VERSION = "v1.0-ai-patrol-officer-icons-p2"' in text
    assert "keep STOP / GO lettering readable" in text
    assert "transform: none;" in text


def test_patch_188_preview_unit_embeds_robot_officer_visual_guide():
    text = (ROOT / "ui" / "unit_preview.py").read_text(encoding="utf-8")
    assert "get_unit_preview_officer_image_uri" in text
    assert 'assets" / "ai_patrol_officer_preview.png"' in text
    assert "unit-preview-officer-card" in text
    assert "Pause · Check · Ask · Proceed carefully." in text
    assert "child-readable stop/go guidance" in text
    assert "visual guide only: no certification, no command, no final authority" in text
    assert "Friendly ALETHEIA robot officer holding stop and go signs" in text


def test_patch_188_is_visual_only_documented():
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    assert "Patch 188 — Robot Officer Visual Integration" in status
    assert "Patch 188 — Robot Officer Visual Integration" in progress
    assert "No scoring, routing, taxonomy, receipt" in status
