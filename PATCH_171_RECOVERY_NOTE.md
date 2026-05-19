# PATCH 171 Recovery Note

## Summary
Patch 171 adds a hard reviewability floor to AI Integrity Patrol. Artifacts with critical opacity or missing-review findings cannot display as low / SANCTUARY-style readings; they route to at least THRESHOLD / Needs Review.

## Why
The opaque-agent demo includes proprietary hidden criteria, a non-reviewable score, no challenge path, and undisclosed ranking logic. That combination must require human review even if the numeric pressure remains moderate.

## Recovery steps
1. Restore `core/ai_integrity_mirror.py` from the previous patch if this guard needs rollback.
2. Remove or update `tests/test_patch_171_ai_integrity_reviewability_floor.py` accordingly.
3. Re-run `python tools/run_patch_checks.py 171` and `python tools/run_patch_checks.py 170`.

## Boundary
This patch does not alter World Lens, Evidence Lab, receipt schema, general taxonomy labels, UI navigation, telemetry/storage, enforcement, certification, or final-authority behavior. Human review remains required.
