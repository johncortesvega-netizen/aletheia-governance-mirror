# ALETHEIA Patch Index

**Version:** v1.0  
**Updated for:** Patch 117 — Refactor Stabilization Checkpoint  
**Last updated:** 2026-05-13

This index is a navigation layer for ALETHEIA's iterative patch history. It does not replace patch manifests, recovery notes, tests, or human review. Its purpose is to make the project easier to enter without hiding the fact that ALETHEIA has been developed through many small, reviewable patches.

ALETHEIA remains a **mirror, not a throne**. Patch history is evidence for review, not proof of truth, safety, legality, ethics, privacy, security, or legitimacy.

## How to read the patch history

Use the patch files in this order:

1. **Current README** — public entry point and module overview.
2. **`docs/public_trust_package.md`** — central trust-facing map.
3. **This patch index** — orientation map for the development trail.
4. **Patch-specific manifest** — exact changed files for a patch.
5. **Patch-specific recovery note** — how to roll back or inspect the patch.
6. **Patch-specific tests** — bounded regression checks for that patch.
7. **`PATCH_STATUS.md` and `docs/progress_database.md`** — running status history.

The presence of tests and manifests does not make the project certified or tamper-proof. They support human review.

## Structural sequence after external review

The current structural improvement path starts at Patch 102:

| Patch | Focus | Runtime behavior |
| --- | --- | --- |
| 102 | Structural improvement entry point, architecture docs, contributor start | No runtime behavior change |
| 103 | Signal-detection transparency and English/Dutch calibration limits | No runtime behavior change |
| 104 | Boundary, privacy, and hosted-use transparency | No Streamlit page wiring change |
| 105 | Patch-history and public-trust navigation | No runtime behavior change |
| 106 | Signal dictionary and glossary for reviewer-facing signal families | No runtime behavior change |
| 107 | Boundary and privacy helpers wired into the Streamlit sidebar | Narrow runtime UI wiring only |
| 108 | Top-of-app boundary notices extracted into `ui/app_shell.py` | UI shell extraction only |
| 109 | Sidebar identity card and static sidebar context extracted into `ui/app_shell.py` | UI shell extraction only |
| 110 | Public header and first-use note extracted into `ui/app_shell.py` | UI shell extraction only |
| 111 | Beginner "Try This First" guide added via `ui/beginner_guide.py` | Static UX helper only |
| 112 | Privacy Audit Panel v1 renderer extracted into `ui/privacy_audit_panel.py` | Static pasted-artifact review UI only |
| 113 | Public trust package consolidated and public review checklist added | Documentation/navigation only |
| 114 | Public release polish and public entry path clarified | Documentation/release-surface only |
| 115 | App shell refactor step 4: sidebar tuning copy extracted | Static shell extraction only |
| 116 | App shell refactor step 5: footer banner extracted into `ui/app_shell.py` | Static shell extraction only |

This order is intentional. Documentation, boundaries, privacy posture, contributor navigation, and trust navigation came before larger app-shell extraction. Patches 108-110 began the `app.py` reduction through small shell extractions only; Patch 115 extracted sidebar tuning copy, Patch 116 extracted the footer banner, and Patch 117 added a refactor stabilization checkpoint. Patches 111-112 added beginner and privacy-review UI helpers without changing scoring or routing.

In short: document the boundary first, extract static shell/UI copy gradually, and keep analytical behavior stable unless a patch explicitly targets it.

## Main patch categories

### Boundary and authority

These patches protect the principle that ALETHEIA surfaces signals while humans keep judgment. Relevant documents include:

- `docs/BOUNDARY.md`
- `docs/ethics.md`
- `docs/scope_layers.md`
- `docs/structural_improvement_entrypoint.md`
- `docs/public_review_checklist.md`

### Privacy and hosted-use caveats

These patches clarify the local-first posture and hosted deployment caveats:

- `docs/privacy_boundary.md`
- `docs/hosting_limits.md`
- `docs/go_live_privacy_review_statement.md`
- `docs/privacy_audit_panel_v1.md`
- `core/privacy_panel.py`
- `ui/privacy_audit_panel.py`

The correct public framing is: **local-first by design; hosted use has platform limits**.

### Signal detection and review limits

These patches document the transparent rule-based and heuristic signal posture:

- `docs/signal_detection.md`
- `docs/SIGNAL_DICTIONARY.md`

Signal outputs are internal governance-risk readings, not verdicts or certifications. The dictionary is a reviewer-facing glossary, not a scoring specification.

### Architecture, onboarding, and beginner path

These patches help reviewers and contributors enter the project safely:

- `docs/architecture.md`
- `docs/new_contributor_start_here.md`
- `docs/beginner_ux.md`
- `ui/beginner_guide.py`
- `CONTRIBUTING.md`

### AI Integrity Mirror

These patches add and polish static artifact-review workflows for AI outputs, prompts, specs, policy claims, and code snippets:

- `docs/ai_integrity_mirror.md`
- `docs/ai_integrity_preview_public_adoption.md`
- `docs/ai_integrity_preview_release_notes.md`
- AI Integrity tests under `tests/test_patch_85_*` through `tests/test_patch_100_*`

The AI Integrity Mirror reviews pasted artifacts only. It does not certify AI systems or vendors.

### Public trust package

The current public trust entry points are:

- `docs/public_trust_package.md`
- `docs/public_review_checklist.md`
- `examples/Trust_Package_README.md`

These organize review evidence. They do not create certification, compliance approval, institutional legitimacy, or final authority.

## Where new contributors should start

New contributors should read:

1. `docs/new_contributor_start_here.md`
2. `docs/architecture.md`
3. `docs/BOUNDARY.md`
4. `docs/privacy_boundary.md`
5. `docs/signal_detection.md`
6. `docs/SIGNAL_DICTIONARY.md`
7. `docs/public_trust_package.md`
8. `CONTRIBUTING.md`

Then inspect only one patch at a time.

## Patch-file naming convention

Typical patch artifacts:

```text
PATCH_113_MANIFEST.txt
PATCH_113_RECOVERY_NOTE.md
tests/test_patch_113_public_trust_package_consolidation.py
```

This convention makes the development trail easier to audit without forcing contributors to read the entire history at once.

## What this index does not claim

This index does not claim that ALETHEIA is complete, certified, secure, private in all deployments, legally valid, ethically final, or institutionally legitimate. It is a navigation map for a reviewable research/prototype tool.

**ALETHEIA surfaces signals. Humans keep the judgment.**


## Patch 114 — Public Release Polish v1

Patch 114 makes the public entry path clearer after the trust-package consolidation. It adds `docs/public_release_polish_v1.md` and updates public-facing docs so reviewers can start with boundary, privacy, signal basis, beginner path, trust package, and review checklist before reading the full patch history.

This is documentation/release-surface polish only. It does not change app behavior, scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, telemetry, analytics, storage, privacy guarantees, certification, enforcement, or final-truth behavior.


## Patch 115 — App Shell Router Refactor Step 4

Patch 115 extracts static sidebar tuning-section headings and notes from `app.py` into `ui/app_shell.py`. Interactive controls, session state, module routing, scoring, receipts, downloads, and analysis behavior remain in `app.py`.

This is static shell extraction only. It does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, telemetry, analytics, storage, privacy guarantees, certification, enforcement, or final-truth behavior.

## Patch 117 — Refactor Stabilization Checkpoint

Patch 117 pauses the app-shell extraction sequence and adds a review checkpoint. It documents the refactor boundary in `docs/refactor_stabilization_checkpoint.md` and adds tests that check `ui/app_shell.py` helper presence, `app.py` orchestration, non-authoritative language, no privacy guarantee, no certification, no enforcement, no final truth, and no accidental internal repair notes.

Scope: documentation and regression tests only. No runtime behavior change, no scoring, no verdict-routing, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync. Humans keep the judgment.

## Patch 118 — Beginner UX Polish v2

Patch 118 polishes the beginner guide added in Patch 111. It adds a first-audit checklist, “what this means / what this does not mean” wording, and stop-and-review prompts for high-consequence or unclear cases.

Scope: static beginner UX copy and documentation only. No runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no external calls, no telemetry, no analytics, no privacy guarantee, no certification, no enforcement, and no final truth claim.

## Patch 119 — App Shell Router Refactor Step 6

Patch 119 continues the gradual `app.py` shell/router refactor by adding `ui/module_intro.py` and moving one small Stress Test scan-mode intro note into `render_stress_test_scan_intro`.

Scope: copy-only module intro extraction. `app.py` remains the orchestrator for mode choice, widgets, session state, module routing, scoring, receipts, uploads, downloads, and analysis behavior. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

## Patch 120 — Module Intro Extraction Step 2

Patch 120 continues the static module-intro extraction path by adding `render_boundary_cases_intro` and `render_consent_audit_intro` to `ui/module_intro.py`.

Scope: copy-only module intro extraction. `app.py` remains the orchestrator for mode choice, widgets, session state, module routing, scoring, receipts, uploads, downloads, and analysis behavior. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

## Patch 121 — Shared Status / Notice Cards

Patch 121 adds `ui/status_cards.py` and moves the AI Integrity boundary caption group into `render_ai_integrity_boundary_cards`.

Scope: copy-only status/notice card extraction. `app.py` remains the orchestrator for mode choice, widgets, session state, module routing, scoring, receipts, uploads, downloads, and analysis behavior. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

## Patch 122 - Refactor Stabilization Checkpoint 2

Patch 122 adds `docs/refactor_stabilization_checkpoint_2.md` and regression tests after the Patch 119-121 copy extractions.

Scope: documentation and regression tests only. `app.py` remains the orchestrator for mode choice, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. No runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

## Patch 123 - About / Public Info Page Extraction

Patch 123 moves the in-app `Why ALETHEIA` / About tab copy from `app.py` into `pages_ui/about_page.py`.

Scope: page-level display extraction only. `app.py` remains the orchestrator for tabs, image resolution, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. No runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

## Patch 124 - Trust Package Page Extraction

Patch 124 adds `pages_ui/trust_package_page.py` and wires a display-only Public Trust Package section into the Protocol Guide tab.

Scope: page-level display extraction only. Documentation remains the source of truth, especially `docs/public_trust_package.md` and `docs/public_review_checklist.md`. `app.py` remains the orchestrator for tabs, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. No runtime analysis behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

## Patch 125 - Evidence Lab Static UI Extraction

Patch 125 adds `pages_ui/evidence_lab_page.py` and moves stable Evidence Lab intro copy plus public-data build guidance out of `app.py`.

Scope: static UI copy extraction only. `app.py` remains the orchestrator for Evidence Lab upload widgets, build buttons, dataframe processing, public upload diagnostics, scoring, validation, downloads, receipts, session state, Evidence Lab / World Lens synchronization, and analysis behavior. No evidence processing change, no upload handling change, no dataframe logic change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

## Patch 126 - Final Structural Simplification Freeze

Patch 126 adds `docs/final_structural_simplification_freeze.md` and locks the roadmap posture around refinement rather than expansion.

Scope: documentation and regression-test only. ALETHEIA is not in expansion mode. It is in refinement mode. Allowed work is limited to moving existing UI code into clearer files, removing duplication, consolidating repeated copy, improving documentation navigation, tightening tests, and locking the existing release-candidate surface. No app runtime behavior change, no new scoring, no new panel, no new analysis mode, no new intelligence, no receipt schema change, no module-routing change, no session-state change, no privacy scan change, no AI Integrity scan change, no World Lens math change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

## Patch 127 - Encoding Cleanup and Tab Icon Restore

Patch 127 fixes visible mojibake in the public UI surface and restores the tab icons after the late structural-refactor chain. This is a refinement patch, not a feature expansion.

Scope: public UI text cleanup only. No scoring, no module-routing change, no receipt schema change, no signal change, no privacy scan change, no AI Integrity scan change, no World Lens math change, no external calls, no telemetry, no certification, no enforcement, and no final-truth behavior. Human review remains required.

## Patch 128 - Public UI Text Consistency Pass

Patch 128 refines the public UI copy after Patch 127's encoding cleanup. It does not expand the machine. It clarifies the current positioning: ALETHEIA's strength is restraint, compliance can become a mirage when paper governance hides capture pressure, regulation is a floor rather than the final measure of integrity, and the mirror asks where power is moving, who can appeal, what is hidden, and where human review is weakened.

Changed surface: About / Why ALETHEIA, Trust Package page, Evidence Lab static intro, and beginner guide copy. No scoring, routing, receipt schema, signal logic, privacy scan, AI Integrity scan, World Lens math, external call, telemetry, storage, certification, enforcement, or final-truth behavior changed.

Patch 128 public wording note: the compliance mirage is a review concern, not a legal conclusion. ALETHEIA asks reviewers to look beyond paperwork toward power movement, appeal, hidden influence, and human review.

Patch 128 public wording note: regulation as a floor means compliance is not treated as the final measure of integrity; the compliance mirage remains a review concern, not a legal conclusion.

## Patch 129 - Input and Error Clarity Pass

Patch 129 improves selected public input and error messages without changing ALETHEIA's behavior. It adds `ui/input_clarity.py` for copy-only guidance around empty AI Integrity input, empty batch artifacts, English/Dutch language-calibration caveats, public-data uploads, and direct CSV read failures.

This patch keeps the machine in refinement mode: clearer messages, same mirror. No scoring, routing, receipts, signal logic, privacy scan behavior, AI Integrity scan behavior, World Lens math, external calls, telemetry, storage, certification, enforcement, or final-truth behavior changed. Human review remains required.
## Patch 130 — Release Candidate Freeze

Patch 130 records ALETHEIA as being in release-candidate refinement mode after the Patch 127-129 public polish sequence. The current behavior is the surface to preserve. Future work should be limited to bug fixes, copy/readability fixes, input clarity, test hygiene, documentation navigation, and small behavior-preserving cleanup.

This is not expansion. No new modules, no new scoring, no new risk states, no live model calls, no agentic review, no enterprise workflow, no telemetry, no analytics, no storage or identity sync, no certification, no enforcement, no privacy guarantee, and no final-truth claim are introduced or planned by this freeze.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
## Patch 136 - Aletheia Unit Preview Stabilization

Patch 136 is a stabilization checkpoint for Aletheia Unit Preview. It adds documentation and tests only, verifying the preview remains session-only, non-authoritative, non-scoring, non-routing, and non-persistent. The checkpoint confirms normal module tabs, including Receipt Reader, remain available after the gate passes. No scoring, verdict routing, receipt schema, receipt generation, signal behavior, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, external-call behavior, telemetry, analytics, storage, certification, enforcement, final-truth, or privacy-guarantee behavior changes.

## Patch 135 - Aletheia Unit Preview v1

Patch 135 adds Aletheia Unit Preview as a pre-app intake layer. It is a front-door preview, not a new module or router. It suggests where to begin using transparent local rules, then lets the user proceed to the normal app. It does not score, route verdicts, create receipts, call module engines, certify, approve, reject, enforce, store data, call external services, use LLMs, create embeddings, sync identities, or claim final truth. Human review remains required.

## Patch 134 - Receipt Reader Standard View v1

Patch 134 adds a simple Receipt Reader - Standard View for pasted ALETHEIA receipts. It parses obvious fields, shows missing values as missing, and maps native states into secondary review bands for interoperability. It does not rescore, override, approve, reject, certify, enforce, change receipt schemas, modify existing receipt generation, call external services, use LLMs, create embeddings, store data, collect telemetry, or claim final truth. Human review remains required.

## Patch 133 - Receipt Reader Standard View Design Doc

Patch 133 adds the design document for Receipt Reader - Standard View. It defines a future interpretation layer for pasted ALETHEIA receipts: native receipt values first, Standard View review bands second, and human review always required. This is documentation/design only: no runtime Receipt Reader UI, parser, scoring, receipt schema change, new risk state, external standard as authority, external call, telemetry, storage, compliance certification language, or final-truth claim is introduced.

## Patch 132 - Start Page Stabilization Checkpoint

Patch 132 records the Patch 131 Start Page / How to Start gate as stable. It adds checkpoint documentation and tests only, verifying session-state-only behavior and confirming the normal module interface still renders after the gate passes. It does not add UI capability, modules, scoring, routing, receipt schema changes, signal changes, Privacy Audit scan behavior changes, AI Integrity scan behavior changes, World Lens math changes, external calls, telemetry, analytics, tracking, storage, certification, enforcement, privacy-guarantee claims, or final-truth claims. Humans keep the judgment.

## Patch 131 - Start Page / How to Start Gate

Patch 131 belongs to release-candidate refinement. It adds a Start Page / How to Start gate before the main module interface renders, using Streamlit session-state only. It is not a new module, router, wizard, role selector, personalization layer, stored preference, or analysis engine. No cookies, accounts, persistent storage, telemetry, analytics, tracking, external calls, local LLM calls, embeddings, database, auth, login, scoring, routing, receipt schema, signal behavior, Privacy Audit scan behavior, AI Integrity scan behavior, or World Lens math changed. Humans keep the judgment.
