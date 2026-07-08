# Patch 263 Recovery Note

If Patch 263 causes routing issues, restore the previous inline router block from Patch 262 at the bottom of `app.py` and remove the `render_controlled_router(...)` delegation plus `ui/main.py`.

The patch is intentionally narrow: it moves only the selected-module radio, Receipt Reader location caption, and page dispatch. It should not require reverting scoring, taxonomy, receipts, Evidence Lab, World Lens, or state logic.
