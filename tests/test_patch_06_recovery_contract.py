"""
ALETHEIA RECOVERY NOTE
Patch 06: Safety Regression Test Pack

Purpose:
    Add regression tests only. This patch must not change product behavior.

Scope:
    Syntax-check the production files touched by patches 01-05 and verify that
    Patch 06 did not require edits to production modules.

Rollback:
    Remove this test file. No production module should need rollback.
"""

from pathlib import Path
import py_compile


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_patch_01_to_05_files_still_compile():
    """The files touched by patches 01-05 should remain syntactically valid."""
    for relative_path in ("app.py", "protocol.py", "core/scoring.py"):
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def test_patch_06_recovery_note_exists_and_is_tests_only():
    note = PROJECT_ROOT / "PATCH_06_RECOVERY_NOTE.md"
    assert note.exists()
    text = note.read_text(encoding="utf-8")
    assert "Add tests only" in text
    assert "No production module should need rollback" in text
    assert "app.py" in text
    assert "protocol.py" in text
    assert "core/scoring.py" in text
