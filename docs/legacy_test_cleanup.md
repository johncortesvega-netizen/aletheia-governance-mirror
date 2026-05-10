# ALETHEIA v0.1 — Legacy Test Cleanup

Status: Patch 49
Purpose: make local checks reliable without deleting older regression history.

## Why this patch exists

Older ALETHEIA tests still contain useful history, but some were written against APIs or file layouts that changed before the v0.1 governance-mirror hardening work.

Patch 49 separates two workflows:

1. **Current safe checks** — the default checks for the modern patch chain.
2. **Legacy full-suite cleanup** — a deliberate later cleanup pass for older tests.

This prevents old collection errors from blocking current patch verification.

## Current safe check

Use this as the default local command:

```bat
tools\run_checks.bat
```

It runs:

- the latest patch-specific test;
- compile checks for the active app, protocol, witness, and automation files;
- a non-blocking legacy test inventory report.

## Patch-specific check

Use this after applying one patch:

```bat
tools\run_patch_checks.bat 49
```

## Legacy inventory

To inspect older tests without failing the current workflow:

```bat
python tools\run_legacy_test_inventory.py
```

or:

```bat
py tools\run_legacy_test_inventory.py
```

## Full legacy suite

The full suite is intentionally not the default until legacy blockers are resolved.

```bat
tools\run_full_checks.bat
```

This may fail until the legacy cleanup list is addressed.

## Known legacy blockers

The current known blockers are:

- `tests/tests/test_patch_29_hard_capture_receipt_trace.py` — nested duplicate path can cause pytest import-file mismatch.
- `tests/test_patch_20_1_batch_question_upload_mode.py` — imports `combine_witness_text_uploads`, which is not present in the current `core/witness.py`.
- `tests/test_scoring_repair_questions.py` — imports `repair_prompts_from_report`, which is not present in the current `core/scoring.py`.

Patch 49 does not delete these tests. It documents them and keeps them out of the default safe workflow.

## Cleanup rule

Do not silently remove legacy tests.

For each legacy test, choose one explicit action:

1. update the test to the current API;
2. restore the missing compatibility helper if still needed;
3. move the test into an archived legacy folder;
4. mark it as intentionally obsolete with a recovery note.

## Authority boundary

Test cleanup changes developer workflow only.

It adds no governance authority, no Global ID sync, no public ledger, no real 9k selection, no World Leader logic, no automatic reset, no neural data, no memory extraction, no spiritual validation, and no automated enforcement.
