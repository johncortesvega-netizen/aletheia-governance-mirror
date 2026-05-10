# ALETHEIA PATCH 20.2 RECOVERY NOTE

Patch: 20.2
Name: Separate Batch Testing UI
Type: UI workflow + local-only batch performance guard

## Intent
Keep batch review separate from the single Mirror Check / tree scanner flow.
Batch Testing should only open after the user clicks the Batch Testing button.
It should accept pasted text or `.txt` uploads, split up to 50 items, run local-only scans, and produce one ZIP containing all local witness receipts.

## Touched files
- app.py
- tests/test_patch_20_batch_witness_receipts.py
- tests/test_patch_20_2_separate_batch_testing_ui.py
- PATCH_20_2_RECOVERY_NOTE.md

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
- The normal Mirror Check remains a single-idea review path.
- Lists are no longer auto-converted into batch runs from the single Review idea button.
- Batch Testing appears only after clicking `Batch Testing — 50 phrases max`.
- Batch Testing supports pasted lists and `.txt` upload.
- Batch runs use the local deterministic path, not OpenAI / deep scan.
- Batch output stays local and downloads as one ZIP.

## Rollback
Revert app.py and remove this test file/recovery note. No protocol or scoring rollback should be needed.

## Validation
- python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py
- python -m pytest tests -q
