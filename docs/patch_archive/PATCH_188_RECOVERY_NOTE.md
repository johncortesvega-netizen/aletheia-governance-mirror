# Patch 188 Recovery Note — Robot Officer Visual Integration

## What this patch does
Patch 188 adds the friendly cardboard ALETHEIA robot officer visual identity to the Preview Unit and main app shell. The main mascot asset is now the robot officer with STOP / GO signs, and the Preview Unit has a visual guidance card that says pause, check, ask, and proceed carefully.

## What this patch does not do
It does not alter scoring, routing, taxonomy, receipts, Evidence Lab, World Lens, AI static scan behavior, protocol logic, storage, telemetry, certification, enforcement, or authority behavior.

## Recovery steps
If the new visual assets fail to render:
1. Confirm these files exist:
   - `assets/ai_patrol_officer_stop_go.png`
   - `assets/ai_patrol_officer_preview.png`
   - `assets/ai_patrol_officer_character_sheet.png`
2. Confirm `app.py` points `MASCOT_LOGO_IMAGE` to `assets/ai_patrol_officer_stop_go.png`.
3. Confirm `ui/unit_preview.py` contains `get_unit_preview_officer_image_uri()` and the `unit-preview-officer-card` markup/CSS.
4. Revert only this patch's changed files to restore the Patch 187 visual state.

## Validation
Run:

```bat
python tools\run_patch_checks.py 188
python -m pytest -q tests/test_patch_188_robot_officer_visual_integration.py tests/test_patch_187_stacked_brand_and_full_app_logo.py tests/test_patch_185_aletheia_ai_patrol_branding.py
python -m py_compile app.py ui/app_shell.py ui/unit_preview.py
```
