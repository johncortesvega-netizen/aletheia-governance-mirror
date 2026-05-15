# Patch 71.1 Recovery Note — Module Demo Label Isolation

Patch 71.1 is a narrow UI/demo-library correction after Patch 71.

## What changed

- `app.py` now defines separate demo maps for Mirror Check and Stress Test:
  - `MIRROR_CHECK_DEMO_SCENARIOS`
  - `STRESS_TEST_DEMO_SCENARIOS`
- Stress Test uses `Stress Test demo examples` and `Load Stress Test scenario demo`.
- Mirror Check uses `Mirror Check scenario demo examples` and `Load Mirror Check scenario demo`.
- The original `SCENARIOS` name remains as a backward-compatible alias to the Mirror Check demo map, but active module UI paths use module-specific maps.

## Recovery / rollback

If the UI behaves unexpectedly, restore `app.py` from the Patch 71 verified state and remove:

- `tests/test_patch_71_1_module_demo_label_isolation.py`
- `PATCH_71_1_MANIFEST.txt`
- `PATCH_71_1_RECOVERY_NOTE.md`

Then rerun:

```bat
tools\run_patch_checks.bat 71
```

## Boundary

This patch does not change scoring, receipts, tree visuals, batch catalog behavior, storage, authority boundaries, public ledger behavior, Global ID sync, or central storage. Human review remains required.
