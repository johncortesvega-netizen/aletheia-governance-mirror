# Patch 44 — Progress Database + Patch Status Hardening

## Purpose

Move patch continuity and roadmap state further into the repository so the project does not rely only on chat memory.

## Added / Updated

- Added `docs/patch_workflow.md`.
- Hardened `docs/progress_database.md` with a module map, patch workflow, current status, and next-patch pointer.
- Updated `PATCH_STATUS.md` to mark Patch 43 as passed and set Patch 44 as current.
- Added `tests/test_patch_44_progress_database.py`.
- Updated README/About/App copy to surface the local continuity workflow.

## Boundaries

No governance authority was added.
No Global ID sync was added.
No public ledger was added.
No enforcement or leader-removal language was added.
This patch is project-continuity and developer-workflow hardening only.

## Check

```bat
tools\run_patch_checks.bat 44
```

or directly:

```bat
python -m pytest -q tests/test_patch_44_progress_database.py
python -m py_compile app.py about_page.py protocol.py core/witness.py tools/run_patch_checks.py tools/package_patched_items.py
```
