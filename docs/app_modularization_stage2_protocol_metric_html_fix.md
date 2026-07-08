# Patch 230 — Protocol Metric HTML Rendering Fix

## Purpose
Patch 230 repairs a presentation regression introduced during Stage 2 metric-card modularization.

The Stress Test protocol-reading card already built trusted internal HTML snippets for colored emphasis. After extraction into `ui/components/metric_cards.py`, the shared card helper escaped all values by default, causing the HTML markup to appear as visible text.

## Change
- `metric_card(...)` remains escaped by default.
- Internal callers may explicitly opt into trusted internal HTML via:
  - `value_is_html=True`
  - `helper_is_html=True`
- The Stress Test protocol-reading card now opts in because its HTML is generated internally by the app, not user input.

## Boundary
This is presentation-only.
No scanner logic, scoring, MEI7 gate, Z-axis, Stress Test math, Evidence Lab calculations, World Lens math, receipts, telemetry, or authority behavior changed.
