from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_python_patch_runner_exists_and_uses_glob_resolution():
    text = read("tools/run_patch_checks.py")
    assert "glob.glob" in text
    assert "test_patch_" in text
    assert "py_compile" in text


def test_batch_runner_delegates_to_python_helper_without_cmd_wildcard():
    text = read("tools/run_patch_checks.bat")
    assert "run_patch_checks.py" in text
    assert "test_patch_36_*.py" not in text


def test_safe_default_checks_explain_legacy_full_collection_status():
    text = read("tools/run_checks.bat")
    assert "run_patch_checks.bat 36_1" in text
    assert "full pytest collection is intentionally not run" in text


def test_progress_database_tracks_patch_36_1_and_next_patch():
    progress = read("docs/progress_database.md")
    status = read("PATCH_STATUS.md")
    assert "Patch 36.1" in progress
    assert "Patch 37" in status
    assert "Consent-Audit Engine" in status
