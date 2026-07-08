# Patch 254 — Modularization Final Audit

## Purpose

This document closes the first major ALETHEIA app modularization round. It records what was extracted from `app.py`, which bridges were removed, what still remains in `app.py`, and what should be handled in later cleanup.

The audit is intentionally documentation-only. It does not claim the architecture is final or complete. It records the current modular boundary so future refactors can proceed without losing the mirror boundary, receipt behavior, or governance-review semantics.

## Completed modularization stages

### Shared UI components

The following reusable UI surfaces were extracted from `app.py` into `ui/components/`:

| Stage | Component file | Purpose |
|---:|---|---|
| 1 | `ui/components/semantic_pressure_panel.py` | Shared semantic pressure panels, evidence implications, stress triggers, and World Lens semantic flags. |
| 2 | `ui/components/metric_cards.py` | Shared metric/status cards and soft-card wrappers. |
| 3 | `ui/components/review_cards.py` | Shared review, repair-question, and recommendation cards. |
| 4 | `ui/components/tree_visuals.py` | Mirror/Stress visual tree rendering helpers. |
| 5 | `ui/components/receipt_blocks.py` | Shared receipt display blocks. |
| 6 | `ui/components/module_headers.py` | Shared module notice/reference panels. |

### Page modules

The following pages were extracted from `app.py` into `ui/pages/`:

| Stage | Page file | Status |
|---:|---|---|
| 7 | `ui/pages/protocol_guide.py` | Extracted. |
| 8 | `ui/pages/boundary_cases.py` | Extracted. |
| 9 | `ui/pages/mirror_check.py` | Extracted. |
| 10 | `ui/pages/stress_test.py` | Extracted. |
| 11 | `ui/pages/evidence_lab.py` | Extracted. |
| 12 | `ui/pages/world_lens.py` | Extracted. |

## Bridge-removal status

The heavy page extractions initially used a temporary namespace bridge. The broad `render_*_page(globals())` handoffs have now been replaced with explicit dependency maps.

| Page | Previous broad bridge | Current boundary |
|---|---|---|
| Mirror Check | `render_mirror_check_page(globals())` | `render_mirror_check_page(mirror_check_dependency_map(globals()))` |
| Stress Test | `render_stress_test_page(globals())` | `render_stress_test_page(stress_test_dependency_map(globals()))` |
| Evidence Lab | `render_evidence_lab_page(globals())` | `render_evidence_lab_page(evidence_lab_dependency_map(globals()))` |
| World Lens | `render_world_lens_page(globals())` | `render_world_lens_page(world_lens_dependency_map(globals()))` |

The current boundary is not final dependency injection, but it is no longer an unconstrained namespace pass. Each heavy page now declares the dependencies it expects.

## Current app.py role

After the modularization round, `app.py` should remain responsible for:

- application bootstrapping;
- page navigation / module selection;
- global imports and compatibility fallbacks;
- dependency-map construction;
- session-state continuity where cross-page state is still shared;
- core helper functions that are not yet safe to move;
- top-level Streamlit shell and boundary notices.

`app.py` should not be treated as fully cleaned. It is now smaller and more inspectable, but still acts as the coordination shell.

## Remaining cleanup targets

Future cleanup should avoid broad behavior changes. Recommended next steps:

1. **Dependency-map reduction**
   - Replace injected helpers with direct imports where safe.
   - Remove dependency-map entries one at a time.
   - Preserve loud failures for missing dependencies during transition.

2. **Cross-page state documentation**
   - Document session-state keys shared by Evidence Lab and World Lens.
   - Keep state names stable until tests cover them.

3. **Core/UI boundary cleanup**
   - Keep scoring, scanner, MEI7, Z-axis, World Lens math, and receipt generation in `core/` or stable runtime modules.
   - Keep visual rendering in `ui/components/` and `ui/pages/`.

4. **Test coverage expansion**
   - Add active tests for page import boundaries.
   - Add smoke tests for dependency-map completeness.
   - Preserve `python -m pytest` as active-suite validation.

5. **Legacy test triage**
   - Continue the Patch 219 legacy-test cleanup plan.
   - Do not let legacy broken tests be confused with active release checks.

## Boundary preservation

This modularization round did not intentionally change:

- scanner logic;
- scoring;
- MEI7 ethics gate;
- Z-axis behavior;
- Stress Test metrics;
- Evidence Lab calculations;
- World Lens math;
- 9k allocation rules;
- receipt schema;
- telemetry/storage behavior;
- authority-boundary language.

ALETHEIA remains a mirror, not a throne. Modularization improves maintainability; it does not grant the app authority.

## Manual validation checklist

After applying this patch set and any future bridge cleanup, run:

```cmd
python -m py_compile app.py ui\components\*.py ui\pages\*.py
python -m pytest
python -m streamlit run app.py
```

Then manually verify:

- Mirror Check opens and renders semantic pressure output.
- Stress Test opens, demos run, semantic signals render, and receipts are available.
- Evidence Lab opens and produces evidence/claim-mechanism output.
- World Lens opens, internal tabs render, and report packet works.
- Boundary Cases opens.
- Protocol Guide opens.
- Why ALETHEIA support utilities still clearly place Receipt Reader.
- Only one top-level module renders at a time.
