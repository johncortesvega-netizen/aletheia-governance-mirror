# PATCH 190 Recovery Note — Original Governance Mirror Design Restore

If this patch causes problems, revert the Patch 190 files listed in `PATCH_190_MANIFEST.txt` and restore the previous Patch 189 identity from the archived artifacts.

Expected restored direction:
- Main public identity: ALETHEIA / Governance Mirror.
- App version marker: `v1.0-original-governance-mirror-p1`.
- Main logo asset: `assets/aletheia_robot_laurel_logo.png`.
- Navigation labels: `Protocol Guide` and `Why ALETHEIA`.
- Preview Unit visual: original laurel robot guide, not stop/go officer framing.
- Public copy: audit, simulation, evidence, global comparison, reports, open source, and human review.

Rollback note:
- To return to the Patch 189 rebrand state, restore `app.py`, `ui/app_shell.py`, `ui/unit_preview.py`, `pages_ui/about_page.py`, `pages_ui/evidence_lab_page.py`, README, and the affected tests from the previous checkout.
- Recreate Patch 189 root artifacts from `docs/patch_archive/` only if you need the previous root artifact layout.

Boundary preserved:
- Patch 190 is UI/copy/test-hygiene only.
- It does not change scoring, routing, taxonomy, receipt generation, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, storage, telemetry, certification, enforcement, or authority behavior.
- ALETHEIA remains a mirror, not a throne. Human review remains required.
