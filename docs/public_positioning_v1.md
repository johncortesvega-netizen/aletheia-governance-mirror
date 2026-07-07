# ALETHEIA Public Positioning v1
**Patch:** 215  
**Status:** Public README / reviewer doorway support  
**Scope:** Documentation only

## One-line description

ALETHEIA is an open-source governance-risk mirror that surfaces pressure signals in policies, proposals, AI systems, doctrines, receipts, and scenarios so humans can review them more clearly.

## Core public tagline

> ALETHEIA reflects. Humans review. Power stays accountable.

## What ALETHEIA is

ALETHEIA is a diagnostic review aid for governance-risk language and structures. It helps reviewers inspect whether a system, proposal, policy, AI artifact, or institutional design may contain:

- capture risk;
- authority drift;
- weak appeal paths;
- evidence gaps;
- claim/mechanism gaps;
- consent pressure;
- hidden influence;
- service-access pressure;
- semantic concealment;
- missing safeguards.

It is designed for review contexts where language may appear compliant, neutral, democratic, benevolent, technical, or humanitarian while still moving power away from accountability.

## What ALETHEIA is not

ALETHEIA is not:

- a judge;
- an oracle;
- a legal authority;
- a political authority;
- a religious authority;
- a scientific certifier;
- an enforcement system;
- a compliance certificate;
- an automated decision system;
- a substitute for human review.

The internal labels `SANCTUARY`, `THRESHOLD`, and `ASYLUM` are workflow/review labels only. They are not final truth claims, safety claims, guilt claims, legitimacy claims, or permission claims.

## Rules-based public clarity

ALETHEIA should be described as deterministic and rule-based, not as a predictive ML model. Its current readings are produced by inspectable heuristics: pressure-code rules, proximity scanning, claim/mechanism comparisons, safeguard detection, thresholds, and hand-calibrated formulas.

This is an intentional boundary choice. ALETHEIA is built to be audited, questioned, corrected, and overruled by human review. The public should understand that the system surfaces review signals; it does not discover final truth.

## Why the project matters

Many institutions and systems can look governed on the surface while quietly concentrating power, weakening appeal, hiding mechanisms, or inflating evidence. ALETHEIA responds by making those pressure patterns visible without converting the tool itself into authority.

The project is useful when a reviewer needs a structured way to ask:

- Where does power concentrate?
- Who can appeal?
- What evidence supports the claim?
- What mechanism makes the safeguard real?
- What happens under emergency pressure?
- Who can stop, audit, revoke, or repair the system?
- Is the language creating trust faster than the structure earns it?

## Public reviewer promise

ALETHEIA should preserve this promise across every surface:

> The tool may surface a pattern. The human remains responsible for interpretation, evidence, and action.

## Strong public framing

Use this framing in README, website, demo, and release notes:

> ALETHEIA does not try to become another AI judge. It is a governance mirror: it surfaces capture pressure, weak safeguards, evidence gaps, and authority drift, then returns the reading to human review.

## Recommended public sections

A public-facing page or README should include:

1. What ALETHEIA is / is not.
2. Why rule-based and local-first.
3. Three example scans.
4. Current limitations.
5. How to run locally.
6. How to review without trusting it.
7. Mirror-boundary language.
8. Release-candidate status.

## Current limitations to state openly

- The scanner is deterministic and auditable, but it can miss novel, contextual, ironic, coded, or domain-specific language.
- The app is powerful but dense; first-time users may need guided workflows.
- The codebase is still single-developer release-candidate work.
- `app.py` remains a large orchestrator file and should be modularized later with regression protection.
- World Lens and 9k allocation are audit lenses only, not mandate systems or institutional claims.
- Hosted deployments can have platform-level logging outside the app-code boundary.

## Boundary rule for future public claims

Public copy may say:

> ALETHEIA helps surface governance-risk patterns for human review.

Public copy must not say:

> ALETHEIA proves, certifies, decides, validates, governs, ranks, authorizes, or replaces review.

## Release-candidate posture

ALETHEIA v1.0 should be presented as a serious release-candidate governance mirror: usable, inspectable, and worth studying, but not production authority and not finished in a final sense.

The correct maturity claim is:

> The boundary model is coherent enough to review publicly; the implementation still requires continued testing, refactoring, examples, and contributor scrutiny.
