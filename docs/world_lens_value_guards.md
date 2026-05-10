# Patch 61E — World Lens Value Guards

Patch 61E locks the World Lens interpretation layer with deterministic selected-year guards.

The goal is to prevent silent fallback, stale country-year display, or confusing seat totals after the Country-Year Explorer and trust-prior display patches.

## Guard rules

World Lens must verify:

- selected-year rows are tied to the selected year only;
- 9k allocation totals are interpreted per selected year;
- full selected-year grids should sum to approximately 9,000 seats;
- focus-country cards must come from the selected country and selected year;
- verdict-seat totals must be derived from the active selected-year rows;
- missing raw trust remains labeled as missing, not measured;
- neutral trust-prior fallback remains visible as a fallback, not observed survey evidence.

## Mirror boundary

These guards are diagnostic checks. They do not create governance authority, legal authority, automatic reset, Global ID sync, public ledger authority, or enforcement.

ALETHEIA reflects.
Humans review.
Power stays accountable.
