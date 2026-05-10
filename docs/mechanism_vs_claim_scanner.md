# ALETHEIA v0.1 — Mechanism-vs-Claim Scanner

Status: Patch 38
Function: Detect performative ethics and distinguish value language from operational safeguards.

## Purpose

The Mechanism-vs-Claim Scanner helps ALETHEIA separate ethical claims from concrete governance mechanisms.

A governance document may use words like freedom, justice, transparency, dignity, safety, love, accountability, or service. These words can be sincere, but they are not enough by themselves. ALETHEIA should look for the mechanisms that make those values inspectable, appealable, correctable, and enforceable by human review.

Core rule:

> Mechanisms outweigh adjectives.

## Claim Language

Claim language states values, intentions, ideals, or identity.

Examples:

- We value freedom.
- We protect dignity.
- We are transparent.
- We serve the people.
- We act with love.
- We are accountable.
- We oppose corruption.
- We follow the highest ethics.

Claim language is not bad. It becomes weak when it is not connected to a practical safeguard.

## Mechanism Language

Mechanism language explains how a value is protected in practice.

Examples:

- Independent appeal process.
- Public audit trail.
- Time-limited authority.
- Human review before restriction.
- Correction mechanism.
- Exit right.
- Evidence requirement.
- Conflict-of-interest rule.
- Independent oversight.
- Plain-language notice.
- Non-retaliation rule.
- Withdrawal right.
- Review deadline.
- Public reasoning requirement.

## Integrity Levels

### High Integrity

Ethical claims are paired with concrete safeguards.

Signal:

- values are operationalized;
- appeal and correction are defined;
- authority is time-limited;
- evidence requirements are visible;
- human review is preserved;
- responsibility is assigned.

### Medium Integrity

Some mechanisms exist, but important values remain underspecified.

Signal:

- some safeguards are present;
- appeal or correction may be weak;
- accountability may be vague;
- evidence standards may be partial;
- implementation risk remains.

### Low Integrity

The document relies mostly on ethical adjectives, slogans, or identity claims without concrete safeguards.

Signal:

- many values, few procedures;
- no appeal process;
- no audit trail;
- no time limits;
- no correction path;
- no independent review;
- no evidence requirement;
- authority is protected by language rather than mechanisms.

## Output Template

```text
Mechanism-vs-Claim Scan

Ethical language integrity: High / Medium / Low
Claim signals found:
Mechanism signals found:
Missing safeguards:
Main risk:
Failure classification:
Recommended repair:
Human review note:
```

## Safe Use

ALETHEIA may say:

- This document uses strong ethical language without enough operational safeguards.
- This proposal needs an appeal process, correction mechanism, audit trail, or independent review.
- The values are stated, but the enforcement and repair mechanisms are unclear.

ALETHEIA must not say:

- The author is lying.
- The system is corrupt with certainty.
- The AI has proven bad faith.
- Human review is unnecessary.

## Relationship to Other Layers

- Capture Risk: missing mechanisms can increase opacity, unaccountable authority, non-appealability, and ideological lock-in.
- Failure Classification: performative ethics may indicate Policy Failure, Implementation Failure, or Data Failure.
- Consent-Audit: consent claims must be checked against refusal reality, withdrawal, appeal, and alternatives.
- Boundary Cases: performative ethics is a recurring edge case because values language can hide capture.
