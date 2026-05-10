# ALETHEIA PATCH 20 RECOVERY NOTE

Patch: 20
Name: Batch Witness Receipts
Type: Local receipt workflow / bounded batch UI

## Intent
Allow Mirror Check to review up to 50 pasted ideas in one batch and download one local ZIP archive containing every receipt plus a batch index.

## Touched files
- app.py
- core/witness.py
- tests/test_patch_20_batch_witness_receipts.py
- PATCH_20_RECOVERY_NOTE.md

## Do not touch
- protocol.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/empirical.py
- verdict logic
- scoring formulas
- capture markers
- public ledger / Global ID behavior

## Expected behavior
- Single Mirror Check still works.
- Batch input supports one phrase per line, numbered lists, or `---` separators.
- Batch review is capped at 50 items.
- Batch output is a local ZIP only.
- ZIP contains `batch_index.txt`, `batch_index.json`, and receipt text/json files for each item.
- No external sync, no public ledger, no authority handoff.

## Rollback
Remove the batch UI block in app.py, remove the new batch helper functions in core/witness.py, and delete this patch's test/recovery files.

## Validation
- python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py
- python -m pytest tests -q
