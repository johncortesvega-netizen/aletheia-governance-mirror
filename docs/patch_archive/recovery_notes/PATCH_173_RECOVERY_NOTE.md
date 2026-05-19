# PATCH 173 Recovery Note

## Summary
Patch 173 connects the AI static scan to Mirror Check and Stress Test as a subordinate context layer. It adds optional receipt/UI context only; it does not change the main taxonomy, World Lens, Evidence Lab, protocol engine, or receipt authority boundary.

## Recovery steps
1. Restore the files listed in `PATCH_173_MANIFEST.txt` from the pre-patch state to remove the integration.
2. Re-run `python tools/run_patch_checks.py 173` after any adjustment.
3. If receipt output is disputed, compare receipts with and without `ai_static_scan_context`; the context is informational and subordinate to the primary module reading.

## Notes
- AI static scan findings are not certification, enforcement, or final AI integrity verdicts.
- Mirror Check / Stress Test remains the primary ALETHEIA protocol path.
- Human review remains required.
