# PATCH 100 RECOVERY NOTE — Release Stabilization / Public Adoption Package

Patch 100 is a release-surface stabilization patch for **ALETHEIA v1.0 AI Integrity Preview**.

If rollback is needed, remove or revert only the files listed in `PATCH_100_MANIFEST.txt`.

No scoring math, verdict routing, signal patterns, signal weights, receipt schema, live model calls, external calls, repository crawling, storage layer, Global ID sync, public ledger sync, or enforcement behavior should have changed.

Expected verification:

```bat
tools\run_patch_checks.bat 100
tools\run_patch_checks.bat 99
tools\run_patch_checks.bat 98
```

Important boundary: ALETHEIA remains a mirror, not a throne. The AI Integrity Preview reflects static artifact-level signals for human review only. It does not certify models, certify code safety, guarantee privacy, guarantee security, approve vendors, prove truth, or replace legal, medical, political, religious, institutional, or human judgment.
