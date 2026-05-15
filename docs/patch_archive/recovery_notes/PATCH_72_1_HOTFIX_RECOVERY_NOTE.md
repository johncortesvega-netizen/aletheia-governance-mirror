# PATCH 72.1 HOTFIX RECOVERY NOTE - Threshold Mapping Card Summary

If this hotfix must be reverted, restore these files from the last known working state after Patch 72.1:

- `app.py`
- `tests/test_patch_72_1_hotfix_threshold_mapping_card_summary.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.1 added an expandable Threshold mapping preview, but user review showed it was not visible in the expected place in the live app.

This hotfix makes the mapping immediately visible by adding a compact line to the main Mirror Check judgment card:

- Threshold mapping direction
- Z-axis
- Repair index

The full expandable preview remains below the metrics.

## What did not change

- No canonical taxonomy changed.
- No scoring logic changed.
- No verdict-routing logic changed.
- No receipt schema changed.
- No tree visual changed.
- No Stress Test logic changed.
- No Boundary Cases changed.
- No World Lens changed.
- No authority-boundary logic changed.

ALETHEIA remains:

- Authority claim: `False`
- Human review required: `True`
- Public ledger: `False`
- Global ID sync: `False`
- Central storage: `False`
- Dataflow boundary: `Power -> Mirror. Never Mirror -> Power.`

## Validation

Run:

```bat
tools\run_patch_checks.bat 72_1_hotfix
```
