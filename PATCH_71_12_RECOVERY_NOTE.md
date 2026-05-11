# PATCH 71.12 RECOVERY NOTE - Mirror Check Review Band Row Render Fix

If Patch 71.12 must be reverted, restore these files from the last known working state after Patch 71.11:

- `app.py`
- `tests/test_patch_71_12_mirror_check_review_band_row_rendering.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 71.12 fixes the remaining THRESHOLD-specific HTML-rendering defect in the Mirror Check latest-reading card.

Cause:
- Patch 71.11 fixed the detail rows, including `Stress label`.
- The visual review-band line above the details was still created with an indented multiline HTML block.
- In THRESHOLD outputs, Streamlit Markdown could still render that block as literal code.

Fix:
- Build the THRESHOLD `review_band_line` as inline HTML.
- Remove the obsolete `review_band_detail_line` fragment from the render path.
- Preserve the Patch 71.11 inline detail rows and HTML escaping.

## What did not change

- No receipt schema changed.
- No scoring logic changed.
- No verdict-routing logic changed.
- No taxonomy changed.
- No tree visual changed.
- No Stress Test logic changed.
- No Boundary Cases changed.
- No World Lens changed.
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
tools\run_patch_checks.bat 71_12
```
