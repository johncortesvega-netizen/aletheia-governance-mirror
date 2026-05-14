"""Run ALETHEIA's current safe validation suite.

This Python entry point mirrors ``tools/run_checks.bat`` so the same local
check can be launched consistently from shells that prefer Python commands.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _python() -> str:
    return sys.executable or "python"


def _run(args: list[str]) -> int:
    print("$ " + " ".join(args), flush=True)
    return int(subprocess.run(args, cwd=ROOT).returncode)


def main() -> int:
    print("Running ALETHEIA current safe checks...")
    code = _run([_python(), "tools/run_current_suite.py"])
    if code != 0:
        return code

    print("")
    print("Reporting legacy test inventory (non-blocking)...")
    _run([_python(), "tools/run_legacy_test_inventory.py"])

    print("")
    print("ALETHEIA current safe checks passed.")
    print("Older historical patch contracts and legacy tests are documented separately and are not run by default.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
