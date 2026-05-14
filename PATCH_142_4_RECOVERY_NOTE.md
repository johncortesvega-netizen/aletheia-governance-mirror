# Patch 142.4 Recovery Note — Receipt Reader Narrative Standard View Output

If this patch causes display problems, restore `ui/receipt_reader.py` from the previous working version and remove `tests/test_patch_142_4_receipt_reader_narrative_output.py`.

This patch is presentation/parsing-only. It does not change ALETHEIA scoring, verdict routing, taxonomy, receipt schemas, receipt generation, signal weights, module engines, World Lens math, AI Integrity behavior, Privacy Audit behavior, telemetry/storage behavior, or authority boundaries.

Receipt Reader remains a verbal support utility for uploaded receipts. It reads and translates receipt values; it does not rescore, certify, approve, reject, enforce, override, or create a new receipt.
