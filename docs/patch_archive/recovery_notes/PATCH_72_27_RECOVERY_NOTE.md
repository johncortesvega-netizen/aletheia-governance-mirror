# PATCH 72.27 RECOVERY NOTE - Mirror Stress Live UI Taxonomy Guard

If Patch 72.27 must be reverted, restore these files from the last known working state after Patch 72.26:

- `app.py`
- `tests/test_patch_72_27_mirror_stress_live_ui_taxonomy_guard.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.27 applies the live UI humility/taxonomy display guard to Mirror Check, Stress Test, and Audit self-check UI.

Patches 72.24–72.26 focused on World Lens. The screenshots showed the same issue in Mirror/Stress/Audit:

```text
verdict = SANCTUARY
verdict = ASYLUM
Result state = SANCTUARY
```

Patch 72.27 keeps the raw/internal taxonomy for receipts and traceability, but visible UI cards/tables now show public display labels first:

```text
Low-risk internal reading
Review / threshold reading
High-risk internal reading
```

with internal taxonomy labels and humility notes present as context.

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
tools\run_patch_checks.bat 72_27
```
