# Thin Entrypoint Refactor Plan — Patch 259

Patch 259 defines the next safe refactor direction after the modularization
bridge-removal sequence.

## Principle

Do not change the navigation model before the shell is thin.

The next phase should reduce `app.py` without changing what users see, how pages
are selected, how state flows between Evidence Lab and World Lens, or where
Receipt Reader appears.

## Preferred path

1. Inventory `app.py` responsibilities. Completed in Patch 259.
2. Extract shell helpers while preserving current routing.
3. Move routing to `ui/main.py` while preserving current radio navigation.
4. Extract shared state helpers.
5. Extract display-only protocol helpers.
6. Only then decide whether Streamlit native multipage helps.

## Near-term target structure

```text
app.py                         # eventual thin entrypoint
ui/main.py                     # controlled single-app router
ui/app_shell_runtime.py         # header/sidebar/footer/shell helpers
ui/state.py                    # session-state helpers
ui/components/protocol_display.py
ui/components/
ui/pages/
core/
config/
```

## Why not native multipage yet?

Native multipage may eventually be useful, but it is not the safest immediate
step. ALETHEIA has a deliberate single controlled review flow, a pre-app Unit
Preview gate, shared Evidence Lab / World Lens state, and a Receipt Reader that
must remain a support utility rather than a main review tab.

The safer near-term goal is a thin entrypoint, not a new navigation model.

## Runtime boundary

This plan is documentation-only. It changes no runtime behavior, scanner logic,
scoring, MEI7 routing, Z-axis mapping, receipt schema, Evidence Lab calculation,
World Lens math, telemetry, storage, external calls, or authority-boundary copy.
