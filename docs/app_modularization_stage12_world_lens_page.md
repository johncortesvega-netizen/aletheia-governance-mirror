# Patch 244 — App Modularization Stage 12: World Lens Page

## Scope

This patch extracts the World Lens page body from `app.py` into `ui/pages/world_lens.py`.

The extraction uses the same transitional runtime namespace bridge used for earlier heavy page extractions. The page receives `globals()` from `app.py` and executes the preserved World Lens body in that namespace. This keeps existing session-state, data-frame, receipt, and helper behavior intact while reducing `app.py` size.

## Files

- `app.py`
- `ui/pages/world_lens.py`

## Boundary

No governance behavior changes are intended. This patch does not alter:

- scanner logic;
- scoring;
- MEI7 / ethics gate behavior;
- Z-axis mapping;
- Evidence Lab calculations;
- World Lens math;
- 9k seat allocation rules;
- receipts or witness schema;
- telemetry or storage behavior.

## Test focus

After applying, verify:

1. World Lens opens from the top-level module selector.
2. Optional context note / semantic pressure guide works.
3. World Lens context dial works.
4. Grid basis selector works.
5. Selected-year allocation, Verdicts, Integrity & Collapse, Comparisons, Trust & Sources, Coverage, Country-Year Detail, and Report Packet internal tabs render.
6. Evidence Lab state still feeds World Lens.
7. Only one top-level module renders at a time.
