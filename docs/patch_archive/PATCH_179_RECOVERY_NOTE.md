# PATCH 179 Recovery Note

## Summary
Patch 179 is a receipt-formatting patch. It adds plain-English summary sections to exported local witness receipts, batch indexes, World Lens markdown receipts, and Evidence Lab receipt/review examples. It does not change values, scoring, schema fields, hashes, CSV exports, or protocol logic.

## Recovery steps
1. Restore the files listed in `PATCH_179_MANIFEST.txt` from the pre-patch state if the receipt formatting needs to be reverted.
2. Re-run `python tools/run_patch_checks.py 179`.
3. Open a Mirror Check or Stress Test receipt and confirm the machine-readable JSON remains present after the human-readable sections.
4. Open a batch ZIP and confirm each receipt remains present as `.txt` and `.json`, with `batch_index.txt` and `batch_index.json` still included.

## Notes
- Batch receipts were included intentionally because Mirror Check and Stress Test batch archives are review artifacts too.
- The batch index summary does not merge multiple readings into one verdict.
- Human review remains required.
