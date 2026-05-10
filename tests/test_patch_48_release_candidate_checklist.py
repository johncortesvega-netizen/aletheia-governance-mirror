from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_release_candidate_checklist_exists_and_names_scope():
    text = read("docs/release_candidate_checklist.md")
    assert "ALETHEIA v0.1" in text
    assert "Included v0.1 modules" in text
    assert "Explicit v0.1 exclusions" in text
    assert "Manual smoke test" in text
    assert "Release readiness criteria" in text


def test_release_candidate_checklist_preserves_authority_boundaries():
    text = read("docs/release_candidate_checklist.md")
    required = [
        "real Global ID sync",
        "real 9k selection",
        "World Leader activation or deactivation",
        "automatic reset authority",
        "neural-data extraction",
        "replacement of human judgment",
        "This claim is divinely verified",
        "The AI has decided",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_status_and_progress_database_updated():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    assert "| 47 | App Navigation + Smoke Test Cleanup | Passed |" in status
    assert "| 48 | Release Candidate Checklist | Current |" in status
    assert "tools\\run_patch_checks.bat 48" in status
    assert "Patch 49 — Full Test Suite / Legacy Test Cleanup" in status
    assert "Patch 48 Notes" in progress
    assert "docs/release_candidate_checklist.md" in progress


def test_readme_and_about_page_surface_release_candidate_checklist():
    readme = read("README.md")
    about = read("about_page.py")
    assert "Release candidate checklist" in readme
    assert "docs/release_candidate_checklist.md" in readme
    assert "tools\\run_patch_checks.bat 48" in readme
    assert "Release Candidate Checklist" in about
    assert "testable package" in about
