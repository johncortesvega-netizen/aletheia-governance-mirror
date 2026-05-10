# Patch 69 — Stress Test Question Prompt Detection

## Summary

Stress Test batch mode now recognizes audit / repair-question banks as question prompts instead of scoring them as governance scenarios.

## Why

The file `formal doctrine repair-question baseline.txt` contains 50 formal doctrine repair questions. When run through Stress Test, these should be review tools, not SANCTUARY / THRESHOLD / ASYLUM scenario verdicts.

## Behavior

If a Stress Test batch is mostly audit questions:

- Input status: `QUESTION_PROMPT`
- State: `QUESTION_PROMPT`
- Risk: `Review Tool`
- Protocol label: `Audit Question / Review Tool`
- Normal metrics are suppressed
- Authority boundary remains local-only and human-review-required

## Safety

No authority, enforcement, Global ID sync, public ledger, central storage, or governance decision layer was added.
