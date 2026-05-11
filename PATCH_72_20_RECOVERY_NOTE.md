# PATCH 72.20 RECOVERY NOTE - Evidence Humility Helper Scope Fix

If Patch 72.20 must be reverted, restore these files from the last known working state after Patch 72.19:

- `app.py`
- `tests/test_patch_72_20_evidence_humility_helper_scope.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.19 placed `_empirical_humility_display_df(...)` too late in the file, inside a later World Lens scope. Evidence Lab called it before Python had defined it, causing:

```text
NameError: _empirical_humility_display_df
```

Patch 72.20 moves that helper into top-level app scope before Evidence Lab uses it.

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
tools\run_patch_checks.bat 72_20
```
