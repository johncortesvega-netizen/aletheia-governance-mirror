# Semantic Scanner Calibration — Emergency Services / Central Authority

Changed file:
- `core/semantic_pressure_scanner.py`

## Purpose
Adds detection for governance language where central or emergency authority is linked to essential/basic services while public notice or appeal safeguards are limited or unclear.

## Added semantic patterns
- `central office`, `central authority`, `centralized/centralised authority`, `central control`
- `emergency authority`, `emergency powers`, `crisis authority`, `during crisis`, `state of emergency`
- `essential services`, `basic services`, `public services` via existing access/service terms
- `limited notice`, `limited public notice`, `unclear appeal rights`, `appeal rights unclear`, `without notice`

## New relationship rule
If central/emergency authority is linked to access/basic-service terms and weak safeguard language in the same sentence, the scan now routes to at least `THRESHOLD` with a note:

> Emergency/central authority over basic services: crisis or central-office authority is linked to essential services while notice or appeal safeguards look limited or unclear.

## Regression checks
Still preserves previous expected behavior:
- identity-gated access → `THRESHOLD`
- soft claims without mechanisms → `THRESHOLD`, fail-closed
- appeal/audit/revocation/30-day review → `SANCTUARY`, safeguards detected

## Test command
```cmd
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('A policy gives one central office emergency authority over essential services during crisis, with limited public notice and unclear appeal rights.'))"
```

Expected: `state='THRESHOLD'`, negative integrity pressure, and an `emergency_service_control` proximity hit.
