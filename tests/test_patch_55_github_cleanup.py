from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_55_docs_exist_and_explain_public_cleanup():
    required = [
        "docs/github_cleanup_package.md",
        "docs/contributing.md",
        "docs/repository_map.md",
    ]
    for path in required:
        assert (ROOT / path).exists(), path

    cleanup = read("docs/github_cleanup_package.md")
    assert "GitHub Cleanup Package" in cleanup
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in cleanup
    assert "does not command" in cleanup or "does not" in cleanup


def test_contributing_keeps_safe_boundaries_and_check_commands():
    contributing = read("docs/contributing.md")
    assert "tools\\run_checks.bat" in contributing
    assert "tools\\run_patch_checks.bat 55" in contributing
    for forbidden in ["automated enforcement", "leader removal", "divine verification", "Global ID sync"]:
        assert forbidden in contributing


def test_repository_map_points_to_core_public_files():
    repo_map = read("docs/repository_map.md")
    for expected in [
        "README.md",
        "docs/baseline_v01.md",
        "docs/protocol_guide.md",
        "docs/limitations.md",
        "tools/run_checks.bat",
        "examples/",
    ]:
        assert expected in repo_map


def test_patch_55_status_and_readme_are_updated():
    status = read("PATCH_STATUS.md")
    readme = read("README.md")
    about = read("about_page.py")
    assert "Patch 55" in status
    assert "GitHub Cleanup Package" in status
    assert "GitHub-ready public package" in readme
    assert "docs/repository_map.md" in readme
    assert "GitHub Cleanup Package" in about
    assert "no governance authority" in about
