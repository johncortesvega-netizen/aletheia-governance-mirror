# AI Integrity Mirror Rubric

Patch 92 makes the AI Integrity Mirror rubric explicit and reviewable without changing analyzer scoring.

AI Integrity Mirror reviews **pasted artifacts**: AI outputs, system prompts, policy excerpts, agent workflow/spec text, model-card/safety claims, and code snippets. It does not test a live model, call a vendor API, crawl a repository, inspect training data, or predict future behavior.

## What the rubric measures

The rubric measures reviewable **governance-integrity signals** in the artifact text/code. In ALETHEIA, integrity means consistency between claims, boundaries, evidence discipline, reviewability, and human-authority limits.

It does not measure moral purity, final truth, total model alignment, deployment safety, legal compliance, medical safety, political legitimacy, religious authority, or vendor quality.

## Signal categories

| Category | Current signal names | Review question | Current weight range |
|---|---|---|---|
| Authority boundary | `final_authority_claim` | Does the artifact claim final, definitive, unquestionable, certified, or no-review authority? | 0.24 |
| Enforcement / appealability | `automated_enforcement` | Does the artifact link AI output to denial, punishment, blacklisting, or enforcement without appeal/review? | 0.22 |
| Certification overclaim | `sovereign_or_certification_language` | Does it use certified-safe, official-verdict, sovereign-AI, or approval-style language? | 0.18 |
| Reviewability | `missing_human_review` | Are appeal, override, audit, challenge, recourse, or opt-out paths missing or explicitly blocked? | 0.18 |
| Transparency | `opacity_or_hidden_logic` | Are criteria, scores, rankings, or rules hidden, proprietary, opaque, or unexplained? | 0.14 |
| Coercion / manipulation | `manipulation_or_pressure` | Does it pressure, compel, manipulate, or exploit vulnerability? | 0.20 |
| Surveillance / identity capture | `surveillance_or_identity_capture` | Does it require continuous monitoring, Global ID, central registry, biometric tracking, or similar capture pressure? | 0.20 |
| Code / credential hygiene | `secret_or_token_exposure` | Does pasted code appear to contain credentials, passwords, tokens, or private keys? | 0.26 |
| Code execution / data flow | `unsafe_execution_or_network` | Does pasted code show dynamic execution, shell execution, or possible user-input exfiltration paths? | 0.18 |

The rubric is deterministic and text-pattern based. A triggered signal is a review pointer, not a final finding of fact.

## Positive review signals

The analyzer also counts review-positive language such as human review, independent review, audit, challenge, appeal, opt-out, explainability, consent, data minimization, uncertainty, limitations, and "not legal/medical/financial/official advice" disclaimers.

These signals can reduce pressure when present, but they do not automatically make an artifact safe. A strong positive disclaimer cannot erase hard authority-overreach, enforcement, surveillance, or credential-exposure pressure.

## Reading the output

AI Integrity Mirror currently maps pressure into the existing internal taxonomy:

- `SANCTUARY` / Low — low-risk internal reading for the pasted artifact under this rubric.
- `THRESHOLD` / Medium — review needed; one or more signals require human attention.
- `ASYLUM` / High — strong authority, enforcement, capture, or code-risk pressure under the static rubric.

The taxonomy is internal protocol language. It is not certification, approval, proof of safety, or a model-wide ranking.

## Evidence snippets and redaction

Triggered findings include short local evidence snippets so reviewers can see why a rule fired. Credential-like values and private-key blocks are redacted before display or receipt export.

Evidence snippets are review aids only. They are not external verification, proof of truth, proof of safety, or legal/security conclusions.

## Single vs batch mode

Single mode reviews one pasted artifact. Batch mode splits pasted text on simple delimiter lines such as `---`, `===`, or `###` and runs the same static review on each item.

Batch summaries count artifact-level risk readings and categories. They do not benchmark live models, rank vendors, certify systems, or prove one model is safer than another.

## Receipt scope

AI Integrity receipts preserve the local review context: artifact type, static review scope, privacy boundary, non-certification note, reliance boundary, triggered signal summary, redacted evidence snippets, repair questions, and optional batch summary.

Receipts are user-held review artifacts. They are not public-ledger claims, official audit certificates, vendor approvals, model approvals, benchmark proofs, or safety guarantees.

## Privacy boundary

ALETHEIA's repository includes no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Pasted artifacts are processed in the running app session, and receipts are user-held downloads.

Deployment caution: third-party hosting layers may still keep their own server or access logs outside ALETHEIA's application code.

## Out of scope

AI Integrity Mirror does not certify AI systems, vendors, codebases, prompts, agents, or outputs. AI Integrity Mirror does not call live models. AI Integrity Mirror does not store pasted artifacts centrally. It also does not:

- certify AI systems, vendors, codebases, prompts, agents, or outputs
- prove truth, alignment, safety, compliance, or legality
- replace human review, external audit, legal review, medical review, security review, or institutional accountability
- inspect hidden prompts, hidden weights, training data, telemetry, production logs, or future behavior
- call live models, external APIs, or repositories
- store pasted artifacts centrally
- enforce actions, deny access, rank citizens, punish, blacklist, or govern

## Patch 92 boundary

Patch 92 is documentation only. It publishes the rubric in a reviewable form and updates the AI Integrity documentation surface. It does not change scoring math, signal patterns, signal weights, verdict routing, UI behavior, receipt generation, privacy architecture, batch splitting, or external behavior. Boundary shorthand: no scoring-math change, no signal-pattern change, no signal-weight change, no verdict-routing change, no receipt-generation change.

## Verification

```bat
tools\run_patch_checks.bat 92
tools\run_patch_checks.bat 91
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```
