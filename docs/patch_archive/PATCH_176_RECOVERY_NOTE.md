# PATCH 176 Recovery Note

## Summary
Patch 176 adds a plain-English summary layer to Receipt Reader. It changes presentation tone only. Receipt values, parsing, scoring, taxonomy, receipt schema, World Lens, Evidence Lab, and protocol logic are not changed.

## Recovery steps
1. Restore `ui/receipt_reader.py` from the pre-Patch-176 state if the plain-English summary tone needs to be reverted.
2. Remove `tests/test_patch_176_receipt_reader_plain_language_tone.py` if reverting the patch.
3. Re-run `python tools/run_patch_checks.py 175` to confirm the previous Receipt Reader AI static scan context support remains intact.

## Notes
- The new summary explicitly says the computer does not decide, does not give official permission, and does not prove final safety/truth.
- The values shown in the summary are copied from the uploaded receipt and are not changed or rescored.
- Human review remains required.
