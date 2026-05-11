# PATCH 72.28 RECOVERY NOTE - Shared Copy Humility Polish

If Patch 72.28 must be reverted, restore these files from the last known working state after Patch 72.27:

- `app.py`
- `core/empirical.py`
- `core_empirical.py`
- `tests/test_patch_72_28_shared_copy_polish.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.28 is a copy-only humility polish. It applies the small backlog collected during screenshot review:

- Mirror Check:
  - `Near Sanctuary` becomes `Near low-risk boundary`.
  - `Questions before trusting this model` becomes `Questions before relying on this reading`.
  - legacy `Protocol audit result` and `final label` wording is guarded against.

- Shared state details:
  - `Selected country / scenario` becomes `Selected case / scenario`.
  - `Grid basis` becomes `Evidence basis`.

- Evidence Lab:
  - method note uses internal authority-boundary review wording.
  - schema help removes duplicated `population` from helpful empirical columns.
  - source mapping uses CPI-style/corruption-capture wording more carefully.
  - disclaimer says `enforcement authority`.

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
tools\run_patch_checks.bat 72_28
```
