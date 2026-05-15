# PATCH 71.7 RECOVERY NOTE — Threshold Review Band Display

If Patch 71.7 must be reverted, restore these files from the last known working state after Patch 71.6:

- `app.py`
- `tests/test_patch_71_7_threshold_review_band_display.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 71.7 adds a small display-only review band inside the canonical THRESHOLD state.

Canonical taxonomy remains unchanged:

- `ASYLUM`
- `THRESHOLD`
- `SANCTUARY`

When the canonical state is `THRESHOLD`, the UI can now show one of:

- **Needs Repair** — closer to Asylum, but still repairable.
- **Needs Review** — mixed or incomplete safeguards.
- **Near Sanctuary** — mostly stable, but not fully safe yet.

## What did not change

- No receipt schema changed.
- No scoring logic changed.
- No Stress Test verdict-routing logic changed.
- No Mirror Check logic changed.
- No tree visual changed.
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
tools\run_patch_checks.bat 71_7
```
