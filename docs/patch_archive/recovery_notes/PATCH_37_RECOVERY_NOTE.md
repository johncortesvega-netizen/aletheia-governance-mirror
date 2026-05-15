# Patch 37 — Consent-Audit Engine

## Status
Current patch.

## Purpose
Add a public-safe consent integrity layer to ALETHEIA v0.1 so the app can distinguish genuine consent from apparent consent under pressure.

## Added / changed

- `docs/consent_audit_engine.md`
- `prompts/consent_audit_prompt.md`
- `tests/test_patch_37_consent_audit.py`
- `PATCH_37_MANIFEST.txt`
- `PATCH_37_RECOVERY_NOTE.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `README.md`
- `about_page.py`
- `app.py`

## Safe-language boundaries

ALETHEIA may say:

- Consent pressure detected.
- Consent integrity is unclear.
- Refusal may not be realistically possible.
- Human review required before treating this as valid consent.
- Add an alternative path, withdrawal right, appeal, and non-retaliation rule.

ALETHEIA must not say:

- This consent is legally invalid.
- The AI has voided the agreement.
- This person is guilty.
- Human review is unnecessary.

## Recovery

If this patch causes issues, remove the Consent-Audit section from the Boundary Cases tab and keep the standalone docs/prompts for later reintegration.

## Checks

Run:

```bat
tools\run_patch_checks.bat 37
```
