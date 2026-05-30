from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_193_app_version_and_artifacts() -> None:
    app = read("app.py")
    assert 'APP_VERSION = "v1.0-original-governance-mirror-p4"' in app
    assert (ROOT / 'PATCH_193_MANIFEST.txt').exists()
    assert (ROOT / 'PATCH_193_RECOVERY_NOTE.md').exists()
    assert (ROOT / 'PATCH_193_DELETE_LIST.txt').exists()
    assert (ROOT / 'docs/patch_archive/manifests/PATCH_192_MANIFEST.txt').exists()
    assert (ROOT / 'docs/patch_archive/recovery_notes/PATCH_192_RECOVERY_NOTE.md').exists()
    assert (ROOT / 'docs/patch_archive/delete_lists/PATCH_192_DELETE_LIST.txt').exists()


def test_patch_193_unit_preview_uses_visual_reference_grid() -> None:
    text = read('ui/unit_preview.py')
    assert 'get_unit_preview_visual_reference_cards' in text
    assert 'render_unit_preview_visual_reference_cards' in text
    assert '### Visual reference posters' in text
    assert 'calm 2x2 poster grid' in text
    assert 'render_unit_preview_html_reference' not in text
    assert 'Sydney Protocol v3.2' not in text
    assert 'GPA v8.2' not in text
    assert 'The Sydney Protocol: Command Dossier' in text
    assert "The Sydney Protocol: Architect's Checklist" in text


def test_patch_193_visual_card_assets_are_packaged() -> None:
    expected = {
        'assets/visual_cards/global_peace_architecture.jpg': (1600, 900),
        'assets/visual_cards/sovereign_master_blueprint.jpg': (1600, 900),
        'assets/visual_cards/sydney_protocol_command_dossier.jpg': (1600, 900),
        'assets/visual_cards/sydney_protocol_architect_checklist.jpg': (1600, 900),
    }
    for rel, size in expected.items():
        image = Image.open(ROOT / rel)
        assert image.size == size, rel
