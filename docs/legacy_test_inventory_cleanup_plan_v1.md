# ALETHEIA Legacy Test Inventory Cleanup Plan
**Patch:** 219  
**Status:** Cleanup governance / documentation-only  
**Scope:** Historical tests, active release checks, patch regressions, and cleanup labels

## 1. Purpose

Patch 218 made the default pytest command collect the active suite only. Patch 219 explains what happens next: the old test tree must not be hidden, ignored, or presented as passing when it is not. It must be treated as a legacy inventory that is triaged openly.

This plan separates test reliability from historical preservation:

- active release tests remain the default gate;
- patch-specific regressions remain available for focused checks;
- legacy tests are inventoried, labelled, restored, archived, or deleted;
- documentation must never imply that the entire historical test tree passes unless it actually does.

This is part of the mirror boundary. ALETHEIA should apply evidence-integrity standards to its own repository.

## 2. Current test categories

### ACTIVE_RELEASE_GATE

Tests that are expected to pass under the default command:

```bat
python -m pytest
```

These tests live under:

```text
tests/active/
```

A failure here should block release-candidate claims until resolved.

### PATCH_REGRESSION

Patch-specific tests added to preserve a recent behavior or boundary. These may be run directly while a patch is being reviewed.

Examples:

```bat
python -m pytest tests/test_patch_214_regression_guardrails.py -q
```

Stable patch regressions can later be promoted into `tests/active/`.

### LEGACY_INVENTORY

Older tests retained for historical review. These may reference superseded modules, old UI flows, renamed functions, removed receipt fields, or earlier patch assumptions.

Legacy inventory is not a release gate until triaged.

### RESTORE_CANDIDATE

A legacy test whose purpose is still valid, but whose imports, expected fields, or module path need updating.

Restore candidates should be rewritten against current public/core APIs and then promoted into either `tests/active/` or a stable patch-regression location.

### DELETE_CANDIDATE

A legacy test that no longer describes the current app, current architecture, or current boundary model and does not provide useful regression value.

Deletion should be recorded in a patch manifest or cleanup note.

### ARCHIVED_HISTORICAL

A test or test fixture that is kept only as development history. It should not be run by default and should not be cited as active validation.

## 3. Triage workflow

For each legacy test file:

1. Identify what behavior it was originally trying to protect.
2. Check whether that behavior still exists in the current architecture.
3. Assign one label: `RESTORE_CANDIDATE`, `DELETE_CANDIDATE`, or `ARCHIVED_HISTORICAL`.
4. If restored, update imports and assertions to current modules and terminology.
5. If deleted or archived, record why.
6. Promote only stable, current, boundary-relevant tests into `tests/active/`.

## 4. Promotion rule

A restored test can move into the active release gate only when it meets all of these conditions:

- it imports from current modules;
- it does not depend on removed UI/session-state internals;
- it checks a current boundary, scanner, receipt, evidence, or World Lens behavior;
- it passes consistently in a clean local environment;
- it does not assert final truth, certification, enforcement, or authority claims.

## 5. What should be restored first

High-value restoration candidates:

1. Mirror boundary tests: no automated judging, no final authority, no false `SANCTUARY` for authoritarian prompts.
2. Semantic pressure tests: opaque capture, weak emergency safeguards, identity-gated access, claim/mechanism gaps.
3. Receipt tests: local-only receipt generation and reader non-rescoring behavior.
4. World Lens tests: 9k remains an audit lens and incomplete years do not claim full validation.
5. Evidence Lab tests: claim support, evidence gaps, and Extraordinary Claim Protocol boundaries.

Low-value candidates for deletion or archival:

- tests for removed function names;
- tests for old UI text that has been intentionally rewritten;
- tests that assert obsolete patch numbers as behavior;
- tests that validate deprecated modules or old experimental demos;
- tests that duplicate active guardrail coverage without adding new risk coverage.

## 6. README language standard

Acceptable wording:

> The active release-gate suite passes under the default pytest configuration. Legacy tests are retained as inventory and are being triaged.

Unacceptable wording unless true:

> The full test suite passes.

> All historical tests are green.

> The repository is fully validated.

## 7. Boundary note

Test cleanup is not cosmetic. It protects the credibility of the mirror. If ALETHEIA asks users to distinguish evidence from claims, the repository must distinguish active checks from historical artifacts.
