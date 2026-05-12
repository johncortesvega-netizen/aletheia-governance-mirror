# Patch 101 Recovery Note — Human-Auditable Protocol Baseline Self-Audit

If Patch 101 causes any issue, revert only the files listed in `PATCH_101_MANIFEST.txt`.

Patch 101 adds a local static baseline comparison layer and a go-live privacy-boundary statement. It does not change analyzer scoring, signal weights, verdict routing, receipt hashing, live model behavior, external calls, storage, enforcement, public ledger sync, Global ID sync, or central user-input storage.

The self-audit is intentionally human-auditable, not self-certifying. A matching baseline is review evidence only. A mismatch, missing file, or unknown watched file must be interpreted by a human reviewer before release.

Boundary reminders:
- Not tamper-proof.
- Not automated approval.
- Not a security guarantee.
- Not a privacy guarantee.
- Not certification.
- Not proof of safety.
- Not a hosting audit.
- Human review remains required.

Suggested recovery check after revert:

```bat
tools\run_patch_checks.bat 100
```
