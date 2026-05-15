# Patch 142.1 Recovery Note - Receipt Reader Parser Calibration

Patch 142.1 is a small Receipt Reader parser/UI calibration patch.

If rollback is needed, restore the previous versions of:

- `ui/receipt_reader.py`
- `tests/test_patch_142_1_receipt_reader_parser_calibration.py`
- `PATCH_142_1_MANIFEST.txt`
- `PATCH_142_1_RECOVERY_NOTE.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_index.md`
- `docs/architecture.md`
- `data/protocol_baseline_manifest.json`

Expected behavior after the patch:

- Receipt Reader remains upload-only.
- Uploaded `.txt`, `.md`, or `.json` ALETHEIA receipts are read locally in the session.
- The parser prefers `MACHINE-READABLE RECEIPT JSON` when present.
- Text fallback accepts `Risk:` and `Trust index:`.
- Repair questions come only from JSON `repair_questions` or `SILENT OPERATOR REPAIR QUESTIONS`.
- Component readings such as `Power balance: Threshold +` are not displayed as repair questions.
- Values are displayed as a compact vertical list.

Boundary check:

This patch does not rescore, reroute verdicts, infer missing values, generate receipts, override uploaded receipt values, alter receipt schemas, change AI Integrity scan behavior, change Privacy Audit scan behavior, change World Lens math, call external services, use live model calls, use embeddings, create telemetry, create analytics, create storage, certify, approve, reject, enforce, or claim final truth. Human review remains required.
