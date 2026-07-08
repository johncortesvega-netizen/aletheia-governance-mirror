# Patch 233 Recovery Note

If the app fails after this patch, restore `app.py` from Patch 232 and remove `ui/components/receipt_blocks.py`.

This patch is visual-only. Receipt payload generation remains in `core.witness` and existing app code.
