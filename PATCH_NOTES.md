# Patch S3.1 — Semantic UI Cleanup

Changed files:
- `app.py`

Purpose:
- Keep semantic-pressure output useful for normal users while moving developer-heavy material deeper into the UI.

Changes:
- `render_semantic_pressure_panel(...)` still shows the compact user-facing layer:
  - state
  - claims
  - mechanisms
  - diagnostic integrity pressure
  - summary message
  - notes and secondary metrics inside `Show semantic scan details`
- Contextual proximity hit tables moved into a nested expander:
  - `Developer/debug details`
- Normalized scan text moved under `Developer/debug details`.
- Plain-text semantic report moved under `Developer/debug details` → `Plain-text semantic report`.
- No scanner logic, scoring, receipts, World Lens flags, Stress Test metrics, or Evidence Lab calculations changed.

Validation:
- `python -m py_compile app.py` passes.
