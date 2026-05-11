# PATCH 72.15 RECOVERY NOTE - World Lens Year and Focus Guard

If Patch 72.15 must be reverted, restore these files from the last known working state after Patch 72.14:

- `app.py`
- `tests/test_patch_72_15_world_lens_year_focus_guard.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.15 fixes three World Lens UI/runtime issues:

1. The World Lens evidence-year selector no longer snaps back to the Evidence Lab synced year on every rerun after a user manually chooses another valid year.

2. The selected-year value guard now has a safe `focus_iso3` value before it runs, preventing:

```text
NameError: focus_iso3
```

3. Prototype region-bracket mode now defines its own heading before rendering the overview, preventing an undefined-heading crash.

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
tools\run_patch_checks.bat 72_15
```
