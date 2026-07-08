# Patch 259 — App Shell Inventory / Thin Entrypoint Plan

Status: READY FOR LOCAL REVIEW  
Patch type: documentation / refactor planning  
Runtime impact: none

## Purpose

Patch 259 records what still lives in `app.py` after the modularization and
bridge-removal sequence completed in patches 220-254.

The goal is not to perform another broad runtime refactor immediately. The goal
is to prevent the next phase from becoming a large, risky rewrite. This patch
creates a concrete extraction map for turning `app.py` into a thinner entrypoint
while preserving the current controlled single-app review flow.

## Current state

`app.py` is still large, but its role has changed. It now acts mostly as a
Streamlit orchestrator plus compatibility bridge for older local helpers.

Current measured size:

```text
app.py: 4130 lines
```

Primary extracted page modules already exist under `ui/pages/`:

- `ui/pages/mirror_check.py`
- `ui/pages/stress_test.py`
- `ui/pages/evidence_lab.py`
- `ui/pages/world_lens.py`
- `ui/pages/boundary_cases.py`
- `ui/pages/protocol_guide.py`

Primary extracted shared UI components already exist under `ui/components/`:

- `semantic_pressure_panel.py`
- `metric_cards.py`
- `review_cards.py`
- `tree_visuals.py`
- `receipt_blocks.py`
- `module_headers.py`

Bridge-removal status:

- Mirror Check — dependency map active
- Stress Test — dependency map active
- Evidence Lab — dependency map active
- World Lens — dependency map active

## Remaining `app.py` responsibility map

### 1. Imports and compatibility fallbacks

`app.py` still imports a wide surface from:

- `core/`
- `config/`
- `ui/`
- `ui/components/`
- `ui/pages/`
- `pages_ui/`
- Streamlit, pandas, numpy, Plotly, and local file helpers

It also contains fallback imports for deployment compatibility, especially around
empirical helpers and protocol imports.

Recommended future action: keep compatibility fallbacks in place until a separate
import-boundary patch proves they can be moved safely.

### 2. App-local guardrail helpers

`app.py` still contains app-local guard functions such as:

- `app_detects_missing_safeguard_negation`
- `app_detects_ai_ownership_capture_pressure`
- `enforce_missing_safeguard_threshold_route`

These are behavior-sensitive. They should not be moved in a layout-only patch.
If extracted later, they should move into `core/` with active behavior tests.

### 3. World Lens / empirical display helpers

`app.py` still contains display and allocation helpers such as:

- `_truthy_series`
- `_country_allocation_base`
- `_replace_allocation_columns`
- `_empirical_humility_display_df`
- `_world_lens_public_display_df`
- `_world_lens_taxonomy_label`
- `_world_lens_ui_table_df`

These influence Evidence Lab and World Lens presentation. They should be handled
in a dedicated empirical/World Lens extraction patch, not mixed with shell
extraction.

### 4. Protocol/taxonomy display helpers

`app.py` still contains protocol display helpers such as:

- `_protocol_public_label`
- `_protocol_humility_note`
- `_protocol_taxonomy_ui_table_df`
- `_protocol_metric_display`

These are candidates for a future `ui/protocol_display.py` or
`ui/components/protocol_display.py` extraction, provided no labels or display
semantics change.

### 5. Simulation, audit, and scanner glue

`app.py` still contains or wraps several behavior-sensitive helper functions:

- `classify_verdict`
- `deterministic_seed_from_payload`
- `apply_guardrail_verdict`
- `review_band_for_state`
- `display_score_from_judgment`
- `plot_trace`
- `action_chart`
- `build_features_from_scan`
- `apply_capture_feature_override`
- `run_audit`
- `allocate_slots`

These are not shell code. They should eventually move toward `core/` or a
behavior module only after active regression tests cover their public examples.

### 6. Visual and asset helpers

`app.py` still contains helpers such as:

- `resolve_about_header_image`
- `asset_image_data_uri`
- `deterministic_signal_summary`
- `render_visual_source_card`

These are likely safe candidates for future UI/assets extraction.

### 7. Stress phrase and calibration helpers

`app.py` still contains stress-test helper logic such as:

- `stress_contains`
- `detects_missing_safeguard_negation`
- `apply_missing_safeguard_feature_override`
- `apply_ai_ownership_capture_feature_override`
- `apply_ai_ownership_capture_metric_caps`
- `source_conformance_hits`
- `source_conformance_label`
- `source_conformance_coverage`
- `stress_label_for_phrase`
- `parse_expected_pressure_line`
- `evaluate_expected_verdict`
- `normalize_stress_results_df`
- `run_stress_phrase`

This is behavior-sensitive and should remain out of shell-extraction patches.

### 8. Governance judgment and witness/report helpers

`app.py` still contains helpers such as:

- `governance_scan`
- `sanitize_public_message`
- `local_governance_judgment`
- `run_sydney_protocol_self_check`
- `render_sydney_protocol_self_check_gate`
- `llm_governance_judgment`
- `build_witness_report`
- `friendly_threshold_direction_label`
- `silent_operator_question`
- `render_chat_judgment`

Some of these are legacy-named helpers still used by current pages through
dependency maps. They should be inventoried before extraction. Moving them should
not be paired with navigation changes.

### 9. Session-state substrate and shared protocol state

`app.py` still owns shared state helpers:

- `_df_active`
- `_source_signal_active`
- `update_protocol_state`
- `render_shared_protocol_state_notice`
- `render_audit_module_integrity_panel`

This group is a strong candidate for a future `ui/state.py` or
`ui/protocol_state.py` extraction, but it is also central to Evidence Lab ->
World Lens state sharing. Extract only with active tests.

### 10. App shell and top-level rendering

The bottom of `app.py` still performs:

- mascot/logo URI preparation;
- optional header image display;
- global header rendering;
- Unit Preview gate;
- app boundary notices;
- sidebar rendering;
- sidebar lens/steps/voices/sensitivity controls;
- selected-module radio navigation;
- selected-page dispatch;
- Why ALETHEIA support utility rendering;
- app footer rendering.

This is the safest next extraction target because it is layout/orchestration
rather than scoring logic.

## Recommended next extraction sequence

### Patch 260 — App Shell Extraction Prep

Create a small shell module without changing routing behavior:

```text
ui/app_shell_runtime.py
```

Candidate responsibilities:

- app header preparation;
- app boundary notices;
- sidebar rendering helper;
- navigation label display helper;
- footer wrapper;
- receipt-reader location hint.

Keep all scoring, scanner, Evidence Lab, World Lens, and witness logic untouched.

### Patch 261 — Move Routing to `ui/main.py`

After shell helpers are stable, create:

```text
ui/main.py
```

Target endpoint:

```python
from ui.main import run_app

if __name__ == "__main__":
    run_app()
```

Do not adopt native Streamlit multipage yet. Preserve the current controlled
single-app radio navigation.

### Patch 262 — Shared Session State Extraction

Create a dedicated state module only after routing is stable:

```text
ui/state.py
```

Candidate responsibilities:

- protocol state defaults;
- Evidence Lab / World Lens shared-state checks;
- active DataFrame detection;
- shared protocol-state notice wrapper.

### Patch 263 — Protocol Display Extraction

Move display-only protocol helpers to a dedicated UI module if active checks stay
green:

```text
ui/components/protocol_display.py
```

Candidates:

- `_protocol_public_label`
- `_protocol_humility_note`
- `_protocol_taxonomy_ui_table_df`
- `_protocol_metric_display`

### Patch 264+ — Behavior-Sensitive Helper Extraction

Only after shell/state/display extraction is stable, consider moving behavior
helpers toward `core/`. Each extraction needs active regression tests.

## What not to do next

Do not immediately switch to Streamlit native multipage routing.

Reasons:

- Unit Preview is a pre-app orientation layer.
- Receipt Reader is intentionally a support utility under Why ALETHEIA.
- Evidence Lab and World Lens share state.
- The public boundary requires a controlled review surface.
- Recent patches just stabilized the page extraction and dependency maps.

Native multipage can be reconsidered later, after `app.py` is thin and stable.

## Acceptance criteria for future shell refactors

Future shell patches should preserve:

- current navigation order;
- Unit Preview behavior;
- Receipt Reader location under Why ALETHEIA;
- Mirror Check / Stress Test / Evidence Lab / World Lens page behavior;
- dependency-map calls until replaced by direct imports intentionally;
- active pytest gate;
- no telemetry/storage/external-call changes;
- no scanner, scoring, MEI7, Z-axis, receipt, Evidence Lab, or World Lens math changes.

