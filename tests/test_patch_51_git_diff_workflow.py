from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_git_diff_workflow_doc_exists_and_has_core_commands():
    text = read("docs/git_diff_workflow.md")
    required = [
        "Git Diff Workflow",
        "git init",
        "git apply --check",
        "git apply",
        "git commit",
        "patched-items-only",
        "ALETHEIA reflects. Humans review. Power stays accountable.",
    ]
    for phrase in required:
        assert phrase in text


def test_git_helper_bat_files_exist_and_are_safe():
    status = read("tools/check_git_status.bat")
    export = read("tools/export_patch_diff.bat")
    assert "git status --short" in status
    assert "Git is not installed" in status
    assert "git diff --binary -- ." in export
    assert "Usage: tools\\export_patch_diff.bat" in export


def test_public_docs_surface_git_diff_workflow():
    readme = read("README.md")
    about = read("about_page.py")
    assert "docs/git_diff_workflow.md" in readme
    assert "Git Diff Workflow" in about
    assert "git apply --check" in about


def test_patch_status_and_manifest_are_current():
    status = read("PATCH_STATUS.md")
    manifest = read("PATCH_51_MANIFEST.txt")
    assert "| 51 | Git Diff Workflow Setup | Current |" in status
    assert "Patch 52 — Optional UX Polish" in status
    assert "docs/git_diff_workflow.md" in manifest
    assert "tools/check_git_status.bat" in manifest
    assert "tools/export_patch_diff.bat" in manifest
    assert "tests/test_patch_51_git_diff_workflow.py" in manifest
