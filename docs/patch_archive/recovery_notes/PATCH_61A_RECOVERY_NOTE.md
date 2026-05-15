# Patch 61A — Asylum Repair Questions

## Change

Added a high-risk repair-question guard so ASYLUM / High / Malicious Leadership
outputs cannot produce an empty Silent Operator repair-question block.

## Safety boundary

The patch only adds review questions. It does not add enforcement, authority,
leader removal, public ledger behavior, Global ID sync, or automatic action.
It keeps the output in a human review only posture.

## Check

```bat
tools\run_patch_checks.bat 61A
```
