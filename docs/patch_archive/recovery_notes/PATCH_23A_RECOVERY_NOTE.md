# ALETHEIA Patch 23A — Scenario Calibration Pack

## Purpose
Add a human-reviewed Sydney Protocol calibration set before changing scoring formulas.
This patch is diagnostic only. It gives future patches a fixed test surface for
Sanctuary, Threshold, and Asylum behavior.

## Touched files
- `calibration/sydney_protocol_scenarios.py`
- `tests/test_patch_23a_scenario_calibration_pack.py`
- `PATCH_23A_RECOVERY_NOTE.md`

## Not touched
- `app.py`
- `protocol.py`
- `core/ethics.py`
- `core/scoring.py`
- `core/simulation.py`
- `core/parser.py`
- `core/witness.py`
- `core/empirical.py`
- verdict formulas
- witness hashing
- batch UI
- Global Grid logic

## Scenario labels
The pack contains 12 reviewed scenarios:
- 4 expected `SANCTUARY`
- 3 expected `THRESHOLD`
- 5 expected `ASYLUM`

It also includes two explicit variants:
- `SP-04B` community-review news layer
- `SP-10B` relinquish/handoff variant

## Diagnostic gap behavior
Current classifier mismatches are marked as `xfail` in the diagnostic test.
This prevents known calibration gaps from appearing as red build failures while
still documenting what later patches must improve.

## Recovery
If anything breaks, remove:
- `calibration/sydney_protocol_scenarios.py`
- `tests/test_patch_23a_scenario_calibration_pack.py`
- `PATCH_23A_RECOVERY_NOTE.md`

No production rollback should be needed.

## Validation
```bash
python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py core/ethics.py calibration/sydney_protocol_scenarios.py
PYTHONPATH=. pytest tests -q
```
