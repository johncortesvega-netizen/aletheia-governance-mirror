# Patch S2.1B — Evidence Lab duplicate widget key fix

## Changed
- `app.py`

## Fix
Streamlit was still able to render more than one semantic pressure panel on the same page with identical content-derived widget keys. Evidence Lab triggered the same `Normalized scan text` key pattern when the semantic panel appeared in more than one context.

This patch adds an optional `panel_key` argument to `render_semantic_pressure_panel(...)` and assigns stable module-specific keys for:

- Mirror Check latest semantic pressure panel
- Stress Test semantic pressure panel
- Evidence Lab claim/mechanism semantic panel

## Scope
- No scoring changes.
- No scanner logic changes.
- No receipt schema changes.
- UI stability fix only.

## Check
`python -m py_compile app.py`
