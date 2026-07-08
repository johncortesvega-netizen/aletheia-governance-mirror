# Patch 208 Recovery Note — Stress Test Demo Semantic Alignment

If this patch causes unexpected Stress Test display behavior, revert:

- `app.py`
- `core/semantic_pressure_scanner.py`

The patch changes only Stress Test semantic source selection and scanner calibration for demo-related weak-safeguard patterns. It does not alter Stress Test scoring, receipts, storage, telemetry, or enforcement behavior.

Expected quick checks:

```bat
python -m py_compile app.py core\semantic_pressure_scanner.py
```

Expected semantic behavior:

- Emergency powers without expiry: THRESHOLD
- Biometric access to basic services without fallback: THRESHOLD
- Algorithmic welfare triage lacking explainability/challenge/override: THRESHOLD
- Public procurement under capture risk: THRESHOLD
- Crisis migration queue with safeguards: SANCTUARY / no strong pressure
- Local resource allocation with repair paths: SANCTUARY / no strong pressure
```
