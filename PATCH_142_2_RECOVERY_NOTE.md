# Patch 142.2 Recovery Note — Unit Preview Scenario Intent Hotfix

Patch 142.2 is a small Unit Preview hotfix. If the patch needs to be reverted, restore `ui/unit_preview.py` to the Patch 142.1 version and remove `tests/test_patch_142_2_unit_preview_scenario_intent.py`, `PATCH_142_2_MANIFEST.txt`, and this note.

The intended behavior after the patch is that scenario-shaped prompts route to **Stress Test** before the Mirror Check fallback. The regression case is:

> an evil penguin rises to power after a revolution

This should suggest Stress Test, not Mirror Check.

The compact button row is UI placement only. The packaged reference previews remain local and below the buttons.

No scoring, verdict routing, taxonomy, QUESTION_PROMPT logic, receipt schema, receipt generation, signal regex or weights, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, upload/download behavior, external calls, live model calls, embeddings, telemetry, analytics, database/storage, certification, enforcement, approval/rejection behavior, privacy guarantee, or final-truth claim changed. Human review remains required.
