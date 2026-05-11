# PATCH 71.11 RECOVERY NOTE - Mirror Check Stress Label Row Render Fix

If Patch 71.11 must be reverted, restore these files from the last known working state after Patch 71.10:

- `app.py`
- `tests/test_patch_71_11_mirror_check_stress_label_row_rendering.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 71.11 fixes the last visible HTML-rendering defect in the Mirror Check latest-reading card.

Cause:
- Patch 71.10 removed the main raw-HTML/code regression, but the final `Stress label` line could still be interpreted as Markdown/code because it was emitted as a separate indented line inside the card detail block.
- The result was a visible literal fragment such as `<strong>Stress label:</strong> MEI7 Ethics Gate / Asylum` in the UI.

Fix:
- Keep the `judgment_card_html` + `textwrap.dedent(...).strip()` render path from Patch 71.10.
- Build the card detail rows as inline `<div>` HTML strings joined into `detail_rows_html`.
- Render the detail rows on one inline HTML line inside the outer detail container.
- Escape dynamic display values before inserting them into `unsafe_allow_html=True` content.

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
tools\run_patch_checks.bat 71_11
```
