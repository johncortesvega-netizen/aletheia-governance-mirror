from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def test_patch_166_app_shell_uses_ai_patrol_public_branding():
    text = (ROOT / "ui" / "app_shell.py").read_text(encoding="utf-8")
    assert 'PUBLIC_V1_LABEL = "AI Patrol — ALETHEIA v1"' in text
    assert 'AI PATROL' in text
    assert 'Friendly integrity patrol for human review.' in text
    assert 'Signal stop or go. Keep appeal open.' in text
    assert 'AI Patrol suggests. People decide. It never rules, certifies, commands, or replaces people.' in text


def test_patch_166_unit_preview_rebrand_copy_is_present():
    text = (ROOT / "ui" / "unit_preview.py").read_text(encoding="utf-8")
    assert 'container.title("AI Patrol Preview Unit")' in text
    assert 'Friendly integrity patrol. Mirror, not throne.' in text
    assert 'AI Patrol Preview Unit suggests where to begin.' in text
    assert 'AI Patrol gives stop/go review signals, not verdicts.' in text
    assert 'Preview patrol path' in text
    assert 'Proceed to AI Patrol' in text
    assert 'Suggested patrol path' in text


def test_patch_166_navigation_and_module_labels_show_rebrand():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'APP_VERSION = "v1.0-ai-patrol-rebrand"' in text
    assert '"🤖 AI Integrity Patrol"' in text
    assert '"🛂 Patrol Guide"' in text
    assert '"ℹ️ Why AI Patrol"' in text
    assert 'st.subheader("Mirror Check — Patrol Review")' in text
    assert 'st.subheader("AI Integrity Patrol — Static Review, Not Certification")' in text
    assert 'st.subheader("Patrol Guide")' in text


def test_patch_166_about_page_and_readme_include_ai_patrol_positioning():
    about_text = (ROOT / "pages_ui" / "about_page.py").read_text(encoding="utf-8")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert 'Why AI Patrol / ALETHEIA' in about_text
    assert 'AI Patrol is the friendlier public face of ALETHEIA' in about_text
    assert 'friendly integrity patrol and mirror' in about_text
    assert '# AI Patrol — ALETHEIA v1.0' in readme_text
    assert '**AI Patrol is the friendlier public face of ALETHEIA.**' in readme_text
    assert '**AI Patrol Preview Unit**' in readme_text


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
