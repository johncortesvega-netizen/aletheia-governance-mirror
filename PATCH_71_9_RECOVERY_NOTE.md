# PATCH 71.9 RECOVERY NOTE — Mirror Check Review Band Display

If Patch 71.9 must be reverted, restore these files from the last known working state after Patch 71.8:

- `app.py`
- `tests/test_patch_71_9_mirror_check_review_band_display.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 71.9 applies the display-only Threshold review band to Mirror Check result cards.

Canonical taxonomy remains unchanged:

- `ASYLUM`
- `THRESHOLD`
- `SANCTUARY`

When Mirror Check is canonically `THRESHOLD`, the UI may now show one of:

- **Needs Repair**
- **Needs Review**
- **Near Sanctuary**

## What did not change

- No receipt schema changed.
- No scoring logic changed.
- No verdict-routing logic changed.
- No taxonomy changed.
- No tree visual changed.
- No Stress Test changed.
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
tools\run_patch_checks.bat 71_9
```
