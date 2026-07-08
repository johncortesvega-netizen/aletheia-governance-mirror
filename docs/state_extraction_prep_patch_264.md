# Patch 264 — State Extraction Prep

## Goal

Prepare the next state extraction without changing runtime behavior, state key names, default values, lifecycle, routing, scoring, taxonomy logic, or UI meaning.

Patch 264 is deliberately a prep patch. It maps the current Streamlit `st.session_state` substrate so Patch 265 can create `ui/state.py` safely and narrowly.

## Boundary

Patch 264 does **not** create `ui/state.py` and does **not** move any runtime state code.

Do not change in this patch:

- `st.session_state` key names;
- default values;
- reset behavior;
- widget keys;
- Evidence Lab / World Lens synchronization keys;
- Mirror Check history and batch state;
- Stress Test batch/result state;
- Sydney Protocol self-check caching;
- Unit Preview gate behavior;
- router state key `aletheia_active_module`;
- scoring, taxonomy, MEI7, Z-axis, receipts, scanner, or World Lens calculations.

## Current state ownership map

| State area | Keys / pattern | Current owner | Lifecycle | Patch 265 extraction risk |
|---|---|---|---|---|
| Unit Preview gate | `aletheia_unit_preview_passed` via `UNIT_PREVIEW_SESSION_KEY` | `app.py` + `ui/unit_preview.py` | set once after Proceed, then rerun | Medium: stop/rerun ordering must not change |
| Router selection | `aletheia_active_module` | `ui/main.py` | Streamlit radio widget key | Medium: belongs with router, not generic state yet |
| Sydney Protocol self-check | `sydney_protocol_self_check` | `app.py` | lazy cached fail-closed check | High: fail-closed behavior must not drift |
| Sidebar review lens | `sidebar_weight_profile`, `sidebar_steps`, `sidebar_agent_voices`, `sidebar_capture_sensitivity`, `sidebar_alignment_floor` | `app.py` sidebar block | widget defaults + Reset lens button | Medium: widget defaults and reset values must match exactly |
| Shared protocol substrate | `protocol_state` | `app.py` helper `update_protocol_state` | recomputed from evidence/scoring state plus updates | High: cross-module bridge for Audit/Simulation/Grid |
| Evidence Lab core dataframes | `empirical_master_df`, `empirical_scored_df`, `empirical_allocation_df`, `direct_empirical_upload_df` | `ui/pages/evidence_lab.py`, read by `app.py` and `ui/pages/world_lens.py` | uploaded/generated dataframe cache | High: dataframe identity/copy behavior matters |
| Evidence Lab scoring cache | `empirical_active_scoring_signature`, `empirical_active_prepared_df`, `empirical_active_scored_all_df` | `ui/pages/evidence_lab.py` | signature-based cache | High: stale-cache regressions are easy |
| Evidence Lab diagnostics | `empirical_ingest_diagnostics`, `use_generated_master_for_scoring`, `empirical_use_template` | `ui/pages/evidence_lab.py`, read by `app.py` | upload/build toggles and diagnostics display | Medium |
| Evidence/World Lens sync | `aletheia_synced_iso3`, `aletheia_synced_country_name`, `aletheia_synced_evidence_year`, `aletheia_empirical_country_year`, `aletheia_empirical_allocation_year`, `empirical_allocation_year`, `aletheia_global_grid_year`, `grid_year_v2` | `ui/pages/evidence_lab.py` and `ui/pages/world_lens.py` | cross-page country/year synchronization | High: state-sharing is behavior |
| Evidence Lab explorer cache | `empirical_country_year_explorer_active_signature`, `empirical_country_year_explorer_active_payload` | `ui/pages/evidence_lab.py` | selected country-year detail cache | Medium |
| Mirror Check chat state | `chat_audit_history`, `audit_chat_query`, `audit_chat_input_source`, `audit_active_input_signature`, `audit_demo_choice`, `audit_demo_loaded_text`, `chat_audit_query` | `ui/pages/mirror_check.py` | chat history, input source, demo loading | Medium |
| Mirror Check batch state | `audit_batch_archive_bytes`, `audit_batch_index`, `audit_batch_summary`, `audit_batch_count`, `audit_batch_last_source`, `audit_batch_testing_open`, `audit_batch_upload_signature` | `ui/pages/mirror_check.py` | upload/batch summary persistence | Medium |
| Stress Test current result | `last_query`, `last_query_raw`, `last_input_mode`, `last_input_status`, `last_scan`, `last_scan_mode`, `last_features`, `last_sim`, `last_report`, `last_invisibility_report`, `last_stress_semantic_scan`, `last_demo_scenario_text` | `ui/pages/stress_test.py` | latest simulation result and diagnostics | Medium |
| Stress Test input/demo state | `simulation_scenario_text`, `simulation_input_source`, `simulation_demo_choice`, `simulation_demo_resolved_text` | `ui/pages/stress_test.py` | widget and demo source state | Medium |
| Stress Test batch state | `stress_batch_active_signature`, `stress_batch_archive_bytes`, `stress_batch_index`, `stress_batch_summary` | `ui/pages/stress_test.py` | uploaded batch persistence | Medium |

## State keys that Patch 265 must preserve

Patch 265 may centralize only small, proven helpers after these keys are protected by focused tests. It must not rename or reinterpret the following keys:

```text
aletheia_active_module
aletheia_empirical_allocation_year
aletheia_empirical_country_year
aletheia_global_grid_year
aletheia_synced_country_name
aletheia_synced_evidence_year
aletheia_synced_iso3
aletheia_unit_preview_passed
audit_active_input_signature
audit_batch_archive_bytes
audit_batch_count
audit_batch_index
audit_batch_last_source
audit_batch_summary
audit_batch_testing_open
audit_batch_upload_signature
audit_chat_input_source
audit_chat_query
audit_demo_choice
audit_demo_loaded_text
chat_audit_history
chat_audit_query
direct_empirical_upload_df
empirical_active_prepared_df
empirical_active_scored_all_df
empirical_active_scoring_signature
empirical_allocation_df
empirical_allocation_year
empirical_country_year_explorer_active_payload
empirical_country_year_explorer_active_signature
empirical_ingest_diagnostics
empirical_master_df
empirical_scored_df
empirical_use_template
grid_year_v2
last_demo_scenario_text
last_features
last_input_mode
last_input_status
last_invisibility_report
last_query
last_query_raw
last_report
last_scan
last_scan_mode
last_sim
last_stress_semantic_scan
protocol_state
sidebar_agent_voices
sidebar_alignment_floor
sidebar_capture_sensitivity
sidebar_steps
sidebar_weight_profile
simulation_demo_choice
simulation_demo_resolved_text
simulation_input_source
simulation_scenario_text
stress_batch_active_signature
stress_batch_archive_bytes
stress_batch_index
stress_batch_summary
sydney_protocol_self_check
use_generated_master_for_scoring
```

## Candidate extraction for Patch 265

Safe candidates for a first `ui/state.py` pass:

1. constants for sidebar default/reset values;
2. a small `ensure_sidebar_defaults(st)` helper if it preserves widget behavior;
3. a small `reset_sidebar_lens(st)` helper for the existing Reset lens values;
4. possibly protocol-state helper placement **only if** tests first protect dataframe-derived flags.

Risky candidates to defer:

- Evidence Lab dataframe caches;
- World Lens country/year synchronization;
- Mirror Check and Stress Test batch state;
- Sydney Protocol self-check fail-closed cache;
- Unit Preview stop/rerun gate;
- router selection key, unless router tests are updated together.

## Acceptance for Patch 264

- No runtime state movement.
- No `ui/state.py` yet.
- Active suite remains green.
- Patch 265 has a clear state ownership map and a safe extraction boundary.
