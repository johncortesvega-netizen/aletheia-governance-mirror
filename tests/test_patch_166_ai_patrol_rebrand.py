from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def test_patch_166_app_shell_uses_ai_patrol_public_branding():
    text = (ROOT / "ui" / "app_shell.py").read_text(encoding="utf-8")
    assert 'PUBLIC_V1_LABEL = "ALETHEIA Governance Mirror"' in text
    assert 'ALETHEIA Governance Mirror' in text
    assert 'Protocol-guided audit and simulation framework for human review.' in text
    assert 'Reflect pressure. Keep appeal open.' in text
    assert 'ALETHEIA reflects. People decide. It never rules, certifies, commands, or replaces people.' in text


def test_patch_166_unit_preview_rebrand_copy_is_present():
    text = (ROOT / "ui" / "unit_preview.py").read_text(encoding="utf-8")
    assert 'unit-preview-brand-title' in text
    assert 'Governance mirror. Mirror, not throne.' in text
    assert 'ALETHEIA Preview Unit suggests where to begin.' in text
    assert 'ALETHEIA gives mirror-review signals, not verdicts.' in text
    assert 'Preview review path' in text
    assert 'Proceed to ALETHEIA' in text
    assert 'Suggested review path' in text


def test_patch_166_navigation_and_module_labels_show_rebrand():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'APP_VERSION = "v1.0-original-governance-mirror' in text
    assert '"📜 Protocol Guide"' in text
    assert '"ℹ️ Why ALETHEIA"' in text
    assert '"🪞 Mirror Check"' in text
    assert 'st.subheader("Protocol Guide")' in text


def test_patch_166_about_page_and_readme_include_ai_patrol_positioning():
    about_text = (ROOT / "pages_ui" / "about_page.py").read_text(encoding="utf-8")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert 'Why ALETHEIA' in about_text
    assert 'ALETHEIA is a free, open-source governance mirror' in about_text
    assert 'governance mirror' in about_text
    assert '# ALETHEIA — Governance Mirror v1.0' in readme_text
    assert '**ALETHEIA is a free, open-source governance mirror.**' in readme_text
    assert '**ALETHEIA Preview Unit**' in readme_text


def test_patch_166_new_mascot_assets_are_bundled_as_square_pngs():
    for asset_name in [
        'assets/aletheia_robot_laurel_logo.png',
        'assets/aletheia_mascot.png',
        'assets/about_header.png',
    ]:
        asset = ROOT / asset_name
        assert asset.exists(), f"Missing asset: {asset_name}"
        assert asset.suffix.lower() == '.png'
        with Image.open(asset) as img:
            assert img.size[0] == img.size[1]
            assert img.size[0] >= 512
