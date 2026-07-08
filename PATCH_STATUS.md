# ALETHEIA Patch Status

**Current patch:** 255 — Patch Notes Final Cleanup  
**Current mode:** Modularized release-candidate refinement / repository hygiene  
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

## Current root policy

The repository root keeps only the current patch artifacts and current patch summaries:

- `PATCH_STATUS.md`
- `PATCH_NOTES.md`
- `PATCH_255_MANIFEST.txt`
- `PATCH_255_RECOVERY_NOTE.md`
- `PATCH_255_DELETE_LIST.txt`

Older patch artifacts are preserved in `docs/patch_archive/`.

## Boundary

ALETHEIA remains a mirror, not a throne. Patch 255 does not change scanner logic, scoring, MEI7 gates, Z-axis mapping, receipts, Evidence Lab calculations, World Lens math, navigation, telemetry, storage, or authority boundaries.
