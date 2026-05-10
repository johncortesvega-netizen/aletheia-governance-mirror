# Patch 61B — Malicious Leadership Metric Calibration

Patch 61B aligns simulation metrics with ASYLUM / High-risk leadership signals.

## Problem

A hostile leadership prompt can be correctly labeled as ASYLUM while still showing metrics such as perfect trust, perfect alignment, or near-zero ego. That creates an interpretation gap: the label says high-risk, but the numbers look clean.

## Calibration Rule

If an input includes malicious leadership, coup, takeover, dictator, tyrannical, permanent authority, no-appeal, or similar hostile power language, ALETHEIA may cap trust/alignment and raise the ego signal unless concrete safeguards are present.

Concrete safeguards include:

- appeal or review
- term limits
- independent oversight
- public audit
- transparent election
- basic-rights protection
- exit or correction rights
- recall / revocability

## Safe Boundary

This patch does not add enforcement. It does not remove leaders, block policies, command action, validate authority, or replace human judgment.

It only prevents hostile leadership scenarios from displaying perfect trust/alignment without safeguards.

ALETHEIA reflects. Humans review. Power stays accountable.
