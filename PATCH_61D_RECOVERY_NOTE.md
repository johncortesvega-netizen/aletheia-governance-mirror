# Patch 61D — Missing Raw Trust Display

## Purpose
Clarify World Lens trust evidence by separating observed raw trust from neutral trust-prior fallback values.

## Changes
- Added World Lens formatting helpers for raw trust, trust prior, and coverage labels.
- Updated Country-Year Explorer to show `Raw trust: not available` instead of an ambiguous dash.
- Updated trust prior display to show `0.500 neutral default` when a neutral fallback is used.
- Renamed overview coverage cards to `Raw trust survey coverage` and `Neutral trust-prior fallback coverage`.
- Added documentation and tests for the interpretation guardrail.

## Authority boundary
No scoring authority or enforcement behavior was added. This patch only hardens interpretation.

## Check
```bat
tools\run_patch_checks.bat 61D
```
