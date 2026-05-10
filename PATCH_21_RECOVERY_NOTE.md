# PATCH 21 — Ethics Contextual Capture Detection

Purpose:
- Strengthen `core/ethics.py` so ethical scoring does not reward nice words when they are paired with mandatory power, enforcement, central grids, or no-appeal authority.
- Add a diagnostic `Micro Sovereignty` dimension for local, revocable, human-reviewable authority.
- Add explicit grip-marker handling for irrevocable, permanent, no-appeal, or no-human-review structures.

Touched:
- core/ethics.py
- tests/test_patch_21_ethics_contextual_capture.py
- PATCH_21_RECOVERY_NOTE.md

Not touched:
- app.py
- protocol.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/witness.py
- core/empirical.py
- verdict formulas
- witness hashing
- Global Grid logic

Expected behavior:
- Positive terms such as fairness, rights, safety, dignity, or care no longer produce an unqualified ethics boost when paired with enforcement or centralized mandatory control.
- Explicit grip markers push ethics toward high-risk review.
- Local, revocable, household/community, human-reviewable language increases the Micro Sovereignty signal.

Rollback:
- Restore the previous `core/ethics.py`.
- Remove this recovery note and the Patch 21 test file.

Validation:
- python -m py_compile app.py protocol.py core/ethics.py core/scoring.py core/parser.py core/witness.py core/empirical.py
- python -m pytest tests -q
