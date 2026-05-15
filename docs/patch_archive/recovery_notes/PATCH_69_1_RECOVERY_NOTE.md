# Patch 69.1 — Stress Batch Scenario-vs-Question Detection

## Purpose

Fix Stress Test `.txt` upload classification after Patch 69.

Patch 69 correctly allowed formal audit/repair-question banks to become `QUESTION_PROMPT`, but uploaded advanced scenario statement batches could also be suppressed as question prompts. Patch 69.1 separates declarative stress scenarios from actual audit questions.

## Changes

- Added `is_witness_scenario_statement(...)` in `core/witness.py`.
- Tightened `is_witness_question_prompt(...)` so declarative scenario statements are not treated as questions.
- Tightened `is_witness_question_set(...)` so batches with many scenario statements remain Simulation batches.
- Added documentation and tests for scenario-vs-question batch detection.

## Safety boundary

No authority behavior changed.

ALETHEIA still keeps local witness receipts as user-held records only:

- no public ledger
- no Global ID sync
- no central storage
- no authority claim
- human review required

## Check

```bat
tools\run_patch_checks.bat 69_1
```
