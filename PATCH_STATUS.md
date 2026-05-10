# ALETHEIA Patch Status

This file is the compact local patch ledger for ALETHEIA v0.1. Longer implementation notes live in `docs/progress_database.md`.

| Patch | Name | Status |
|---|---|---|
| 33 | Baseline v0.1 + Safe Language + Eternal Baseline | Passed |
| 34 | Boundary Cases Matrix | Passed |
| 35 | Failure Classification | Passed |
| 36 | Patch Automation Toolkit | Passed |
| 36.1 | Automation Script Hotfix + Safe Check Workflow | Passed |
| 37 | Consent-Audit Engine | Passed |
| 38 | Mechanism-vs-Claim Scanner | Passed |
| 39 | Self-Audit Mode | Passed |
| 40 | Evidence Lab + Extraordinary Claim Protocol | Passed |
| 41 | Local Witness Receipt v2 | Passed |
| 42 | World Lens Simulation | Passed |
| 43 | Protocol Guide Consolidation | Passed |
| 44 | Progress Database + Patch Status Hardening | Passed |
| 45 | Public README + Limitations Polish | Passed |
| 46 | Sample Reports / Example Audits | Passed |
| 47 | App Navigation + Smoke Test Cleanup | Passed |
| 48 | Release Candidate Checklist | Passed |
| 49 | Full Test Suite / Legacy Test Cleanup | Passed |
| 50 | v0.1 Release Package | Passed |
| 51 | Git Diff Workflow Setup | Passed |
| 52 | Optional UX Polish | Passed |
| 53 | Final v0.1 Smoke Release | Passed |
| 54 | Example Audit Runner / Demo Inputs | Passed |
| 55 | GitHub Cleanup Package | Passed |
| 56–60 | v1 Finalization Bundle | Passed |
| 61A | Asylum Repair Questions | Passed |
| 61B | Malicious Leadership Metric Calibration | Passed |
| 61C | Country-Year Available-Year Filter | Passed |
| 61D | Missing Raw Trust Display | Passed |
| 61E | World Lens Value Guards | Passed |
| 62 | Post-61 Regression Smoke Test | Current |

## Current Patch

Patch 62 — Post-61 Regression Smoke Test

## Current Check Command

```bat
tools\run_patch_checks.bat 62
```

## Safe Default Check

```bat
tools\run_checks.bat
```

## Next Logical Patch

Patch 63 — optional GitHub-ready cleanup / deployment smoke, or hold v1 if no new issue is found.

## Workflow Rule

When the user says `next patch`, treat the previous patch as passed and continue from the latest working project state.

## Patch 55 Boundary

Patch 55 is public repository packaging only. It does not add governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger authority, neural validation, religious validation, legal authority, or automated enforcement.


## Patch 56–60 Boundary

Patch 56–60 finalizes ALETHEIA v1.0 as a public MVP package and adds future-planning documentation. It does not add governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger authority, neural validation, religious validation, legal authority, or automated enforcement.

## Patch 61A — Asylum Repair Questions

Status: Passed.

Adds a high-risk repair-question guard so ASYLUM / High / Malicious Leadership outputs include Silent Operator repair questions instead of an empty repair path. This remains mirror-only and human-review-only.

Check command:

```bat
tools\run_patch_checks.bat 61A
```

## Patch 61B — Malicious Leadership Metric Calibration

Status: Passed.

Caps perfect trust/alignment and raises the ego signal for malicious leadership scenarios unless concrete safeguards are present. This is metric calibration only; it adds no enforcement or authority.

Check command:

```bat
tools\run_patch_checks.bat 61B
```

## Patch 61C — Country-Year Available-Year Filter

Status: Passed.

Scopes the Country-Year Explorer year dropdown to the selected country only. Prevents stale/global/default year fallback and adds clear country-specific available-year wording.

Check command:

```bat
tools\run_patch_checks.bat 61C
```

## Patch 61D — Missing Raw Trust Display

Status: Passed.

Clarifies World Lens trust interpretation by separating observed raw trust evidence from neutral trust-prior fallback values. Missing raw trust is displayed as `not available`, and neutral priors are labeled as `0.500 neutral default`.

Check command:

```bat
tools\run_patch_checks.bat 61D
```

## Patch 61E — World Lens Value Guards

Status: Passed.

Adds deterministic selected-year guards for World Lens. It verifies selected-year seat totals, focus-country values, no-stale-year behavior, verdict-seat derivation, and clear trust-prior interpretation.

Check command:

```bat
tools\run_patch_checks.bat 61E
```

## Patch 62 — Post-61 Regression Smoke Test

Status: ready for local verification.

Consolidates 61A–61E with one regression smoke test across Simulation and World Lens. Confirms ASYLUM repair questions, malicious-leadership metric calibration, country-year filtering, missing raw-trust labeling, selected-year 9k seat guards, and Netherlands 2024 fixture stability.

Check command:

```bat
tools\run_patch_checks.bat 62
```


## Patch 63 — Post-62 Release Refresh

Status: Ready for local verification.

Updates README, About, public release notes, progress database, and release-refresh docs after Patch 61A–61E and Patch 62. This is release-surface hardening only; it adds no governance authority or enforcement.

Check command:

```bat
tools\run_patch_checks.bat 63
```

## Patch 64 — Mirror Check Batch Baseline Validation

Status: Ready for local verification.

Records three 50-question Mirror Check batch baselines and documents the expected `QUESTION_PROMPT` receipt contract: 50 receipts, 50 JSON receipts, no scenario-hash mismatches, no normal scoring, and authority boundary preserved.

Check command:

```bat
tools\run_patch_checks.bat 64
```

## Patch 65 — Stress Test Prompting Guide + Batch Baseline

Status: Ready for local verification.

Adds Stress Test scenario-writing guidance, an official 50-scenario Stress Test baseline, and an explicit opt-in local Stress Test batch tester. The batch runner produces local Simulation receipts only and preserves the authority boundary.

Check command:

```bat
tools\run_patch_checks.bat 65
```

## Patch 66 — Stress Test Risk Sensitivity Calibration

Status: Delivered

Raises Stress Test sensitivity for missing appeal, no term limits, biometric access pressure, consent under pressure, fallback-data confusion, founder control, surveillance, and non-meaningful human review. Subtle stress cases now route to `THRESHOLD / Needs Safeguards`; hard capture remains `ASYLUM / High`.

## Patch 67 — Stress Test Threshold Repair + Metric Softening

Status: Delivered

Adds repair questions and light metric softening for `THRESHOLD / Needs Safeguards` Stress Test outputs. Medium-risk scenarios no longer display perfect trust/alignment and zero ego while still requiring safeguards. ASYLUM behavior remains unchanged.

Check:

```bat
tools\run_patch_checks.bat 67
```
