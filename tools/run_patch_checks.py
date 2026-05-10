"""Run patch-specific ALETHEIA checks on Windows/macOS/Linux.

Usage:
    python tools/run_patch_checks.py 36
    python tools/run_patch_checks.py 36_1

This helper avoids CMD wildcard expansion problems by resolving test files in
Python before invoking pytest.
"""
from __future__ import annotations

import glob
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _python() -> str:
    return sys.executable or "python"


def _normalize_patch_id(raw: str) -> str:
    return raw.strip().lower().replace("patch", "").replace(".", "_").replace("-", "_")


def _find_patch_tests(patch_id: str) -> list[str]:
    normalized = _normalize_patch_id(patch_id)
    patterns = [
        str(ROOT / "tests" / f"test_patch_{normalized}_*.py"),
        str(ROOT / "tests" / f"test_patch_{normalized}.py"),
    ]
    matches: list[str] = []
    for pattern in patterns:
        matches.extend(glob.glob(pattern))
    # Keep stable order and unique paths.
    unique = sorted(dict.fromkeys(matches))
    return [str(Path(p).relative_to(ROOT)) for p in unique]


def _run(args: list[str]) -> int:
    print("$ " + " ".join(args), flush=True)
    completed = subprocess.run(args, cwd=ROOT)
    return int(completed.returncode)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python tools/run_patch_checks.py <patch_number>")
        print("Example: python tools/run_patch_checks.py 36_1")
        return 2

    patch_id = argv[1]
    test_files = _find_patch_tests(patch_id)
    if not test_files:
        print(f"No patch-specific tests found for patch {patch_id}.")
        print("Expected files like: tests/test_patch_<patch>_*.py")
        return 1

    print(f"Running ALETHEIA Patch {patch_id} checks...")
    print("Patch tests:")
    for test_file in test_files:
        print(f" - {test_file}")

    code = _run([_python(), "-m", "pytest", "-q", *test_files])
    if code != 0:
        print("Patch-specific pytest failed.")
        return code

    compile_targets = ["app.py", "about_page.py", "protocol.py"]
    existing_targets = [target for target in compile_targets if (ROOT / target).exists()]
    if existing_targets:
        code = _run([_python(), "-m", "py_compile", *existing_targets])
        if code != 0:
            print("Python compile check failed.")
            return code

    print("Patch checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
