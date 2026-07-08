# Patch 265 — State Extraction

Patch 265 performs the first narrow runtime state extraction after the Patch 264 inventory.

## Scope

This patch creates `ui/state.py` and moves only the safest shared state surface:

- sidebar review-lens legacy profile normalization;
- sidebar review-lens reset defaults.

## New canonical owner

`ui/state.py` now owns the sidebar review-lens default contract:

| Key | Default |
|---|---:|
| `sidebar_weight_profile` | `Starting preset` |
| `sidebar_steps` | `40` |
| `sidebar_agent_voices` | `6` |
| `sidebar_capture_sensitivity` | `0.55` |
| `sidebar_alignment_floor` | `0.45` |

It also preserves the legacy migration:

- old value `Default` is normalized to `Starting preset`.

## Runtime behavior preserved

`app.py` still renders the sidebar controls and widget keys. It now delegates the two state mutations to:

- `normalize_sidebar_lens_state(st.session_state)`
- `reset_sidebar_lens_state(st.session_state)`

The visible sidebar behavior, widget keys, labels, slider ranges, and defaults are unchanged.

## Explicit non-scope

Patch 265 does not move:

- `aletheia_active_module` router selection;
- `aletheia_unit_preview_passed` Unit Preview gate;
- `sydney_protocol_self_check` caching;
- `protocol_state` shared substrate;
- Evidence Lab dataframes or cache signatures;
- Evidence/World Lens country-year sync keys;
- Mirror Check chat or batch state;
- Stress Test current-result or batch state;
- scoring, taxonomy, Z-axis, receipt parsing, telemetry/storage, or native multipage behavior.

## Patch 266 boundary

The next safe step is a config/static-data inventory. Do not use Patch 266 to move behavior-sensitive scoring constants, taxonomy thresholds, Z-axis boundary logic, or state lifecycles.
