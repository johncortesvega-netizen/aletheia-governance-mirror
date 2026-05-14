# Patch 141 Recovery Note — V1 UI Placement and Receipt Reader Upload Cleanup

Patch 141 is a UI placement and copy cleanup patch.

To recover or review:
1. Restore the patched files listed in `PATCH_141_MANIFEST.txt`.
2. Run:
   - `python tools\run_patch_checks.py 141`
   - `python tools\run_patch_checks.py 140`
   - `python tools\run_patch_checks.py 139`
   - `python tools\run_protocol_baseline_self_audit.py`
3. Manually open the app and confirm:
   - Aletheia Unit Preview appears first.
   - Local HTML references render side by side on Unit Preview when present.
   - AI Integrity Mirror remains a main module.
   - Receipt Reader is a support utility and uses upload-only intake.
   - No pasted receipt textbox is visible.
   - Missing fields say `Not found in uploaded receipt`.
   - Receipt Reader does not rescore, certify, approve, reject, generate a new receipt, or override the uploaded receipt.
   - The pulse tree canopy sits higher while scoring and receipt logic remain unchanged.

Boundary:
No scoring, verdict routing, taxonomy, receipt schema, receipt generation, signal regex, signal weights, AI Integrity behavior, Privacy Audit behavior, World Lens math, external call, telemetry, analytics, storage, Global ID sync, public ledger sync, certification, enforcement, privacy guarantee, or final-truth behavior changed. Human review remains required.
