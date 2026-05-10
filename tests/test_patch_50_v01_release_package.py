from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_v01_release_package_exists_and_contains_core_boundary():
    text = read("docs/v01_release_package.md")
    assert "ALETHEIA v0.1" in text
    assert "governance mirror for human review" in text
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in text
    assert "What v0.1 does not do" in text
    assert "must not" in text


def test_release_package_explicitly_excludes_authority_mechanisms():
    text = read("docs/v01_release_package.md")
    required = [
        "real Global ID sync",
        "real 9k selection",
        "World Leader logic",
        "public ledger",
        "neural validation",
        "automated enforcement",
        "religious validation",
    ]
    for phrase in required:
        assert phrase in text


def test_readme_and_about_surface_release_package():
    readme = read("README.md")
    about = read("about_page.py")
    assert "docs/v01_release_package.md" in readme
    assert "Patch 50" in readme
    assert "v0.1 Release Package" in about
    assert "docs/v01_release_package.md" in about


def test_patch_status_and_manifest_are_current():
    status = read("PATCH_STATUS.md")
    manifest = read("PATCH_50_MANIFEST.txt")
    assert "| 50 | v0.1 Release Package | Current |" in status
    assert "Patch 51 — Git Diff Workflow Setup" in status
    assert "docs/v01_release_package.md" in manifest
    assert "tests/test_patch_50_v01_release_package.py" in manifest
