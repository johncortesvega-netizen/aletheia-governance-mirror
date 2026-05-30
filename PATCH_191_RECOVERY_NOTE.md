# PATCH 191 Recovery Note — Original Mascot Asset Refresh + Warm Preview Palette

If this patch causes problems, revert the Patch 191 files listed in `PATCH_191_MANIFEST.txt` and restore the previous Patch 190 state from the archived artifacts.

Expected restored direction:
- Main public identity remains ALETHEIA / Governance Mirror.
- App version marker: `v1.0-original-governance-mirror-p2`.
- Main mascot/logo asset now matches the approved top-right concept robot.
- About header returns to the warm concept header image.
- Preview Unit mascot card uses a warm cream/green/red palette rather than a blue-tinted card.

Rollback note:
- To return to the Patch 190 state, restore `app.py`, `ui/unit_preview.py`, and the three refreshed asset files from the previous checkout.
- Recreate Patch 190 root artifacts from `docs/patch_archive/` only if you need the previous root artifact layout.

Boundary preserved:
- Patch 191 is visual/UI/test-hygiene only.
- It does not change scoring, routing, taxonomy, receipt generation, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, storage, telemetry, certification, enforcement, or authority behavior.
- ALETHEIA remains a mirror, not a throne. Human review remains required.
