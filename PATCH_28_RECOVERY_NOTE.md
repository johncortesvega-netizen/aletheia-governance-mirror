# PATCH 28 RECOVERY NOTE — Educational Decentralization Scoring

Type: lightweight scoring calibration.

Patch 28 wires Cognitive Resilience into review metrics with deliberately small, bounded adjustments.

## Added behavior

- High Cognitive Resilience + high educational decentralization + low central information capture can slightly stabilize visible metrics.
- Low Cognitive Resilience or high central information capture lightly lowers integrity and raises friction, trust friction, and collapse probability.
- High Cognitive Resilience never launders capture: no-audit, no-appeal, single-keyholder, surveillance, biometrics, contextual capture, or grip markers block positive stabilization.

## Files touched

- `core/cognitive_resilience.py`
- `app.py`
- `tests/test_patch_28_educational_decentralization_scoring.py`
- `PATCH_28_RECOVERY_NOTE.md`

## Hard boundaries preserved

Patch 28 does not add:

- global ID sync
- public ledger
- push-warning authority layer
- automatic enforcement
- centralized truth authority
- user/person classification as malicious

Cognitive Resilience remains a system property, not a judgment of people.

## Verification

Run from repo root on Windows cmd:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_28_educational_decentralization_scoring.py -q
```

Recommended combined check:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_27A_cognitive_resilience_calibration.py tests/test_patch_27B_cognitive_resilience_diagnostic.py tests/test_patch_28_educational_decentralization_scoring.py -q
```
