# Patch 257 — Modularization Test Path Repair

Status: READY FOR LOCAL REVIEW

Patch 257 adds active current-structure tests for the post-modularization layout.
It establishes that `app.py` is now the orchestrator, while page modules live in
`ui/pages/` and shared rendering helpers live in `ui/components/`.

Boundary preserved: test/documentation update only. No runtime behavior, scoring,
semantic scanner logic, MEI7, Z-axis behavior, Stress Test metrics, Evidence Lab
calculations, World Lens math, receipt schema, external calls, telemetry,
storage, certification, enforcement, or authority behavior changed.

Validation target:

```bat
python -m py_compile tests\active\test_modularization_current_paths.py
python -m pytest
```

# ALETHEIA Patch Status

**Current patch:** 256 — Legacy Test Quarantine / Import-Break Cleanup  
**Current mode:** Modularized release-candidate refinement / legacy-test hygiene  
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

Patch 256 adds explicit collection quarantine for legacy tests that are known to target superseded repository contracts:

- two broken-import historical test files;
- old root-level patch-artifact contract tests superseded by Patch 255's `docs/patch_archive/` layout.

This keeps the active suite honest while preserving legacy files for audit continuity and later restoration/deletion decisions.

## Boundary

ALETHEIA remains a mirror, not a throne. Patch 256 does not change scanner logic, scoring, MEI7 gates, Z-axis mapping, receipts, Evidence Lab calculations, World Lens math, navigation, telemetry, storage, or authority boundaries.
