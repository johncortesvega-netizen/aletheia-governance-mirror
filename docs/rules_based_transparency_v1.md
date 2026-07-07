# ALETHEIA Rules-Based Transparency v1
**Patch:** 216  
**Status:** Public documentation clarification  
**Scope:** Documentation only; no runtime or scoring change

## Purpose

This document clarifies what ALETHEIA's current governance-risk readings are and are not. It exists to prevent the public language around ALETHEIA from implying scientific prediction, machine-learning authority, empirical certainty, or automated judgment.

## Plain statement

ALETHEIA v1.0 is a deterministic, rule-based governance mirror. It is not a machine-learning risk model, oracle, compliance certifier, legal authority, moral authority, scientific instrument, or automated decision system.

Its readings are generated through inspectable heuristics: keyword and phrase patterns, proximity checks, pressure-code mappings, claim/mechanism comparison, safeguard detection, hand-calibrated arithmetic, and explicit review thresholds.

## What the readings mean

A reading means:

> The submitted text contains, or does not visibly contain, pressure patterns according to ALETHEIA's current rules.

A reading does not mean:

> The system has proven truth, safety, legality, legitimacy, morality, corruption, capture, or guilt.

`SANCTUARY`, `THRESHOLD`, and `ASYLUM` are internal workflow labels. They support review routing. They are not final truth categories.

## Why rule-based?

ALETHEIA deliberately chooses deterministic heuristics because governance review must be inspectable before it asks for trust. A black-box model would create a new authority surface: users could treat opaque model output as a verdict.

The rule-based approach preserves:

- visible failure modes;
- auditable pressure codes;
- reviewable thresholds;
- local-first operation;
- no mandatory model dependency;
- human responsibility for interpretation and action.

## Known limits

Rule-based review has real limits. It can miss:

- new language patterns;
- coded references;
- irony or sarcasm;
- domain-specific context;
- evidence outside the submitted text;
- sophisticated language that hides control without known trigger terms.

It can also over-flag ambiguous language. That is intentional when the alternative would be false clearance. ALETHEIA should prefer human review over automated permission.

## How to describe the scoring

Acceptable public wording:

> ALETHEIA uses deterministic heuristics, pressure codes, proximity checks, and hand-calibrated formulas to surface governance-risk signals for human review.

Avoid wording such as:

> ALETHEIA predicts governance failure.
> ALETHEIA proves capture.
> ALETHEIA scientifically measures legitimacy.
> ALETHEIA certifies a proposal as safe.

## Protocol vocabulary boundary

Terms such as semantic pressure, integrity pressure, collapse pressure, V-axis, Z-axis, and Sydney Protocol are internal review vocabulary. They are not claims of physics, divine authority, institutional mandate, empirical certainty, or final legitimacy.

The correct interpretation is:

> These labels help reviewers talk about pressure patterns without turning the tool into authority.

## Future model-assisted support

If future versions add model-assisted support, it must remain:

- opt-in;
- explainable;
- subordinate to deterministic checks;
- local or privacy-scoped where possible;
- clearly separated from final review;
- unable to certify, enforce, or decide.

No model may become the throne.


## Test-claim transparency

The same rule applies to tests: public documentation should distinguish active release checks from legacy test inventory. A passing curated check is useful evidence, but it is not proof that every historical test file in the repository passes.

Do not make a stronger validation claim than the active check evidence supports.
