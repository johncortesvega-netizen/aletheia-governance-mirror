"""CLI wrapper for ALETHEIA Protocol Baseline Self-Audit."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.protocol_baseline_self_audit import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main(["--root", str(ROOT), *sys.argv[1:]]))
