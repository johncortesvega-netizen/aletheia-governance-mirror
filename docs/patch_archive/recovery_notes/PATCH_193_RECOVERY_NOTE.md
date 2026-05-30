# PATCH 193 Recovery Note — Unit Preview Visual Reference Poster Refresh

If this patch causes problems, revert the Patch 193 files listed in `PATCH_193_MANIFEST.txt` and restore the previous Patch 192 state from the archived artifacts.

Expected restored direction:
- Main public identity remains ALETHEIA / Governance Mirror.
- App version marker: `v1.0-original-governance-mirror-p4`.
- Preview Unit reference area shows four poster-style local visual references instead of the old two HTML previews.
- The earlier pink/blue Sydney Protocol preview surfaces are replaced by the new Command Dossier and Architect's Checklist posters.

Rollback note:
- To return to the Patch 192 state, restore `app.py`, `ui/unit_preview.py`, and the four `assets/visual_cards/` poster images from the previous checkout.
- Recreate Patch 192 root artifacts from `docs/patch_archive/` only if you need the previous root artifact layout.

Boundary preserved:
- Patch 193 is UI/asset/test-hygiene only.
- It does not change scoring, routing, taxonomy, receipt generation, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, storage, telemetry, certification, enforcement, or authority behavior.
- ALETHEIA remains a mirror, not a throne. Human review remains required.
