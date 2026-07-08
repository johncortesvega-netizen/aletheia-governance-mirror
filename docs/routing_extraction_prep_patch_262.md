# Patch 262 — Routing Extraction Prep

Patch 262 prepares the controlled-router extraction without moving runtime code.

## Goal

Document the current top-level navigation/dispatch contract so the next patch can move the router deliberately instead of rediscovering behavior from failing tests.

## Non-goals

Patch 262 does **not**:

- create or wire `ui/main.py`;
- switch to Streamlit native multipage;
- rename navigation labels;
- change the default selected module;
- change the `st.session_state` key used by the top-level module radio;
- move session-state defaults/helpers;
- move scoring, taxonomy, Z-axis, receipt, Evidence Lab, World Lens, or protocol behavior.

## Current routing owner

For Patch 262, app.py remains the runtime owner of the controlled router.

| Responsibility | Current owner | Patch 263 target | Risk |
|---|---|---|---|
| Top-level navigation labels | `app.py` / `APP_NAVIGATION_LABELS` | likely `ui/main.py` or imported navigation config | medium |
| Streamlit module selector | `app.py` / `st.radio(...)` | `ui/main.py` | medium |
| Active module state key | `aletheia_active_module` in `app.py` radio | preserve exactly | high if renamed |
| Receipt Reader location hint | `app.py` caption above dispatch | preserve near module selector | medium |
| Page dispatch | `app.py` conditional calls | `ui/main.py` | medium/high |
| Why ALETHEIA support utilities | `app.py` branch | preserve Receipt Reader placement | high |
| Footer placement | `app.py` inside Why ALETHEIA branch | preserve existing behavior unless separately changed | medium |

## Current navigation labels and order

The current top-level controlled-router order is:

1. `🪞 Mirror Check`
2. `🚀 Stress Test`
3. `📊 Evidence Lab`
4. `🌐 World Lens`
5. `🧭 Boundary Cases`
6. `📜 Protocol Guide`
7. `ℹ️ Why ALETHEIA`

Receipt Reader is intentionally not a top-level module in this build. It remains under:

`Why ALETHEIA → Support utilities → Receipt Reader — Standard View`

## Current dispatch contract

The top-level radio uses:

- label: `ALETHEIA module`
- options: `APP_NAVIGATION_LABELS`
- `horizontal=True`
- `label_visibility="collapsed"`
- `key="aletheia_active_module"`

Current dispatch targets:

| Selected module | Dispatch target |
|---|---|
| `🪞 Mirror Check` | `render_mirror_check_page(mirror_check_dependency_map(globals()))` |
| `🚀 Stress Test` | `render_stress_test_page(stress_test_dependency_map(globals()))` |
| `📊 Evidence Lab` | `render_evidence_lab_page(evidence_lab_dependency_map(globals()))` |
| `🌐 World Lens` | `render_world_lens_page(world_lens_dependency_map(globals()))` |
| `🧭 Boundary Cases` | `render_boundary_cases_page(...)` with existing protocol-state dependencies |
| `📜 Protocol Guide` | `render_protocol_guide_page()` |
| `ℹ️ Why ALETHEIA` | `render_about_public_info_page(...)`, Support utilities, Receipt Reader Standard View, footer banner |

## Patch 263 extraction target

Patch 263 may create `ui/main.py` and move only:

- selected-page resolution;
- module radio construction;
- page dispatch;
- Receipt Reader location hint if it belongs with router framing.

Patch 263 should not move:

- session-state defaults/helpers;
- static examples/demo data;
- scoring/taxonomy/Z-axis thresholds;
- page-module internals;
- native multipage behavior.

## Acceptance for Patch 262

- Runtime behavior unchanged.
- Active suite remains green.
- A focused active test now protects the current navigation labels, order, selector key, and dispatch targets.
- Future extraction work has a canonical route map to update when `ui/main.py` becomes the router owner.
