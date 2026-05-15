# PATCH 72.16 RECOVERY NOTE - World Lens Comparison Packet Summary Columns

If Patch 72.16 must be reverted, restore these files from the last known working state after Patch 72.15:

- `app.py`
- `tests/test_patch_72_16_world_lens_comparison_summary_columns.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.16 makes the selected-year comparison packet more audit-friendly.

The packet already contained enough row-level data to reconstruct most World Lens cards. This patch adds the visible selected-year overview and coverage values as explicit summary columns, including:

- countries scored
- selected-year seats
- weighted integrity/friction/collapse
- average empirical coverage
- raw trust survey coverage
- trust-prior fallback coverage
- WGI coverage
- V-Dem coverage
- missing raw trust/WGI/V-Dem rows
- trust-prior rows and missing trust-prior rows
- verdict seat totals

It also adds a note clarifying that trust-prior coverage is fallback/model continuity coverage, not observed raw survey coverage.

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
tools\run_patch_checks.bat 72_16
```
