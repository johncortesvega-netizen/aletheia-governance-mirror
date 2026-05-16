# Structural Improvement Entry Point

Patch 102 starts the maintainability path for ALETHEIA without changing scoring, verdict routing, Streamlit behavior, privacy posture, or authority boundaries.

The external reviews raised useful structural advice: ALETHEIA's philosophy and code appear coherent, but the project should become easier to enter, maintain, and review. The safest first move is documentation architecture, not a large refactor.

## Structural principle

ALETHEIA must remain a bounded governance mirror. Structural improvements should make the mirror easier to inspect, not more authoritative.

Every future structural patch should preserve this line:

> ALETHEIA surfaces signals. Humans keep the judgment.

## Why this comes before code refactoring

The project has a long patch history, a large Streamlit surface, static rule-based signal logic, privacy-by-design choices, and several public-facing modules. Refactoring `app.py` before documenting the intended structure would increase the chance of accidental drift.

Patch 102 therefore creates the entry layer for later work:

1. Explain the architecture in plain terms.
2. Explain the contributor path.
3. Clarify the staged refactor order.
4. Preserve the non-authority and privacy boundaries.
5. Keep all current runtime behavior unchanged.

## Recommended structural sequence

### 1. Boundary and contributor documentation

Create public documentation that says what ALETHEIA is, what it is not, how modules connect, and how contributors should avoid authority drift.

### 2. Signal transparency documentation

Document the rule-based heuristic nature of the signal system. This is a transparency strength, but it has limits: nuance, irony, culturally specific meaning, and languages outside the English-first review scope may require extra human review. Dutch/Nederlands examples may be used for batch testing, not as a general compatibility claim.

### 3. Privacy and hosting-limit documentation

Keep the local-first recommendation visible. The hosted Streamlit app is useful for public demonstration and light review, but sensitive audits should be run locally.

### 4. Patch-history navigation

The patch/recovery history is evidence of iterative hardening, but it can overwhelm new contributors. Add an index that groups patches by module and purpose.

### 5. Gradual `app.py` reduction

Only after the documentation layer is clear, reduce `app.py` in small behavior-preserving extractions:

- common boundary and notice UI helpers;
- repeated receipt/result display helpers;
- page rendering modules;
- copy constants for public boundary language;
- shared protocol display helpers.

`app.py` should eventually become the Streamlit shell/router, not the entire application.

## Non-goals for this patch

Patch 102 does not:

- change scoring;
- change verdict routing;
- change receipt schemas;
- add LLM calls;
- add external calls;
- add telemetry;
- add authentication;
- add central storage;
- certify safety, security, privacy, legality, truth, ethics, or legitimacy;
- refactor `app.py`.

## Structural success criteria

A future contributor should be able to answer these questions before editing code:

- What is ALETHEIA's authority boundary?
- Which modules exist and how do they relate?
- Why is the signal system rule-based?
- Why is local use recommended for sensitive audits?
- Why does the repo contain many patch and recovery files?
- Which files should be refactored first, and which should not be touched casually?

Patch 102 is the first answer to those questions.
