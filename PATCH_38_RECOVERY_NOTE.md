# Patch 38 — Mechanism-vs-Claim Scanner

## Summary

Added the Mechanism-vs-Claim Scanner to help ALETHEIA distinguish ethical value language from concrete operational safeguards.

## Added

- `docs/mechanism_vs_claim_scanner.md`
- `prompts/mechanism_vs_claim_prompt.md`
- `tests/test_patch_38_mechanism_vs_claim.py`
- `PATCH_38_MANIFEST.txt`
- `PATCH_38_RECOVERY_NOTE.md`

## Updated

- `app.py`
- `about_page.py`
- `README.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## Design Rule

Mechanisms outweigh adjectives.

ALETHEIA may flag performative ethics, missing safeguards, and mechanism gaps for human review. It must not infer bad faith, assign final guilt, or replace human judgment.

## Check

```bat
tools\run_patch_checks.bat 38
```

## Safe-language guardrail

No command authority, no enforcement, no leader removal, no spiritual validation, no final intent claim.
