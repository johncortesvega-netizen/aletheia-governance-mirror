# Patch 267 — Safe Config Extraction

Patch 267 performs the first narrow config/static-data extraction prepared by Patch 266.

## Goal

Move only low-risk static UI/config surfaces out of `app.py` while preserving runtime behavior, navigation, taxonomy logic, scoring, allocation, and receipt semantics.

## Extracted canonical owners

| Value | Old owner | New owner | Risk | Notes |
|---|---|---|---|---|
| `APP_VERSION` | `app.py` | `ui/config.py` | low | Static display/release identifier. |
| `SUPPORTED_INPUT_LANGUAGE_NOTE` | `app.py` | `ui/config.py` | low | Static boundary copy; wording preserved. |
| `APP_UX_POLISH_SUMMARY` | `app.py` | `ui/examples.py` | low | Static UI guidance list. |
| `DEMO_INPUT_FILES` | `app.py` | `ui/examples.py` | low | Static demo-file metadata only. Demo loading behavior remains in `app.py`. |

## Runtime boundary

Patch 267 does **not** move:

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
- demo scenario maps
- navigation labels/order/default behavior

## Acceptance

- `app.py` imports the extracted static values from `ui.config` and `ui.examples`.
- The extracted values are not still assigned in `app.py`.
- Behavior-sensitive constants still live in `app.py`.
- `load_demo_input()` remains in `app.py` and continues to resolve bundled files through `PROJECT_ROOT`.
- Active suite remains green.
