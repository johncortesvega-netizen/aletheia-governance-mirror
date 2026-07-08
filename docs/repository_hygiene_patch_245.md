# Repository Hygiene Patch 245

## Purpose
Patch 245 cleans the repository package after the modularization round. It makes the root folder easier to review while preserving patch accountability.

## What changed
- Old root-level patch artifacts are archived under `docs/patch_archive/`.
- The distributable zip no longer includes `.git/`, `__pycache__/`, `.pytest_cache/`, or bytecode files.
- `PATCH_STATUS.md` and `PATCH_NOTES.md` now describe the current state through Patch 245.

## Patch archive layout

```text
docs/patch_archive/
  manifests/
  recovery_notes/
  delete_lists/
```

## Runtime boundary
This is a hygiene/documentation patch only. It does not alter ALETHEIA's scanner, scoring, semantic pressure layer, MEI7 gate, Z-axis, Stress Test, Evidence Lab, World Lens, receipt handling, telemetry/storage behavior, certification boundary, enforcement boundary, or final-truth boundary.

## Reviewer note
If you are reviewing repository history, use Git for commit history and `docs/patch_archive/` for the human-readable patch trail. The root folder intentionally keeps only the latest cleanup patch artifacts plus `PATCH_STATUS.md` and `PATCH_NOTES.md`.
