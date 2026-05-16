from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_151_public_ui_uses_english_first_scope():
    combined = "\n".join(
        read(rel)
        for rel in [
            "app.py",
            "about_page.py",
            "ui/app_shell.py",
            "ui/input_clarity.py",
        ]
    )
    assert "ALETHEIA is English-first" in combined
    assert "Dutch/Nederlands examples may be used for batch testing" in combined
    assert "general app-wide language-compatibility claim" in combined
    assert "English + Nederlands/Dutch input supported" not in combined
    assert "English and Nederlands/Dutch inputs are calibrated" not in combined
    assert "calibrated across the app" not in combined


def test_patch_151_docs_preserve_dutch_fixtures_without_compatibility_claim():
    combined = "\n".join(
        read(rel)
        for rel in [
            "README.md",
            "CONTRIBUTING.md",
            "docs/signal_detection.md",
            "docs/SIGNAL_DICTIONARY.md",
            "docs/batch_file_catalog.md",
            "docs/public_review_checklist.md",
            "docs/public_trust_package.md",
            "docs/structural_improvement_entrypoint.md",
            "docs/stress_test_dutch_gap_fix.md",
        ]
    )
    assert "English-first" in combined
    assert "batch-test fixtures" in combined or "batch testing" in combined
    assert "general app-wide language-compatibility claim" in combined
    forbidden = [
        "calibrated input support is English",
        "English + Nederlands/Dutch input supported",
        "English and Nederlands/Dutch are calibrated across the app",
        "strongest English/Dutch calibration path",
    ]
    for phrase in forbidden:
        assert phrase not in combined


def test_patch_151_existing_language_scope_tests_were_updated():
    test_files = "\n".join(
        read(rel)
        for rel in [
            "tests/test_patch_67_2_dutch_gap_and_language_scope.py",
            "tests/test_patch_109_app_shell_router_refactor_step_2.py",
            "tests/test_patch_113_public_trust_package_consolidation.py",
            "tests/test_patch_129_input_error_clarity.py",
            "tests/test_patch_106_signal_dictionary_glossary.py",
        ]
    )
    assert "English-first" in test_files
    assert "English + Nederlands/Dutch input supported" not in test_files
    assert "English and Nederlands/Dutch" not in test_files
    assert "English/Dutch calibration" not in test_files
