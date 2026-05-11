# PATCH 72.17 RECOVERY NOTE - World Lens Sanctuary Display Humility Guard

If Patch 72.17 must be reverted, restore these files from the last known working state after Patch 72.16:

- `app.py`
- `core/empirical.py`
- `core_empirical.py`
- `tests/test_patch_72_17_world_lens_sanctuary_display_humility_guard.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.17 aligns country-year evidence display with the Humility Protocol.

`SANCTUARY` remains an internal taxonomy label, but the UI no longer presents it as the primary final claim for a country-year row. High-integrity / low-collapse country-year rows now display as a low-risk internal reading with an explicit note that ALETHEIA does not claim final safety, final Sanctuary, or final authority.

Legacy uploaded scored masters that already contain the older `SANCTUARY evidence pattern` overlay text are rewritten in the UI display layer.

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
tools\run_patch_checks.bat 72_17
```
