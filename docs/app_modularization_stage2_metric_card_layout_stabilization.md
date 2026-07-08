# Patch 228 — Metric Card Layout Stabilization

## Purpose
Patch 228 stabilizes the visual behavior of the modularized `metric_card(...)` and `soft_card(...)` helpers introduced in Patch 227.

After Stage 2 extraction, some cards could become too narrow inside Streamlit column containers, especially long status/classification cards in Stress Test and explanatory cards in Mirror Check. This patch keeps the component extraction but restores stable block-level layout behavior.

## Changes
- `ui/components/metric_cards.py`
  - Adds explicit component classes: `aletheia-metric-card`, `aletheia-soft-card`, and related label/body classes.
  - Keeps helpers presentation-only.
  - Does not compute, rescore, classify, or route any reading.
- `app.py`
  - Adds CSS guardrails so modularized metric/soft cards render full-width inside their parent Streamlit containers.
  - Adds wrapping rules for long labels, values, and helper text.
  - Uses responsive value font sizing for narrow columns.

## Boundary
No runtime governance behavior changes:
- no scanner logic changes;
- no semantic pressure changes;
- no scoring changes;
- no MEI7 gate changes;
- no Z-axis changes;
- no Stress Test metric changes;
- no Evidence Lab calculation changes;
- no World Lens math changes;
- no receipt changes;
- no telemetry/storage changes.

## Validation focus
After applying this patch, manually check:
- Stress Test process-reading/status card no longer collapses into a narrow word column.
- Stress Test metric cards remain aligned.
- Mirror Check explanatory cards wrap normally.
- World Lens metric/status cards still render normally.
- Navigation containment still shows one active module body at a time.
