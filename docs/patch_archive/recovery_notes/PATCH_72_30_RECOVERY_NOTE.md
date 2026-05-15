# PATCH 72.30 RECOVERY NOTE - Protocol Guide Copy Humility Polish

If Patch 72.30 must be reverted, restore these files from the last known working state after Patch 72.29:

- `app.py`
- `tests/test_patch_72_30_protocol_guide_copy_humility_polish.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.30 gives Protocol Guide the same copy/humility treatment as the other modules.

It changes public-facing Protocol Guide language so labels remain raw/internal taxonomy, not final safety or authority claims.

Main copy changes:

- Protocol Guide identity now uses ALETHEIA v1.0 — Governance Mirror.
- Internal taxonomy labels replace the old Sanctuary / Threshold / Asylum labels heading.
- SANCTUARY is explicitly described as a raw/internal compatibility label for a low-risk internal reading.
- World Lens replaces old Global Grid public wording.
- 9k is described as a human anti-tyranny scaffold / threshold steward, not a sovereign body, mandate, Sanctuary, or final legitimacy.

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
tools\run_patch_checks.bat 72_30
```
