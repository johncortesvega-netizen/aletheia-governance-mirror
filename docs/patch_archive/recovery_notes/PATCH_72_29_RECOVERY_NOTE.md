# PATCH 72.29 RECOVERY NOTE - World Lens Copy Humility Polish

If Patch 72.29 must be reverted, restore these files from the last known working state after Patch 72.28:

- `app.py`
- `tests/test_patch_72_29_world_lens_copy_humility_polish.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.29 is a World Lens copy-only humility polish.

It updates remaining public-facing World Lens text that still sounded too much like verdict/final/report language:

- `verdict signal` becomes `internal taxonomy signal`.
- distribution messages refer to internal taxonomy distribution.
- report packet language becomes review packet language.
- simulation copy reinforces that final review remains human.
- receipt markdown uses World Lens source state and evidence allocation status.

## What did not change

- No scoring formula changed.
- No verdict-routing logic changed.
- No witness receipt schema changed.
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
tools\run_patch_checks.bat 72_29
```
