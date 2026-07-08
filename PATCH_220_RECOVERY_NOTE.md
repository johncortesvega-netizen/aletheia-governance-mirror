# Patch 220 — Streamlit Tab Inactive-Panel Guard

## Why this patch exists
After several interactions, Streamlit tabs could intermittently render inactive panels as visible, making Evidence Lab / World Lens / other module content appear as one long continuous page inside a single selected tab.

Patch 202 intentionally removed broad tab-mapping CSS because it could create its own tab-containment failures. Patch 220 keeps the safer approach but adds support for Streamlit/BaseWeb inactive-panel attributes beyond the literal `hidden` attribute.

## What changed
`app.py` CSS now hides tab panels that Streamlit itself marks as inactive via:

- `hidden`
- `aria-hidden="true"`
- `data-state="inactive"`

The patch does **not** use:

- `:has()`
- `nth-of-type`
- fixed tab-order assumptions
- manual active-tab selection logic

## What did not change
No runtime logic changed:

- no scanner changes
- no scoring changes
- no MEI7 gate changes
- no Z-axis changes
- no Evidence Lab math changes
- no World Lens math changes
- no receipt changes
- no pytest config changes
- no telemetry/storage changes

## Recovery
If tab rendering worsens, revert only the Patch 220 CSS block in `app.py` back to the Patch 202 native-hidden-panel rule.
