# Semantic v1 Patch Notes — Consolidated Session

This file consolidates transient patch notes that were previously left at repository root or inside `core/`. The notes are archived here to keep the root and runtime package clean while preserving the review trail.

Boundary: these updates support human review. They do not certify, approve, reject, enforce, monitor, or replace accountable judgment.

## Session summary

- Added and calibrated `core/semantic_pressure_scanner.py`.
- Integrated semantic pressure as a subordinate diagnostic into Mirror Check, Stress Test, Evidence Lab, World Lens, and Receipt Reader.
- Added emergency/central-authority-over-essential-services calibration.
- Cleaned semantic debug output so raw proximity hits, normalized text, and plain-text reports stay behind explicit developer/debug controls.
- Kept scanner output subordinate to module readings and human review.

## Archived transient notes

### S3.2 Semantic debug hard-hide

# Patch S3.2 — Semantic debug hard-hide

Changed file:
- app.py

Purpose:
- Keep semantic panels useful for normal review while preventing raw debug machinery from dominating World Lens, Stress Test, Mirror Check, or Evidence Lab.

Changes:
- Replaced the always-rendered nested "Developer/debug details" expander with an explicit checkbox:
  - "Show developer/debug details"
- Default is OFF.
- When OFF, the UI does not render:
  - contextual proximity hits table
  - normalized text area
  - plain-text semantic report
- When ON, the same diagnostics are still available for calibration/troubleshooting.

No changes to:
- semantic scanner logic
- scores
- receipts
- World Lens flags
- Stress Test/Evidence Lab calculations

### Semantic pressure scanner calibration

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

