from pathlib import Path


def test_patch_72_11_mascot_asset_exists():
    asset = Path("assets/aletheia_robot_laurel_logo.png")
    assert asset.exists()
    assert asset.stat().st_size > 1000


def test_patch_72_11_app_embeds_mascot_logo_in_header_and_sidebar():
    text = Path("app.py").read_text(encoding="utf-8")

    assert "import base64" in text
    assert 'MASCOT_LOGO_IMAGE = PROJECT_ROOT / "assets" / "aletheia_robot_laurel_logo.png"' in text
    assert "def asset_image_data_uri(path: Path) -> str:" in text
    assert "mascot_logo_uri = asset_image_data_uri(MASCOT_LOGO_IMAGE)" in text
    assert text.count("aletheia-mascot-logo") >= 3
    assert '<div class="hero-emblem" aria-hidden="true"><img class="aletheia-mascot-logo" src="{mascot_logo_uri}" alt="" /></div>' in text
    assert '<div class="sidebar-emblem-mark"><img class="aletheia-mascot-logo" src="{mascot_logo_uri}" alt="" /></div>' in text
    assert 'with st.sidebar:' in text
    assert 'st.markdown(\n        f"""\n        <div class="sidebar-emblem-card">' in text


def test_patch_72_11_replaces_dove_corner_logos_only():
    text = Path("app.py").read_text(encoding="utf-8")

    assert "🕊️" not in text
    assert ".hero-emblem" in text
    assert ".sidebar-emblem-mark" in text
    assert "overflow: hidden;" in text
    assert "object-fit: cover;" in text


def test_patch_72_11_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_11_MANIFEST.txt",
        "PATCH_72_11_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_11_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_11_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Mascot Logo Replacement" in manifest
    assert "tools\\run_patch_checks.bat 72_11" in recovery
    assert "Patch 72.11" in status
    assert "Patch 72.11" in progress
    assert "Mascot Logo Replacement" in status + progress
