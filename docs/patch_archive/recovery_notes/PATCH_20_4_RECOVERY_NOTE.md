# PATCH 20.4 — Batch Upload State Fix

Purpose:
- Keep Batch Testing separate from the normal Mirror Check tree scanner.
- Fix the .txt upload flow so uploaded text is loaded into the batch text area once and the Run Batch Testing button remains active.
- Prevent the uploader from fighting the editable text area on Streamlit reruns.

Touched:
- app.py
- tests/test_patch_20_4_batch_upload_state_fix.py

Not touched:
- protocol.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/witness.py
- core/empirical.py
- verdict formulas
- witness hashing logic
- Global Grid logic

Expected behavior:
- Uploading a .txt file fills the Batch Testing text area.
- The user can still edit the uploaded text before review.
- Run Batch Testing stays enabled when parsed items exist.
- Uploading a new file clears stale batch results.
- Normal Mirror Check remains separate.

Rollback:
- Revert app.py to Patch 20.3.
- Remove this recovery note and the Patch 20.4 test file.
