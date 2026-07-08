# Contributing to ALETHEIA

ALETHEIA welcomes careful contributions that preserve the core boundary:

> ALETHEIA reflects. Humans review. Power stays accountable.

ALETHEIA is a governance mirror, not an authority. It helps surface governance-risk signals, evidence gaps, pressure patterns, missing safeguards, and review questions. It does not certify, enforce, approve, reject, rank, monitor, or replace human judgment.

---

## Philosophy first, code second

Before changing code, confirm that the change preserves the project boundary:

`Power -> Mirror. Never Mirror -> Power.`

A useful contribution should make ALETHEIA clearer, easier to inspect, easier to run locally, easier to test, easier to review, or easier to maintain.

A contribution should not make ALETHEIA:

- more authoritative;
- more hidden;
- more centralized;
- more like an approval system;
- more like a final decision mechanism;
- more dependent on unverifiable or opaque logic.

For first-time contributors, start with:

1. `README.md`
2. `docs/public_positioning_v1.md`
3. `docs/rules_based_transparency_v1.md`
4. `docs/test_suite_triage_v1.md`
5. `docs/modularization_final_audit_v1.md`
6. `docs/how_to_review_aletheia_without_trusting_it.md`

---

## What ALETHEIA is and is not

ALETHEIA uses transparent, rule-based and heuristic signal detection in key review paths. It is not a machine-learning risk model, predictive engine, scientific instrument, legal authority, ethics certifier, or automated judge.

The system may use weighted formulas, pressure codes, proximity checks, semantic patterns, and deterministic routing. These are review signals, not measurements of truth.

Do not describe ALETHEIA outputs as:

- proof;
- verdicts;
- certification;
- automated approval;
- legal findings;
- scientific validation;
- final truth;
- safety guarantees;
- privacy guarantees;
- institutional authority.

Use language like:

- internal review label;
- diagnostic signal;
- pressure pattern;
- evidence gap;
- human-review prompt;
- repair question;
- governance-risk indicator.

---

## Before contributing

Read these first:

- `README.md`
- `CONTRIBUTING.md`
- `docs/BOUNDARY.md`
- `docs/privacy_boundary.md`
- `docs/hosting_limits.md`
- `docs/rules_based_transparency_v1.md`
- `docs/test_suite_triage_v1.md`
- `docs/legacy_test_inventory_cleanup_plan_v1.md`
- `docs/modularization_final_audit_v1.md`
- `docs/modularization_bridge_inventory_v1.md`
- `docs/namespace_bridge_removal_plan_v1.md`
- `PATCH_STATUS.md`
- `PATCH_NOTES.md`
- `docs/patch_archive/README.md`

For signal-language work, also read:

- `docs/signal_detection.md`
- `docs/SIGNAL_DICTIONARY.md`
- `docs/validation_and_precision.md`

---

## Core rules

1. Respect the **mirror, not throne** philosophy.
2. Never add functionality that removes, bypasses, or replaces human judgment.
3. Never turn ALETHEIA into an enforcement, certification, ranking, surveillance, identity-sync, or final-decision system.
4. Keep ALETHEIA local-first by default.
5. Do not add telemetry, analytics, tracking, backend upload endpoints, Global ID sync, public ledger sync, or central user-input storage without explicit human review and public boundary documentation.
6. Keep hosted-use language bounded: hosted deployments may have platform-level logs outside ALETHEIA’s application-code boundary.
7. Do not describe ALETHEIA as a privacy guarantee, security guarantee, compliance approval, ethics certification, legal finding, or final truth system.
8. Keep rule-based and heuristic scoring transparent. Do not present formulas as scientific laws, predictive truth, or objective legitimacy.

---

## Safe contribution areas

Good first contribution areas include:

- documentation clarity;
- typo fixes;
- accessibility improvements;
- local setup improvements;
- public boundary copy;
- reviewer guidance;
- test coverage for active checks;
- example inputs;
- pressure-code explanation clarity;
- non-authoritative UI explanations;
- behavior-preserving refactors;
- modularization cleanup that does not alter outputs.

---

## High-review areas

Changes in these areas require extra care:

- scoring logic;
- verdict routing;
- MEI7 / ethics-gate behavior;
- Z-axis mapping;
- ASYLUM / THRESHOLD / SANCTUARY taxonomy;
- pressure-code definitions;
- semantic-pressure scanner patterns;
- signal weights or language calibration;
- receipt schema;
- witness receipt generation;
- privacy posture;
- external-call behavior;
- app-wide authority-boundary copy;
- World Lens empirical mapping;
- 9k allocation logic;
- Evidence Lab calculations;
- Stress Test metrics;
- any feature that could be mistaken for certification, enforcement, approval, ranking, or final judgment.

---

## Prohibited direction

Do not add features or language that turn ALETHEIA into:

- an automated governance decision system;
- a model-wide AI certification system;
- a legal, medical, political, religious, or institutional authority;
- a public ledger authority;
- a Global ID sync layer;
- a central user-input storage system by default;
- a surveillance or monitoring system;
- a vendor ranking system presented as final truth;
- a safety, security, privacy, or compliance guarantee.

Examples of prohibited claims or directions:

- “ALETHEIA certifies this policy.”
- “ALETHEIA proves this is safe.”
- “ALETHEIA approves this system.”
- “ALETHEIA determines legitimacy.”
- “ALETHEIA replaces human review.”
- “ALETHEIA guarantees privacy/security/compliance.”
- “ALETHEIA should enforce outcomes.”

---

## Signal-detection transparency

ALETHEIA uses transparent rule-based and heuristic signal detection in key review paths. This is a reviewability and privacy choice, not a claim that the system understands all nuance.

Contributors should preserve the public signal basis:

- ALETHEIA is English-first.
- Dutch/Nederlands examples may be used for batch testing, but full multilingual semantic coverage is not claimed.
- Subtle context may be missed.
- Rule-based detection can over-trigger or under-trigger.
- Human review remains required.
- Pressure codes are reviewer aids, not truth labels.
- `docs/SIGNAL_DICTIONARY.md` is a reviewer-facing glossary, not a scoring specification.

Do not invent untested weights, hidden categories, or authority-sounding labels.

---

## Test strategy

ALETHEIA now separates active release checks from legacy test inventory.

Default test command:

```bat
python -m pytest
```

The default pytest configuration should run the active suite only, normally under:

```text
tests/active/
```

This means:

- active checks must stay green;
- legacy tests are not automatically treated as release blockers;
- failing legacy tests must not be hidden or misrepresented;
- legacy tests should be triaged according to the cleanup plan.

Read:

- `docs/test_suite_triage_v1.md`
- `docs/legacy_test_inventory_cleanup_plan_v1.md`
- `docs/test_migration_labels_v1.md`
- `tests/README.md`

Use labels such as:

- `ACTIVE_RELEASE_GATE`
- `PATCH_REGRESSION`
- `LEGACY_INVENTORY`
- `RESTORE_CANDIDATE`
- `DELETE_CANDIDATE`
- `ARCHIVED_HISTORICAL`

Do not claim “all tests pass” unless the full intended test scope is explicitly stated.

---

## Patch workflow

ALETHEIA uses small, reviewable patches. A patch should normally include:

- changed files only;
- patch-specific tests when appropriate;
- `PATCH_<id>_MANIFEST.txt`;
- `PATCH_<id>_RECOVERY_NOTE.md`;
- `PATCH_<id>_DELETE_LIST.txt`;
- `PATCH_STATUS.md` update;
- `PATCH_NOTES.md` update;
- documentation update when the patch affects contributor, reviewer, boundary, test, or architecture expectations.

Root-level patch files should remain limited to the current patch. Older patch files should be archived under:

```text
docs/patch_archive/manifests/
docs/patch_archive/recovery_notes/
docs/patch_archive/delete_lists/
```

The patch trail supports human review. It is not a certification, guarantee, or substitute for code inspection.

---

## Local checks

Run basic checks before submitting:

```bat
python -m py_compile app.py ui\components\*.py ui\pages\*.py
python -m pytest
```

When working on a specific patch, also run the relevant patch check if available:

```bat
tools\run_patch_checks.bat <patch_id>
```

Run broader checks when needed:

```bat
tools\run_checks.bat
```

`tools\run_checks.bat` may represent the current active safety/release path, not the entire historical test inventory. If a change touches tests, document what was run and what was intentionally out of scope.

---

## Modularization rules

ALETHEIA has been modularized into shared components and pages.

Shared UI components live under:

```text
ui/components/
```

Page modules live under:

```text
ui/pages/
```

Contributors should keep UI rendering separate from governance logic where practical.

Current modularization expectations:

- page modules should avoid broad `globals()` handoffs;
- dependencies should be explicit where possible;
- behavior-preserving refactors should not change scanner output, scoring, MEI7 routing, Z-axis mapping, receipts, Evidence Lab calculations, World Lens math, or authority-boundary language;
- any bridge-removal or dependency-injection change should include tests and documentation.

Read:

- `docs/modularization_final_audit_v1.md`
- `docs/modularization_bridge_inventory_v1.md`
- `docs/namespace_bridge_removal_plan_v1.md`
- `docs/modularization_post_bridge_cleanup_roadmap_v1.md`

---

## Local-first and privacy

For sensitive audits, run ALETHEIA locally.

The repository is designed without built-in:

- external model calls by default;
- telemetry;
- analytics SDKs;
- trackers;
- backend upload endpoints;
- public ledger sync;
- Global ID sync;
- central user-input database.

Hosted deployments can still have hosting-layer logs, request metadata, crash logs, or operational monitoring outside ALETHEIA’s application-code boundary.

Read:

- `docs/BOUNDARY.md`
- `docs/privacy_boundary.md`
- `docs/hosting_limits.md`

Do not describe hosted use as equivalent to local privacy.

---

## Reviewer-readiness path

Before proposing code changes, use this review path:

1. Read `docs/reviewer_start_here.md`.
2. Read `docs/glossary.md` before interpreting scores or module names.
3. Read `docs/rules_based_transparency_v1.md`.
4. Read `docs/how_to_review_aletheia_without_trusting_it.md`.
5. Read `docs/validation_and_precision.md` before making claims about scores, precision, or validation.
6. Run the active checks:

```bat
python -m pytest
```

7. If touching protocol baseline behavior, run:

```bat
python tools/run_protocol_baseline_self_audit.py
```

Treat any difference as a human-review prompt, not as an automated release decision.

---

## Patch-history navigation

ALETHEIA has a long patch trail by design. New contributors should not try to read everything at once.

Start with:

1. `docs/new_contributor_start_here.md`
2. `README.md`
3. `docs/public_positioning_v1.md`
4. `docs/rules_based_transparency_v1.md`
5. `docs/BOUNDARY.md`
6. `docs/privacy_boundary.md`
7. `docs/signal_detection.md`
8. `docs/SIGNAL_DICTIONARY.md`
9. `docs/test_suite_triage_v1.md`
10. `docs/modularization_final_audit_v1.md`
11. `docs/patch_archive/README.md`
12. `PATCH_STATUS.md`
13. `PATCH_NOTES.md`

Then inspect the specific `PATCH_*_MANIFEST.txt`, `PATCH_*_RECOVERY_NOTE.md`, `PATCH_*_DELETE_LIST.txt`, and patch-specific test file for the change you are reviewing.

---

## Final contribution principle

Contributions should improve reviewability without turning ALETHEIA into a certification, enforcement, approval, rejection, ranking, surveillance, or final-decision system.

When in doubt, preserve the boundary:

> Mirror, not throne.
