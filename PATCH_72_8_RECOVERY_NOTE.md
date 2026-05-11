# PATCH 72.8 RECOVERY NOTE - Stress Batch Input Reset and Protocol Capture Risk Presentation

If Patch 72.8 must be reverted, restore these files from the last known working state after Patch 72.7:

- `app.py`
- `core/witness.py`
- `tests/test_patch_72_8_stress_batch_reset_and_capture_risk.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.8 fixes the Stress Test batch UI carry-over issue.

After running one batch, changing the uploaded/pasted batch input now closes the previous active batch result for the current draft. The app does not show the old result/download as current until the user explicitly clicks `Run Stress Batch` again.

Patch 72.8 also clarifies ASYLUM / High receipts:

- `Collapse risk` remains the raw simulation boolean.
- `Protocol capture risk` shows protocol/ethics high-risk pressure separately.
- This avoids the confusing presentation where ASYLUM / High appears next to `collapse_risk: False` without explanation.

## What did not change

- No scoring logic changed.
- No verdict-routing logic changed.
- No canonical taxonomy changed.
- No Threshold Mapping math changed.
- No tree visual changed.
- No Stress Test batch scoring changed.
- No Evidence Lab, Boundary Cases, or World Lens logic changed.
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
tools\run_patch_checks.bat 72_8
```
