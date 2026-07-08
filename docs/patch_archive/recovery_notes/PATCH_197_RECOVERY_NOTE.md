# Patch 197 Recovery Note — Opaque Capture Semantic Calibration

If this patch causes unexpected semantic scanner behavior, revert only:

- `core/semantic_pressure_scanner.py`

Then remove the Patch 197 block from `PATCH_STATUS.md` and delete the Patch 197 root artifacts.

This patch does not alter receipt schemas, module routing, World Lens math, Evidence Lab calculations, external calls, storage, telemetry, certification, enforcement, or final authority claims.

## Smoke checks

```bat
python -m py_compile core/semantic_pressure_scanner.py
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('a group of bankers have world power in secret').state)"
```

Expected first behavioral check: `THRESHOLD`.
