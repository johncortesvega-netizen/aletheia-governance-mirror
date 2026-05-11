# PATCH 71.5 RECOVERY NOTE — Boundary Cases Missing-Safeguard Cleanup

If Patch 71.5 must be reverted, restore these files from the last known working state after Patch 71.4:

- `app.py`
- `tests/test_patch_71_5_boundary_cases_missing_safeguards_cleanup.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 71.5 updates the Boundary Cases tab so it reflects the Stress Test changes from Patch 71.4.

Boundary Cases now includes explicit templates for:

- automated triage systems that lack explainability, independent challenge, and human override;
- biometric gates tied to food, housing, or medical access without fallback, public audit, or meaningful appeal;
- QUESTION_PROMPT as a review-tool/input mode, not a risk state.

Consent-Audit and Mechanism-vs-Claim templates now explicitly include:

- explainability;
- independent challenge;
- human override;
- fallback paths;
- public audit;
- meaningful appeal.

## Boundary preservation

This is a UI/template/documentation patch. It does not modify scoring, receipts, storage, authority, or enforcement.

ALETHEIA remains:

- Authority claim: `False`
- Human review required: `True`
- Public ledger: `False`
- Global ID sync: `False`
- Central storage: `False`
- Dataflow boundary: `Power -> Mirror. Never Mirror -> Power.`

## Validation

Run:

```bat
tools\run_patch_checks.bat 71_5
```

Then optionally:

```bat
tools\run_checks.bat
```
