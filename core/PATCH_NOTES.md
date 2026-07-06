# Semantic Pressure Scanner Patch

Adds a deterministic relationship-aware scanner for unstructured governance text.

## Changed files
- `core/semantic_pressure_scanner.py` — new scanner module.
- `app.py` — adds the scanner to the Boundary Cases diagnostics area under Mechanism-vs-Claim.

## What it adds
- Entity normalization: named actors/systems are replaced with generic tokens before scanning.
- Proximity scanning: checks pressure/condition terms near access, identity, service, or basic-rights terms.
- Rhetoric-to-mechanism ratio: compares soft ethical claims with concrete safeguards.
- Modal pressure detection: detects obligation/permanence language versus appeal/revocation/fallback language.
- Fail-closed behavior: governance/value text with no recognizable safeguards is routed to review instead of being treated as safe.

## Boundary
This scanner produces mirror signals for human review. It does not certify intent, safety, legality, ethics, or final legitimacy.
