from pathlib import Path
import hashlib
from PIL import Image


def test_patch_72_12_refreshed_mascot_asset_exists_and_is_square_png():
    asset = Path("assets/aletheia_robot_laurel_logo.png")
    assert asset.exists()
    assert asset.stat().st_size > 100000
    img = Image.open(asset)
    assert img.size == (512, 512)
    assert img.format == "PNG"


def test_patch_72_12_refreshed_asset_hash_matches_expected_image():
    asset = Path("assets/aletheia_robot_laurel_logo.png")
    digest = hashlib.sha256(asset.read_bytes()).hexdigest()
    assert digest == "42d4e9a1370170a729bcd8b3a9d92e26ffe3e74d423f30604799907d4e064ec4"


def test_patch_72_12_app_still_points_to_mascot_logo_asset():
    text = Path("app.py").read_text(encoding="utf-8")
    assert 'MASCOT_LOGO_IMAGE = PROJECT_ROOT / "assets" / "aletheia_robot_laurel_logo.png"' in text
    assert 'mascot_logo_uri = asset_image_data_uri(MASCOT_LOGO_IMAGE)' in text
    assert 'class="aletheia-mascot-logo"' in text


def test_patch_72_12_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_12_MANIFEST.txt",
        "PATCH_72_12_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_12_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_12_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Mascot Asset Refresh" in manifest
    assert r"tools\run_patch_checks.bat 72_12" in recovery
    assert "Patch 72.12" in status
    assert "Patch 72.12" in progress
    assert "Mascot Asset Refresh" in status + progress
