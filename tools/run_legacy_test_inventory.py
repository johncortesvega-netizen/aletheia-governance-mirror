"""Inventory legacy ALETHEIA tests that are outside the current patch-suite.

This script does not modify or delete tests. It reports legacy collection risks
so cleanup can happen deliberately instead of blocking the safe current suite.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_RE = re.compile(r"^test_patch_(\d+)(?:[_\.](\d+))?[_a-zA-Z0-9]*\.py$")
KNOWN_BLOCKERS = {
    "tests/tests/test_patch_29_hard_capture_receipt_trace.py": "nested duplicate path can cause pytest import-file mismatch",
    "tests/test_patch_20_1_batch_question_upload_mode.py": "imports combine_witness_text_uploads, which is not present in current core/witness.py",
    "tests/test_scoring_repair_questions.py": "imports repair_prompts_from_report, which is not present in current core/scoring.py",
}


def classify(path: Path, min_current_patch: int = 33) -> str:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    if rel.startswith("tests/tests/"):
        return "nested duplicate test path"
    match = PATCH_RE.match(path.name)
    if match and int(match.group(1)) < min_current_patch:
        return "legacy patch test"
    if match and int(match.group(1)) >= min_current_patch:
        return "current patch test"
    return "legacy unnumbered regression test"


def main() -> int:
    tests_dir = ROOT / "tests"
    all_tests = sorted(tests_dir.rglob("test*.py")) if tests_dir.exists() else []
    legacy = []
    current = []
    nested = []

    for path in all_tests:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        label = classify(path)
        if label == "current patch test":
            current.append(rel)
        else:
            legacy.append((rel, label, KNOWN_BLOCKERS.get(rel, "requires review before full-suite enforcement")))
            if rel.startswith("tests/tests/"):
                nested.append(rel)

    print("ALETHEIA Legacy Test Inventory")
    print(f"Current patch tests: {len(current)}")
    print(f"Legacy / cleanup candidates: {len(legacy)}")
    print()

    if nested:
        print("Nested duplicate test paths:")
        for rel in nested:
            print(f" - {rel}")
        print()

    print("Known blockers:")
    for rel, reason in KNOWN_BLOCKERS.items():
        exists = "present" if (ROOT / rel).exists() else "missing"
        print(f" - {rel} [{exists}]: {reason}")
    print()

    print("Cleanup candidates:")
    for rel, label, note in legacy:
        print(f" - {rel} — {label}; {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
