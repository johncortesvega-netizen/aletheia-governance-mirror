# ALETHEIA Tree / Threshold Band + Semantic Message Patch

Changed file:
- `app.py`

## Semantic scanner UI message
Improves the green/safeguard case copy:
- If concrete mechanisms or sovereignty/reversibility signals are detected, the UI now says:
  "Concrete safeguards detected. No strong pressure relationship was detected by this scanner; human review still required."
- If neither pressure nor safeguards are detected, the UI now distinguishes that from a safeguard-positive result.

## Threshold language
Updates display-only review-band language:
- `Threshold− / near Asylum`: closer to Asylum; repair is needed before trust can increase.
- `Threshold / middle review`: safeguards are mixed, incomplete, or unclear.
- `Threshold+ / near Sanctuary`: safeguards are visible, but not a final safety claim.

Canonical taxonomy remains:
- `ASYLUM`
- `THRESHOLD`
- `SANCTUARY`

The plus/minus bands are visual/explanatory only.

## Tree / canopy visualization
Adds a clearer visual review-band rail inside the tree card:
- Asylum → Threshold− → Threshold → Threshold+ → Sanctuary
- Active band is highlighted with a colored pill and marker.
- The tree canopy color for THRESHOLD now shifts by band:
  - Threshold−: warmer orange
  - Threshold: yellow
  - Threshold+: yellow-green

This makes the tree communicate *where inside the review boundary* the case sits, without changing receipt metrics or protocol scoring.

## Validation
- `python -m py_compile app.py` passed.
