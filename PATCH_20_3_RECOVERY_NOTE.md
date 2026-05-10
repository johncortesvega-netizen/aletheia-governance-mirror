# ALETHEIA PATCH 20.3 RECOVERY NOTE

Patch: 20.3
Name: Side-by-Side Batch Testing Panel
Type: UI workflow separation

## Intent
Move Batch Testing into its own side panel next to the normal Mirror Check questionnaire.
The `.txt` upload must stay inside the Batch Testing panel only, not inside the normal tree scanner / one-idea review path.

## Touched files
- app.py
- tests/test_patch_20_3_side_by_side_batch_panel.py
- PATCH_20_3_RECOVERY_NOTE.md

## Do not touch
- protocol.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/witness.py
- core/empirical.py
- scoring formulas
- witness hashing logic
- Global Grid logic
- public ledger / Global ID behavior

## Expected behavior
- The left side remains the normal one-idea Mirror Check questionnaire.
- The right side contains Batch Testing.
- Batch Testing opens only after clicking `Batch Testing — 50 phrases max`.
- The `.txt` uploader appears only in the Batch Testing side panel.
- Batch review stays local-only and produces a ZIP with all receipts.
- The normal Review idea button never auto-converts a list into batch mode.

## Rollback
Revert app.py and remove this test file/recovery note. No protocol or scoring rollback should be needed.

## Validation
- python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py
- python -m pytest tests -q
