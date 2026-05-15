# PATCH 22.2 RECOVERY NOTE

Patch: 22.2
Name: Calibrated Metrics UI Wording
Type: UI wording / receipt-language cleanup

Intent:
- Stop calling ethics-calibrated Mirror Check metrics "raw" in the UI.
- Preserve the raw pre-ethics values in local witness receipts.
- Keep scoring, ethics, protocol verdicts, witness hashing, batch logic, and Global Grid behavior unchanged.

Touched files:
- app.py
- protocol.py
- tests/test_patch_22_2_calibrated_metrics_wording.py
- PATCH_22_2_RECOVERY_NOTE.md

Do not touch:
- core/ethics.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/witness.py
- core/empirical.py
- verdict formulas
- witness hash mechanics
- batch UI / batch classification
- Global ID / public ledger behavior

Expected behavior:
- Mirror Check metric card reads "Integrity", not "Raw simulation integrity".
- The friction metric reads "Friction", not "Protocol friction".
- The protocol summary says "Integrity reading", not "Raw simulation integrity".
- A caption tells the user that raw pre-ethics values remain in the local witness receipt.

Rollback:
- Revert app.py and protocol.py to Patch 22.1.
- Remove this test file and recovery note.

Validation:
- python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py core/ethics.py
- python -m pytest tests -q
