# Patch 210 Recovery Note — Trigger Matrix / Pressure Codes

Patch 210 adds a transparent pressure-code matrix to ALETHEIA's semantic pressure layer.

## What changed

- `core/semantic_pressure_scanner.py`
  - Adds `PRESSURE_CODE_DEFINITIONS`.
  - Adds `pressure_code_explanation(...)` and `pressure_code_rows(...)` helpers.
  - Adds `pressure_codes` to `SemanticPressureScan`.
  - Maps scanner evidence into stable codes such as `OPAQUE_CAPTURE_CLAIM`, `IDENTITY_GATED_ACCESS`, `EMERGENCY_POWER_WEAK_SAFEGUARD`, and `CLAIM_MECHANISM_GAP`.
  - Includes codes in the plain-text semantic report.

- `app.py`
  - Imports the pressure-code row helper.
  - Shows a compact **Pressure-code matrix** in the shared semantic pressure panel details.

- `ui/receipt_reader.py`
  - Carries pressure codes into the semantic pressure layer summary.
  - Shows a **Pressure-code matrix** behind an opt-in expander inside Receipt Reader.
  - Adds a `Pressure Codes` column to batch receipt summaries.

## What did not change

- No scoring change.
- No state routing change.
- No receipt schema change.
- No stored receipt value change.
- No World Lens math change.
- No Evidence Lab calculation change.
- No Stress Test metric change.
- No telemetry, storage, external call, certification, enforcement, or authority behavior added.

## Validation

```bat
python -m py_compile core\semantic_pressure_scanner.py app.py ui\receipt_reader.py
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('a group of bankers have world power in secret').pressure_codes)"
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('A government creates emergency powers after a crisis, but the powers have no sunset clause, weak appeal rights, and limited independent review.').pressure_codes)"
```

Expected examples:
- opaque hidden-power claim -> includes `OPAQUE_CAPTURE_CLAIM`.
- emergency powers with weak safeguards -> includes `EMERGENCY_POWER_WEAK_SAFEGUARD`, `MISSING_SAFEGUARD`, and `MODAL_PRESSURE`.
