# Semantic Pressure Scanner Calibration Patch

Changed file:
- `core/semantic_pressure_scanner.py`

## What changed
- Added phrase-level detection for identity-gated access, including:
  - `only possible after`
  - `after identity verification`
  - `public benefits`
  - `identity verification`
- Added a same-sentence access-gating rule:
  - access/basic-service term + grip/condition term + identity/verification term => at least THRESHOLD.
- Expanded safeguard/mechanism recognition:
  - `appealed`, `appealable`, `revoked`, `reviewed`, `independently audited`, `independent audit`, `within 30 days`, `review window`, `automatic expiry`.
- Expanded sovereignty/reversibility recognition for appeal/audit/review/revocation/time-limit phrases.
- Removed identity/verification terms from the generic access bucket so access-gating output is cleaner.
- Prioritized `identity_gated_access` hits at the top of proximity output.
- Added a positive note when concrete safeguards are visible without pressure hits.

## Expected calibration behavior
1. `Access to public benefits is only possible after identity verification.`
   - THRESHOLD
   - identity-gated access signal
   - negative integrity pressure

2. `This system protects dignity, safety, harmony, inclusion, and public trust.`
   - THRESHOLD
   - rhetoric-to-mechanism gap
   - fail-closed review if governance context is enabled

3. `Any decision can be appealed, revoked, independently audited, and reviewed within 30 days.`
   - SANCTUARY direction
   - multiple mechanism/safeguard signals
   - sovereignty/reversibility signals

## Validation
- `python -m py_compile core/semantic_pressure_scanner.py` passes.
- Manual three-sentence calibration test passes.
