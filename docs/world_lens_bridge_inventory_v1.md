# World Lens Bridge Inventory v1
**Patch:** 252 — World Lens Bridge Inventory / Prep  
**Status:** planning-only / no runtime change  
**Context:** Post Patch 251, before removing the final `globals()` bridge from `ui/pages/world_lens.py`.

## Purpose
World Lens is the last major page still using a broad runtime namespace bridge. This document records the dependencies that must be made explicit before `render_world_lens_page(globals())` is replaced with a narrow dependency map.

The goal is not to change World Lens behavior. The goal is to make the final bridge-removal patch safer by naming every dependency group before code is changed.

## Current bridge risk
World Lens is the most sensitive remaining page because it combines:

- selected-year public data;
- 9k allocation views;
- country/year detail tables;
- internal tab navigation;
- Evidence Lab state sharing;
- semantic pressure flags;
- report packet generation;
- trust/source/coverage displays;
- several formatting and dataframe helpers.

A direct removal of `globals()` without inventory risks import errors, broken state transfer, or silent changes in World Lens interpretation. Therefore Patch 252 is documentation-only prep.

## Dependency groups to preserve

### 1. Streamlit and data utilities
Likely needed directly or indirectly:

- `st`
- `pd`
- `np`
- `go` / Plotly helpers when used by charts
- dataframe normalization helpers
- safe formatting helpers
- local CSS/card helpers

### 2. World Lens data sources
World Lens should keep using the same public-data loading path and the same selected-year behavior. Dependencies may include:

- WGI/world governance data loaders;
- country/year dataframe builders;
- coverage calculators;
- selected-year selectors;
- allocation/grid basis constants;
- country detail lookup helpers.

### 3. 9k allocation logic
These must remain audit-lens only:

- 9k allocation calculations;
- population-weighted representation helpers;
- selected-year allocation validators;
- partial/incomplete-year guardrails;
- display formatting for allocation tables.

Boundary: 9k remains a representative audit lens, not a mandate claim, world parliament, certification layer, or executive system.

### 4. Evidence Lab state sharing
World Lens currently reads some Evidence Lab state from `st.session_state`. The bridge removal must preserve:

- active Evidence Lab table/state;
- active evidence-source signature;
- user-uploaded or synthetic data selection;
- semantic/evidence context where used;
- safe handling when Evidence Lab has not been run.

Bridge removal must not make World Lens infer, invent, or silently overwrite Evidence Lab state.

### 5. Semantic pressure integration
World Lens uses semantic pressure as a subordinate diagnostic layer. Dependencies include:

- `scan_semantic_pressure(...)`;
- semantic pressure panel/flag renderers;
- pressure-code mappings;
- regional/contextual interpretation text;
- no-signal handling.

Boundary: semantic pressure flags support human review. They do not override World Lens data, certify a region, or produce final truth claims.

### 6. UI components
Likely explicit imports after bridge removal:

- `metric_card(...)` / `soft_card(...)`;
- module header/notice helpers;
- semantic pressure flag/panel helpers;
- any local report-card helpers still in `app.py`;
- expander/table rendering utilities.

### 7. Report packet generation
The final bridge removal must preserve:

- current report packet text;
- selected-year context;
- evidence context summary;
- source/trust notes;
- download buttons or text blocks;
- wording that avoids authority or certification claims.

### 8. Session-state keys to preserve
Patch 253 should identify the exact keys used by World Lens before changing code. Candidate categories:

- selected year;
- selected country/region;
- selected internal World Lens tab;
- active Evidence Lab input/table state;
- semantic context note;
- report packet text/state;
- grid/allocation basis choices.

No key should be renamed in the bridge-removal patch unless a compatibility alias is added.

## Proposed Patch 253 code shape
Patch 253 should replace the broad bridge with a named dependency map, similar to Mirror Check, Stress Test, and Evidence Lab:

```python
render_world_lens_page(world_lens_dependency_map(globals()))
```

Inside `ui/pages/world_lens.py`, the page should read only named entries from the dependency map and fail clearly if a required dependency is missing.

## Acceptance criteria for Patch 253
After bridge removal:

- World Lens opens without import errors.
- Optional context note still works.
- Semantic pressure guide/details still render.
- Grid basis selector still works.
- All internal World Lens tabs still render:
  - Overview
  - Allocation
  - Verdicts
  - Integrity & Collapse
  - Comparisons
  - Trust & Sources
  - Coverage
  - Country-Year Detail
  - Report Packet
- Evidence Lab state still feeds World Lens when available.
- World Lens remains one top-level module only under navigation containment.
- No scoring, scanner, MEI7, Z-axis, 9k math, Evidence Lab calculations, receipts, or authority-boundary behavior changes.
