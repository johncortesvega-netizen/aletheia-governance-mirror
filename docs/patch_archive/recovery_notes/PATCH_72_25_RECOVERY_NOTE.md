# PATCH 72.25 RECOVERY NOTE - World Lens Receipt Table Completion

If Patch 72.25 must be reverted, restore these files from the last known working state after Patch 72.24:

- `app.py`
- `tests/test_patch_72_25_world_lens_receipt_table_completion.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.25 completes the public display guard from Patch 72.24.

Patch 72.24 renamed many World Lens table columns to `internal_taxonomy_label`, but the display helper still mainly detected `verdict`-style source columns. That meant some receipt tables had the raw internal taxonomy label but not the display fields.

Patch 72.25 fixes that by treating these as taxonomy source columns:

- `internal_taxonomy_label`
- `raw_aletheia_verdict`
- `raw_verdict`
- `aletheia_verdict`
- `verdict`

It also sanitizes remaining `THRESHOLD · THRESHOLD evidence pattern...` and `ASYLUM · ASYLUM evidence pattern...` final interpretation strings.

## What did not change

- No scoring formula changed.
- No verdict-routing logic changed.
- No 9k allocation formula changed.
- No Evidence Lab data model changed.
- No World Lens data model changed.
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
tools\run_patch_checks.bat 72_25
```
