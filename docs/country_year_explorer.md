# Patch 61C — Country-Year Available-Year Filter

Patch 61C hardens the Country-Year Explorer so the year control is scoped to the selected country rather than a global year range.

## Problem

The interface could read as if every country had the full global range of available years. When a country had missing data, that made stale/default-year behavior hard to see.

## Rule

When a country is selected, ALETHEIA computes available years from rows for that country/ISO3 only.

- No silent fallback to a previous country.
- No silent fallback to a global/default year.
- No stale selected-year display.
- No invented country-year row.

## User-facing wording

The explorer should say:

```text
Available years for Netherlands · NLD: 1996–2024.
```

If the selected country has gaps, the list can show only those years:

```text
Available years for Country X · XXX: 2004, 2008, 2012, 2020, 2024.
```

If no country-year data is available, the app should show a warning and stop the country-year review path rather than falling back to another country or year.

## Boundary

This patch only hardens year-selection interpretation. It does not add Global ID sync, real 9k selection, automatic resets, enforcement, or authority claims.
