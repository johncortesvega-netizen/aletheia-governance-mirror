from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_190_app_shell_returns_to_original_governance_mirror_identity() -> None:
    app = read("app.py")
    shell = read("ui/app_shell.py")
    assert 'APP_VERSION = "v1.0-original-governance-mirror-' in app
    assert 'MASCOT_LOGO_IMAGE = PROJECT_ROOT / "assets" / "aletheia_robot_laurel_logo.png"' in app
    assert '"📜 Protocol Guide"' in app
    assert '"ℹ️ Why ALETHEIA"' in app
    assert 'PUBLIC_V1_LABEL = "ALETHEIA Governance Mirror"' in shell
    assert '<span class="hero-title-main">ALETHEIA</span><span class="hero-title-subline">GOVERNANCE MIRROR</span>' in shell
    assert 'Protocol-guided audit and simulation framework for human review.' in shell
    assert 'ALETHEIA reflects. People decide.' in shell


def test_patch_190_visible_app_copy_no_longer_uses_ai_patrol_rebrand_terms() -> None:
    for rel in [
        "app.py",
        "ui/app_shell.py",
        "ui/unit_preview.py",
        "ui/module_intro.py",
        "ui/module_page_template.py",
        "ui/status_cards.py",
        "pages_ui/about_page.py",
        "pages_ui/evidence_lab_page.py",
        "README.md",
    ]:
        text = read(rel)
        assert "AI Patrol" not in text, rel
        assert "AI PATROL" not in text, rel
        assert "Patrol Guide" not in text, rel
        assert "Why AI Patrol" not in text, rel
        assert "ai_patrol_officer_stop_go" not in text, rel


def test_patch_190_preview_unit_uses_original_mirror_language_and_laurel_robot() -> None:
    text = read("ui/unit_preview.py")
    assert "get_unit_preview_mascot_image_uri" in text
    assert 'assets" / "aletheia_robot_laurel_logo.png"' in text
    assert 'unit-preview-brand-main">ALETHEIA</span>' in text
    assert 'unit-preview-brand-subline">Governance Mirror</span>' in text
    assert "Preview review path" in text
    assert "Suggested review path" in text
    assert "Proceed to ALETHEIA" in text
    assert "plain-language mirror guidance" in text


def test_patch_190_about_and_readme_describe_original_public_good_concept() -> None:
    about = read("pages_ui/about_page.py")
    readme = read("README.md")
    assert 'st.subheader("Why ALETHEIA")' in about
    assert "free, open-source governance mirror" in about
    assert "warm botanical details" in about
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in about
    assert "# ALETHEIA — Governance Mirror v1.0" in readme
    assert "**ALETHEIA is a free, open-source governance mirror.**" in readme
    assert "Boundary Cases, Protocol Guide, and Why ALETHEIA" in readme


def test_patch_190_latest_patch_artifacts_and_archived_patch_189_are_present() -> None:
    assert (ROOT / "PATCH_190_MANIFEST.txt").exists()
    assert (ROOT / "PATCH_190_RECOVERY_NOTE.md").exists()
    assert (ROOT / "PATCH_190_DELETE_LIST.txt").exists()
    assert (ROOT / "docs/patch_archive/manifests/PATCH_189_MANIFEST.txt").exists()
    assert (ROOT / "docs/patch_archive/recovery_notes/PATCH_189_RECOVERY_NOTE.md").exists()
    assert (ROOT / "docs/patch_archive/delete_lists/PATCH_189_DELETE_LIST.txt").exists()
