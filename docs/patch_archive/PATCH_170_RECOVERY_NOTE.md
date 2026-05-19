# PATCH 170 Recovery Note

## Summary
Patch 170 is a UI/layout repair for the AI Integrity Patrol single-artifact result readout. It collapses detailed result sections into compact panels while preserving the existing static AI Integrity analysis, receipt generation, and download behavior.

## Recovery steps
1. Restore `app.py` from the pre-Patch-170 state if the compact result panels create rendering issues.
2. Remove `tests/test_patch_170_ai_integrity_patrol_result_layout.py` if reverting the patch.
3. Re-run `python tools/run_patch_checks.py 169` and then any active patch checks needed for the local branch.

## Boundary reminder
The patch does not change scoring, taxonomy, receipt schema, World Lens math, Evidence Lab logic, AI Integrity rubric behavior, external calls, telemetry, storage, certification, enforcement, or final authority. Human review remains required.
