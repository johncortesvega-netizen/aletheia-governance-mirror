# PATCH 72.24 RECOVERY NOTE - World Lens Public Display Taxonomy Guard

If Patch 72.24 must be reverted, restore these files from the last known working state after Patch 72.23:

- `app.py`
- `tests/test_patch_72_24_world_lens_public_display_taxonomy_guard.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.24 centralizes public taxonomy display for World Lens.

Raw/internal taxonomy labels remain available for compatibility:

```text
SANCTUARY
THRESHOLD
ASYLUM
```

Public display tables now map them to:

```text
SANCTUARY -> Low-risk internal reading
THRESHOLD -> Review / threshold reading
ASYLUM -> High-risk internal reading
```

Tables also add `internal_taxonomy_label` and `humility_note` so reviewers can see the raw label without mistaking it for a final safety or authority claim.

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
tools\run_patch_checks.bat 72_24
```
