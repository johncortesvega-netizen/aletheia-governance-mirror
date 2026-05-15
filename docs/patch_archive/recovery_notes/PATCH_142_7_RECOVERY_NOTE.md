# Patch 142.7 Recovery Note — Receipt Reader World Lens ZIP Selection Fix

If Patch 142.7 needs to be reverted, restore `ui/receipt_reader.py` to the Patch 142.6 version and remove `tests/test_patch_142_7_receipt_reader_world_lens_zip_selection.py` plus this patch's manifest/recovery files.

This patch only changes Receipt Reader ZIP classification for uploaded receipt files. It prevents World Lens `*_summary.json` / index-style files from being used as the inspected representative receipt and prefers the actual World Lens receipt document instead.

No scoring, World Lens math, verdict routing, receipt generation, module engine behavior, AI Integrity behavior, Privacy Audit behavior, Stress Test behavior, telemetry/storage behavior, external calls, or authority boundaries are changed. Human review remains required.
