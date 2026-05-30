from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_191_app_version_advances_and_patch_artifacts_exist() -> None:
    app = read("app.py")
    assert 'APP_VERSION = "v1.0-original-governance-mirror-' in app
    assert (ROOT / 'PATCH_191_MANIFEST.txt').exists()
    assert (ROOT / 'PATCH_191_RECOVERY_NOTE.md').exists()
    assert (ROOT / 'PATCH_191_DELETE_LIST.txt').exists()
    assert (ROOT / 'docs/patch_archive/manifests/PATCH_190_MANIFEST.txt').exists()
    assert (ROOT / 'docs/patch_archive/recovery_notes/PATCH_190_RECOVERY_NOTE.md').exists()
    assert (ROOT / 'docs/patch_archive/delete_lists/PATCH_190_DELETE_LIST.txt').exists()


def test_patch_191_refreshes_original_mascot_assets() -> None:
    mascot = Image.open(ROOT / 'assets/aletheia_robot_laurel_logo.png')
    about = Image.open(ROOT / 'assets/about_header.png')
    alt = Image.open(ROOT / 'assets/aletheia_mascot.png')
    assert mascot.size == (320, 530)
    assert alt.size == (320, 530)
    assert about.size == (1024, 430)


def test_patch_191_preview_unit_uses_warm_palette_not_blue_tint() -> None:
    text = read('ui/unit_preview.py')
    assert 'original ALETHEIA top-right mascot asset' in text
    assert 'color: #b23a42 !important;' in text
    assert 'color: #355c2b !important;' in text
    assert 'rgba(255, 252, 246, 0.98)' in text
    assert 'rgba(247, 241, 228, 0.95)' in text
    assert 'object-position: center top;' in text
    assert 'transform: scaleX(-1);' not in text
    assert 'rgba(228,246,255,0.94)' not in text
