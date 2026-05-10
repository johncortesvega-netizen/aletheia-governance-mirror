# PATCH 22.1 — Ethics-Calibrated Receipt Metrics

Purpose:
- Make Mirror Check receipts visibly reflect ethics-to-scoring calibration.
- Apply ethics-adjusted integrity when the ethics layer finds a meaningful integrity gap.
- Preserve raw pre-ethics metrics for review.
- Add an explicit ETHICS ADJUSTMENT block to local witness receipts.

Touched:
- core/ethics.py
- core/witness.py
- tests/test_patch_22_1_ethics_calibrated_receipts.py

Not touched:
- app.py
- protocol.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/empirical.py
- batch UI
- witness hash boundary behavior
- Global ID / ledger behavior

Recovery:
- Revert this patch if visible metrics become too conservative.
- Raw metrics remain preserved in receipts for comparison.

Validation:
- python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py core/ethics.py
- python -m pytest tests -q
