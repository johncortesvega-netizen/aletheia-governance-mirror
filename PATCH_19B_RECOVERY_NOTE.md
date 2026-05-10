# ALETHEIA PATCH 19B RECOVERY NOTE

Patch: 19B
Name: Mirror Check Recalibration
Type: Protocol calibration / receipt-question cleanup

## Intent

Use the Patch 19A calibration scenario pack to tighten Mirror Check behavior
without adding a new module.

## What changed

- Added explicit AI Sovereignty Capture markers for AI-only / no-human-input governance.
- Let clearly safeguarded public systems pass the ethics gate when appeal, audit, review, and sunset/final-human-decision safeguards are explicit.
- Returned OUT_OF_SCOPE for non-governance inputs instead of letting ethics fallback label them ASYLUM.
- Reworded repair questions so ASYLUM and THRESHOLD states are not called healthy.
- Passed protocol-level repair questions into Mirror Check local witness receipts.

## Touched files

- protocol.py
- app.py
- tests/test_mirror_check_calibration_scenarios.py
- tests/test_patch_19b_recalibration_contract.py
- PATCH_19B_RECOVERY_NOTE.md

## Not touched

- core/scoring.py
- core/simulation.py
- core/parser.py
- core/witness.py
- core/empirical.py
- scoring formulas
- witness hashing logic
- Global Grid logic
- public ledger / Global ID behavior

## Rollback

Revert the touched files above. Patch 19A can remain as a diagnostic scenario pack.

## Validation

```bash
python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py
python -m pytest tests -q
```
