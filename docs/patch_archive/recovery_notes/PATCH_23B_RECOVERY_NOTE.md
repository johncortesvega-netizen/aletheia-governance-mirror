# ALETHEIA Patch 23B — Nonlinear Ego Penalty

## Intent
Make ego pressure behave like a tipping-point risk. A little ego pressure remains reviewable. High ego pressure now degrades integrity, raises friction, and raises collapse probability more sharply.

## Touched files
- `core/scoring.py`
- `tests/test_patch_23b_nonlinear_ego_penalty.py`
- `PATCH_23B_RECOVERY_NOTE.md`

## Not touched
- `app.py`
- `protocol.py`
- `core/ethics.py`
- `core/simulation.py`
- `core/parser.py`
- `core/witness.py`
- `core/empirical.py`
- witness hashing
- batch UI
- Global Grid logic
- Global ID / ledger behavior

## Behavior
- Adds `nonlinear_ego_penalty(ego_pressure)`.
- Uses a bounded `ego_pressure ** 1.5` curve in `compute_scores`.
- Uses the same nonlinear pressure in `collapse_probability` and `trust_friction`.
- Preserves protocol hard overrides as the stronger layer.

## Recovery
If behavior feels too harsh, revert only `core/scoring.py` and remove `tests/test_patch_23b_nonlinear_ego_penalty.py`. No UI or receipt rollback is needed.

## Validation
```bash
python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py core/ethics.py
PYTHONPATH=. pytest tests -q
```
