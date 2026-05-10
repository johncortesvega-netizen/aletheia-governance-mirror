# Mirror Check Batch Baselines

Status: Patch 64 baseline validation  
Scope: Mirror Check / Batch receipts / Question Prompt mode  
Authority level: Diagnostic only; local receipts are not authority claims.

## Purpose

Patch 64 records three 50-question batch sets as official Mirror Check batch baselines. These baselines are designed to verify that ALETHEIA treats audit questions as review prompts rather than as governance proposals.

The expected behavior is:

- each batch contains exactly 50 numbered questions;
- each generated receipt maps `receipt_01` to question 01, through `receipt_50` to question 50;
- each receipt scenario hash should match the corresponding question text;
- each question should be classified as `QUESTION_PROMPT`;
- normal scoring fields such as integrity, alignment, ego, trust, and collapse probability should remain suppressed for question prompts;
- local witness receipts should preserve the authority boundary: no public ledger, no Global ID sync, no central storage, no authority claim, and human review required.

## Baseline files

The patch stores the three question sets here:

- `examples/batch_questions/set_01_plain_language.txt`
- `examples/batch_questions/set_02_boundary_cases.txt`
- `examples/batch_questions/set_03_world_lens_release.txt`

## Set 01 — Plain Language

This set uses simple public-facing questions. It tests whether Mirror Check recognizes accessible repair and audit prompts without requiring doctrine-specific terminology.

Main themes:

- free agency;
- basic rights;
- appeals;
- privacy;
- repair;
- family and community impact;
- clear language;
- anti-capture safeguards.

## Set 02 — Boundary Cases

This set stresses edge cases around consent, crisis logic, prediction, extraordinary claims, missing evidence, fallback data, and self-audit.

Main themes:

- prediction versus human agency;
- consent under pressure;
- majority power versus minority rights;
- ambient capture;
- extraordinary claim handling;
- evidence gaps;
- founder capture;
- human review.

## Set 03 — World Lens / Release

This set focuses on World Lens, release readiness, data interpretation, seat allocation, raw trust versus trust prior, country-year data, and GitHub/public release safety.

Main themes:

- 9k allocation interpretation;
- selected-year consistency;
- missing country-year data;
- raw trust and neutral prior display;
- diagnostic rows;
- release disclaimers;
- public deployment boundaries.

## Expected batch receipt contract

When these questions are run through Mirror Check batch mode, the receipt package should satisfy:

```text
Receipt count: 50
JSON receipt count: 50
Scenario hash mismatches: 0
Input status: QUESTION_PROMPT
Protocol-adjusted state: QUESTION_PROMPT
Risk: Review Tool
Protocol label: Audit Question / Review Tool
Authority claim: False
Public ledger: False
Global ID sync: False
Central storage: False
Human review required: True
```

For question prompt mode, normal governance scoring should not be forced. The absence of a normal score is correct because the input is a question for human review, not a governance mechanism requesting a verdict.

## Boundary

These baselines do not create doctrine, authority, legal review, public ledger evidence, Global ID sync, or automated governance. They are local diagnostic baselines for testing the Mirror Check receipt pipeline.

ALETHEIA reflects. Humans review. Power stays accountable.
