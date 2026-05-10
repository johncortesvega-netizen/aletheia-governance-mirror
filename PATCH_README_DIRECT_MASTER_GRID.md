# ALETHEIA v9.6.8 Direct Master / Global Grid Patch

This patch hardens the Empirical Study -> Global Grid handoff.

## What changed

- Direct merged evidence uploads now show source diagnostics before scoring.
- Previously exported ALETHEIA scored master/Grid CSVs are detected and preserved instead of being neutralized by a second scoring pass.
- Direct scored masters still pass the identity and modern-year guard.
- Source diagnostics distinguish:
  - WGI source values
  - V-Dem source values
  - raw WVS/OWID trust survey values
  - ALETHEIA empirical trust prior values
- `empirical_trust_prior` is preserved through preparation/collapse/scoring and can be used as a fallback trust prior when raw `wvs_generalized_trust` is unavailable.
- Scored empirical outputs now carry through raw WGI, V-Dem, trust, and external validation columns directly from the scoring helper.
- Global Grid labels raw survey trust separately from trust prior so a complete master with trust priors does not look like it has raw OWID/WVS trust coverage.

## Interpretation

- Raw trust coverage means rows with a source survey value such as `wvs_generalized_trust`.
- Trust prior coverage means rows with an ALETHEIA-ready trust prior, including preserved values from an already-scored master.
- WGI coverage remains 0% when the active file has WGI columns but no usable numeric values.
- The Grid remains selected-year based; 9k allocation is not summed across all country-years.
