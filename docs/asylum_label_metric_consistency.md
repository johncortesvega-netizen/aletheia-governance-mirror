# Patch 68.1 — Asylum Label / Metric Consistency

Patch 68.1 keeps final Stress Test receipts internally consistent when a pattern reaches **ASYLUM / High**.

## Rule

If the final `protocol_adjusted_state` is `ASYLUM`, the visible protocol label and metrics must also reflect the ASYLUM state.

Required receipt behavior:

- protocol label ends with `/ Asylum`
- trust index is capped at `0.80`
- alignment is capped at `0.85`
- ego signal is at least `0.10`
- repair questions remain present
- authority boundary remains mirror-only

## Why

Some advanced stress labels were correctly escalated to `ASYLUM / High`, but still displayed a `Needs Safeguards` label with THRESHOLD-style metrics such as trust `0.92`, alignment `0.92`, and ego `0.05`.

That was confusing. Patch 68.1 does not add authority and does not trigger action. It only keeps the receipt wording and metric presentation aligned with the final risk state.

## Boundary

This remains a local, human-reviewable mirror signal:

- no authority claim
- no public ledger
- no Global ID sync
- no central storage
- human review required
