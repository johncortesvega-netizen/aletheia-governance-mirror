# Patch 142.16 Recovery Note — Boundary Cases Navigation Placement Polish

If this patch needs rollback, revert the navigation-order edits in `app.py`, restore the previous navigation documentation text, and remove `tests/test_patch_142_16_boundary_cases_navigation_placement.py` plus this manifest/recovery note.

This patch is placement/copy only. It moves Boundary Cases behind World Lens so the primary work modules are easier to scan before the reference/calibration layer. Boundary Cases remains available and unchanged. It does not create Boundary Cases receipts, change scoring, change verdict routing, alter taxonomy, modify receipt schemas, change World Lens math, or add authority claims.

Validation target:

```bat
python tools\run_patch_checks.py 142_16
python tools\run_patch_checks.py 142_15
python tools\run_patch_checks.py 142_13
python tools\run_protocol_baseline_self_audit.py
```
