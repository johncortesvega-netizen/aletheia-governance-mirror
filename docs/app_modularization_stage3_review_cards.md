# Patch 231 — App Modularization Stage 3: Review Cards

## Purpose
Patch 231 continues the low-risk modularization path by extracting shared review-card rendering helpers from `app.py` into `ui/components/review_cards.py`.

The goal is maintainability only: repeated UI card rendering for result explanations, repair questions, and fallback recommendations now lives in a reusable component module.

## Changed files
- `app.py`
- `ui/components/review_cards.py`
- `docs/app_modularization_stage3_review_cards.md`
- `PATCH_STATUS.md`
- `PATCH_231_MANIFEST.txt`
- `PATCH_231_RECOVERY_NOTE.md`
- `PATCH_231_DELETE_LIST.txt`

## Extracted helpers
- `render_soft_card_grid(...)`
- `render_repair_question_cards(...)`
- `render_recommendation_cards(...)`

## Boundary
This patch is presentation-only. It does not change:
- scanner logic
- scoring
- MEI7 gate
- Z-axis
- Stress Test math
- Evidence Lab calculations
- World Lens math
- receipts
- telemetry
- authority boundaries

## Test focus
After applying, verify:
1. Stress Test still renders "Why this result?" cards.
2. Stress Test repair questions still render.
3. Fallback recommendations still render if no repair questions exist.
4. Mirror Check, Evidence Lab, and World Lens still open without traceback.
