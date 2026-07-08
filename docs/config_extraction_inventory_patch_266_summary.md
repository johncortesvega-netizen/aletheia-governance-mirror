# Patch 266 summary — Config Extraction Inventory

Patch 266 documents the safe/risky boundary for future config/static-data extraction.

## Runtime status

No runtime config movement. No `ui/config.py`, `ui/constants.py`, `ui/examples.py`, or `ui/labels.py` is created in this patch.

## Safe-first candidates for Patch 267

- `APP_VERSION`
- `SUPPORTED_INPUT_LANGUAGE_NOTE`
- `APP_UX_POLISH_SUMMARY`
- `DEMO_INPUT_FILES`
- scenario demo maps only with exact-content tests

## Explicitly out of scope for Patch 267

- `TOTAL_9K`
- `DEMOGRAPHIC_BRACKETS`
- `WORLD_BANK_AGGREGATE_ISO3`
- `REVIEW_BAND_LABELS`
- `MISSING_SAFEGUARD_NEGATION_PATTERNS`
- `MIN_FULL_GRID_COUNTRIES`
- scoring/taxonomy/Z-axis thresholds
- allocation logic
- data-validity gates

Next patch: Patch 267 may perform a narrow safe config extraction, not a broad constants cleanup.
