# Patch 41 — Local Witness Receipt v2

## Status
Applied as a local-first receipt hardening patch.

## What changed

- Added `docs/local_witness_receipt.md`.
- Added `prompts/local_witness_receipt_prompt.md`.
- Hardened `core/witness.py` receipts with:
  - `receipt_version: local-witness-v2`
  - document fingerprint
  - processed document fingerprint
  - report fingerprint
  - audit receipt fingerprint
  - app/rubric/prompt versions
  - active modules
  - explicit authority boundary
- Added a Local Witness Receipt v2 UI template in `app.py`.
- Added an About-page explanation.
- Updated README, patch status, and progress database.

## Safety boundaries

No public ledger.
No Global ID sync.
No central storage.
No authority claim.
No enforcement.
Human review remains required.

## Check command

```bat
tools\run_patch_checks.bat 41
```
