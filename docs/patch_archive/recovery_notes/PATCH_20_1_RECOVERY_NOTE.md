# ALETHEIA PATCH 20.1 RECOVERY NOTE

Patch: 20.1
Name: Batch Question Mode + TXT Upload
Type: Mirror Check batch-input guardrail / local receipt workflow

## Intent
- Let Mirror Check accept pasted lists or uploaded `.txt` files for batch review.
- Detect numbered question banks as `QUESTION_SET` so they are not collapsed into one governance proposal.
- Keep batch review separate from the single-result Pulse Tree.
- Produce one local witness receipt per item inside the existing batch `.zip` archive.

## Touched files
- app.py
- core/witness.py
- tests/test_patch_20_batch_witness_receipts.py
- tests/test_patch_20_1_batch_question_upload_mode.py
- PATCH_20_1_RECOVERY_NOTE.md

## Do not touch
- protocol.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/empirical.py
- verdict formulas
- witness hashing meaning
- Global ID / ledger behavior

## Expected behavior
- A 50-line numbered question list is split into 50 batch items.
- `.txt` uploads can be used as batch input.
- Question banks are labeled `QUESTION_SET` in the batch index.
- Batch review downloads a `.zip` with `batch_index.txt`, `batch_index.json`, and one receipt pair per item.
- Single Mirror Check still works as before.

## Rollback
Revert the touched files to Patch 20.
