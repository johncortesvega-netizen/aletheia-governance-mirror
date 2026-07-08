# ALETHEIA Patch Status

**Current patch:** 258 — Behavior Regression Review  
**Current mode:** Modularized release-candidate refinement / legacy-test behavior review  
**Runtime impact of current patch:** None

## Current stable architecture snapshot

Shared UI components now live under `ui/components/`:

- `semantic_pressure_panel.py`
- `metric_cards.py`
- `review_cards.py`
- `tree_visuals.py`
- `receipt_blocks.py`
- `module_headers.py`

Primary pages now live under `ui/pages/`:

- `protocol_guide.py`
- `boundary_cases.py`
- `mirror_check.py`
- `stress_test.py`
- `evidence_lab.py`
- `world_lens.py`

Bridge-removal status:

- Mirror Check — completed
- Stress Test — completed
- Evidence Lab — completed
- World Lens — completed

## Current test hygiene status

Patch 256 quarantined historical tests that target superseded repository contracts.
Patch 257 added active tests for the current modularized file/path contract.
Patch 258 adds active behavior-regression review tests for the current public
semantic-pressure examples and review posture.

The default active gate remains:

```bat
python -m pytest
```

This validates the active suite, not the full historical legacy inventory.

## Boundary

ALETHEIA remains a mirror, not a throne. Patch 258 does not change scanner logic,
scoring, MEI7 gates, Z-axis mapping, receipts, Evidence Lab calculations, World
Lens math, navigation, telemetry, storage, or authority boundaries.
