# PATCH 71.6 RECOVERY NOTE — Tree Central Glow Removal

If Patch 71.6 must be reverted, restore these files from the last known working state after Patch 71.5:

- `app.py`
- `tests/test_patch_71_6_tree_central_glow_removal.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 71.6 removes the large central glow/blob behind the tree canopy in `render_pulse_tree`.

This is a visual-only cleanup:

- canopy leaves remain;
- trunk and branches remain;
- fallen leaves remain;
- caption remains below the visual;
- state color remains tied to the protocol-adjusted state.

## What did not change

- No scoring logic changed.
- No receipt logic changed.
- No Stress Test verdict logic changed.
- No Mirror Check logic changed.
- No Boundary Cases logic changed.
- No World Lens logic changed.
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
tools\run_patch_checks.bat 71_6
```

Then optionally:

```bat
tools\run_checks.bat
```
