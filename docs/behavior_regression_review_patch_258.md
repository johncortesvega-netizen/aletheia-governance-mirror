# Patch 258 — Behavior Regression Review

Patch 258 adds a small active behavior-regression review layer after the legacy-test
quarantine and modularization path repair work.

## Why this patch exists

The full historical test triage found one remaining high-noise bucket: items that
could include real behavioral regressions, stale documentation assertions, old
patch-contract assumptions, or tests whose failure output was attached to the
wrong file during bulk parsing.

Patch 258 does not try to bulk-rewrite that entire mixed bucket. Instead, it
creates a narrow current-release behavior contract for the public examples and
semantic-pressure patterns that must remain stable after modularization.

## What changed

Added:

- `tests/active/test_behavior_regression_review.py`

Updated:

- `tests/README.md`
- `PATCH_STATUS.md`
- `PATCH_NOTES.md`

The new active test checks current deterministic semantic behavior for:

- opaque hidden-power claims;
- emergency authority with weak safeguards;
- claim/mechanism gaps;
- identity-gated public-benefit access;
- concrete safeguard language.

These tests intentionally avoid brittle exact-value contracts for older
calibration scores unless those values represent the current active public
behavior. They assert the review posture: pressure signals must route to human
review, and concrete safeguards must remain low-pressure.

## What did not change

No runtime behavior changed. This patch does not modify:

- scanner logic;
- scoring;
- MEI7;
- Z-axis behavior;
- receipts;
- Stress Test calculations;
- Evidence Lab calculations;
- World Lens math;
- telemetry/storage;
- privacy posture;
- authority-boundary language.

## How to interpret the remaining legacy behavior bucket

The remaining legacy failures should be reviewed in this order:

1. Separate stale documentation/path assertions from actual output assertions.
2. For actual output mismatches, compare against the current public boundary and
   active examples, not only against old patch-era numeric expectations.
3. Restore a historical test only when it still describes the current release
   contract.
4. Archive or delete a historical test when it describes a superseded contract.
5. Add a new active regression test when a behavior is current and important.

## Interpretation rule

A behavior-regression test should protect the mirror boundary, not freeze every
old implementation detail.

The active question is:

> Does the current behavior still surface review-needed governance pressure
> without becoming an authority, certifier, enforcer, or final-truth system?
