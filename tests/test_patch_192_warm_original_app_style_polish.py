from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_192_app_version_and_warm_css_layer_present() -> None:
    app = read("app.py")
    assert 'APP_VERSION = "v1.0-original-governance-mirror-p3"' in app
    assert "Patch 192: original poster-style warm governance-mirror app polish" in app
    assert "--aletheia-cream: #fbf6ea;" in app
    assert "--aletheia-green: #355c2b;" in app
    assert "--aletheia-red: #b23a42;" in app
    assert "rgba(255, 250, 241, 0.98)" in app
    assert "Warm cream, muted green, and soft red accents frame the operating boundaries without adding authority." in app


def test_patch_192_public_copy_no_longer_uses_blue_or_patrol_frame() -> None:
    about = read("pages_ui/about_page.py")
    evidence = read("pages_ui/evidence_lab_page.py")
    app = read("app.py")
    assert "free, open-source governance mirror for human review" in about
    assert "compact stop/go" not in about
    assert "Evidence Lab — Evidence Patrol" not in evidence
    assert 'container.subheader("Evidence Lab")' in evidence
    assert "bright patrol frame" not in evidence
    assert "warm governance-mirror frame" in evidence
    assert "Sky-blue base" not in app


def test_patch_192_patch_artifacts_and_archived_patch_191_are_present() -> None:
    assert (ROOT / "PATCH_192_MANIFEST.txt").exists()
    assert (ROOT / "PATCH_192_RECOVERY_NOTE.md").exists()
    assert (ROOT / "PATCH_192_DELETE_LIST.txt").exists()
    assert (ROOT / "docs/patch_archive/manifests/PATCH_191_MANIFEST.txt").exists()
    assert (ROOT / "docs/patch_archive/recovery_notes/PATCH_191_RECOVERY_NOTE.md").exists()
    assert (ROOT / "docs/patch_archive/delete_lists/PATCH_191_DELETE_LIST.txt").exists()
