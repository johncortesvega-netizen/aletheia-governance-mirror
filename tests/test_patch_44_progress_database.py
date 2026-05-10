from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_workflow_document_exists_and_contains_commands():
    text = read("docs/patch_workflow.md")
    required = [
        "ALETHEIA v0.1 — Patch Workflow",
        "tools\\run_patch_checks.bat 44",
        "tools\\run_checks.bat",
        "PATCH_<number>_MANIFEST.txt",
        "patched-items-only rule",
        "next patch",
    ]
    for phrase in required:
        assert phrase in text


def test_progress_database_tracks_patch_44_and_module_map():
    text = read("docs/progress_database.md")
    required = [
        "Patch 44 — Progress Database + Patch Status Hardening — current",
        "Module Map",
        "Progress Database",
        "docs/patch_workflow.md",
        "Patch 45 — Release Notes + Limitations Hardening",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_status_marks_43_passed_and_44_current():
    text = read("PATCH_STATUS.md")
    assert "| 43 | Protocol Guide Consolidation | Passed |" in text
    assert "| 44 | Progress Database + Patch Status Hardening | Current |" in text
    assert "tools\\run_patch_checks.bat 44" in text
    assert "Patch 45 — Release Notes + Limitations Hardening" in text


def test_app_readme_about_surface_progress_database_workflow():
    app = read("app.py")
    readme = read("README.md")
    about = read("about_page.py")
    manifest = read("PATCH_44_MANIFEST.txt")

    assert "Progress Database + Patch Status Hardening" in app
    assert "docs/patch_workflow.md" in app
    assert "Patch 44 Progress Database + Patch Status Hardening" in readme
    assert "docs/patch_workflow.md" in readme
    assert "Progress Database" in about
    assert "docs/patch_workflow.md" in about
    assert "docs/patch_workflow.md" in manifest
    assert "tests/test_patch_44_progress_database.py" in manifest
