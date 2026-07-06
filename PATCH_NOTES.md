# Patch S1 — Mirror Check semantic pressure integration

Changed file:
- `app.py`

What changed:
- Adds a shared `render_semantic_pressure_panel(...)` helper.
- Runs `scan_semantic_pressure(...)` during Mirror Check review.
- Stores semantic pressure payloads in the local scan/report entry.
- Renders a subordinate **Semantic pressure signals** panel directly below the main Mirror Check reading.
- Shows compact semantic metrics:
  - state
  - claim count
  - mechanism count
  - diagnostic integrity pressure
- Keeps details behind an expander:
  - notes
  - proximity hits
  - normalized text
  - plain text semantic report

Boundary:
- This patch does **not** make the semantic scanner the final judge.
- It does **not** rescore, certify, approve, reject, or enforce.
- It adds relationship-aware pressure signals under Mirror Check for human review.

Syntax check:
- `python -m py_compile app.py` passed in patch workspace.
