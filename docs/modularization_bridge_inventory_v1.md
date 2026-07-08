# ALETHEIA Modularization Bridge Inventory
**Patch:** 245  
**Type:** Documentation-only / modularization control plane  
**Status:** Active planning reference  
**Context:** After Stage 12 page extraction

## 1. Purpose

Stages 1-12 split shared UI components and several major pages out of `app.py`. The current extracted pages still preserve behavior through a temporary runtime namespace bridge. This document records that bridge explicitly so later cleanup can remove it in a controlled way.

The current goal is not to remove the bridge immediately. The goal is to avoid hidden coupling, prevent accidental logic changes, and define the safe migration path from `globals()`-based page calls to explicit imports and dependency injection.

Boundary: this document does not change scoring, scanner behavior, MEI7, Z-axis routing, Evidence Lab calculations, World Lens math, receipt logic, telemetry posture, or authority boundaries.

## 2. Current page extraction state

### Pages already extracted

| Page / module | File | Current call pattern | Bridge status | Notes |
|---|---|---:|---|---|
| Protocol Guide | `ui/pages/protocol_guide.py` | `render_protocol_guide_page()` | No runtime bridge | Mostly static/support documentation page. |
| Boundary Cases | `ui/pages/boundary_cases.py` | explicit arguments | Partial bridge avoided | Safer page split; still uses passed helpers/values from app. |
| Mirror Check | `ui/pages/mirror_check.py` | `render_mirror_check_page(globals())` | Active bridge | Large stateful page; should be converted after dependency inventory. |
| Stress Test | `ui/pages/stress_test.py` | `render_stress_test_page(globals())` | Active bridge | Large stateful page; contains demo loading, sliders, semantic layer, receipt display, batch paths. |
| Evidence Lab | `ui/pages/evidence_lab.py` | `render_evidence_lab_page(globals())` | Active bridge | Shares data/state with World Lens. |
| World Lens | `ui/pages/world_lens.py` | `render_world_lens_page(globals())` | Active bridge | Largest remaining coupling; depends on Evidence Lab state, selected-year data, 9k allocation, internal tabs, exports. |

### Shared UI components already extracted

| Component | File | Purpose |
|---|---|---|
| Semantic pressure panel | `ui/components/semantic_pressure_panel.py` | Shared semantic diagnostic UI, pressure codes, reviewable guidance, semantic trigger summaries. |
| Metric/status cards | `ui/components/metric_cards.py` | Shared metric and soft-card presentation. |
| Review/repair cards | `ui/components/review_cards.py` | Stress Test why-this-result, repair questions, recommendation cards. |
| Tree visuals | `ui/components/tree_visuals.py` | Mirror/Stress reading tree visuals. |
| Receipt blocks | `ui/components/receipt_blocks.py` | Shared receipt display panels. |
| Module headers | `ui/components/module_headers.py` | Shared protocol-state notices and reference-point blocks. |

## 3. Active namespace bridge locations

These calls are the remaining explicit bridge points in `app.py`:

```python
render_stress_test_page(globals())
render_evidence_lab_page(globals())
render_world_lens_page(globals())
render_mirror_check_page(globals())
```

The bridge exists to preserve behavior while page bodies are moved out of `app.py`. It is temporary. It must not be treated as the final architecture.

## 4. Why the bridge exists

The extracted pages still depend on a wide set of names previously living in `app.py`, including:

- Streamlit object and session state usage;
- demo scenario dictionaries;
- scoring/evaluation helpers;
- protocol-state helpers;
- receipt/witness helpers;
- batch-processing helpers;
- plot/table helpers;
- data-frame variables;
- active Evidence Lab and World Lens state;
- selected-year and 9k allocation context;
- imported core functions that were originally only imported at app level.

Passing `globals()` keeps the first extraction behavior-preserving. It avoids a risky rewrite where many dependencies are moved at once.

## 5. Target end-state

The target end-state is explicit page dependencies, for example:

```python
render_mirror_check_page(
    scanner=scan_semantic_pressure,
    evaluate=evaluate_governance_text,
    render_tree=render_pulse_tree,
    receipt_writer=build_local_witness_receipt,
    protocol_state=protocol_state_service,
)
```

The final pattern should make clear:

- what each page imports directly;
- what data each page reads from `st.session_state`;
- what each page writes to `st.session_state`;
- which functions remain in `core/`;
- which UI helpers remain in `ui/components/`;
- which app-level navigation/state helpers remain in `app.py`.

## 6. Dependencies to inventory before bridge removal

### Mirror Check

Likely dependency groups:

- text input state and audit history;
- governance evaluation/scoring helper;
- semantic pressure scan helper;
- mirror tree renderer;
- receipt generation and raw receipt display;
- threshold direction review helpers;
- batch testing helpers;
- shared protocol-state notice.

Recommended target file split:

- `ui/pages/mirror_check.py` stays as page shell;
- Mirror-specific pure helpers move to `ui/page_helpers/mirror_check_helpers.py` only if they are UI-bound;
- scoring/evaluation remains in `core/`.

### Stress Test

Likely dependency groups:

- demo scenario library;
- manual slider defaults;
- scenario feature extraction;
- stress/scoring evaluation;
- semantic scan candidate selection;
- tree visual renderer;
- repair question rendering;
- receipt generation and ZIP/batch behavior;
- local witness receipt UI.

Recommended target file split:

- `ui/pages/stress_test.py` page shell;
- `core/stress_test_engine.py` for non-UI stress evaluation if not already isolated;
- `ui/page_helpers/stress_test_helpers.py` for UI-bound formatting and input orchestration.

### Evidence Lab

Likely dependency groups:

- synthetic demo data creation;
- upload parsing/data normalization;
- claim-mechanism evidence checks;
- semantic evidence panel;
- active Evidence Lab dataframe state;
- handoff state consumed by World Lens.

Recommended target file split:

- keep page shell in `ui/pages/evidence_lab.py`;
- move reusable data validation/parsing to `core/evidence_lab.py`;
- keep presentation-only helpers in `ui/components/` or `ui/page_helpers/`.

### World Lens

Likely dependency groups:

- active empirical dataset lookup;
- selected-year filtering;
- 9k allocation logic;
- WGI/V-Dem/trust coverage fields;
- comparison/export table construction;
- internal World Lens tabs;
- Evidence Lab handoff state;
- semantic regional flags.

Recommended target file split:

- `ui/pages/world_lens.py` page shell;
- `core/world_lens_engine.py` for data transformations and allocation checks;
- `ui/page_helpers/world_lens_tables.py` for display-table formatting;
- keep 9k boundary language in docs/components, not hidden in computation.

## 7. Helpers that should remain in `app.py` for now

`app.py` should remain responsible for:

- app bootstrapping;
- page configuration;
- top-level navigation containment;
- global CSS/theme injection;
- top-level module selector;
- global Receipt Reader location hint;
- high-level protocol state initialization;
- calling page renderers;
- fallback error boundary if added later.

Do not move these until page-level dependencies are explicit.

## 8. Helpers that should not remain in `app.py` long term

Candidates for later extraction:

- pure scoring or calibration helpers that still live in `app.py`;
- data transformation helpers used by Evidence Lab or World Lens;
- receipt display helpers already partially extracted;
- demo scenario definitions if they are large and stable;
- batch-processing utilities;
- repeated copy blocks and module guidance text.

## 9. Safe bridge removal sequence

Recommended order:

1. **Mirror Check bridge removal** — smallest of the major stateful pages after extraction.
2. **Stress Test bridge removal** — larger; do after Mirror Check because it shares several components.
3. **Evidence Lab bridge removal** — do before World Lens because World Lens consumes its state.
4. **World Lens bridge removal** — last; largest dependency surface and most data-coupled page.

Do not remove all bridges in one patch.

## 10. Acceptance criteria for each future bridge-removal patch

Each bridge-removal patch must satisfy:

- no `globals()` call for the target page;
- page imports are explicit;
- session-state keys read/written by the page are documented;
- active pytest suite passes;
- target page opens and performs the same user-visible flow;
- no scoring, routing, receipt, MEI7, Z-axis, Evidence Lab, World Lens math, telemetry, or authority behavior changes unless explicitly declared.

## 11. Why this matters

The bridge is acceptable as a transitional safety mechanism. It is not acceptable as a permanent architecture because it hides page dependencies and makes future review harder.

This inventory keeps the modularization aligned with ALETHEIA's own standard: visible dependencies, explicit boundaries, and no hidden authority path.
