from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def load_module(rel: str):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_legacy_cleanup_doc_names_safe_and_legacy_workflows():
    text = read("docs/legacy_test_cleanup.md")
    required = [
        "ALETHEIA v0.1 — Legacy Test Cleanup",
        "tools\\run_checks.bat",
        "tools\\run_patch_checks.bat 49",
        "tools\\run_legacy_test_inventory.py",
        "tools\\run_full_checks.bat",
        "tests/tests/test_patch_29_hard_capture_receipt_trace.py",
        "combine_witness_text_uploads",
        "repair_prompts_from_report",
        "Do not silently remove legacy tests",
    ]
    for phrase in required:
        assert phrase in text


def test_run_current_suite_discovers_latest_patch_and_modern_inventory():
    module = load_module("tools/run_current_suite.py")
    modern_tests = [str(path.name) for path in module.find_patch_tests(33)]
    patch_49_tests = [str(path.name) for path in module.find_tests_for_patch("49")]
    assert "test_patch_33_logic_baseline.py" in modern_tests
    assert "test_patch_48_release_candidate_checklist.py" in modern_tests
    assert "test_patch_49_legacy_test_cleanup.py" in modern_tests
    assert patch_49_tests == ["test_patch_49_legacy_test_cleanup.py"]
    assert module.latest_patch_id(33) == "49"
    assert "test_patch_20_1_batch_question_upload_mode.py" not in modern_tests
    assert "test_scoring_repair_questions.py" not in modern_tests


def test_tools_and_pytest_config_define_safe_boundaries():
    run_checks = read("tools/run_checks.bat")
    full_checks = read("tools/run_full_checks.bat")
    inventory = read("tools/run_legacy_test_inventory.py")
    pytest_ini = read("pytest.ini")

    assert "tools\\run_current_suite.py" in run_checks
    assert "latest patch-specific" in run_checks
    assert "tools\\run_legacy_test_inventory.py" in run_checks
    assert "non-blocking" in run_checks
    assert "pytest -q tests --ignore=tests\\tests" in full_checks
    assert "KNOWN_BLOCKERS" in inventory
    assert "tests/tests" in pytest_ini
    assert "--ignore=tests/tests" in pytest_ini


def test_status_progress_readme_and_about_surface_patch_49():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    workflow = read("docs/patch_workflow.md")
    readme = read("README.md")
    about = read("about_page.py")
    manifest = read("PATCH_49_MANIFEST.txt")

    assert "| 48 | Release Candidate Checklist | Passed |" in status
    assert "| 49 | Full Test Suite / Legacy Test Cleanup | Current |" in status
    assert "tools\\run_patch_checks.bat 49" in status
    assert "Patch 50 — v0.1 Release Package" in status

    assert "Patch 49 Notes" in progress
    assert "docs/legacy_test_cleanup.md" in progress
    assert "Legacy Test Cleanup" in workflow
    assert "Legacy test cleanup" in readme
    assert "docs/legacy_test_cleanup.md" in readme
    assert "Legacy Test Cleanup" in about
    assert "tools/run_current_suite.py" in manifest
    assert "pytest.ini" in manifest
