# Patch 151 — English-First Language Scope Copy Clarification

Patch 151 is a copy-only transparency patch.

It changes public language from Dutch/Nederlands app-wide compatibility wording to a narrower and more accurate boundary:

> ALETHEIA is English-first. Dutch/Nederlands examples may be used for batch testing, but this is not a general app-wide language-compatibility claim. Human review remains required.

## What changed

- Public app copy now says English-first rather than English + Dutch/Nederlands supported.
- About / Why ALETHEIA copy now frames Dutch/Nederlands as batch testing/examples only.
- Input-clarity and signal-detection docs now avoid general Dutch/Nederlands compatibility claims.
- README, reviewer docs, contributor docs, trust-package copy, and patch index/status/progress records were updated to match.
- Related copy assertions in tests were updated so future checks do not reintroduce the old compatibility claim.

## What did not change

- Dutch/Nederlands batch fixtures were not removed.
- Dutch stress-test rules were not removed.
- No scoring, routing, taxonomy, receipt schema/generation, signal regex/weights, Stress Test behavior, Mirror Check behavior, AI Integrity behavior, Privacy Audit behavior, World Lens math, upload/download behavior, external calls, telemetry, storage, Global ID sync, public ledger sync, certification, enforcement, official authority, or final-truth behavior changed.

Human review remains required.

## Validation

```bat
python tools\run_patch_checks.py 151
```
