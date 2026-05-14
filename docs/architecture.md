# ALETHEIA Architecture Overview

ALETHEIA is a Streamlit governance-risk mirror. Its architecture is intentionally bounded: it reflects review signals for humans and does not become an authority layer.

## Core boundary

ALETHEIA is a mirror, not a throne. It can surface governance-risk patterns, missing safeguards, consent pressure, capture pressure, evidence gaps, appeal weaknesses, and authority-overreach signals. It does not decide truth, enforce action, certify systems, replace law, replace medicine, replace politics, replace religion, or replace human judgment.

## Current application shape

The public app is currently organized around a large Streamlit entry file plus supporting core modules, documentation, examples, tests, and patch/recovery records.

The large `app.py` is a known maintainability issue. It should be reduced gradually and only through small, behavior-preserving patches. The near-term goal is not to rewrite the app; it is to make each part easier to inspect.

## Main review windows

### Mirror Check

Mirror Check is the primary pasted-text review path. It surfaces governance-risk signals and repair questions for human review. Its readings are not verdicts or certifications.

### Stress Test

Stress Test reviews governance scenarios under pressure. It helps expose consent, appeal, safeguard, capture, coercion, and authority-boundary risks. It does not simulate binding policy or issue commands.

### Evidence Lab

Evidence Lab organizes evidence posture and extraordinary-claim review. It can distinguish strong, partial, weak, absent, or extraordinary evidence contexts, but it does not validate final truth.

### World Lens

World Lens maps selected country-year evidence and population-weighted exposure into governance-risk review language. It is not a political mandate, election mechanism, real 9k body, Global ID system, or governing authority.

### AI Integrity Mirror

AI Integrity Mirror is a static, local-first review module for pasted AI artifacts: prompts, outputs, specs, model-card excerpts, policy claims, and code snippets. It does not call live models, benchmark vendors, crawl repositories, or certify AI systems.

## Shared protocol logic

The modules use shared protocol logic and shared boundary language. This should be described carefully as shared protocol logic, not as a claim that every module always maintains live synchronized technical state.

## Signal detection posture

ALETHEIA uses transparent rule-based and heuristic signal detection in key places. This is explainable and reviewable, but limited. It may miss nuance, irony, implicit context, culturally specific language, or language outside its strongest English/Dutch calibration.

This limitation is intentional to document clearly, not hide. Human review remains required.

Patch 103 adds the dedicated signal transparency note: `docs/signal_detection.md`. Treat that file as the public basis for explaining why rule-based detection is explainable and local-first, but limited with irony, coded language, culturally specific context, and languages outside the strongest English/Dutch calibration path.

## Privacy and external-call posture

ALETHEIA is designed to avoid built-in telemetry, external model calls, backend upload endpoints, public ledger sync, Global ID sync, and central user-input storage. Local use is recommended for sensitive audits. Hosted deployments may still create hosting-layer logs outside ALETHEIA's application code boundary.

## Patch and recovery records

Patch manifests, recovery notes, status files, and the progress database are part of the reviewability structure. They show what changed, why it changed, how to test it, and which boundaries were preserved. They can feel large to new contributors, so future work should add better patch-history navigation rather than deleting the audit trail.

Patch 131 adds `ui/start_page.py` and a small session-state gate in `app.py`. This is a readability and boundary-clarity refinement only: it shows a Start Page / How to Start screen before the full module interface, then reveals the existing app after `Proceed to ALETHEIA` is clicked. The gate uses session-state only. No cookies, accounts, persistent storage, telemetry, analytics, tracking, external calls, local LLM calls, embeddings, database, auth, login, scoring, routing, receipt schema, signal behavior, Privacy Audit scan behavior, AI Integrity scan behavior, or World Lens math are changed. Humans keep the judgment.

Patch 133 defines Receipt Reader - Standard View as a design-only future interpretation layer. It will explain pasted ALETHEIA receipts by showing native values first and secondary plain-language review bands second. The design does not add runtime UI, parsing code, scoring, receipt schema changes, new risk states, external standards as authority, external calls, telemetry, storage, certification, enforcement, or final-truth claims.

Patch 134 implements Receipt Reader - Standard View v1 as a small local helper in `ui/receipt_reader.py` and a reachable app tab. It parses obvious pasted receipt fields only, shows missing fields as `Not found in pasted receipt`, displays native values before secondary review bands, and keeps the original receipt authoritative. It does not change scoring, routing, receipt schemas, receipt generation, signal behavior, Privacy Audit scan behavior, AI Integrity scan behavior, World Lens math, uploads, downloads, external calls, LLM calls, embeddings, database/storage behavior, telemetry, certification, enforcement, or final-truth behavior.

## Future extraction target

A safe future structure would move repeated UI and copy into dedicated modules while keeping behavior stable:

```text
app.py                         # Streamlit shell/router
ui/boundary_notice.py          # shared boundary notices
ui/receipt_display.py          # receipt/result display helpers
ui/shared_state_panel.py       # shared protocol display helpers
pages_ui/mirror_check_page.py  # Mirror Check page renderer
pages_ui/stress_test_page.py   # Stress Test page renderer
pages_ui/evidence_lab_page.py  # Evidence Lab page renderer
pages_ui/world_lens_page.py    # World Lens page renderer
copy/boundary_copy.py          # auditable public boundary language
```

This is a target map, not a claim that the files already exist.

## Boundary, privacy, and hosted-use layer

Patch 104 adds a small boundary/privacy layer around the existing architecture:

- `docs/BOUNDARY.md` records the public non-authority boundary.
- `docs/privacy_boundary.md` records the local-first repository/application privacy posture.
- `docs/hosting_limits.md` records Streamlit/hosted deployment caveats.
- `core/boundary.py` centralizes reusable boundary text for future UI use.
- `core/privacy_panel.py` centralizes reusable privacy/local-first panel text for future UI use.

These helper modules are not a behavioral refactor. They are intentionally not wired into `app.py` in Patch 104. The purpose is to make later UI and app-shell refactors safer by giving them one bounded language source.

Architectural boundary: ALETHEIA is local-first by design, but hosted deployments may have platform-level logs outside ALETHEIA's application code. The project must not claim privacy certification, security certification, compliance approval, or final authority.


## Documentation navigation layer

Patch 105 adds `docs/patch_index.md` and `docs/public_trust_package.md` as navigation documents. They do not change architecture or runtime behavior. They help reviewers locate the boundary, privacy, hosted-use, signal-detection, contributor, and patch-history documents without reading the entire repository first.

This layer is deliberately non-authoritative: it organizes review evidence, but it does not certify ALETHEIA.


## App shell extraction layer

Patch 108 starts the app-shell refactor by moving stable top-of-app boundary notices into `ui/app_shell.py`. Patch 109 continues the same structural path by moving the stable sidebar identity card and sidebar context copy into `ui/app_shell.py`.

This is intentionally not a page-module refactor yet. `app.py` remains the orchestrator for navigation, interactive controls, session-state updates, scoring calls, receipt generation, downloads, and module routing. The shell helper only renders static UI copy and boundary/privacy context.

Boundary preserved: this extraction does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, external calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior.


App.py remains the orchestrator for behavior; Patch 109 only extracts sidebar shell copy.

## Patch 110 — App Shell Router Refactor Step 3

Patch 110 continues the behavior-preserving app-shell refactor. The stable public header and first-use note now live in `ui/app_shell.py` as copy-only helpers. This keeps top-level product framing easier to review while preserving `app.py` as the runtime orchestrator.

App.py remains the orchestrator for behavior. Patch 110 only extracts static public header and first-use note copy; it does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior.



## Patch 111 — Beginner Try This First UX

Patch 111 adds `ui/beginner_guide.py` as a copy-only beginner guide and wires it into the top-level Streamlit shell. It helps first-time users start with Mirror Check, read the risk reading, inspect observed reasons, review repair questions, and optionally download a local receipt.

`app.py` remains the runtime orchestrator. The guide does not read or write session state, route modules, run analysis, change scoring, alter receipts, make external calls, collect telemetry, certify outcomes, enforce action, or claim final truth.


## Patch 112 — Privacy Audit Panel v1

Patch 112 extracts the Privacy Boundary Audit Panel renderer into `ui/privacy_audit_panel.py`. The existing static privacy-boundary scan remains in `core.ai_integrity_mirror`; the helper only renders the already-built audit dictionary inside AI Integrity Mirror results.

App.py remains the orchestrator for behavior, module routing, session state, scoring, receipts, downloads, and interactive controls. The panel is static pasted-artifact review support only: no runtime monitoring, no repository crawling, no host-log inspection, no external calls, no privacy guarantee, no compliance approval, no certification, no enforcement, and no final truth claim.

## Patch 113 — Public Trust Package Consolidation

Patch 113 consolidates the trust-facing documentation path. `docs/public_trust_package.md` becomes the central map to boundary statements, privacy/local-first posture, hosted-use caveats, signal-detection transparency, the signal dictionary, architecture docs, beginner UX, the Privacy Audit Panel v1 documentation, patch history, and the public review checklist.

This is documentation/navigation only. It does not change `app.py`, module routing, scoring, verdict routing, signal patterns, signal weights, receipt schemas, external calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, compliance approval, certification, enforcement, or final-truth behavior.



## Patch 114 — Public Release Polish v1

Patch 114 is a public-entry documentation polish layer. It does not change runtime architecture. It points reviewers toward `docs/public_release_polish_v1.md`, `docs/public_trust_package.md`, and `docs/public_review_checklist.md` before deeper patch-history inspection.

Architecture boundary: no app behavior, scoring, routing, signal patterns, receipt schemas, external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final-truth behavior changed.


## Patch 115 — App Shell Router Refactor Step 4

Patch 115 continues the gradual `app.py` router/shell refactor after Patch 114. It extracts static sidebar tuning-section headings and explanatory captions into `ui/app_shell.py` while keeping interactive controls and all behavior in `app.py`.

Architecture boundary: `app.py` still owns session state, controls, module routing, scoring, receipts, downloads, and analysis calls. Patch 115 only moves static sidebar shell copy. It does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final-truth behavior.

## Patch 116 — App Shell Router Refactor Step 5

Patch 116 continues the behavior-preserving app-shell refactor by moving the stable footer banner into `ui/app_shell.py` as `render_app_footer_banner`. The footer remains public shell copy: “ALETHEIA reflects. People decide.”

`app.py` remains the runtime orchestrator. Patch 116 does not move interactive controls, session state, module routing, scoring, receipts, downloads, analysis behavior, external calls, telemetry, analytics, storage, certification, enforcement, or final-truth claims.


## Patch 117 — Refactor Stabilization Checkpoint

Patch 117 is a stabilization checkpoint for the app-shell router refactor. It does not extract new UI and does not change runtime behavior. It verifies that `ui/app_shell.py` remains a static shell-copy helper module and that `app.py` remains the orchestrator for interactive controls, session state, module routing, scoring, receipts, downloads, and analysis behavior.

The checkpoint explicitly preserves the boundary: no scoring, no verdict-routing, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

## Patch 118 — Beginner UX Polish v2

Patch 118 improves the first-use guidance in `ui/beginner_guide.py` and `docs/beginner_ux.md`. It adds a first-audit checklist, plain “what this means / what this does not mean” wording, and stop-and-review prompts.

This is static copy and documentation only. `app.py` remains the runtime orchestrator. Patch 118 does not move scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, session state, downloads, external calls, telemetry, analytics, storage, certification, enforcement, or final-truth claims.

## Patch 119 — App Shell Router Refactor Step 6

Patch 119 adds `ui/module_intro.py` and extracts exactly one small static module-intro block from `app.py`: the Stress Test "Scan my idea" note. The new helper is copy-only and importable without opening Streamlit unless rendered.

`app.py` remains the runtime orchestrator. Patch 119 does not move scoring, verdict-routing, signal-pattern logic, signal weights, receipt schemas, module routing, session state, file uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final truth behavior.

## Patch 120 — Module Intro Extraction Step 2

Patch 120 continues the module-intro extraction path in `ui/module_intro.py`. It moves two additional static/non-interactive intro blocks out of `app.py`: the Boundary Cases calibration note and the Consent-Audit Engine heading plus short explanatory copy.

`app.py` remains the runtime orchestrator. Patch 120 does not move scoring, verdict-routing, signal-pattern logic, signal weights, receipt schemas, module routing, session state, file uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final truth behavior.

## Patch 121 — Shared Status / Notice Cards

Patch 121 starts a shared status-card layer in `ui/status_cards.py`. It moves the static AI Integrity boundary caption group into `render_ai_integrity_boundary_cards` so boundary copy is easier to audit without changing analyzer behavior.

`app.py` remains the runtime orchestrator. Patch 121 does not move scoring, verdict-routing, signal-pattern logic, signal weights, receipt schemas, module routing, session state, file uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final truth behavior.

## Patch 122 - Refactor Stabilization Checkpoint 2

Patch 122 is a stabilization checkpoint after the Patch 119, Patch 120, and Patch 121 extractions. It adds `docs/refactor_stabilization_checkpoint_2.md` and regression tests for helper importability, `app.py` wiring, helper boundaries, non-authoritative language, and repair-note hygiene.

`app.py` remains the runtime orchestrator. Patch 122 does not move scoring, verdict-routing, signal-pattern logic, signal weights, receipt schemas, module routing, session state, file uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final truth behavior.

## Patch 123 - About / Public Info Page Extraction

Patch 123 starts low-risk page extraction by moving the in-app `Why ALETHEIA` / About tab into `pages_ui/about_page.py`. The helper renders public information copy only.

`app.py` remains the runtime orchestrator. It still owns tab selection, optional header image resolution, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. Patch 123 adds no external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final truth behavior.

## Patch 124 - Trust Package Page Extraction

Patch 124 adds `pages_ui/trust_package_page.py` and calls it from the Protocol Guide tab. The helper renders a public trust package review route that points to the relevant documentation rather than duplicating the docs as authority.

`app.py` remains the runtime orchestrator. It still owns tab selection, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. Patch 124 adds no external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final truth behavior.

## Patch 125 - Evidence Lab Static UI Extraction

Patch 125 adds `pages_ui/evidence_lab_page.py` and moves stable Evidence Lab intro copy plus public-data build guidance out of `app.py`.

`app.py` remains the runtime orchestrator. It still owns Evidence Lab upload widgets, build buttons, dataframe processing, public upload diagnostics, scoring, validation, downloads, receipts, session state, Evidence Lab / World Lens synchronization, privacy scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. Patch 125 adds no external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final truth behavior.

## Patch 126 - Final Structural Simplification Freeze

Patch 126 records the corrected project posture: ALETHEIA is not in expansion mode. It is in refinement mode.

Allowed structural work is limited to moving existing UI code into clearer files, removing duplication, consolidating repeated copy, improving documentation navigation, tightening tests, and locking behavior. The current behavior is treated as the release-candidate surface to preserve.

`app.py` remains unchanged by Patch 126. There is no app runtime behavior change, new module, new scoring, new panel, new analysis mode, new intelligence, receipt schema change, module-routing change, session-state change, privacy scan change, AI Integrity scan change, World Lens math change, external call, telemetry, analytics, storage, identity sync, certification, enforcement, privacy guarantee, or final truth behavior.

## Patch 127 - Encoding Cleanup and Tab Icon Restore

Patch 127 keeps the release-candidate structure intact and only repairs visible text-encoding corruption in public UI text. The restored tab icons and punctuation do not change the application architecture.

`app.py` remains the orchestrator. The existing `ui/` and `pages_ui/` helper boundaries remain unchanged.

Boundary preserved: no scoring, no routing, no receipt schema, no signal logic, no privacy scan logic, no AI Integrity scan logic, no World Lens math, no external calls, no telemetry, no privacy guarantee, no certification, no enforcement, and no final-truth behavior changed. Human review remains required.

## Patch 128 - Public UI Text Consistency Pass

Patch 128 keeps the current architecture intact and changes public UI copy only. It uses the existing extracted page/helper structure (`pages_ui/about_page.py`, `pages_ui/trust_package_page.py`, `pages_ui/evidence_lab_page.py`, and `ui/beginner_guide.py`) to make the release-candidate surface easier to understand.

The patch reinforces refinement mode, not expansion: no app runtime behavior, scoring, routing, receipts, signal logic, privacy scan logic, AI Integrity scan logic, World Lens math, external calls, telemetry, analytics, storage, certification, enforcement, or final-truth behavior changed. Human review remains required.

Patch 128 public wording note: the compliance mirage is a review concern, not a legal conclusion. ALETHEIA asks reviewers to look beyond paperwork toward power movement, appeal, hidden influence, and human review.

Patch 128 public wording note: regulation as a floor means compliance is not treated as the final measure of integrity; the compliance mirage remains a review concern, not a legal conclusion.

## Patch 129 - Input and Error Clarity Pass

Patch 129 adds `ui/input_clarity.py` as a copy-only helper for selected user-facing input and upload messages. `app.py` still owns orchestration, interactive controls, session state, module routing, scoring calls, upload handling, receipt generation, and downloads.

The helper only renders clearer empty-input, empty-batch, language-calibration, public-data upload, and direct CSV read-failure messages. This is a refinement-mode change, not expansion: no scoring, routing, receipt schema, signal, privacy-audit, AI Integrity scan, World Lens, external-call, telemetry, storage, certification, enforcement, privacy-guarantee, or final-truth behavior changes.
## Patch 130 — Release Candidate Freeze

Patch 130 records ALETHEIA as being in release-candidate refinement mode after the Patch 127-129 public polish sequence. The current behavior is the surface to preserve. Future work should be limited to bug fixes, copy/readability fixes, input clarity, test hygiene, documentation navigation, and small behavior-preserving cleanup.

This is not expansion. No new modules, no new scoring, no new risk states, no live model calls, no agentic review, no enterprise workflow, no telemetry, no analytics, no storage or identity sync, no certification, no enforcement, no privacy guarantee, and no final-truth claim are introduced or planned by this freeze.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
