from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_194_app_version_and_artifacts() -> None:
    app = read("app.py")
    assert 'APP_VERSION = "v1.0-original-governance-mirror-p5"' in app
    assert (ROOT / 'PATCH_194_MANIFEST.txt').exists()
    assert (ROOT / 'PATCH_194_RECOVERY_NOTE.md').exists()
    assert (ROOT / 'PATCH_194_DELETE_LIST.txt').exists()
    assert (ROOT / 'docs/patch_archive/manifests/PATCH_193_MANIFEST.txt').exists()
    assert (ROOT / 'docs/patch_archive/recovery_notes/PATCH_193_RECOVERY_NOTE.md').exists()
    assert (ROOT / 'docs/patch_archive/delete_lists/PATCH_193_DELETE_LIST.txt').exists()


def test_patch_194_visual_posters_are_opt_in_expander_only() -> None:
    text = read('ui/unit_preview.py')
    assert 'with container.expander("Open visual reference posters", expanded=False):' in text
    assert 'Open them only when you want orientation material; they are not final authority.' in text
    assert 'Render packaged visual reference cards behind an opt-in expander.' in text


def test_patch_194_visible_captions_do_not_include_replacement_wording() -> None:
    text = read('ui/unit_preview.py')
    assert 'replacing the earlier blue' not in text
    assert 'replacing the earlier pink' not in text
    assert 'replacement' not in text.lower()
    assert 'Command-dossier poster for reviewing the protocol context and boundary layer.' in text
    assert "Architect's-checklist poster for reviewing the protocol principles and baseline context." in text
