from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_36_tools_exist_and_explain_checks():
    run_checks = ROOT / "tools" / "run_checks.bat"
    run_patch_checks = ROOT / "tools" / "run_patch_checks.bat"
    packager = ROOT / "tools" / "package_patched_items.py"
    assert run_checks.exists()
    assert run_patch_checks.exists()
    assert packager.exists()

    text = read("tools/run_checks.bat")
    assert "python -m pytest -q tests" in text
    assert "python -m compileall ." in text
    assert "All ALETHEIA checks passed" in text

    patch_text = read("tools/run_patch_checks.bat")
    assert "Usage: tools\\run_patch_checks.bat PATCH_NUMBER" in patch_text
    assert "python -m pytest -q %TEST_FILE%" in patch_text
    assert "python -m py_compile app.py about_page.py" in patch_text


def test_patch_36_packager_uses_manifest_and_blocks_unsafe_paths():
    text = read("tools/package_patched_items.py")
    assert "read_manifest" in text
    assert "zipfile.ZipFile" in text
    assert "Unsafe manifest path" in text
    assert "Missing manifest files" in text
    assert "one project-relative path per line" in text


def test_patch_36_progress_database_records_patch_sequence():
    progress = read("docs/progress_database.md")
    assert "Patch 33" in progress
    assert "Patch 34" in progress
    assert "Patch 35" in progress
    assert "Patch 36" in progress
    assert "Consent-Audit Engine" in progress
    assert "next patch" in progress

    status = read("PATCH_STATUS.md")
    assert "Patch 36 — Patch Automation Toolkit — current" in status
    assert "Patch 37 — Consent-Audit Engine" in status


def test_patch_36_manifest_lists_only_project_relative_files():
    manifest = read("PATCH_36_MANIFEST.txt").splitlines()
    files = [line.strip() for line in manifest if line.strip() and not line.startswith("#")]
    assert "tools/run_checks.bat" in files
    assert "tools/package_patched_items.py" in files
    assert "docs/progress_database.md" in files
    assert "tests/test_patch_36_patch_automation.py" in files
    assert all(not Path(item).is_absolute() for item in files)
    assert all(".." not in Path(item).parts for item in files)
    assert all((ROOT / item).is_file() for item in files)
