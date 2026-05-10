# Patch 63 — Post-62 Release Refresh

Status: release refresh after Patch 61A–61E and Patch 62.

## Purpose

Patch 63 updates the public release surface after the World Lens and Simulation calibration series.
It makes the latest post-62 state visible in the README, About page, public release notes, progress database, and patch status files.

## What changed before this refresh

- Patch 61A added ASYLUM / High-risk repair questions so high-risk outputs do not end with an empty repair path.
- Patch 61B calibrated malicious-leadership metrics so hostile leadership prompts cannot display perfect trust/alignment without concrete safeguards.
- Patch 61C scoped Country-Year Explorer years to the selected country and blocked silent global/default fallback.
- Patch 61D clarified missing raw trust by separating observed raw trust from neutral trust-prior fallback values.
- Patch 61E added selected-year World Lens value guards.
- Patch 62 consolidated the 61A–61E changes into one regression smoke check.

## Release interpretation

The post-62 release state is still diagnostic only.
ALETHEIA remains a mirror, not a throne.

It may identify risk, missing safeguards, missing evidence, unclear trust priors, stale country-year selection, or repair gaps.
It must not command, enforce, vote, govern, remove leaders, validate spiritual authority, create Global ID sync, create a public ledger, or replace human judgment.

## Current recommended checks

```bat
tools\run_checks.bat
tools\run_patch_checks.bat 63
```

For the consolidated post-61 smoke check:

```bat
tools\run_patch_checks.bat 62
```

## Current release note

ALETHEIA v1.0 plus the post-62 refresh includes the completed public MVP and the latest calibration fixes for Simulation and World Lens interpretation.
