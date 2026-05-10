# Patch 67 — Stress Test Threshold Repair + Metric Softening

Patch 67 makes medium-risk Stress Test outputs more useful.

Patch 66 correctly stopped subtle stress scenarios from being washed into `SANCTUARY`. Patch 67 adds the next layer: when a scenario is `THRESHOLD` or `Needs Safeguards`, ALETHEIA should not display a perfectly clean metric profile or an empty repair path.

## Behavior

If a Stress Test scenario is `THRESHOLD`, `Medium`, or its protocol label contains `Needs Safeguards`, ALETHEIA adds repair questions and applies a light metric softening layer.

This is diagnostic only. It does not command, enforce, block, remove leaders, or replace human judgment.

## Threshold repair questions

Threshold outputs should ask questions such as:

- What safeguard is missing or ambiguous here?
- Who can appeal, correct, or pause this mechanism?
- What evidence would move this from Needs Safeguards toward trust?
- What prevents this safeguard gap from becoming capture?
- How can affected people challenge the outcome without ALETHEIA becoming the authority?

## Metric softening

For `THRESHOLD / Needs Safeguards` scenarios, ALETHEIA prevents perfect readings:

- `trust_index` is capped at `0.92`
- `alignment` is capped at `0.92`
- `ego` is floored at `0.05`
- `ego_pressure` / `Ep` is floored at `0.05`

ASYLUM behavior remains unchanged and continues to use the stronger high-risk repair and calibration layers.

## Boundary

ALETHEIA remains a mirror:

- Authority claim: `False`
- Human review required: `True`
- Public ledger: `False`
- Global ID sync: `False`
- Central storage: `False`
