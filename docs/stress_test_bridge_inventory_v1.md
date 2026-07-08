# Stress Test Bridge Inventory
**Patch:** 248  
**Status:** planning / documentation only  
**Target page:** `ui/pages/stress_test.py`  
**Current bridge:** `render_stress_test_page(runtime_namespace)` with `globals().update(runtime_namespace)`

## Purpose

Patch 248 records the remaining Stress Test namespace bridge before any removal work begins. The goal is to prevent a risky extraction of Stress Test dependencies by making the dependency surface explicit first.

Stress Test is more complex than Mirror Check because it touches text-derived feature extraction, manual sliders, demo scenarios, batch processing, semantic pressure diagnostics, tree visuals, local witness receipts, and protocol-state updates. For that reason, the bridge should not be removed in one blind step.

## Current call shape

At the time of this inventory, `app.py` renders Stress Test through the temporary page bridge:

```python
render_stress_test_page(globals())
```

Inside `ui/pages/stress_test.py`, the bridge is applied with:

```python
globals().update(runtime_namespace)
```

This is acceptable as an intermediate migration state, but it is not the desired long-term architecture.

## Declared dependency groups

The Stress Test page currently depends on the following categories of external names from `app.py` and shared modules.

### 1. Streamlit / data / utility dependencies

- `st`
- `pd`
- `html`
- `hashlib`

These should eventually become explicit imports inside `ui/pages/stress_test.py` where possible.

### 2. App constants and configuration

- `APP_VERSION`
- `MAX_BATCH_RECEIPTS`
- `STRESS_TEST_DEMO_SCENARIOS`
- `steps`
- `n_agents`
- `weights`

These should become either explicit imports from a config/constants module or a small `StressTestConfig` object.

### 3. Protocol state / shared status helpers

- `update_protocol_state`
- `render_shared_protocol_state_notice`
- `render_module_page_template_intro`
- `ModulePageTemplateCopy`
- `_protocol_humility_note`
- `_protocol_metric_display`
- `_protocol_taxonomy_ui_table_df`

These are UI/protocol-display dependencies. They should be injected or moved into shared page-support modules before full bridge removal.

### 4. Stress/scoring/model helpers

- `build_features_from_scan`
- `run_audit`
- `apply_guardrail_verdict`
- `classify_verdict`
- `display_score_from_judgment`
- `divine_floor`
- `ego_tolerance`
- `enforce_asylum_metric_consistency`
- `enforce_missing_safeguard_threshold_route`
- `normalize_asylum_protocol_label`
- `review_band_for_state`
- `stress_label_for_phrase`

These are the core stress-routing dependencies. They must be extracted or explicitly imported carefully because any mismatch can change Stress Test behavior.

### 5. Repair-question helpers

- `ensure_asylum_repair_questions`
- `ensure_threshold_repair_questions`
- `silent_operator_question`

These control repair prompts and should remain behavior-preserving during bridge removal.

### 6. Semantic pressure helpers

- `choose_stress_semantic_scan`
- `choose_strongest_semantic_scan`
- `render_semantic_stress_triggers`
- `build_ai_static_scan_protocol_context`

These connect Stress Test to the semantic pressure layer. They should stay aligned with the shared component in `ui/components/semantic_pressure_panel.py`.

### 7. Visual/UI components

- `metric_card`
- `render_soft_card_grid`
- `render_repair_question_cards`
- `render_recommendation_cards`
- `render_pulse_tree`
- `plot_trace`
- `action_chart`
- `render_stress_test_scan_intro`
- `render_receipt_sky_panel`

Most of these are already modularized components. The next bridge-removal patch should import these explicitly instead of receiving them through `globals()`.

### 8. Local witness / receipt helpers

- `build_local_witness_receipt`
- `build_local_witness_batch_zip`
- `build_local_question_prompt_receipt`
- `render_local_witness_receipt_text`
- `parse_witness_batch_input`
- `is_witness_question_prompt`
- `is_witness_question_set`

These require careful handling because Stress Test generates receipts and batch artifacts. Bridge removal must not alter the receipt schema or witness-boundary language.

### 9. Text/entity handling helpers

- `decouple_actor`

Used by the Invisibility Filter. This must stay behavior-compatible.

## Recommended removal strategy

Do not remove the Stress Test bridge directly. Use a two-step approach.

### Patch 249 — Stress Test dependency-map bridge

Replace:

```python
render_stress_test_page(globals())
```

with something like:

```python
render_stress_test_page(stress_test_dependency_map(globals()))
```

This mirrors the safer approach used for Mirror Check in Patch 247.

The dependency map should include only the names listed in this inventory. If a required name is missing, fail loudly with a clear dependency error rather than silently falling back to broad globals.

### Patch 250 — Stress Test explicit imports / injection cleanup

After the dependency-map bridge is stable, move low-risk imports directly into `ui/pages/stress_test.py`:

- Streamlit/data utilities
- shared UI components
- semantic pressure component helpers
- receipt block renderer

Keep high-risk stress-routing functions explicit and documented until they can be moved into a core stress module.

## Non-goals

This patch does not change:

- Stress Test scoring
- semantic scanner behavior
- MEI7 gate behavior
- Z-axis behavior
- receipt schema
- batch behavior
- demo scenario values
- World Lens or Evidence Lab logic
- telemetry/storage behavior
- authority-boundary language

## Acceptance criteria for the next runtime patch

A future Stress Test bridge-removal patch should pass the following checks:

1. `python -m py_compile app.py ui/pages/stress_test.py`
2. `python -m pytest`
3. Stress Test opens without traceback.
4. Demo scenario loading works.
5. Manual slider mode works.
6. Invisibility Filter works.
7. Stress Test Tree renders.
8. Semantic pressure signals render.
9. Batch testing expander works.
10. Receipt visual/download path works.
11. No inactive modules render under the active module.

## Boundary note

Bridge removal is maintainability work only. It must never be used to alter the risk routing, to soften high-risk cases, or to introduce authority claims. ALETHEIA remains a mirror, not a throne.
