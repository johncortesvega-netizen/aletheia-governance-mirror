# PATCH 194 Recovery Note — Unit Preview Poster References Opt-In Polish

If this patch causes problems, revert the Patch 194 files listed in `PATCH_194_MANIFEST.txt` and restore the previous Patch 193 state from the archived artifacts.

Expected restored direction:
- Main public identity remains ALETHEIA / Governance Mirror.
- App version marker: `v1.0-original-governance-mirror-p5`.
- Preview Unit visual posters are available only after opening the collapsed `Open visual reference posters` expander.
- Visible poster captions describe orientation purpose and do not mention patch-history replacement wording.

Rollback note:
- To return to the Patch 193 state, restore `app.py` and `ui/unit_preview.py` from the previous checkout.
- Recreate Patch 193 root artifacts from `docs/patch_archive/` only if you need the previous root artifact layout.

Boundary preserved:
- Patch 194 is UI/copy/test-hygiene only.
- It does not change scoring, routing, taxonomy, receipt generation, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, storage, telemetry, certification, enforcement, or authority behavior.
- ALETHEIA remains a mirror, not a throne. Human review remains required.
