# PATCH 72.1 RECOVERY NOTE - Threshold Mapping UI Preview

If Patch 72.1 must be reverted, restore these files from the last known working state after Patch 72:

- `app.py`
- `core/witness.py`
- `tests/test_patch_72_1_threshold_mapping_ui_preview.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.1 surfaces the Patch 72 Threshold Mapping Layer in the live Mirror Check UI.

It adds:
- a public `build_threshold_mapping_layer(...)` helper in `core/witness.py`
- a `scan` argument to `render_chat_judgment(...)`
- an expandable **Threshold mapping preview** below the core metrics

The preview shows:
- Threshold direction
- Z-axis
- Repair index
- component readings
- Threshold - pressure signals
- Threshold + growth signals

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
tools\run_patch_checks.bat 72_1
```
