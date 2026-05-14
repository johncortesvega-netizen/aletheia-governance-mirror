"""Run the current ALETHEIA patch-suite safely.

This is the default post-Patch-49 suite. It intentionally runs the latest
patch-specific test and compile checks, while leaving older historical patch
contract tests and legacy regression tests for explicit cleanup passes.

Usage:
    python tools/run_current_suite.py
    python tools/run_current_suite.py --patch 49
    python tools/run_current_suite.py --all-modern
    python tools/run_current_suite.py --skip-compile
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_RE = re.compile(r"^test_patch_(\d+)(?:[_\.](\d+))?[_a-zA-Z0-9]*\.py$")


def _python() -> str:
    return sys.executable or "python"


def patch_sort_key(path: Path) -> tuple[int, int, str]:
    match = PATCH_RE.match(path.name)
    if not match:
        return (9999, 9999, path.name)
    major = int(match.group(1))
    minor = int(match.group(2) or 0)
    return (major, minor, path.name)


def find_patch_tests(min_patch: int = 33) -> list[Path]:
    tests_dir = ROOT / "tests"
    matches: list[Path] = []
    if not tests_dir.exists():
        return matches
    for path in tests_dir.glob("test_patch_*.py"):
        match = PATCH_RE.match(path.name)
        if not match:
            continue
        major = int(match.group(1))
        if major >= min_patch:
            matches.append(path)
    return sorted(matches, key=patch_sort_key)


def find_tests_for_patch(patch_id: str) -> list[Path]:
    normalized = patch_id.strip().lower().replace("patch", "").replace(".", "_").replace("-", "_")
    tests_dir = ROOT / "tests"
    if not tests_dir.exists():
        return []
    matches = list(tests_dir.glob(f"test_patch_{normalized}_*.py"))
    matches.extend(tests_dir.glob(f"test_patch_{normalized}.py"))
    return sorted(dict.fromkeys(matches), key=patch_sort_key)


def latest_patch_id(min_patch: int = 33) -> str | None:
    tests = find_patch_tests(min_patch)
    if not tests:
        return None
    latest = tests[-1]
    match = PATCH_RE.match(latest.name)
    if not match:
        return None
    major = match.group(1)
    minor = match.group(2)
    return f"{major}_{minor}" if minor else major


def relative(paths: list[Path]) -> list[str]:
    return [str(path.relative_to(ROOT)) for path in paths]


def run(args: list[str]) -> int:
    print("$ " + " ".join(args), flush=True)
    return int(subprocess.run(args, cwd=ROOT).returncode)


def existing_compile_targets() -> list[str]:
    targets = [
        "app.py",
        "about_page.py",
        "protocol.py",
        "core/witness.py",
        "tools/run_patch_checks.py",
        "tools/run_checks.py",
        "tools/package_patched_items.py",
        "tools/run_current_suite.py",
        "tools/run_legacy_test_inventory.py",
    ]
    return [target for target in targets if (ROOT / target).exists()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run current ALETHEIA safe checks.")
    parser.add_argument("--min-patch", type=int, default=33, help="First patch number considered current. Default: 33")
    parser.add_argument("--patch", help="Run tests for a specific patch id, such as 49 or 36_1.")
    parser.add_argument("--all-modern", action="store_true", help="Run all Patch 33+ historical contract tests. This may fail if old contracts assert old current-status text.")
    parser.add_argument("--skip-compile", action="store_true", help="Skip Python compile checks.")
    args = parser.parse_args(argv)

    if args.all_modern:
        tests = find_patch_tests(args.min_patch)
        label = f"Patch {args.min_patch}+ historical contract tests"
    else:
        patch_id = args.patch or latest_patch_id(args.min_patch)
        if not patch_id:
            print(f"No current patch tests found for patch >= {args.min_patch}.")
            return 1
        tests = find_tests_for_patch(patch_id)
        label = f"Patch {patch_id} current test(s)"

    if not tests:
        print("No current patch tests found.")
        return 1

    print(f"Running ALETHEIA current safe checks: {label}")
    for test_path in relative(tests):
        print(f" - {test_path}")

    code = run([_python(), "-m", "pytest", "-q", *relative(tests)])
    if code != 0:
        print("Current safe pytest failed.")
        return code

    if not args.skip_compile:
        compile_targets = existing_compile_targets()
        if compile_targets:
            code = run([_python(), "-m", "py_compile", *compile_targets])
            if code != 0:
                print("Current safe compile check failed.")
                return code

    print("Current safe checks passed.")
    print("Legacy tests are intentionally handled by tools/run_legacy_test_inventory.py and docs/legacy_test_cleanup.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
