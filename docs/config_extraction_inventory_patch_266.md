# Patch 266 — Config Extraction Inventory

Patch 266 is a prep-only patch for future configuration/static-data extraction. It does **not** create `ui/config.py`, `ui/constants.py`, `ui/examples.py`, or `ui/labels.py`, and it does **not** move runtime constants out of `app.py`.

The goal is to identify which app-level values are safe static UI/config candidates and which values are behavior-sensitive and must stay with their current owners until a separate, narrowly tested extraction is justified.

## Patch boundary

- No runtime behavior change.
- No import-order change.
- No scoring, taxonomy, Z-axis, allocation, or receipt logic movement.
- No navigation move; Patch 263 already made `ui/main.py` the controlled-router owner.
- No state move; Patch 265 already made `ui/state.py` the narrow sidebar state owner.
- Future config extraction must move only values with a clear canonical owner and active test coverage.

## Current config/static-data surface

| Current value/block | Current owner | Candidate future owner | Patch 267 extraction risk | Notes |
|---|---|---|---|---|
| `APP_VERSION` | `app.py` | `ui/config.py` | low | Display/static release identifier only if no tests depend on import order. |
| `SUPPORTED_INPUT_LANGUAGE_NOTE` | `app.py` | `ui/labels.py` or `ui/config.py` | low | Static copy; safe only if wording stays identical. |
| `ABOUT_HEADER_IMAGE`, `MASCOT_LOGO_IMAGE`, `VISUAL_SOURCE_FILES` | `app.py` | `ui/config.py` or `ui/examples.py` | low/medium | Static asset references, but use `PROJECT_ROOT`; move only with path tests. |
| `APP_UX_POLISH_SUMMARY` | `app.py` | `ui/labels.py` | low | Static UI guidance copy. |
| `DEMO_INPUT_FILES` | `app.py` | `ui/examples.py` | low | Static demo-file metadata; keep `load_demo_input` behavior unchanged. |
| `MIRROR_CHECK_DEMO_SCENARIOS` | `app.py` | `ui/examples.py` | low/medium | Static scenario examples, but module-specific UI depends on exact keys/text. |
| `STRESS_TEST_DEMO_SCENARIOS` | `app.py` | `ui/examples.py` | low/medium | Static scenario examples; keep labels/text stable. |
| `SCENARIOS` compatibility alias | `app.py` | likely stay until callers/tests are retired | medium | Backward-compatibility alias; do not remove during config cleanup. |
| `STRESS_TEST_DEFAULTS` | `app.py` | `ui/examples.py` | medium | Static multiline demo text but semantically loaded; move only with exact-content tests. |
| `APP_NAVIGATION_LABELS`, `APP_NAVIGATION_MAP` | `app.py` feeding `ui/main.py` | maybe `ui/main.py` or `ui/labels.py` | medium | Routing contract is already protected by Patch 262/263. Do not rename, reorder, or change default behavior. |
| `DEMOGRAPHIC_BRACKETS` | `app.py` | likely not yet | high | Used by prototype allocation behavior. Treat as behavior-sensitive until allocation tests cover it. |
| `WORLD_BANK_AGGREGATE_ISO3` | `app.py` | likely not yet | high | Directly affects 9k allocation denominator and country filtering. Not safe config. |
| `TOTAL_9K` | `app.py` | likely not yet | high | Allocation/scaffold behavior-sensitive. Do not move in Patch 267. |
| `REVIEW_BAND_LABELS` | `app.py` | likely not yet | high | Display labels are coupled to review-band behavior; do not move without band tests. |
| `MISSING_SAFEGUARD_NEGATION_PATTERNS` | `app.py` | likely not yet | high | Detection behavior-sensitive. Do not move as static copy. |
| `SOURCE_CONFORMANCE_MATRIX` | `app.py` | likely not yet | medium/high | Looks static, but source-conformance interpretation may affect UI meaning. Move only after focused tests. |
| `MIN_FULL_GRID_COUNTRIES` | `app.py` | likely not yet | high | World Lens/data-validity behavior-sensitive. Do not move in Patch 267. |

## Safe-first candidates for Patch 267

Patch 267 may extract only clearly static UI/demo surfaces, preferably in one small module and one small test:

1. `APP_VERSION`
2. `SUPPORTED_INPUT_LANGUAGE_NOTE`
3. `APP_UX_POLISH_SUMMARY`
4. `DEMO_INPUT_FILES`
5. possibly `MIRROR_CHECK_DEMO_SCENARIOS` and `STRESS_TEST_DEMO_SCENARIOS`, if exact key/text tests are added first

## Not safe for Patch 267

Do **not** move these in the next patch:

- `TOTAL_9K`
- `DEMOGRAPHIC_BRACKETS`
- `WORLD_BANK_AGGREGATE_ISO3`
- `REVIEW_BAND_LABELS`
- `MISSING_SAFEGUARD_NEGATION_PATTERNS`
- `MIN_FULL_GRID_COUNTRIES`
- scoring thresholds
- taxonomy/Z-axis boundary logic
- allocation denominator logic
- receipt reader parsing or display meaning
- Evidence Lab / World Lens data validity gates

## Acceptance for Patch 266

- Config extraction inventory exists.
- Runtime code remains unchanged except patch status/notes.
- No new config modules are introduced yet.
- Active suite remains green.
- Patch 267 has a clear safe/risky boundary.
