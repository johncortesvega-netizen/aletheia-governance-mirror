from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def test_patch_188_legacy_robot_officer_assets_remain_archived():
    expected = [
        "assets/ai_patrol_officer_stop_go.png",
        "assets/ai_patrol_officer_preview.png",
        "assets/ai_patrol_officer_character_sheet.png",
    ]
    for name in expected:
        path = ROOT / name
        assert path.exists(), f"Missing legacy robot officer asset: {name}"
        assert path.suffix.lower() == ".png"
        with Image.open(path) as img:
            assert img.size[0] >= 512
            assert img.size[1] >= 512


def test_patch_188_main_app_uses_robot_officer_logo_with_readable_stop_go():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'MASCOT_LOGO_IMAGE = PROJECT_ROOT / "assets" / "aletheia_robot_laurel_logo.png"' in text
    assert 'APP_VERSION = "v1.0-original-governance-mirror-p1"' in text
    assert "original governance-mirror logo; no STOP / GO officer framing" in text
    assert "transform: none;" in text


def test_patch_188_preview_unit_embeds_robot_officer_visual_guide():
    text = (ROOT / "ui" / "unit_preview.py").read_text(encoding="utf-8")
    assert "get_unit_preview_mascot_image_uri" in text
    assert 'assets" / "aletheia_robot_laurel_logo.png"' in text
    assert "unit-preview-mascot-card" in text
    assert "Audit · Simulate · Inspect evidence · Review carefully." in text
    assert "plain-language mirror guidance" in text
    assert "visual guide only: no certification, no command, no final authority" in text
    assert "Friendly ALETHEIA laurel robot visual guide" in text


def test_patch_188_is_visual_only_documented():
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    assert "Patch 188 — Robot Officer Visual Integration" in status
    assert "Patch 188 — Robot Officer Visual Integration" in progress
    assert "No scoring, routing, taxonomy, receipt" in status
