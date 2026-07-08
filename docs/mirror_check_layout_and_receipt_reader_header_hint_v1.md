# Patch 241 — Mirror Check Layout Cleanup and Receipt Reader Header Hint

## Purpose
This patch cleans up Mirror Check's explanatory reading panels after page extraction and makes the Receipt Reader location visible from the global module header.

## Changes
- Replaces the uneven two-column Mirror Check explanation layout with sequential, full-width expanders.
- Keeps threshold-direction values in readable tables rather than narrow metric cards.
- Moves component-level threshold details behind a nested expander.
- Adds a global header caption: Receipt Reader is available under Why ALETHEIA → Support utilities → Receipt Reader — Standard View.

## Boundary
This patch is UI/copy only. It does not change governance scoring, semantic scanning, receipts, MEI7 logic, Z-axis mapping, Evidence Lab math, World Lens math, telemetry, or authority boundaries.
