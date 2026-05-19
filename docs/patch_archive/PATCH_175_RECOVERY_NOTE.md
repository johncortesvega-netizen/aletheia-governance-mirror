# PATCH 175 Recovery Note

## Summary
Patch 175 updates Receipt Reader - Standard View so uploaded Mirror Check and Stress Test receipts can expose the new AI STATIC SCAN CONTEXT section as subordinate context. It does not rescore receipts and does not restore the removed standalone AI Integrity module.

## Recovery steps
1. Restore `ui/receipt_reader.py` from the pre-Patch 175 state if Receipt Reader parsing needs to be reverted.
2. Remove `tests/test_patch_175_receipt_reader_ai_static_scan_context.py` if rolling the patch back completely.
3. Re-run `python tools/run_patch_checks.py 174` to confirm the prior state still passes.

## Notes
- The parser intentionally honors explicit primary modules such as Mirror Check and Simulation before scanning full receipt text.
- AI static scan labels inside the subordinate section must not turn the receipt into an AI Integrity receipt.
- Human review remains required.
