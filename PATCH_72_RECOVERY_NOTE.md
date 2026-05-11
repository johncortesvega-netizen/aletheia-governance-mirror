# PATCH 72 RECOVERY NOTE - Threshold Mapping Layer

If Patch 72 must be reverted, restore these files from the last known working state after Patch 71.12:

- `core/witness.py`
- `tests/test_patch_72_threshold_mapping_layer.py`
- `docs/threshold_mapping_layer.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72 adds a receipt-only Threshold Mapping Layer.

The layer makes THRESHOLD readings more legible by recording whether the reading is drifting toward ASYLUM, staying balanced, or growing toward SANCTUARY.

It includes:

- `threshold_direction`
- `z_axis_position`
- `integrity_gap`
- `repair_index`
- component readings for power balance, correction, and access
- Asylum pressure signals
- Sanctuary growth signals

## What did not change

- No canonical taxonomy changed.
- No scoring logic changed.
- No verdict-routing logic changed.
- No receipt authority changed.
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
tools\run_patch_checks.bat 72
```
