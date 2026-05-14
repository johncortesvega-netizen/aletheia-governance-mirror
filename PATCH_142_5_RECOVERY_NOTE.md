# Patch 142.5 Recovery Note — Receipt Reader Batch ZIP Receipt Selection Fix

Patch 142.5 is a small Receipt Reader batch-ZIP parsing hotfix.

If it must be reverted, restore `ui/receipt_reader.py` to the Patch 142.4 version and remove `tests/test_patch_142_5_receipt_reader_batch_zip_receipt_selection.py`, `PATCH_142_5_MANIFEST.txt`, and this recovery note.

Expected pre-revert symptom: uploading a Stress Test batch receipt ZIP shows `Inspect first receipt: batch_index.txt`, and Standard View reports missing metrics because the index file is being treated as a receipt.

Expected post-patch behavior: uploading a batch receipt ZIP summarizes actual receipts and inspects `receipt_01.json` or `receipt_01.txt`, not `batch_index.txt`.

Boundary reminder: this patch only changes uploaded batch ZIP receipt selection/parsing in Receipt Reader. It does not rescore, merge verdicts, generate receipts, alter scoring logic, alter Stress Test behavior, call external services, store data, or claim certification/final truth.
