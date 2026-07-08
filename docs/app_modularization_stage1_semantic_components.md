# App Modularization Stage 1: Semantic Pressure Components

**Patch:** 221  
**Status:** Ready for local review  
**Scope:** UI/component extraction only

## Purpose

Patch 221 starts the app modularization plan without changing ALETHEIA's behavior. It extracts the shared Semantic Pressure UI helpers from the monolithic `app.py` into a dedicated component module:

```text
ui/components/semantic_pressure_panel.py
```

The goal is to reduce `app.py` size and make future page extraction safer while preserving all existing readings, pressure codes, guidance, Stress Test/Evidence Lab/World Lens wiring, and Receipt Reader boundaries.

## What moved out of app.py

The following shared UI/helper functions were moved into `ui/components/semantic_pressure_panel.py`:

- `render_semantic_pressure_panel`
- `render_semantic_stress_triggers`
- `render_semantic_evidence_check`
- `render_world_lens_semantic_flags`
- `semantic_stress_trigger_rows`
- `semantic_evidence_implication_rows`
- `semantic_world_lens_flag_rows`
- `choose_stress_semantic_scan`
- `choose_strongest_semantic_scan`

Private helper functions used by those components moved with them.

## What stayed in app.py

`app.py` still owns the top-level Streamlit tabs, session-state flow, module composition, and page orchestration. This patch does **not** refactor pages yet.

## Boundary preservation

This patch does not modify:

- Semantic scanner logic
- scoring
- MEI7 gate behavior
- Z-axis behavior
- Stress Test metrics
- Evidence Lab calculations
- World Lens math
- Receipt schema
- telemetry/storage behavior
- authority or certification boundaries

## Validation

Run:

```bat
python -m py_compile app.py ui\components\semantic_pressure_panel.py
python -m pytest
python -m streamlit run app.py
```

Expected active-suite result:

```text
5 passed
```

## Review checklist

After applying the patch, manually check:

- Mirror Check still shows semantic pressure signals.
- Stress Test still shows semantic stress triggers and pressure-code cards.
- Evidence Lab still shows semantic claim/mechanism evidence check.
- World Lens still shows semantic regional interpretation flags.
- Pressure-code guidance remains visible behind the semantic details.

If any module loses semantic output, restore `app.py` from the prior patch and re-check imports from `ui.components.semantic_pressure_panel`.
