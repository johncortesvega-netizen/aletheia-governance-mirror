# ALETHEIA Test Suite Triage v1
**Patch:** 217  
**Status:** Test-hygiene documentation  
**Scope:** Documentation only; no test runner or runtime change

## Purpose

This document clarifies how to interpret ALETHEIA's checks during the release-candidate refinement phase. It exists because the repository contains both active release checks and historical/legacy test files from earlier patch contracts.

A passing current check must not be described as proof that every historical test file in the repository passes. Evidence integrity requires a clear distinction between active gates and archived inventory.

## Current categories

### 1. Active release checks

These are the checks intended for the current release-candidate surface. They are the default local safety check.

Typical command:

```bat
tools\run_checks.bat
```

Expected interpretation:

> The current curated release/patch checks and compile smoke checks passed.

Not acceptable interpretation:

> The entire repository test history is clean.

### 2. Patch-specific checks

These are focused checks for a specific patch.

Typical command:

```bat
tools\run_patch_checks.bat <patch_id>
```

Expected interpretation:

> The selected patch contract passed.

Patch-specific checks are useful during small changed-file releases, but they are not a full repo certification.

### 3. Legacy test inventory

Legacy tests may reference older APIs, old file locations, removed helper functions, superseded UI text, or historical patch assumptions. They can be useful as audit memory, but they should not silently define the release gate unless they are refreshed.

Typical command:

```bat
tools\run_full_checks.bat
```

Expected interpretation:

> This is an explicit cleanup or inventory pass. Failures must be triaged, not hidden.

## Triage labels

Each failing legacy test should eventually be assigned one of these labels:

- **restore** — the test reveals a still-valid behavior that was accidentally broken;
- **update** — the test concept remains valid but references old paths, names, text, or APIs;
- **archive** — the test belongs to historical context and should be moved out of the active gate;
- **delete** — the test asserts obsolete behavior and no longer preserves a useful boundary;
- **replace** — the old test should be replaced by a smaller current regression test.

## Public wording rule

Acceptable wording:

> The active release checks pass. Legacy tests are retained as non-blocking inventory pending cleanup.

Avoid wording:

> All tests pass.
> The repo is fully verified.
> The full historical test suite is green.

Unless the full legacy suite has actually been repaired and run successfully, those claims are too strong.

## Boundary reason

This is not just developer housekeeping. Test wording is part of ALETHEIA's own evidence discipline. A governance mirror that warns about claim/mechanism gaps must not create its own documentation gap around checks.

The mirror rule applies internally:

> Do not make a stronger validation claim than the evidence supports.

## Recommended next technical follow-ups

Patch 217 is documentation-only. Later work may add:

1. `tests/current/`, `tests/legacy/`, and `tests/deprecated/` folders.
2. A `pytest.ini` default that points only to the active suite.
3. A generated legacy-failure inventory.
4. A cleanup plan for restoring, updating, archiving, deleting, or replacing old tests.
5. A CI check that blocks only on the active release gate until legacy cleanup is complete.

These later steps should be done carefully and with patch notes so historical accountability is preserved.
