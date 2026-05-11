# Stress Test Batch Baseline

Patch 65 adds a first Stress Test batch baseline for Simulation review.

## Purpose

The baseline helps test whether Stress Test handles scenario-style inputs correctly while preserving the ALETHEIA authority boundary.

## Expected behavior

For each batch scenario:

- Module is `Simulation`.
- Input status is user-supplied scenario input.
- Authority claim remains `False`.
- Human review remains required.
- Public ledger remains `False`.
- Global ID sync remains `False`.
- Central storage remains `False`.
- High-risk or ASYLUM results produce repair questions.
- Malicious leadership scenarios do not return perfect trust/alignment without safeguards.

## Baseline file

The baseline scenario list is stored at:

```text
examples/batch_scenarios/stress_test_scenarios_en_v1.txt
```

This is a test fixture and a user-facing example. It is not a policy dataset and not an authority source.


## Patch 71 official scenario files

The official Stress Test batch filenames are cataloged in `docs/batch_file_catalog.md`:

- `examples/batch_scenarios/stress_test_scenarios_en_v1.txt` — EN baseline, latest verified distribution `THRESHOLD 46 / ASYLUM 4 / SANCTUARY 0`.
- `examples/batch_scenarios/stress_test_scenarios_nl_v1.txt` — NL baseline, latest verified distribution `THRESHOLD 50 / ASYLUM 0 / SANCTUARY 0`.
- `examples/batch_scenarios/governance_language_stress_test_en.txt` — EN advanced governance-language stress set, latest verified distribution `THRESHOLD 29 / ASYLUM 21 / SANCTUARY 0`.

Older filenames may remain as local compatibility aliases, but new docs and release notes should use the official names.
