# Patch UI-TABS-1 — Module Tab Containment Fix

## Problem
After switching between ALETHEIA modules, multiple module bodies could appear visually stacked on the page. This made it look like Mirror Check, Stress Test, Evidence Lab, World Lens, Boundary Cases, Protocol Guide, and Why ALETHEIA were all open at once.

## Change
- Adds fail-closed CSS containment rules for Streamlit tab panels.
- Explicitly hides tab panels marked `hidden` or `aria-hidden="true"`.
- Adds a modern `:has(...)` fallback so only the selected module panel remains visible if Streamlit/browser styling fails to collapse inactive panels.

## Changed files
- `app.py`

## Notes
This patch does not change scoring, scanner logic, receipts, or module behavior. It only restores the intended single-module visual surface.
