# Patch 73.1 Recovery Note — Scope Copy Trim / UI Minimalism

If Patch 73.1 needs to be reverted, restore the previous versions of:

- `app.py`
- `about_page.py`
- `tests/test_patch_73_1_scope_copy_trim.py`
- `PATCH_73_1_MANIFEST.txt`
- `PATCH_73_1_RECOVERY_NOTE.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 73.1 trims first-view UI weight after Patch 73 by collapsing the Scope Layers expander by default in both the integrated app About tab and standalone About page.

The scope wording remains present and reviewable:

- Current operational layer: corruption-pattern / governance-risk mirror for human review.
- Research layer: benchmarks, mappings, tests, validation, and documentation.
- Vision layer: incorruptible-system framing as theoretical horizon.
- Out-of-scope layer: no governance, enforcement, authority allocation, real 9k body, mandate, spiritual/political validation, or replacement of human judgment.

## What did not change

- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model change.
- No authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

## Validation

Run:

```bat
tools\run_patch_checks.bat 73_1
```
