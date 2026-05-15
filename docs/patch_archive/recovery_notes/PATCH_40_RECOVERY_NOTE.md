# Patch 40 — Evidence Lab + Extraordinary Claim Protocol

## Summary

Added a focused Evidence Lab hardening layer for evidence status levels, evidence gaps, and extraordinary-claim handling.

## Added / Updated

- `docs/evidence_lab.md`
- `prompts/evidence_lab_prompt.md`
- `tests/test_patch_40_evidence_lab.py`
- `README.md`
- `about_page.py`
- `app.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## Guardrails

- Extraordinary claims are treated as unverified unless supported by public, testable, non-coercive evidence.
- Personal meaning is not treated as policy authority.
- Evidence Lab audits consequences, evidence gaps, and safeguards.
- No spiritual validation, no AI authority claim, no removal of human review.

## Suggested check

```bat
tools\run_patch_checks.bat 40
```
