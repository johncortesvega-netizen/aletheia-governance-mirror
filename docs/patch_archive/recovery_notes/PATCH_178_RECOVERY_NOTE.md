# PATCH 178 Recovery Note

Patch 178 aligns AI static scan display/context with the primary Mirror Check / Stress Test receipt.

To recover:
1. Restore the files listed in `PATCH_178_MANIFEST.txt` from the previous patch state.
2. Re-run `python tools/run_patch_checks.py 178`.
3. Confirm that Receipt Reader still parses uploaded receipts and that AI static scan context remains subordinate to the primary receipt.

No scoring, taxonomy, World Lens, Evidence Lab, or protocol-engine behavior was intentionally changed.
