# Patch 156 Recovery Note — Mirror Check Page Polish

If this patch needs to be rolled back, restore `app.py` to the previous Mirror Check intro copy and remove `tests/test_patch_156_mirror_check_page_polish.py` plus the Patch 156 manifest/recovery/delete-list files.

The patch is intentionally UI/copy/layout only. It does not alter scoring, routing, receipts, protocol logic, uploads, batch behavior, telemetry, storage, certification, enforcement, or final authority behavior.
