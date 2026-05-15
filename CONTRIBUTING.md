# Contributing to ALETHEIA

ALETHEIA welcomes careful contributions that preserve the core boundary: it is a governance mirror, not an authority.

## Before contributing

Read these first:

- `README.md`
- `docs/structural_improvement_entrypoint.md`
- `docs/architecture.md`
- `docs/signal_detection.md`
- `docs/SIGNAL_DICTIONARY.md`
- `docs/BOUNDARY.md`
- `docs/privacy_boundary.md`
- `docs/hosting_limits.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`


## Core rules (non-negotiable)

1. Respect the **mirror, not throne** philosophy.
2. Never add functionality that removes, bypasses, or replaces human judgment.
3. Never add telemetry, analytics, tracking, backend upload endpoints, Global ID sync, public ledger sync, or central user-input storage without explicit human review and public boundary documentation.
4. Keep ALETHEIA local-first by default.
5. Keep hosted-use language bounded: hosted deployments may have platform-level logs outside ALETHEIA's application code.
6. Do not describe ALETHEIA as a privacy guarantee, security guarantee, compliance approval, ethics certification, legal finding, or final truth system.

## Contribution rule

Do not make ALETHEIA more authoritative. Contributions should improve clarity, reviewability, transparency, maintainability, testing, documentation, accessibility, or local-first usability.

ALETHEIA must not claim to certify truth, safety, privacy, security, legality, ethics, legitimacy, political authority, religious authority, medical authority, or institutional authority.

## Safe contribution areas

Good first contribution areas include:

- documentation clarity;
- public boundary copy;
- test coverage;
- example inputs;
- typo fixes;
- accessibility improvements;
- non-authoritative UI explanations;
- local setup improvements;
- small behavior-preserving refactors.

## High-review areas

Changes in these areas require extra care:

- scoring logic;
- verdict routing;
- ASYLUM / THRESHOLD / SANCTUARY taxonomy;
- receipt schema;
- privacy posture;
- external-call behavior;
- app-wide authority-boundary copy;
- World Lens empirical mapping;
- AI Integrity signal categories;
- signal patterns, signal weights, or language-calibration claims.

## Prohibited direction

Do not add features that turn ALETHEIA into an enforcement, certification, ranking, surveillance, identity-sync, or final-decision mechanism.

Examples of prohibited claims or directions:

- automatic governance decisions;
- model-wide AI certification;
- legal/medical/political/religious authority;
- public ledger authority;
- Global ID sync;
- central user-input storage by default;
- hidden telemetry or analytics;
- vendor ranking as final truth;
- safety, security, or privacy guarantees.

## Signal-detection transparency

ALETHEIA uses transparent rule-based and heuristic signal detection in key review paths. This is a reviewability and privacy choice, not a claim that the system understands all nuance. Contributors should preserve the public signal basis: strongest calibration is English and Dutch/Nederlands, subtle context may be missed, and human review remains required.

Do not describe signal readings as verdicts, proof, certification, automated approval, legal findings, or final truth. Use `docs/SIGNAL_DICTIONARY.md` as a reviewer-facing glossary only; it is not a scoring specification and must not be used to invent untested weights.


## Reviewer-readiness path

Before proposing code changes, use the reviewer path introduced in Patch 143:

1. Read `docs/reviewer_start_here.md`.
2. Read `docs/glossary.md` for project-specific terms before interpreting scores or module names.
3. Run `python tools/run_protocol_baseline_self_audit.py` and treat any difference as a human-review prompt, not as an automated release decision.
4. Use `docs/how_to_review_aletheia_without_trusting_it.md` to inspect the boundary claims directly.
5. Use `docs/validation_and_precision.md` before making claims about scores, precision, or validation.

Contributions should improve reviewability without turning ALETHEIA into a certification, enforcement, approval, rejection, ranking, surveillance, or final-decision system.

## Patch workflow

ALETHEIA uses small reviewable patches. A patch should normally include:

- changed files only;
- patch-specific tests when appropriate;
- `PATCH_<id>_MANIFEST.txt`;
- `PATCH_<id>_RECOVERY_NOTE.md`;
- `PATCH_STATUS.md` update;
- `docs/progress_database.md` update.

Run the relevant patch check:

```bat
tools\run_patch_checks.bat 104
```

Run broader checks when needed:

```bat
tools\run_checks.bat
```

## Local-first and privacy

For sensitive audits, run ALETHEIA locally. The repository is designed without built-in external model calls, telemetry, analytics SDKs, trackers, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Hosted deployments can still have hosting-layer logs, request metadata, crash logs, or operational monitoring outside ALETHEIA's application-code boundary. See `docs/BOUNDARY.md` and `docs/hosting_limits.md`.


## Patch-history navigation

ALETHEIA has a long patch trail by design. New contributors should not try to read everything at once. Start with:

1. `docs/new_contributor_start_here.md`
2. `docs/architecture.md`
3. `docs/BOUNDARY.md`
4. `docs/signal_detection.md`
5. `docs/SIGNAL_DICTIONARY.md`
6. `docs/privacy_boundary.md`
6. `docs/hosting_limits.md`
7. `docs/patch_index.md`
8. `docs/public_trust_package.md`

Then inspect the specific `PATCH_*_MANIFEST.txt`, `PATCH_*_RECOVERY_NOTE.md`, and patch-specific test file for the change you are reviewing.

The patch trail supports human review. It is not a certification, guarantee, or substitute for code inspection.
