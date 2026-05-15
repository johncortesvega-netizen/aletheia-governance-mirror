# PATCH 72.9 RECOVERY NOTE - Evidence Lab Build/Explorer State Guard

If Patch 72.9 must be reverted, restore these files from the last known working state after Patch 72.8:

- `app.py`
- `tests/test_patch_72_9_evidence_lab_state_guard.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.9 addresses Evidence Lab rerun/state behavior.

Streamlit reruns the script when the user clicks a download button or changes a country/year widget. That is normal. Patch 72.9 prevents that rerun from re-scoring the same active uploaded/generated master when the active source table has not changed.

The active Evidence Lab table is now keyed by a stable signature. When the signature matches, ALETHEIA uses the session-state scored table instead of running the full variable-mapping/scoring step again.

## What did not change

- No scoring formula changed.
- No verdict-routing logic changed.
- No 9k allocation formula changed.
- No World Lens logic changed.
- No receipt schema changed.
- No Evidence Lab data model changed.
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
tools\run_patch_checks.bat 72_9
```
