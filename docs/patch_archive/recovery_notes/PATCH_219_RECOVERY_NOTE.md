# Patch 219 Recovery Note — Legacy Test Inventory Cleanup Plan

Patch 219 is documentation-only. It adds a cleanup governance layer for the historical test inventory.

## If something looks wrong

Revert these files only:

- `README.md`
- `docs/legacy_test_inventory_cleanup_plan_v1.md`
- `docs/test_migration_labels_v1.md`
- `tests/README.md`
- `PATCH_STATUS.md`
- `PATCH_219_MANIFEST.txt`
- `PATCH_219_RECOVERY_NOTE.md`
- `PATCH_219_DELETE_LIST.txt`

## Expected behavior

The default pytest behavior remains the Patch 218 behavior:

```bat
python -m pytest
```

It should collect the active suite under `tests/active/`.

Patch 219 does not alter pytest config, app runtime, scanner logic, scoring, receipt logic, World Lens math, Evidence Lab calculations, telemetry, storage, certification, enforcement, or authority behavior.

## Interpretation

This patch does not claim the legacy test tree passes. It says the opposite clearly: legacy tests are inventory until restored, archived, or deleted through explicit triage.
