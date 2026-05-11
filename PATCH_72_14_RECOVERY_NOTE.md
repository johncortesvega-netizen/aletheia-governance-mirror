# PATCH 72.14 RECOVERY NOTE - World Lens Value Guard Fallback

If Patch 72.14 must be reverted, restore these files from the last known working state after Patch 72.13:

- `app.py`
- `tests/test_patch_72_14_world_lens_value_guard_fallback.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.14 fixes the World Lens crash:

```text
NameError: selected_year_value_guard
```

World Lens now uses a safe callable lookup for the selected-year value guard. If the imported helper is unavailable in an older/partial deployment, the app uses a local diagnostic fallback instead of crashing.

The fallback verifies selected-year rows and seat totals only. It does not change scoring, verdicts, allocation, or authority boundaries.

## What did not change

- No scoring formula changed.
- No verdict-routing logic changed.
- No 9k allocation formula changed.
- No Evidence Lab data model changed.
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
tools\run_patch_checks.bat 72_14
```
