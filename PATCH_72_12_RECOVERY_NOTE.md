# PATCH 72.12 RECOVERY NOTE - Mascot Asset Refresh

If Patch 72.12 must be reverted, restore these files from the last known working state after Patch 72.11:

- `assets/aletheia_robot_laurel_logo.png`
- `tests/test_patch_72_12_mascot_asset_refresh.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.12 is a visual asset refresh only.

It keeps the Patch 72.11 mascot-logo wiring in place and swaps the underlying PNG asset for the updated Aletheia robot image with the leaf-based icon language.

The refreshed asset is stored at:

```text
assets/aletheia_robot_laurel_logo.png
```

## What did not change

- No scoring formula changed.
- No verdict-routing logic changed.
- No Evidence Lab logic changed.
- No Stress Test logic changed.
- No Mirror Check logic changed.
- No Boundary Cases logic changed.
- No World Lens logic changed.
- No receipt schema changed.
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
tools\run_patch_checks.bat 72_12
```
