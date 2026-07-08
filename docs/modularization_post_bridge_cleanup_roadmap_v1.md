# Modularization Post-Bridge Cleanup Roadmap

## Purpose

This roadmap defines the next cleanup phase after Patch 254. The goal is to move from explicit dependency maps toward normal module imports without destabilizing ALETHEIA's governance-review behavior.

## Principle

Do not remove every injected dependency at once. Replace dependencies incrementally, test each page, and commit after each stable step.

## Recommended sequence

### Phase A — Low-risk direct imports

Start with helpers that are already stable and stateless:

- UI components from `ui/components/`;
- semantic panel helpers;
- metric card helpers;
- review card helpers;
- tree visual helpers;
- receipt-block helpers.

Acceptance criteria:

- page imports compile;
- no circular import;
- page renders manually;
- active tests pass.

### Phase B — Constants and copy objects

Move static constants/copy dictionaries to dedicated modules where useful.

Potential targets:

- demo scenario copy;
- module labels;
- shared review text;
- support utility placement text.

Acceptance criteria:

- no changed page behavior;
- no changed user-facing meaning unless part of a copy-cleanup patch;
- no scoring changes.

### Phase C — Runtime helpers

Handle runtime helpers more carefully. These may remain injected longer if they depend on app-level state.

Targets to inspect:

- protocol-state update helpers;
- receipt/witness creation helpers;
- batch helper functions;
- World Lens data helpers;
- Evidence Lab state helpers.

Acceptance criteria:

- session-state behavior unchanged;
- receipt output unchanged;
- World Lens/Evidence Lab state sharing unchanged.

### Phase D — Dependency-map removal

Only when a page no longer needs injected app-level helpers should its dependency map be removed.

Final desired form:

```python
render_mirror_check_page()
render_stress_test_page()
render_evidence_lab_page()
render_world_lens_page()
```

This is a future target, not a required immediate change.

## Stop conditions

Stop and revert/repair if any of the following happens:

- a page fails at import time;
- semantic pressure output changes unexpectedly;
- Stress Test metrics change unexpectedly;
- Evidence Lab or World Lens calculations change unexpectedly;
- receipts fail to generate/read;
- top-level navigation starts rendering multiple modules at once;
- README or UI text begins implying authority, certification, or final judgment.

## Documentation rule

Every cleanup step should state explicitly whether it changes runtime behavior. If the intended answer is no, the patch should say:

> No governance, scoring, scanner, MEI7, Z-axis, Evidence Lab, World Lens, receipt, telemetry, or authority-boundary behavior changed.
