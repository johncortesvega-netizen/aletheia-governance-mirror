# Patch 61A — Asylum Repair Questions

## Purpose

High-risk or ASYLUM outputs must never leave the user with an empty repair path.
ALETHEIA is a mirror, not an authority layer, so the repair path is expressed as
questions for human review rather than commands.

## Trigger

ALETHEIA attaches Silent Operator repair questions when any of these signals are present:

- protocol-adjusted state is `ASYLUM`
- risk is `High`
- protocol label contains `Malicious Leadership` or `Asylum`
- scanner power concentration is at least `0.75`

## Required behavior

When the trigger fires, the report should include questions about:

- appeal, pause, or removal of authority without ALETHEIA becoming the authority
- preventing temporary crisis or revolutionary power from becoming permanent control
- protecting basic rights during transition
- independent human review and challenge paths
- non-coercive restoration of legitimacy and accountability
- exit, objection, correction, and anti-retaliation paths for affected people

## Boundary

This patch does not add enforcement. It does not remove leaders, block systems,
validate political claims, or make legal determinations. It only ensures that
high-risk mirror outputs include repair questions for human review.
