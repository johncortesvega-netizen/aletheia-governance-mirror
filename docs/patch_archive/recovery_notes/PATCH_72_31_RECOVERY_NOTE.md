# PATCH 72.31 RECOVERY NOTE - Why ALETHEIA Copy Humility Polish

If Patch 72.31 must be reverted, restore these files from the last known working state after Patch 72.30:

- `app.py`
- `about_page.py`
- `tests/test_patch_72_31_why_aletheia_copy_humility_polish.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.31 gives Why ALETHEIA / About the same copy-humility treatment as the rest of the app.

It updates the page from older classification/V-axis/Grid/proof wording toward:

- review-oriented language
- raw/internal taxonomy label language
- World Lens instead of Global Grid
- Humility / Z-axis boundary instead of V-Axis Compass
- internal review readings instead of classifications
- no proof engine, oracle, final authority, or extraordinary-claim validation

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
tools\run_patch_checks.bat 72_31
```
