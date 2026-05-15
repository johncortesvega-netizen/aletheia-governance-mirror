# ALETHEIA Patch 20.5 — Batch Upload Empirical-Style Staging

Purpose:
- Make Batch Testing handle .txt uploads like Evidence Lab: stage the file first, process only after the explicit Run Batch Testing button.
- Stop the uploader from writing into the editable textarea state.
- Keep Batch Testing separate from the one-idea Mirror Check tree scanner.

Touched:
- app.py
- tests/test_patch_20_4_batch_upload_state_fix.py
- tests/test_patch_20_5_batch_empirical_style_staging.py

Not touched:
- protocol.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/witness.py
- core/empirical.py
- verdict logic
- witness hashing logic
- Global Grid logic

Expected behavior:
- The right-side Batch Testing panel offers two sources: Upload .txt or Paste list.
- Uploaded .txt files are previewed, not copied into the editable text area key.
- Run Batch Testing remains clickable when a valid uploaded file or pasted list yields 1–50 parsed items.
- Batch output remains a local .zip with one receipt per item.

Rollback:
- Revert app.py and these tests to Patch 20.4.
