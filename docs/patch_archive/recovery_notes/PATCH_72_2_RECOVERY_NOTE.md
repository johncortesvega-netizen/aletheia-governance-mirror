# PATCH 72.2 RECOVERY NOTE - Mirror Check Input Change Reset

If Patch 72.2 must be reverted, restore these files from the last known working state after Patch 72.1 Hotfix:

- `app.py`
- `tests/test_patch_72_2_mirror_check_input_change_reset.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.2 fixes a Mirror Check UI-state issue: after creating/downloading a receipt for one scenario, editing the input could leave the old assessment active and make the receipt flow appear to continue without a new explicit review.

The fix:
- hashes the current Mirror Check text as an active input signature
- stores that signature only after `Review idea` is clicked
- compares the visible input against the last reviewed input before rendering the latest reading/receipt
- closes the previous assessment for the current draft when the input changes

## What did not change

- No scoring logic changed.
- No verdict-routing logic changed.
- No receipt schema changed.
- No Threshold Mapping logic changed.
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
tools\run_patch_checks.bat 72_2
```
