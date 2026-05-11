# PATCH 72.7 RECOVERY NOTE - Repair Capacity Mapping Guard

If Patch 72.7 must be reverted, restore these files from the last known working state after Patch 72.6:

- `core/witness.py`
- `protocol.py`
- `app.py`
- `tests/test_patch_72_7_repair_capacity_mapping_guard.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.7 fixes the Threshold Mapping interpretation issue found in Stress Test and Mirror Check receipts.

Generated repair questions are a route for human review. They are not proof that safeguards already exist.

The fix:
- adds `repair_question_index`
- adds `confirmed_repair_capacity`
- keeps `repair_index` aligned to confirmed repair capacity for display compatibility
- prevents ASYLUM component readings from presenting as `Threshold +`
- prints repair questions and confirmed repair capacity separately in receipts
- shows the same split in the UI
- neutralizes old repair-question and label wording

## What did not change

- No scoring logic changed.
- No verdict-routing logic changed.
- No canonical taxonomy changed.
- No receipt authority changed.
- No tree visual changed.
- No Stress Test batch structure changed.
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
tools\run_patch_checks.bat 72_7
```
