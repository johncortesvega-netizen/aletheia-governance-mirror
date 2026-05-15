# PATCH 146.1 RECOVERY NOTE — Unit Preview GitHub Link + AI Audit Evidence Availability

If this patch needs to be reverted, restore `ui/unit_preview.py` to the Patch 146 version and remove the `docs/for-reviewers/ai_audit_loop_evidence*` additions plus `tests/test_patch_146_1_unit_preview_github_audit_evidence.py`.

This patch is presentation/documentation only. It restores a small GitHub link in Aletheia Unit Preview and makes the human-reviewed AI audit-loop screenshots available in a collapsed proof-of-concept section.

The audit-loop evidence remains bounded:

```text
external AI output -> ALETHEIA mirror reading -> human review
```

The screenshots and notes are not official verdicts, certifications, legal findings, or final proof. They are reviewer-readiness evidence for the mirror process.

No scoring, routing, receipt schema/generation, World Lens math, AI Integrity scan behavior, Privacy Audit behavior, Stress Test behavior, Mirror Check behavior, upload/download behavior, external calls, telemetry, analytics, database/storage, Global ID sync, public ledger sync, certification, approval, rejection, enforcement, legal authority, official authority, security/privacy guarantee, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 146_1
python tools\run_patch_checks.py 146
python tools\run_patch_checks.py 145
python tools\run_protocol_baseline_self_audit.py
```
