# ALETHEIA App Modularization Plan
**Patch:** 220  
**Status:** Planning-only / no runtime refactor  
**Scope:** Future `app.py` modularization map, component boundaries, migration order, and no-behavior-change guardrails

## 1. Purpose

`app.py` has grown into the main orchestration surface for ALETHEIA. That is acceptable for rapid release-candidate iteration, but it is not ideal for long-term maintenance, review, or contributor onboarding.

Patch 220 does **not** refactor the app. It records the modularization plan so future work can split the monolith without changing behavior, scoring, routing, receipts, or governance boundaries.

The goal is not to make ALETHEIA more complex. The goal is to make the existing mirror easier to inspect.

## 2. Non-goals

This patch must not:

- change runtime behavior;
- change Streamlit tab behavior;
- change scanner logic;
- change semantic pressure codes;
- change MEI7 gate behavior;
- change Z-axis behavior;
- change Stress Test metrics;
- change Evidence Lab calculations;
- change World Lens math or 9k interpretation;
- change receipt schema;
- add external services, telemetry, storage, or model calls;
- rename public concepts without a migration note.

## 3. Target future structure

A later refactor should move toward this structure:

```text
app.py
ui/
  pages/
    unit_preview.py
    mirror_check.py
    stress_test.py
    evidence_lab.py
    world_lens.py
    receipt_reader_page.py
    boundary_cases.py
    protocol_guide.py
  components/
    semantic_panel.py
    pressure_code_cards.py
    metric_cards.py
    repair_questions.py
    receipt_blocks.py
    tree_visual.py
    tables.py
    callouts.py
  layout/
    theme.py
    navigation.py
    page_shell.py
core/
  semantic_pressure_scanner.py
  witness.py
  empirical.py
  protocol.py
  simulation.py
  evidence.py
  world_lens.py
```

This is a target map, not an immediate implementation.

## 4. What should move to `ui/pages/`

The following large page-level flows should eventually move out of `app.py` into page modules. Each page should expose one top-level render function and avoid owning core scoring logic.

| Current surface | Future module | Target public function |
|---|---|---|
| Aletheia Unit Preview | `ui/pages/unit_preview.py` | `render_unit_preview()` |
| Mirror Check | `ui/pages/mirror_check.py` | `render_mirror_check()` |
| Stress Test | `ui/pages/stress_test.py` | `render_stress_test()` |
| Evidence Lab | `ui/pages/evidence_lab.py` | `render_evidence_lab()` |
| World Lens | `ui/pages/world_lens.py` | `render_world_lens()` |
| Receipt Reader | `ui/pages/receipt_reader_page.py` | `render_receipt_reader_page()` |
| Boundary Cases | `ui/pages/boundary_cases.py` | `render_boundary_cases()` |
| Protocol Guide / Why ALETHEIA | `ui/pages/protocol_guide.py` | `render_protocol_guide()` |

Page modules may orchestrate UI state and call core functions, but they should not define new scoring rules.

## 5. What should move to `ui/components/`

Repeated visual patterns should become reusable components.

### Semantic panel

Target module:

```text
ui/components/semantic_panel.py
```

Should own:

- semantic pressure summary card;
- pressure-code cards;
- pressure-code table expander;
- reviewable-input guidance display;
- developer/debug details toggle.

Should not own:

- scanner logic;
- state routing;
- score calculation.

### Metric cards

Target module:

```text
ui/components/metric_cards.py
```

Should own reusable display blocks for stability, trust, alignment, ego, integrity pressure, repair index, and similar visible metrics.

Should not decide what values mean.

### Repair questions

Target module:

```text
ui/components/repair_questions.py
```

Should render repair questions consistently across Mirror Check, Stress Test, Evidence Lab, World Lens, and receipts.

Should not generate hidden authority claims or convert questions into verdicts.

### Receipt blocks

Target module:

```text
ui/components/receipt_blocks.py
```

Should render:

- simple-English walkthrough;
- status banner;
- layered causal chain;
- semantic pressure layer;
- pressure-code matrix;
- diagnostics expanders.

Receipt parsing and witness logic should remain in core or receipt-reader modules.

### Tree and visual blocks

Target module:

```text
ui/components/tree_visual.py
```

Should render visual metaphors only. It must not become the source of scoring truth.

## 6. What should stay in `core/`

Core modules should contain deterministic logic and data transformations that can be tested without Streamlit.

Keep in core:

- semantic pressure scanner;
- pressure code generation;
- witness receipt creation/parsing;
- evidence scoring helpers;
- empirical/world-lens data transforms;
- protocol gate calculations;
- simulation primitives;
- stress-test scoring primitives.

Core modules should avoid importing Streamlit.

## 7. What should remain in `app.py`

After modularization, `app.py` should become a thin shell:

- imports page render functions;
- sets page configuration;
- applies theme;
- defines navigation;
- calls the selected page render function;
- performs minimal compatibility setup.

Target future size: small enough that a reviewer can understand the app entrypoint quickly.

## 8. Migration order

Use small, reversible patches. Do not split everything at once.

### Phase 1 — component extraction

Extract pure rendering helpers first:

1. semantic panel;
2. pressure-code cards;
3. metric cards;
4. repair-question blocks;
5. callouts/status banners.

These should be lowest risk because they do not change calculations.

### Phase 2 — page extraction

Move one page at a time:

1. Protocol Guide / Why ALETHEIA;
2. Boundary Cases;
3. Unit Preview;
4. Mirror Check;
5. Receipt Reader page;
6. Evidence Lab;
7. World Lens;
8. Stress Test last.

Stress Test should be last because it has the densest interaction between UI, metrics, semantic layer, receipts, and visual outputs.

### Phase 3 — core/API cleanup

Only after page extraction:

- define stable core return objects;
- remove duplicate fallback helpers;
- deprecate old aliases;
- promote stable regression tests into `tests/active/`.

## 9. No-behavior-change validation

Every modularization patch should run at minimum:

```bat
python -m py_compile app.py core\semantic_pressure_scanner.py ui\receipt_reader.py
python -m pytest
```

For page extraction patches, also run one manual smoke path:

1. Mirror Check with opaque capture claim;
2. Stress Test with emergency-power weak safeguards;
3. Evidence Lab synthetic demo;
4. World Lens synthetic demo;
5. Receipt Reader sample receipt if available.

The expected result is not new behavior. The expected result is unchanged behavior in cleaner files.

## 10. Boundary rule

Refactoring must never become a conceptual rewrite. If a future patch changes routing, scoring, scanner categories, receipt fields, or boundary language, it is not a pure modularization patch and must say so explicitly.

> Clean architecture is allowed. Hidden authority drift is not.
