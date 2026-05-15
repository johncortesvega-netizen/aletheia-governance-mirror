# Patch 71.2 Recovery Note — Tree Canopy + Caption Visual Polish

Patch 71.2 is UI-only.

## What changed

The explanatory tree visual in `app.py` now uses a layered ellipse canopy instead of the older loose circle stack. The caption `Visual tree score is explanatory; receipt integrity remains the protocol metric.` is rendered below the SVG visual, not inside the dark tree card.

## What did not change

- No scoring logic changed.
- No receipt fields changed.
- No risk taxonomy changed.
- No demo or batch fixtures changed.
- No authority boundary changed.

ALETHEIA remains a local mirror only: no legal, political, institutional, religious, medical, or automated authority claim; no enforcement; no public ledger; no Global ID sync; no central storage; human review remains required.

## Recovery

If the tree visual appears visually worse after applying this patch, restore the previous `render_pulse_tree` implementation from the Patch 71.1 working zip. Protocol outputs and receipts should remain comparable because this patch only changes presentation markup.

## Verification

Run:

```bat
tools\run_patch_checks.bat 71_2
```
