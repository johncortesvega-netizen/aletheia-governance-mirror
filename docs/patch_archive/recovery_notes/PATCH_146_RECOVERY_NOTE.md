# Patch 146 Recovery Note — Unit Preview Receipt Route + World Lens Context Copy

Patch 146 is a UI/copy clarity patch.

## Recovery

If the patch needs to be reverted, restore:

- `app.py`
- `ui/unit_preview.py`
- `tests/test_patch_146_unit_preview_receipt_route_world_lens_context.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_index.md`
- `data/protocol_baseline_manifest.json`

from the pre-patch 146 project state.

## Intended behavior

- Unit Preview no longer labels its active text area as accepting receipts.
- Unit Preview may still detect receipt-like text and suggest Receipt Reader.
- Receipt Reader remains the upload-only utility that reads receipts.
- World Lens uses an optional context note, a broad review-pressure lens, and bounded context reflection copy.
- World Lens context controls do not alter evidence data, math, allocation, receipts, scoring, or verdict routing.

## Non-authority boundary

This patch does not add certification, enforcement, approval/rejection, legal authority, official authority, privacy guarantee, or final-truth claims.
