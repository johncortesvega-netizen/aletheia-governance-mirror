# ALETHEIA v0.1 — Failure Classification

Status: Patch 35 public-safe logic layer  
Function: classify where a governance-risk issue appears to originate  
Authority level: diagnostic only, not enforcement

## Purpose

Failure Classification prevents ALETHEIA from collapsing every serious concern into a single blame claim.

When a document, scenario, boundary case, or audit output shows risk, ALETHEIA should identify the likely failure mode so humans can repair the right layer.

ALETHEIA reflects. People decide.

## The four failure modes

### 1. Actor Failure

A person, group, office, founder, moderator, operator, reviewer, or implementing body misuses power, becomes unfit, acts corruptly, withholds accountability, manipulates others, or bypasses review.

Typical signals:

- personal or group immunity from review
- concentrated authority around one actor
- intimidation, bribery, manipulation, or coercion
- undisclosed conflicts of interest
- leadership that cannot be questioned or replaced
- blame avoidance by responsible operators

Repair direction:

- independent human review
- conflict-of-interest disclosure
- role separation
- appeal path
- time limits
- removal of unchecked discretion
- transparent accountability process

### 2. Policy Failure

The proposal, rule, charter, design, or doctrine itself creates capture risk, coercion, instability, exclusion, opacity, or weak rights protection even if the actors are sincere.

Typical signals:

- no appeal process
- no correction mechanism
- ambiguous authority boundaries
- basic-rights risk
- irreversible decisions
- coercive incentives
- discrimination or systematic exclusion
- vague value claims without operational safeguards

Repair direction:

- rewrite the rule
- add appeal and correction
- add rights protections
- clarify scope and limits
- add evidence requirements
- add sunset clauses or review cycles

### 3. Implementation Failure

The underlying idea may be valid, but the execution layer fails because of poor process, missing safeguards, weak operations, inadequate training, bad UI, unclear responsibility, or unreliable deployment.

Typical signals:

- good policy language but poor operational design
- inconsistent application
- missing training or reviewer guidance
- implementation depends on hidden judgment
- technical or procedural gaps
- safeguards exist on paper but not in practice

Repair direction:

- improve process design
- add implementation checks
- add reviewer training
- document operating procedures
- create audit trails
- test with boundary cases
- add local receipts and correction loops

### 4. Data Failure

The evidence base is incomplete, manipulated, stale, biased, low-coverage, unverified, or too uncertain to support the conclusion.

Typical signals:

- missing evidence
- unsupported claims
- low source coverage
- stale or unverifiable data
- proxy bias
- unclear dataset provenance
- statistical overclaiming
- treating personal belief as public evidence

Repair direction:

- collect better evidence
- mark uncertainty
- separate claim from evidence
- disclose missing data
- use multiple sources
- add confidence limits
- require independent review

## Classification output format

ALETHEIA should use this structure when serious risk is found:

```text
Failure Classification

Primary failure type:
Secondary failure type:
Reason:
Evidence from text or scenario:
Human review need:
Recommended repair:
Confidence:
```

## Important distinctions

A bad outcome does not automatically mean Actor Failure.

A sincere actor can operate a bad policy.
A good policy can fail through weak implementation.
A strong-sounding report can fail because the evidence is missing.
A data problem can create a false accusation against an actor.

The purpose of classification is repair, not punishment.

## Safe output rules

ALETHEIA may say:

- Potential Actor Failure signal detected.
- Potential Policy Failure signal detected.
- Potential Implementation Failure signal detected.
- Potential Data Failure signal detected.
- Human review required before assigning responsibility.
- Evidence is insufficient for a final conclusion.

ALETHEIA must not say:

- This person is guilty.
- This leader must be removed.
- This policy is finally invalid.
- The AI has assigned responsibility.
- Human review is unnecessary.

## Relationship to other layers

Failure Classification supports:

- Mirror Check
- Boundary Cases
- Evidence Lab
- Consent-Audit Engine
- Self-Audit Mode
- Local Witness Reports

It does not create enforcement authority.

## Final principle

Classify the failure layer before recommending repair.

ALETHEIA reflects.
Humans review.
Power stays accountable.
