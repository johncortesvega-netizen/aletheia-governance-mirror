# PATCH 22 — Ethics-to-Scoring Calibration

## Intent
Make visible Mirror Check metrics reflect the contextual ethics layer added in Patch 21 and exposed in Patch 21.1.

## Scope
Touched files:
- `app.py`
- `core/ethics.py`
- `core/witness.py`
- `tests/test_patch_22_ethics_to_scoring_calibration.py`

## Behavior
- Contextual capture can lower visible integrity.
- Grip markers can raise visible ego pressure and collapse probability.
- Weak micro-sovereignty can add friction/trust friction.
- Raw pre-ethics metrics are preserved in local receipts for review.
- Protocol hard overrides still take precedence.

## Not touched
- `protocol.py`
- `core/scoring.py`
- `core/simulation.py`
- `core/parser.py`
- `core/empirical.py`
- Global Grid logic
- witness hashing mechanics beyond adding raw metrics to the receipt payload
- Global ID / ledger / external sync behavior

## Rollback
Revert the four touched files. No data migration is required.

## Validation
Run:

```bash
python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py core/ethics.py
python -m pytest tests -q
```
