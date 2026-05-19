# Patch 185 Recovery Note — Aletheia AI Patrol Branding Alignment

Patch 185 is a small branding/visual patch. It updates visible app-shell and Preview Unit labels to **Aletheia: AI PATROL** and adds a Preview Unit-only CSS rule that flips the header mascot orientation.

To revert this patch manually:
1. In `ui/app_shell.py`, restore the previous hero/sidebar labels if desired.
2. In `ui/unit_preview.py`, restore the previous Preview Unit title/button wording and remove the Patch 185 `scaleX(-1)` CSS rule.
3. Remove `tests/test_patch_185_aletheia_ai_patrol_branding.py`.
4. Restore `tests/test_patch_166_ai_patrol_rebrand.py` if the earlier Patch 166 wording is preferred.
5. Remove the Patch 185 entries from `PATCH_STATUS.md` and `docs/progress_database.md`.

No scoring, routing, taxonomy, receipt, storage, telemetry, certification, enforcement, or protocol logic is changed by this patch.
