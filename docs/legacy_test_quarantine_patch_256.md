# Patch 256 — Legacy Test Quarantine / Import-Break Cleanup

Patch 256 records the first concrete legacy-test cleanup step after the active-suite split and patch-archive cleanup.

## Why this patch exists

A full historical test run produced many failures, but the failures were not independent runtime bugs. The triage grouped them into a small number of patterns:

| Bucket | Count in triage | Meaning |
|---|---:|---|
| Broken import files | 2 files | Historical tests import helpers that no longer exist in the current codebase. |
| Manifest/root patch-artifact checks | 67 files / 130 failing tests | Historical tests assert root-level `PATCH_N_*` files that Patch 255 intentionally archived. |
| Code moved during modularization | 202 failing tests | Tests check `app.py` even though code now lives under `ui/pages/` or `ui/components/`. |
| Needs manual review | 361 rough triage items | Mixed bucket; may contain stale tests and possible behavior regressions. |

Patch 256 addresses only the lowest-risk quarantine layer: broken imports and old root patch-artifact checks.

## What changed

Added `tests/conftest.py` with `collect_ignore` entries for:

- the two broken-import historical test files;
- historical patch-contract files that still expect old root-level patch artifacts.

The ignored files remain on disk for audit continuity. They are not silently rewritten to pass, and they are not represented as active validation.

## Why this is not a runtime change

This patch affects test collection only. It does not change:

- app runtime behavior;
- scanner logic;
- scoring;
- MEI7 gates;
- Z-axis behavior;
- Stress Test metrics;
- Evidence Lab calculations;
- World Lens math;
- receipt schema;
- telemetry/storage behavior;
- certification/enforcement/authority boundaries.

## Next cleanup steps

1. Repair modularization path tests so they inspect `ui/pages/` and `ui/components/` instead of only `app.py`.
2. Review concrete behavior mismatches separately.
3. Decide whether quarantined historical tests should be restored against the new architecture, archived as `.disabled`, or deleted with explicit notes.

## Interpretation rule

A quarantined legacy test is not a hidden pass. It means:

> This historical test targets a superseded repository contract and needs explicit human review before it can be restored or removed.
