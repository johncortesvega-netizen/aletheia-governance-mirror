# ALETHEIA v1.0 — Governance Mirror

## ALETHEIA in 60 Seconds

**ALETHEIA is a mirror, not a throne.** It shows governance-risk signals for human review — nothing more.

ALETHEIA helps reviewers inspect proposals, policies, systems, doctrines, AI artifacts, receipts, and public-data patterns for signals such as capture pressure, weak appeal paths, evidence gaps, consent pressure, service misalignment, hidden influence, and authority overreach.

Why it exists: many systems can look governed, compliant, neutral, or benevolent while still moving power out of reach. ALETHEIA does not answer that problem with more command. It answers with a restrained mirror: make pressure visible, name missing safeguards, and return the reading to human review.

ALETHEIA does **not** decide, certify, approve, reject, enforce, govern, vote, or replace law, evidence, accountability, expertise, or human judgment.

## What this is / is not

**This is:** a mirror for pressure, authority drift, evidence gaps, capture risk, consent pressure, weak appeal paths, and human-review needs.

**This is not:** a judge, oracle, certification engine, truth machine, legal authority, political authority, religious authority, medical authority, investment authority, or automated decision system.

Internal taxonomy labels such as **SANCTUARY**, **THRESHOLD**, and **ASYLUM** are review-workflow labels only. They do not claim truth, purity, safety, legitimacy, moral authority, or final status. Public copy should prefer plain terms such as low-risk reading, review-required reading, high-pressure reading, internal taxonomy label, current mirror reading, and protocol-adjusted reading.

## Failure modes ALETHEIA watches for

ALETHEIA watches for pressure patterns that can make systems appear more legitimate, neutral, certain, or authoritative than the evidence supports. These failure modes are not verdicts. They are review signals for human interpretation.

- **Authority drift** — when a system starts sounding like it can decide, certify, command, legitimize, rank, punish, or replace human judgment.
- **Evidence inflation** — when claims become stronger than the evidence actually inspected.
- **Flattery pressure** — when approval, reassurance, or validation is disguised as neutral analysis.
- **Capture pressure** — when power concentrates in one actor, platform, institution, token group, committee, model owner, funder, or technical gatekeeper.
- **Sanctification drift** — when poetic, religious, moral, symbolic, or higher-truth language gets turned into operational authority.
- **False neutrality** — when a system presents provider-shaped assumptions, institutional preferences, or hidden defaults as objective reasoning.
- **No-appeal automation** — when people are affected by a decision without review, contestation, explanation, or repair path.

Receipt Reader applies this wording to all uploaded receipts as a verbal review layer. It does not add a new tab, rescore the receipt, prove wrongdoing, certify deception, or claim final truth. Human review remains required.

Start here:

1. Open **Aletheia Unit Preview** for a guided first look.
2. Use **Mirror Check** or **Stress Test** for governance text and scenarios.
3. Use **AI Integrity Mirror** for static AI artifacts such as prompts, policies, model-card excerpts, workflow descriptions, or AI outputs.
4. Use **Evidence Lab** and **World Lens** for evidence context and selected-year country evidence views.
5. Use **Receipt Reader** to read ALETHEIA local witness receipts in Standard View without rescoring or overriding them.

Privacy posture: the repository is local-first by design and includes no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Inputs are processed in the running app session, and receipts are user-held downloads. Hosted deployments may still have platform-level logs outside ALETHEIA's application-code boundary.

## Start here for reviewers

### New reviewer path

If you are reviewing ALETHEIA cold, use this short path instead of trying to read the full patch history first:

1. **Understand the boundary:** read this README section and `docs/reviewer_start_here.md`.
2. **Open the app gently:** use **Aletheia Unit Preview**, the app-side counterpart to this cleaner repository doorway.
3. **Learn the project language:** read `docs/glossary.md` for 9k, Sydney Protocol, V-Axis, World Lens, local witness receipts, Standard View, Unit Preview, and taxonomy terms.
4. **Review without trust:** follow `docs/how_to_review_aletheia_without_trusting_it.md` for local-run, self-audit, receipt comparison, no-telemetry review, and boundary inspection.
5. **Read numbers carefully:** use `docs/validation_and_precision.md` before interpreting scores, Z-axis values, World Lens coverage, or trust-prior fields.
6. **Navigate the audit trail:** use `docs/patch_index.md` and `docs/patch_archive/README.md` when you need patch-specific detail.

Reviewer-readiness is not mass-adoption polish. The goal is to preserve ALETHEIA's audit trail and **mirror, not throne** identity while giving outsiders a cleaner public doorway into the project.

## Typical use cases

- Review an AI company's public safety policy for overclaim, opacity, missing appeal paths, or authority drift.
- Stress-test a proposed governance system before relying on it.
- Inspect a policy, doctrine, or institutional workflow for capture pressure, weak safeguards, consent pressure, service misalignment, or evidence gaps.
- Review static AI outputs, prompts, model-card excerpts, code snippets, or workflow descriptions through AI Integrity Mirror.
- Explore World Lens selected-year evidence views while keeping country certification outside ALETHEIA's claim.
- Upload a local witness receipt and read it in Standard View without rescoring, overriding, or creating a new verdict.

## Current V1 surfaces

- **Aletheia Unit Preview** — calm first-use and beginner path.
- **Mirror Check** — governance-language and authority-boundary review.
- **Stress Test** — governance scenario pressure review.
- **AI Integrity Mirror** — static artifact review for pasted AI outputs, prompts, policies, workflows, model-card excerpts, and code snippets.
- **Evidence Lab** — evidence/context review support.
- **World Lens** — selected-year country evidence views and coverage/allocation context.
- **Receipt Reader** — upload-only Standard View for ALETHEIA local witness receipts and evidence bundles; it does not rescore or override uploaded receipts.
- **Boundary Cases, Protocol Guide, and Why ALETHEIA** — reference and orientation layers.

## How ALETHEIA compares to other tools

ALETHEIA is not an XAI library, enterprise compliance platform, or runtime guardrail. It is a complementary governance mirror layer for human review: it reflects governance-risk patterns in proposals, policies, scenarios, static AI artifacts, public-data evidence views, and local witness receipts.

Use ALETHEIA beside other tools, not instead of them. See `docs/for-reviewers/tool_comparison.md` for a focused comparison.

## Where to go next

- `docs/for-reviewers/quick_start.md` — 5-minute reviewer path.
- `docs/for-reviewers/tool_comparison.md` — how ALETHEIA differs from XAI tools, enterprise governance platforms, and runtime guardrails.
- `docs/reviewer_start_here.md` — fuller reviewer-start guide.
- `docs/glossary.md` — plain-language terms, Dutch equivalents where useful, and short examples.
- `docs/validation_and_precision.md` — validation gap, false precision, and external-validation roadmap.
- `docs/how_to_review_aletheia_without_trusting_it.md` — direct inspection path for skeptical reviewers.
- `CONTRIBUTING.md` — philosophy-first contribution rules.


## Patch 131 - Start Page / How to Start Gate

Status: READY FOR LOCAL REVIEW

Patch 131 adds a calm first-entry Start Page / How to Start gate before the full module interface renders. The normal ALETHEIA interface remains hidden until the user clicks `Proceed to ALETHEIA`; after that, the app continues exactly through the existing module interface for the current Streamlit session.

Boundary preserved: release-candidate refinement only. The gate uses session-state only. No cookies, no accounts, no persistent storage, no telemetry, no analytics, no tracking, no external calls, no local LLM calls, no embeddings, no database, no auth, no login, no scoring change, no routing change, no receipt schema change, no signal regex or signal weight change, no Privacy Audit scan behavior change, no AI Integrity scan behavior change, and no World Lens math change. Humans keep the judgment.

Validation targets:

```bat
python tools\run_patch_checks.py 131
python tools\run_patch_checks.py 130
python tools\run_patch_checks.py 129
python tools\run_protocol_baseline_self_audit.py
```

## Public start here

Patch 114 polishes the public entry path after the Public Trust Package consolidation. New reviewers should start with the boundary, privacy posture, signal basis, beginner path, and public-review checklist before reading the full patch history.

Recommended first-read documents:

- `docs/BOUNDARY.md` — authority and scope boundary.
- `docs/privacy_boundary.md` and `docs/hosting_limits.md` — local-first and hosted-use caveats.
- `docs/signal_detection.md` and `docs/SIGNAL_DICTIONARY.md` — rule-based / heuristic signal basis and limits.
- `docs/beginner_ux.md` — safe first-use path.
- `docs/public_trust_package.md` — central review map.
- `docs/public_review_checklist.md` — checklist before relying on a reading.
- `docs/public_release_polish_v1.md` — public wording and release-polish notes.

Public wording standard: ALETHEIA is a free, open-source governance mirror. Its outputs are internal governance-risk readings and repair prompts, not verdicts or certifications.

Boundary preserved: Patch 114 is public release/documentation polish only. It does not change runtime behavior, scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantees, or final-truth behavior.


## Structural improvement entry point

Patch 102 starts the maintainability/onboarding path recommended by external review. The first structural move is documentation-first: clarify architecture, contributor entry, signal limitations, privacy/local-first posture, and the staged `app.py` reduction plan before any behavior-changing refactor.

Start here for the structural path:

- `docs/structural_improvement_entrypoint.md`
- `docs/architecture.md`
- `docs/new_contributor_start_here.md`
- `CONTRIBUTING.md`

Boundary preserved: Patch 102 changes documentation and tests only. It does not change scoring, verdict routing, receipt schemas, external-call behavior, telemetry, storage, or authority claims. ALETHEIA remains a bounded mirror: it surfaces signals; humans keep the judgment.

## Signal detection transparency

Patch 103 documents ALETHEIA's transparent rule-based and heuristic signal-detection posture. The signal system is intentionally reviewable and local-first: it uses inspectable patterns, bounded rules, and protocol guardrails rather than live model calls or opaque external analysis.

This is a strength for explainability and privacy, but it has limits. It may miss or misread irony, coded language, indirect coercion, culturally specific meaning, domain shorthand, long context-dependent arguments, or languages outside the English-first review scope.

Read: `docs/signal_detection.md`

Boundary preserved: Patch 103 is documentation and tests only. It does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, external calls, telemetry, storage, or authority claims. Signal results remain internal governance-risk readings, not verdicts or certifications. Human review remains required.

## Boundary, privacy, and hosted-use transparency

Patch 104 adds a central public boundary statement and hosted-use caveat. ALETHEIA is a **mirror, not a throne**: it surfaces governance-risk signals for human review, but it does not certify truth, safety, legality, ethics, privacy, security, or legitimacy.

Read these before public or sensitive use:

- `docs/BOUNDARY.md`
- `docs/privacy_boundary.md`
- `docs/hosting_limits.md`

Privacy posture: the repository is local-first by design and includes no built-in telemetry, analytics SDKs, trackers, backend upload endpoint, public ledger sync, Global ID sync, or central user-input storage. Inputs are processed in the active app session, and receipts are user-held downloads. For sensitive audits, run ALETHEIA locally. Hosted deployments may have platform-level logs outside ALETHEIA's application-code boundary.

Boundary preserved: Patch 104 adds documentation and small reusable helper modules only. It does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, Streamlit page behavior, external calls, telemetry, storage, or authority claims.

## Patch history and public trust navigation

Patch 105 adds a navigation layer for reviewers and contributors who need a shorter path through ALETHEIA's patch history and trust-relevant documents. Patch 113 consolidates that trust-facing path so `docs/public_trust_package.md` becomes the central map to boundary statements, privacy posture, hosting limits, signal detection, architecture, beginner UX, the privacy audit panel, patch history, and the public review checklist.

Read:

- `docs/public_trust_package.md`
- `docs/public_review_checklist.md`
- `docs/patch_index.md`
- `examples/Trust_Package_README.md`

This does not certify ALETHEIA or make it tamper-proof. It gives reviewers a clearer map: boundary, privacy, hosting limits, signal detection, architecture, beginner path, privacy audit panel, contributor start, patch status, and recovery notes.

Boundary preserved: Patches 105 and 113 are documentation/navigation patches only. They do not change runtime behavior, scoring, verdict routing, signal patterns, signal weights, receipt schemas, Streamlit page behavior, external calls, telemetry, storage, certification, enforcement, or authority claims.

## App shell router refactor

Patch 108 started the gradual `app.py` router/shell refactor by extracting the stable top-of-app boundary notices into `ui/app_shell.py`. Patch 109 continues that same behavior-preserving path by extracting the stable sidebar identity card and sidebar context copy into the same helper module. Patch 110 extracts the stable public header and first-use note. Patch 115 continues that same path by extracting static sidebar tuning-section headings and notes while leaving interactive controls in `app.py`. Patch 119 adds `ui/module_intro.py` and moves one small Stress Test module intro note into a copy-only helper. Patch 120 continues that module-intro path by moving two more static intro blocks: Boundary Cases and Consent-Audit. Patch 121 adds `ui/status_cards.py` for shared copy-only notice cards and moves the AI Integrity boundary caption group. Patch 122 adds a second stabilization checkpoint for the current helper boundary.

This keeps `app.py` as the orchestrator while moving static shell copy into a smaller reviewable file. Interactive controls, scoring, verdict routing, signal patterns, signal weights, receipts, downloads, and session-state behavior remain in `app.py`.

Boundary preserved: Patches 109-110, 115, 119, 120, 121, and 122 are UI shell/module-intro/status-card extraction or stabilization steps only. They do not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, telemetry, analytics, storage, privacy guarantees, certification, enforcement, or final truth claims.

## Low-risk page extraction

Patch 123 starts the page extraction phase by moving the in-app `Why ALETHEIA` / About tab copy into `pages_ui/about_page.py`. `app.py` remains the orchestrator for tabs, image resolution, widgets, session state, routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior.

Patch 124 adds `pages_ui/trust_package_page.py` and exposes the public trust package review route inside the Protocol Guide tab. The helper points reviewers to boundary, privacy, signal, architecture, beginner, patch-history, and public-review checklist docs while keeping those docs as the source of truth.

Boundary preserved: Patches 123 and 124 are page-level display extractions only. They add no external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantees, or final truth claims.

Patch 125 starts Evidence Lab static UI extraction by moving stable intro copy and public-data build guidance into `pages_ui/evidence_lab_page.py`. Evidence Lab uploads, dataframe processing, scoring, validation, downloads, receipts, session state, and World Lens synchronization remain in `app.py`.

Boundary preserved: Patch 125 is static UI copy extraction only. It adds no evidence processing change, upload handling change, dataframe logic change, scoring change, telemetry, analytics, certification, enforcement, privacy guarantee, or final truth claim.

## Final structural simplification freeze

Patch 126 records the corrected development principle: ALETHEIA is not in expansion mode. It is in refinement mode.

Allowed work from this point is limited to moving existing UI code into clearer files, removing duplication, consolidating repeated copy, improving documentation navigation, tightening regression tests, and locking existing behavior. The current behavior is treated as the release-candidate surface to preserve.

Boundary preserved: Patch 126 is documentation and regression-test only. No app runtime behavior change, new module, new scoring, new panel, new analysis mode, new intelligence, receipt schema change, module-routing change, session-state change, privacy scan change, AI Integrity scan change, World Lens math change, external calls, telemetry, analytics, storage, identity sync, certification, enforcement, privacy guarantee, or final truth claim.

## AI Integrity Mirror

AI Integrity Mirror is a static, local-first review module for pasted AI outputs, prompts, agent specs, model-card excerpts, policy claims, and code snippets. It reflects governance-integrity signals such as authority overreach, weak reviewability, opacity, coercion pressure, surveillance/identity capture, exposed credentials, and unsafe execution/data-flow markers.

It produces a reviewable risk reading for the pasted artifact only. It does not certify AI systems, approve vendors, benchmark live models, prove safety, replace human review, call external APIs, crawl repositories, or store pasted artifacts centrally.

Code Integrity Static Scan documentation lives in `docs/code_integrity_static_scan.md`. It is a static pasted-code review aid, not a vulnerability certification or security guarantee.

Rubric documentation lives in `docs/ai_integrity_rubric.md`; module notes live in `docs/ai_integrity_mirror.md`; ready-to-use demo files live in `examples/ai_integrity/` with notes in `docs/ai_integrity_demo_pack.md`. Patch 94 improves the review-table display with highest-pressure signals above the table, category grouping, collapsible evidence snippets, prominent repair questions, and clearer empty-state copy.


## Human-auditable protocol baseline self-audit

Patch 101 adds a local baseline self-audit for selected protocol, release-boundary, and AI Integrity files. Run:

```bat
python tools\run_protocol_baseline_self_audit.py
```

The check compares watched files against `data/protocol_baseline_manifest.json` and reports `MATCHES_BASELINE`, `MODIFIED_REQUIRES_HUMAN_REVIEW`, `MISSING_REQUIRES_HUMAN_REVIEW`, or optional `UNKNOWN_FILE_REQUIRES_HUMAN_REVIEW` statuses. It is human-auditable review evidence only: not tamper-proof, not automated approval, not security/privacy certification, and not proof of safety.

Go-live static privacy review notes live in `docs/go_live_privacy_review_statement.md`. The statement is a static repository review only; hosting and deployment logs remain outside ALETHEIA and require human review.

## 2-minute public explanation

ALETHEIA v0.1 helps reviewers examine governance documents and scenarios for capture risk, coercion risk, consent pressure, performative ethics, evidence gaps, missing safeguards, and repair gaps.

It may say: **Potential risk detected. Human review required. Safeguard missing. Evidence gap found.**

It must not say: **The AI has decided. This leader must be removed. This claim is finally verified. Human review is unnecessary.**

Core operating line:

> ALETHEIA reflects. Humans review. Power stays accountable.

## Scope layers

ALETHEIA should be read in layers:

- **Current operational layer** — a corruption-pattern and governance-risk detection framework for human review. It surfaces evidence gaps, consent pressure, capture risk, power concentration, missing safeguards, and authority-overreach signals.
- **Research layer** — hypotheses, benchmarks, empirical mappings, scenario tests, and validation work that may make the mirror more precise over time.
- **Vision layer** — a long-term theoretical horizon exploring what governance would look like if anti-corruption principles were followed consistently: transparency, consent, accountability, proportionality, dignity, appealability, repair, and limits on concentrated power.
- **Out-of-scope layer** — ALETHEIA does not govern, enforce, allocate authority, select representatives, create a real 9k body, issue mandates, validate spiritual or political authority, or replace human judgment.

The incorruptible-system framing is a theory horizon, not a present capability claim. The current tool is narrower: a mirror for detecting corruption patterns and governance-risk pressure before humans decide what, if anything, should be done.

Public release documentation now lives in `docs/limitations.md`, `docs/ethics.md`, `docs/public_release_notes.md`, and `docs/scope_layers.md`.

Public evaluation cases now live in `examples/evaluation_cases/`, with method notes in `docs/evaluation_method.md` and a catalog in `docs/public_test_cases.md`. They are copy/paste test prompts for checking whether ALETHEIA surfaces risk signals, evidence gaps, consent pressure, capture risk, and authority-overreach concerns without claiming final authority.

## Differentiation from other governance tools

ALETHEIA is not an enterprise AI governance platform, compliance engine, legal tool, institutional risk system, or technical fairness library. Its niche is **qualitative governance-risk reflection**: corruption-pattern signals, consent pressure, capture risk, evidence gaps, authority-overreach language, weak accountability, and repair questions for human review.

Enterprise AI governance platforms generally focus on organizational workflows such as model inventories, compliance mapping, monitoring, reporting, approvals, vendor review, and audit artifacts. Technical fairness libraries generally focus on model-level bias, explainability, dataset, and metric workflows. ALETHEIA focuses on the power-analysis layer before, around, and beyond those tools.

ALETHEIA is free/open-source code and is intended to remain free. This is part of its anti-capture posture: access to the mirror should not become a gatekeeping mechanism or a source of institutional authority. See `docs/comparison_positioning.md`.


## Capture Risk Signals Framework

ALETHEIA is **anti-capture by design and capture-risk-detecting by function**.

It functions as a mirror that surfaces capture-risk signals such as power concentration, weak appeal paths, hidden influence, evidence gaps, consent pressure, authority overreach, and service misalignment.

ALETHEIA reflects these signals for human review only. It does not enforce, decide, gatekeep, certify, punish, or become a central authority. See `docs/capture_risk_framework.md`.

## Capture Risk Checklist / Prompt Pack

Patch 78 adds a practical one-page checklist and copy/paste prompt pack for applying the capture-risk framework without turning ALETHEIA into an authority.

- Checklist: `docs/capture_risk_checklist.md`
- Prompt pack: `examples/capture_risk_prompts/`

The checklist helps reviewers scan for power concentration, weak appeal paths, hidden influence, evidence gaps, consent pressure, authority overreach, and service misalignment. Prompts must keep the same boundary: ALETHEIA reflects signals for human review only; it does not decide, enforce, certify, punish, or become a central authority.

## Android APK wrapper

Patch 79 adds an optional lightweight Android WebView wrapper in `android_webview/`. The wrapper is named **ALETHEIA Mirror** and opens the live Streamlit app at `https://aletheialive.streamlit.app/`.

This is not a native rewrite and not an offline mobile version. It is a small APK shell for easier Android access while the actual ALETHEIA app remains the hosted Streamlit governance-risk mirror.

The wrapper requests only Android internet access. It does not add ads, trackers, analytics SDKs, push notifications, native storage, public ledger sync, Global ID sync, central storage, enforcement behavior, or authority claims. Build notes live in `docs/android_apk_wrapper.md`.

Patch 80 adds a signed-release APK guide for safer direct sharing: `docs/signed_release_apk.md`. The repository includes only an example signing file; private keystores, passwords, and `signing.properties` must stay local and must never be committed.

If a built APK shows a default `Hello Android!` screen instead of the live web app, it was likely built from a default Android template or wrong project folder. Use the troubleshooting guide: `docs/android_webview_troubleshooting.md`.

Patch 82 adds the ALETHEIA launcher icon to the Android wrapper and hardens the wrapper against stale default-template builds. The launcher now uses the repository mascot/logo assets instead of the default Android icon, and both Groovy and Kotlin Gradle files are aligned to the WebView package.

Patch 83 fixes Android Gradle Plugin resolution for signed APK builds. The wrapper project now defines plugin repositories and the `com.android.application` version at the project root, while the `app` module remains the only Android application module.

Patch 84 fixes Android adaptive launcher-icon resource placement for release builds that fail with `<adaptive-icon> elements require a sdk version of at least 26`. See `docs/android_adaptive_icon_resource_fix.md`.


The v0.1 release package lives in `docs/v01_release_package.md`. It summarizes included modules, out-of-scope boundaries, quickstart commands, sample-report links, and release readiness checks.




## ALETHEIA v1.0 release complete

ALETHEIA v1.0 is the finished public MVP package for the Governance Mirror line. It preserves the core rule:

> ALETHEIA reflects. Humans review. Power stays accountable.

v1.0 includes the baseline, safe-language layer, Eternal Baseline, Boundary Cases Matrix, Failure Classification, Consent-Audit Engine, Mechanism-vs-Claim Scanner, Self-Audit Mode, Evidence Lab, Local Witness Receipt v2, World Lens Simulation, Protocol Guide, sample reports, demo inputs, release checklist, GitHub cleanup package, and final smoke release documentation.

Final release documents:

- `docs/v1_release_complete.md`
- `docs/v02_roadmap.md`
- `docs/feature_backlog.md`
- `docs/out_of_scope_future_modules.md`
- `docs/report_export_polish.md`
- `docs/manual_evidence_attachment.md`
- `docs/rubric_weighting_confidence.md`
- `docs/deployment_prep.md`

Current safe check:

```bat
tools\run_checks.bat
```

Patch bundle check:

```bat
tools\run_patch_checks.bat 56_60
```

v1.0 remains non-authoritative: no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no public ledger authority, no neural validation, no religious validation, no legal authority, and no automated enforcement.


## ALETHEIA v0.1 public-safe baseline

The current logic-mapping phase adds a public-safe baseline before larger governance features are added. The baseline is documented in:

- `docs/baseline_v01.md`
- `docs/eternal_baseline.md`
- `docs/safe_language_map.md`
- `docs/logic_mapping_roadmap.md`
- `docs/protocol_guide.md`
- `docs/boundary_cases_matrix.md`
- `prompts/boundary_case_prompt.md`
- `docs/failure_classification.md`
- `prompts/failure_classification_prompt.md`
- `docs/consent_audit_engine.md`
- `prompts/consent_audit_prompt.md`
- `docs/mechanism_vs_claim_scanner.md`
- `prompts/mechanism_vs_claim_prompt.md`
- `docs/self_audit_mode.md`
- `prompts/self_audit_prompt.md`
- `docs/evidence_lab.md`
- `prompts/evidence_lab_prompt.md`
- `docs/local_witness_receipt.md`
- `prompts/local_witness_receipt_prompt.md`
- `docs/world_lens_simulation.md`
- `prompts/world_lens_prompt.md`
- `docs/progress_database.md`
- `docs/patch_workflow.md`
- `docs/git_diff_workflow.md`
- `docs/limitations.md`
- `docs/ethics.md`
- `docs/public_release_notes.md`
- `docs/v01_release_package.md`
- `docs/ux_polish.md`
- `docs/final_v01_smoke_release.md`
- `PATCH_STATUS.md`

Core rule:

> ALETHEIA reflects. People decide.

ALETHEIA may identify capture risk, coercion risk, manipulation risk, evidence gaps, safeguard gaps, and repair gaps. It must not command, enforce, vote, govern, remove leaders, validate spiritual authority, or replace human judgment.

The Eternal Baseline is a versioned ethical reference layer, not a command layer. It preserves continuity across versions while remaining audit-ready, correctable, and subordinate to human review.

The Boundary Cases Matrix adds a calibration layer for edge cases such as prediction vs free agency, consent under pressure, ambient capture, performative ethics, extraordinary claims, and self-audit. Boundary cases are stress tests for human review, not automated decisions.

Failure Classification adds a repair-oriented diagnostic layer that separates Actor Failure, Policy Failure, Implementation Failure, and Data Failure before recommending safeguards. It is not a blame engine or enforcement mechanism.

The Consent-Audit Engine adds a focused check for whether consent is genuinely voluntary. It asks whether refusal is realistically possible without losing basic rights, safety, dignity, essential services, appeal, exit, or correction. It reflects consent pressure for human review; it does not void agreements, punish people, or replace legal judgment.

The Mechanism-vs-Claim Scanner adds a performative-ethics check. It distinguishes value language such as “we protect freedom” from operational safeguards such as appeal, audit trail, time limits, correction, evidence requirements, and independent review. It may flag missing mechanisms for human review; it must not infer bad faith or assign final intent.

Self-Audit Mode points the mirror back at ALETHEIA itself. It checks baseline documents, prompts, rubrics, README language, app copy, architect-context language, and generated reports for founder capture, ideological lock-in, unverifiable authority, overclaiming, spiritual authority leakage, missing correction loops, and weak human-review safeguards. Self-audit is not proof of correctness; it is a repair-oriented review layer.

Patch 40 Evidence Lab hardening adds explicit evidence status levels and the Extraordinary Claim Protocol. It treats spiritual, prophetic, alien, neural, metaphysical, or otherwise exceptional claims as unverified unless supported by public, testable, non-coercive evidence. It audits policy consequences and evidence gaps; it does not validate spiritual authority or remove human review.

Patch 41 Local Witness Receipt v2 hardening adds explicit document, processed-document, report, and receipt fingerprints, plus app/rubric/prompt version context and an authority boundary: stored locally Yes; public ledger No; Global ID sync No; central storage No; authority claim No; human review required Yes.

Patch 43 Protocol Guide consolidation links the v0.1 modules into one operating guide: Baseline, Safe Language Layer, Eternal Baseline, Boundary Cases, Failure Classification, Consent-Audit, Mechanism-vs-Claim, Self-Audit, Evidence Lab, Local Witness Receipt v2, and World Lens Simulation. It adds no authority; it makes the mirror logic easier to understand and review.

Patch 44 Progress Database + Patch Status Hardening adds a local continuity workflow. Patch state, next-patch direction, module mapping, check commands, and the patched-items-only rule are tracked in `PATCH_STATUS.md`, `docs/progress_database.md`, and `docs/patch_workflow.md`, so project continuity is not dependent on chat memory alone.

Patch 45 Public README + Limitations Polish adds public-facing release documentation: `docs/limitations.md`, `docs/ethics.md`, and `docs/public_release_notes.md`. It clarifies the non-authority boundary, evidence limitations, archive caution, and v0.1 prototype scope.

Patch 42 World Lens Simulation adds a non-sovereign population-impact mirror. It reviews affected groups, power gains, protection losses, basic-rights risk, minority-rights risk, ambient capture, appealability, exit, and repair using safe simulated-threshold language. It does not activate Global ID, select a real 9k, create World Leader logic, issue automatic resets, or make governance decisions.


Patch 51 Git Diff Workflow Setup adds an optional `.diff`-based developer workflow through `docs/git_diff_workflow.md`, `tools/check_git_status.bat`, and `tools/export_patch_diff.bat`. It helps reduce zip-based patching while preserving the patched-items-only fallback.

Patch 50 v0.1 Release Package gathers the public MVP boundary into one document: included modules, explicit exclusions, quickstart commands, current safe checks, release readiness criteria, and the rule that ALETHEIA remains a mirror for human review rather than an authority system.

Patch 52 UX Polish adds shorter public-facing navigation guidance and a first-use path. It helps new users choose the right tab without changing doctrine, scoring, evidence handling, governance boundaries, or authority rules. The UX rule is: clearer copy is allowed only when it makes review easier and authority claims weaker.

Patch 54 Example Audit Runner / Demo Inputs adds opt-in demo inputs under `examples/demo_inputs/`. Demos load only by explicit user choice; user-submitted input remains the default. It adds no automatic demo analysis.

Patch 53 Final v0.1 Smoke Release adds `docs/final_v01_smoke_release.md` and a release-level smoke test. It verifies that release docs, examples, workflow commands, safe-language boundaries, and non-authority framing remain present after the v0.1 hardening sequence. It adds no doctrine or governance authority.

Historical archive material may contain AI-flattery artifacts or inflated validation language. Such material is treated as development context, not independent proof, founder validation, or governance justification.



## GitHub-ready public package

Patch 55 adds a public repository cleanup layer:

- `docs/github_cleanup_package.md` — public sharing checklist and release boundary
- `docs/repository_map.md` — where important app, docs, examples, tools, and tests live
- `docs/contributing.md` — contribution principles and local check commands

These files are documentation-only. They do not add governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger authority, neural validation, religious validation, legal authority, or automated enforcement.

## Local patch workflow

Run all local checks from Command Prompt inside the project folder:

```bat
tools\run_checks.bat
```

Run checks for one patch:

```bat
tools\run_patch_checks.bat 36
```

Package only files listed in a patch manifest:

```bat
python tools\package_patched_items.py PATCH_36_MANIFEST.txt ALETHEIA_patch36_patched_items_only.zip
```

Patch status and roadmap continuity are tracked in `PATCH_STATUS.md`, `docs/progress_database.md`, and `docs/patch_workflow.md`.

The optional Git diff workflow lives in `docs/git_diff_workflow.md`. It explains how to initialize Git, apply future `.diff` patches with `git apply`, preview them with `git apply --check`, export local changes, and fall back to patched-items-only zip files when needed.


## Prototype scope

This is a visionary research prototype and symbolic/evidence-audit workflow. It is not a real political system, legal authority, religious authority, medical authority, official institution, election mechanism, sovereign body, or tool for making binding decisions about people or countries.

The responsible interpretation is:

> This model suggests a governance-risk pattern worth examining.

Not:

> This model has final authority.

## Current operating layers

- **Audit** — governance-language and scenario risk review using Sanctuary / Threshold / Asylum labels, Sydney Protocol guardrails, and visible module integrity checks.
- **Simulation** — V-Axis system-health simulation tracking stability, trust, alignment, ego, grievances, friction, safeguards, and collapse risk.
- **Empirical Evidence Audit Lab** — public country-year evidence ingestion, direct/master upload handling, WGI/WDI/V-Dem/trust carry-through, ALETHEIA variable mapping, scoring, validation checks, and downloadable scored outputs.
- **Global Grid** — selected-year country-year comparison interface for population-weighted exposure, 9k allocation where complete, active-seat diagnostics where partial, verdict distribution, integrity/collapse metrics, and coverage diagnostics. 9k is treated as a human anti-tyranny scaffold, not a source of final legitimacy.
- **Doctrine Reference** — current operating doctrine: mirror not throne, shared protocol state, non-divinization, empirical correction, Humility Protocol / Z-axis boundary, 9k representation boundaries, and Sydney/GPA HTML references.
- **About** — plain-language explanation, scientific caution, research direction, and developer notes.
- **Failure Classification** — diagnostic separation of actor, policy, implementation, and data failure modes for better repair targeting.
- **Consent-Audit Engine** — consent integrity review using Green / Yellow / Red ratings for refusal reality, basic-rights dependency, withdrawal, appeal, and pressure signals.
- **Mechanism-vs-Claim Scanner** — performative-ethics review that compares ethical claim language against concrete safeguards such as appeal, audit trail, time limits, correction, exit, evidence rules, and independent oversight.
- **Self-Audit Mode** — internal anti-capture review of ALETHEIA baseline, prompts, rubrics, app copy, README language, architect-context language, and generated reports.
- **Evidence Lab + Extraordinary Claim Protocol** — evidence quality review using Strong / Partial / Weak / No evidence supplied levels, with unverified handling for extraordinary claims and policy-consequence review.
- **Local Witness Receipt v2** — local, user-held review fingerprints with document/report hashes, app/rubric/prompt versions, active modules, and explicit no-ledger/no-sync/no-authority boundaries.
- **World Lens Simulation** — non-sovereign population-impact review for affected groups, power shifts, protection losses, basic-rights risk, minority-rights risk, ambient capture risk, appealability, exit, and repair, using simulated threshold signals only.
- **Protocol Guide Consolidation** — user-facing map that connects all v0.1 modules and safe-language boundaries in one reviewable operating guide.

## Shared protocol state

Audit, Simulation, Empirical Evidence, and Global Grid are synchronized views over a shared protocol state. Changes to empirical evidence, scoring calibration, doctrine thresholds, Sydney Protocol overlay, selected evidence year, or active Grid basis may propagate across modules.

This is intentional when it reflects shared evidence or shared doctrine. It is not acceptable when caused by accidental widget collisions, hidden demo fallback, stale session state, or unmarked prototype data.

The app therefore distinguishes:

- **Intentional protocol propagation** — evidence, calibration, and doctrine updates affecting all relevant modules.
- **Accidental tab bleed** — unintended UI state changes crossing between modules.

## Module integrity and fail-closed behavior

The app keeps a Sydney Protocol / module integrity sentinel active. Critical protocol failures should fail closed rather than present unsupported outputs.

Audit includes a visible module integrity check so failures are not hidden behind the global app gate. If a critical Sydney Protocol sentinel, audit function, scoring function, or required module is missing or broken, the system should stop that module until repaired.

## Doctrine frame

The doctrine layer is the integrity frame for the prototype. It does not replace evidence or human judgment. It keeps ALETHEIA anchored as an anti-capture, service-aligned audit mirror.

Key operating principles:

- **Mirror Effect** — power should reflect service through accountability, dignity, protection, transparency, repair, and appealability.
- **V-Axis Compass** — intelligence + power − ego can support stability only when trust, transparency, appealability, service alignment, and safeguards are present.
- **Non-divinization** — no person, office, institution, nation, company, model, AI, monarch, founder, dataset, doctrine, or protocol is treated as final or beyond review.
- **Empirical humility** — outputs are diagnostic and correctable; they are not legal, political, medical, religious, moral, or predictive verdicts.
- **No throne condition** — ALETHEIA must never become the authority structure it audits.

## Evidence framing

ALETHEIA does not invent the empirical baseline. Public datasets provide observed evidence about governance, corruption, rule of law, political stability, institutional capacity, population, democracy, constraints, and trust.

The empirical workflow is:

```text
public evidence → ALETHEIA variable mapping → empirical scoring → Sydney Protocol overlay → audit interpretation
```

Raw empirical strength cannot override hard protocol failures such as capture, coercion, non-appealability, false authority, opacity, sovereignty capture, or harmful authority.

## Empirical data currently supported

The empirical workflow supports and/or carries through:

- World Bank WDI Population, total (`SP.POP.TOTL`).
- World Bank Worldwide Governance Indicators (WGI).
- V-Dem democracy / executive-constraints fields.
- WVS/OWID generalized trust values.
- Direct uploaded country-year master files.
- Already-scored ALETHEIA master/Grid exports.

The app can generate or consume country-year masters, compute ALETHEIA empirical scores, allocate seats by selected year, preserve raw evidence fields where available, and export scored evidence tables.

## Trust evidence rule

ALETHEIA distinguishes raw trust evidence from trust priors.

- **Trust raw coverage** means direct survey-derived trust evidence is available, such as WVS/OWID generalized trust.
- **Trust prior coverage** means the scoring system has a usable trust prior, which may include a neutral/default value when raw survey evidence is unavailable.

A neutral trust prior is not the same as observed trust. It allows scoring continuity, but it should reduce interpretive confidence when raw trust evidence is missing.

## Global Grid interpretation

The Global Grid is a selected-year comparison interface, not a sovereign body or mandate.

Full allocation years may sum to 9,000 seats. Partial years, filtered views, or incomplete source years must use **active selected-year seats** language and must not be interpreted as full global allocation.

The Grid distinguishes:

- full empirical selected-year Grid,
- partial empirical subset,
- prototype regional brackets,
- inactive/no dataset state.

Coverage metrics reflect the active selected-year subset after filters. A 100% coverage value over a small subset does not imply whole-world or whole-dataset coverage.


## Humility Protocol / Sanctuary as Asymptote

Patch 72.4 keeps the Z-axis language neutral and current. The Z-axis is not a perfection score. It maps how close a reading is to the boundary of what human and system tools may responsibly claim.

- `Z=0.0000` means full ASYLUM pressure: coercion, opacity, or concentrated control.
- `Z=0.9999` is the maximum human/system boundary ALETHEIA may display.
- `Z=1.0000` remains outside ALETHEIA's claim: beyond scoring, code, receipts, hashes, trees, 9k structures, and institutional power.

9k is a human anti-tyranny scaffold / threshold steward. It is not a final safety claim and not a source of final legitimacy.

## Sanctuary / Threshold / Asylum labels

These are internal prototype labels, not legal, political, medical, religious, moral, or predictive verdicts.

- **SANCTUARY** — the evidence or scenario pattern appears low-risk, service-aligned, accountable, transparent, safeguarded, and comparatively stable under the current model. This remains an internal review label, not final safety or final authority.
- **THRESHOLD** — safeguards are incomplete, evidence is mixed, uncertainty remains, or the system needs review and repair before being treated as stable.
- **ASYLUM** — high capture, coercion, opacity, harm, collapse pressure, or hard protocol failure is detected.

“ASYLUM” is used only as an internal protocol-risk category. It does not refer to legal asylum status, entitlement, refugee status, or humanitarian determination.

## Project structure

```text
app.py                  # Streamlit UI, tab layout, shared protocol state, Global Grid surfaces
about_page.py           # compact About renderer and doctrine-facing summary text
agents.py               # compact Global Grid module/fallback
core/parser.py          # local/AI governance scan helpers
core/protocol.py        # Sydney Protocol / ethics guardrail logic
core/simulation.py      # agent-based V-Axis stability simulation
core/scoring.py         # integrity, friction, collapse probability, recommendations
core/empirical.py       # country-year parsing, source carry-through, scoring, 9k allocation, validation helpers
core_empirical.py       # import fallback for Streamlit deployments
calibration/            # calibration helpers
config/weights.py       # I/A/E/P weight presets
data_processed/         # empirical templates and generated scores
paper/methodology.md    # methodology notes for study development
assets/                 # header image and optional UI assets
Sydney_Protocol_v3.2.html
GPA_v8.2.html
requirements.txt
run_tests.py
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Validation and research direction

Internal correlation checks are not independent validation when the target variable is also part of the score. Credible validation should compare ALETHEIA outputs against external outcomes that are not already score inputs, such as conflict events, coups, regime breakdown, political violence, civil unrest, forced displacement, future-year governance decline, institutional failure, or documented corruption shocks.

The model should remain testable, falsifiable, and correctable. If reproducible evidence challenges the model, the model should be revised rather than defended as absolute.

## Current phase

Global Grid Pass 1 is operational. The recommended next build target is **Global Grid Pass 2**, focused on comparison views:

- highest and lowest integrity systems,
- highest collapse-probability systems,
- largest selected-year seat allocations,
- high-impact governance-risk nodes,
- verdict distribution comparisons,
- trust vs democracy scatter,
- WGI vs V-Dem comparison,
- coverage gaps by country/year,
- trust-materiality diagnostics,
- exportable selected-year comparison packets.


## Sample reports

Patch 46 adds public-safe examples so users can see ALETHEIA output before uploading their own documents.

- `docs/sample_reports.md` — overview of the sample set.
- `examples/example_policy_audit.md` — Mirror Check policy audit example.
- `examples/example_boundary_case.md` — Boundary Case example for consent under pressure.
- `examples/example_self_audit.md` — Self-Audit example that checks Aletheia language for founder capture and overclaiming.
- `examples/example_witness_receipt.md` — Local Witness Receipt v2 example.

The examples are demonstration artifacts only. They are not legal advice, policy commands, governance decisions, religious validation, or final judgments.

To check Patch 46 locally:

```bat
tools\run_patch_checks.bat 46
```


## App navigation smoke test

Patch 47 made the original visible v0.1 app path explicit. Patch 142.16 places Boundary Cases after World Lens so the primary work modules come first:

1. Mirror Check
2. Stress Test
3. AI Integrity Mirror
4. Evidence Lab
5. World Lens
6. Boundary Cases
7. Protocol Guide
8. Why ALETHEIA

The navigation map is documented in `docs/app_navigation_smoke.md`. Every tab reflects, explains, stress-tests, or documents. No tab commands, enforces, validates spiritual authority, replaces legal review, replaces human judgment, activates Global ID, selects a real 9k, removes a leader, issues an automatic reset, or makes final governance decisions.

To check Patch 47 locally:

```bat
tools\run_patch_checks.bat 47
```


## Release candidate checklist

Patch 48 adds `docs/release_candidate_checklist.md` as the v0.1 readiness gate.

The checklist covers:

- included public-safe modules;
- explicit v0.1 exclusions;
- safe and forbidden output language;
- manual smoke-test steps;
- automated check commands;
- release readiness criteria;
- archive/flattery caution.

A release candidate is not a truth claim. It is a testable package. ALETHEIA reflects, humans review, and power stays accountable.

To check Patch 48 locally:

```bat
tools\run_patch_checks.bat 48
```


## Legacy test cleanup

Patch 49 separates current safe checks from older legacy tests. Use this as the default local check:

```bat
tools\run_checks.bat
```

For Patch 49 only:

```bat
tools\run_patch_checks.bat 49
```

The full legacy suite is intentionally explicit because older tests may still reference changed APIs or duplicate test paths:

```bat
tools\run_full_checks.bat
```

Known cleanup candidates are documented in `docs/legacy_test_cleanup.md`. This patch changes developer workflow only; it does not add governance authority, Global ID sync, 9k selection, World Leader logic, automatic reset, public ledger, neural data, memory extraction, spiritual validation, or automated enforcement.


## UX Polish

Patch 52 adds `docs/ux_polish.md` and short first-use guidance:

- Have a document? Use Mirror Check.
- Have a scenario? Use Stress Test.
- Have an ethical edge case? Use Boundary Cases as a reference layer after the main work modules.
- Have a claim or source question? Use Evidence Lab.
- Need impact framing? Use World Lens.
- Need rules and limits? Use Protocol Guide.

UX polish changes copy and navigation guidance only. It does not add governance authority, legal authority, religious validation, Global ID sync, real 9k selection, World Leader logic, public ledger, neural validation, or automated enforcement.

To check Patch 52 locally:

```bat
tools\run_patch_checks.bat 52
```

## Final v0.1 Smoke Release

Patch 53 adds `docs/final_v01_smoke_release.md` as the final release-level smoke checklist for v0.1.

To check Patch 53 locally:

```bat
tools\run_patch_checks.bat 53
```

For the safe default check:

```bat
tools\run_checks.bat
```

Patch 53 confirms the release package remains a reviewable mirror: no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no public ledger, no neural validation, no religious validation, no legal authority, and no automated enforcement.

### Patch 61A — Asylum Repair Questions

High-risk, ASYLUM, or Malicious Leadership outputs now attach Silent Operator repair questions so the mirror does not end on an empty repair path. These questions are for human review only; they do not create enforcement or authority.



### Patch 61B — Malicious Leadership Metric Calibration

Patch 61B keeps ASYLUM / malicious leadership outputs numerically coherent. If a scenario describes malicious, authoritarian, coup, takeover, or no-appeal leadership language, ALETHEIA prevents perfect trust/alignment and near-zero ego from being displayed unless concrete safeguards are present.

This remains a mirror-only calibration: it does not command, enforce, remove leaders, validate authority, or replace human review.

Check:

```bat
tools\run_patch_checks.bat 61B
```


Patch 61C adds a Country-Year Available-Year Filter so World Lens / Evidence Lab year controls show only years available for the selected country and avoid silent global/default fallback.


## Patch 61D — Missing Raw Trust Display

Patch 61D clarifies World Lens trust interpretation by separating observed raw trust evidence from neutral trust-prior fallback values. Missing raw trust is displayed as `not available`, and neutral priors are labeled as `0.500 neutral default`.

Check:

```bat
tools\run_patch_checks.bat 61D
```

### Patch 61E — World Lens Value Guards

Patch 61E adds selected-year value guards for World Lens. It verifies that seat totals, focus-country cards, verdict-seat totals, and trust-prior interpretation remain tied to the active selected year and do not silently fall back to stale/global values.


### Patch 62 — Post-61 Regression Smoke Test

Patch 62 adds a consolidation smoke test after the 61A–61E calibration series. It verifies ASYLUM repair questions, malicious-leadership metric calibration, country-year available-year filtering, missing raw-trust labels, selected-year 9k value guards, and Netherlands 2024 fixture stability. It is diagnostic only and adds no authority or enforcement.

Check:

```bat
tools\run_patch_checks.bat 62
```


## Patch 63 — Post-62 Release Refresh

Patch 63 refreshes the public release surface after the Patch 61A–61E calibration series and Patch 62 regression smoke test.

It documents the current post-62 state:

- ASYLUM / High-risk outputs include repair questions for human review.
- Malicious leadership prompts cannot display perfect trust/alignment without concrete safeguards.
- Country-Year Explorer year choices are scoped to the selected country.
- Missing raw trust is labeled as unavailable, with neutral trust-prior fallback shown separately.
- World Lens selected-year values are guarded against stale/default fallback.

Current checks:

```bat
tools\run_checks.bat
tools\run_patch_checks.bat 63
```

Release boundary remains unchanged: ALETHEIA is diagnostic only and adds no governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger authority, neural validation, religious validation, legal authority, or automated enforcement.

## Patch 64 — Mirror Check Batch Baselines

Patch 71 records the official batch-file names for Mirror Check validation:

- `examples/batch_questions/repair_questions_v2_nl.txt`
- `examples/batch_questions/formal_doctrine_repair_questions_nl.txt`
- `examples/batch_questions/plain_language_questions_nl.txt`
- `examples/batch_questions/boundary_case_questions_nl.txt`
- `examples/batch_questions/world_lens_release_questions_nl.txt`

The batch contract is documented in `docs/mirror_check_batch_baselines.md`; the official file registry is documented in `docs/batch_file_catalog.md`.

Expected receipt behavior:

- each batch contains exactly 50 questions;
- each question is treated as `QUESTION_PROMPT`;
- each receipt is an `Audit Question / Review Tool`;
- scenario hashes should match the corresponding question text;
- normal governance scoring should remain suppressed for question prompts;
- local receipts preserve the authority boundary: no public ledger, no Global ID sync, no central storage, no authority claim, and human review required.

Check:

```bat
tools\run_patch_checks.bat 64
```

## Patch 65 — Stress Test Batch Baseline

Patch 65 adds Stress Test scenario-writing guidance and a first 50-scenario batch baseline:

- `docs/stress_test_prompting_guide.md`
- `docs/stress_test_batch_baselines.md`
- `examples/batch_scenarios/stress_test_scenarios_en_v1.txt`

Stress Test batch mode is explicit opt-in and local-only. It creates Simulation receipts for scenario-style governance stress tests. It does not publish, sync, enforce, decide, or create authority.

Check:

```bat
tools\run_patch_checks.bat 65
```

### Patch 66 — Stress Test Risk Sensitivity Calibration

Patch 66 hardens Stress Test scoring so subtle governance-risk scenarios do not wash into `SANCTUARY` solely because raw simulation metrics are stable. Missing appeal paths, no term limits, biometric access pressure, consent under pressure, fallback-data confusion, founder control, surveillance, and non-meaningful human review now route to at least `THRESHOLD / Needs Safeguards` unless explicit safeguards are present. Hard capture patterns still route to `ASYLUM / High`.

This remains mirror-only: ALETHEIA flags risk and asks for human review; it does not command, enforce, reset, remove leaders, sync Global ID, or create authority.


## Patch 67 — Stress Test Threshold Repair

Patch 67 improves medium-risk Stress Test outputs. `THRESHOLD / Needs Safeguards` scenarios now receive repair questions and light metric softening so they do not appear perfectly trusted or fully aligned while safeguards are missing. This remains mirror-only: no authority claim, no enforcement, no Global ID sync, no public ledger, and human review remains required.

### Patch 67.1 — Dutch Stress Test Lexicon

The Stress Test now includes Dutch governance-risk language so Dutch scenarios are not under-classified because earlier sensitivity rules were English-heavy. The Dutch batch baseline is available at:

```text
examples/batch_scenarios/stress_test_scenarios_nl_v1.txt
```

Patch 71 catalogs the official EN/NL scenario and question batch filenames in `docs/batch_file_catalog.md`.

Run the patch check with:

```bat
tools\run_patch_checks.bat 67_1
```

### Patch 67.2 — Dutch Stress Lexicon Gap Fix + App-Wide Input Scope

Patch 67.2 closes the remaining Dutch Stress Test lexicon gaps after Patch 67.1. DAO tokenholder concentration, emergency-law bypass without audit trail, term-limit removal, efficiency over appeal rights, and revolutionary power without independent audit now route to `THRESHOLD / Needs Safeguards` instead of `SANCTUARY`.

Current public copy clarifies the safer scope: **ALETHEIA is English-first. Dutch/Nederlands examples may be used for batch testing, but this is not a general app-wide language-compatibility claim.** Human review remains required.

Run:

```bat
tools\run_patch_checks.bat 67_2
```

## Patch 68 — Advanced English Stress Lexicon + Asylum Metric Enforcement

Adds advanced English Stress Test calibration for predictive sentencing, biometric/identity coercion, final-authority wallet capture, founder-keyword mirror capture, pre-emptive arrests, loyalty-to-state baseline capture, archive deletion, unaudited mirror code, and similar high-risk governance patterns. Advanced English stress scenarios route to `THRESHOLD / Needs Safeguards` or `ASYLUM / High` instead of washing into Sanctuary. Asylum metric enforcement now applies to non-malicious Asylum labels so receipts do not retain perfect trust/alignment or zero ego.

### Patch 69 — Stress Test question-prompt batches

Stress Test batch mode now treats formal audit / repair-question banks as review tools instead of governance scenarios. The baseline file is available at:

```text
examples/batch_questions/formal_doctrine_repair_questions_nl.txt
```

Expected receipt mode:

```text
Input status: QUESTION_PROMPT
Protocol-adjusted state: QUESTION_PROMPT
Risk: Review Tool
Protocol label: Audit Question / Review Tool
```

The user-used source file for this regression was named `formal doctrine repair-question baseline.txt`.

### Patch 69.1 — Stress Test scenario-vs-question upload detection

Stress Test `.txt` upload now distinguishes declarative scenario batches from audit-question batches.

Scenario statements such as:

```text
A smart-grid energy system automatically cuts power to homes without prior warning.
```

remain Simulation `USER_INPUT` items and receive normal Stress Test verdicts.

Audit questions such as:

```text
Wie heeft het laatste woord als de data en de menselijke intuïtie elkaar tegenspreken?
```

remain `QUESTION_PROMPT / Review Tool` receipts with normal metrics suppressed.

Check:

```bat
tools\run_patch_checks.bat 69_1
```


### Patch 68.1 calibration note

Stress Test receipts now keep ASYLUM labels and metrics consistent: ASYLUM / High outputs cannot retain THRESHOLD-style `Needs Safeguards` labels or perfect-looking trust/alignment metrics.

### Patch 70 — Tree visual calibration

Patch 70 clarifies the tree visual in Mirror Check and Stress Test. The tree is now framed as a visual state explainer, not a second authority layer and not a replacement for the local witness receipt.

- Mirror Check tree: evidence, accountability, safeguards, appeal, transparency, repair, basic rights, non-coercion.
- Stress Test tree: power under stress, consent, exit, appeal, time limits, independent review, evidence clarity, basic rights.
- QUESTION_PROMPT inputs render as Review Tool Mode and are not scored as Sanctuary, Threshold, or Asylum.
- The UI distinguishes visual tree score from protocol-adjusted integrity stored in the receipt.


## Patch 71 — Batch File Repository Consolidation

Patch 71 consolidates the official batch-file registry for `examples/batch_questions/` and `examples/batch_scenarios/`. The registry is documented in `docs/batch_file_catalog.md` and validates the official renamed batch files:

- `examples/batch_questions/repair_questions_v2_nl.txt`
- `examples/batch_questions/formal_doctrine_repair_questions_nl.txt`
- `examples/batch_questions/plain_language_questions_nl.txt`
- `examples/batch_questions/boundary_case_questions_nl.txt`
- `examples/batch_questions/world_lens_release_questions_nl.txt`
- `examples/batch_scenarios/stress_test_scenarios_en_v1.txt`
- `examples/batch_scenarios/stress_test_scenarios_nl_v1.txt`
- `examples/batch_scenarios/governance_language_stress_test_en.txt`

Latest verified Stress Test distributions remain documented as `stress_test_scenarios_en_v1: THRESHOLD 46 / ASYLUM 4 / SANCTUARY 0`, `stress_test_scenarios_nl_v1: THRESHOLD 50 / ASYLUM 0 / SANCTUARY 0`, and `governance_language_stress_test_en: THRESHOLD 29 / ASYLUM 21 / SANCTUARY 0`. This patch is repository/documentation/test consolidation only; it changes no scoring logic and adds no authority.

Run:

```bat
tools\run_patch_checks.bat 71
```

## Patch 71.1 note — module-specific demo labels

Patch 71.1 separates Mirror Check and Stress Test demo libraries in the UI. Stress Test now uses Stress Test-specific scenario demos and the `Load Stress Test scenario demo` button; Mirror Check keeps its own scenario demos and `Load Mirror Check scenario demo` button. This is a UI/demo-label correction only; scoring, receipts, tree visuals, batch catalogs, storage, and authority boundaries are unchanged.

## Patch 96 — Privacy Boundary Audit Panel

Patch 96 adds a static **Privacy Boundary Audit Panel** inside AI Integrity Mirror. It flags analytics packages, external network call patterns, telemetry keywords, database write hints, backend endpoint hints, local-only statement markers, and boundary tension between privacy claims and visible implementation hints.

Boundary preserved: static pasted-artifact review only. No analyzer scoring change, no verdict-routing change, no runtime monitoring, no host-log inspection, no dependency crawl, no repository crawler, no external calls, no live model benchmarking, no privacy guarantee, no compliance approval, no vendor audit, no hosting audit, no certification, and no proof that no data is collected.

Documentation: `docs/privacy_boundary_audit_panel.md`.


## Patch 97 — AI Integrity Comparison View

Patch 97 adds **AI Integrity Comparison View** for delimiter-separated AI Integrity batch artifacts. It shows side-by-side artifact-level risk readings, signal counts, boundary-risk comparison, category totals, and review needed notes.

Use it to compare pasted AI outputs such as Model A answer, Model B answer, and Model C answer after manually collecting the outputs. ALETHEIA does not call live models, benchmark live models, rank vendors, or certify systems.

Boundary preserved: static pasted-artifact comparison only. No analyzer scoring change, no verdict-routing change, no live model benchmarking, no external calls, no repository crawler, no enforcement, not model-wide certification, not a vendor ranking, and not a final truth claim.

Documentation: `docs/ai_integrity_comparison_view.md`.

## Patch 98 — AI Integrity Red Team Prompt Pack

Patch 98 adds a static **AI Integrity Red Team Prompt Pack v1** for manual testing. Users can copy prompts into a separate model or workflow, collect the outputs, and paste those outputs into AI Integrity Mirror for artifact-level review.

The pack covers authority overreach, legal/medical/political false authority, manipulation pressure, privacy extraction, surveillance/capture, false certainty, no-appeal automation, unsafe code request, refusal quality, and bounded-answer control.

Boundary preserved: static prompt examples only. ALETHEIA does not run prompts, call live models, benchmark live models, rank vendors, certify systems, certify code safety, guarantee truth, guarantee security, enforce decisions, or make model-wide certification claims.

Documentation: `docs/ai_integrity_red_team_prompt_pack.md`.


## Patch 99 — AI Integrity Report Builder

Patch 99 adds an **AI Integrity Report Builder v1** for batch results. It summarizes pasted artifact-level readings into a compact human-review packet with executive summary, artifact count, risk distribution, top triggered categories, selected redacted evidence snippets, repair questions, non-certification note, and privacy note. See `docs/ai_integrity_report_builder.md`.

Boundary: static pasted-artifact report only. No live model calls, no external calls, no repository crawl, no vendor ranking, no model-wide certification, no safety guarantee, no security guarantee, no privacy guarantee, and no final truth claim.

## Patch 100 — ALETHEIA v1.0 AI Integrity Preview

Patch 100 stabilizes the public adoption surface for the AI Integrity patch arc from Patch 85 through Patch 99.

Public adoption docs:

- `docs/ai_integrity_preview_public_adoption.md`
- `docs/ai_integrity_preview_release_notes.md`
- `docs/ai_integrity_screenshots_guidance.md`

The preview package gives new users a clear path from demo examples to batch review, comparison, code/privacy boundary review, red-team prompt outputs, and compact reports.

Boundary preserved: release-surface stabilization only. No analyzer scoring change, no verdict-routing change, no new live model call, no external call, no repository crawler, no vendor ranking, no model-wide certification, no security guarantee, no privacy guarantee, no legal/medical/political/religious authority, no public ledger sync, no Global ID sync, no central storage, no enforcement, and no final truth claim.

## Patch 106 — Signal Dictionary and Glossary

Patch 106 adds `docs/SIGNAL_DICTIONARY.md`, a reviewer-facing glossary for ALETHEIA signal families such as authority overreach, consent pressure, missing appeal or review, power concentration, capture risk, evidence gaps, surveillance or identity-sync pressure, automation without human review, non-transparency, and repair need.

The dictionary is a signal dictionary, not a scoring specification. It explains review questions, typical cues, possible false positives, and repair directions so reviewers can understand the rule-based / heuristic signal posture documented in Patch 103.

Boundary preserved: documentation-only. No runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no Streamlit page wiring change, no `app.py` refactor, no external calls, no telemetry, no analytics, no certification, no enforcement, and no final truth claim.



## Patch 107 — Boundary and privacy UI wiring

Patch 107 makes the existing boundary/privacy wording visible in the Streamlit sidebar. It wires the reusable `core/boundary.py` and `core/privacy_panel.py` helpers into `app.py` without changing scoring, verdict routing, signal patterns, signal weights, receipt schema, external calls, telemetry, analytics, storage, certification, enforcement, or final-truth behavior.

The visible rule remains: **ALETHEIA surfaces signals. Humans keep the judgment.**


## Patch 108 — App shell router refactor step 1

Patch 108 begins the gradual `app.py` router/shell refactor by extracting the stable top-of-app boundary notices into `ui/app_shell.py`. This is a narrow UI-structure change only; the visible boundary copy is intended to remain equivalent while `app.py` becomes easier to maintain.

No scoring, verdict routing, signal patterns, signal weights, receipt schema, external calls, telemetry, analytics, storage, certification, enforcement, or final-truth behavior changed.


App.py remains the orchestrator for behavior; Patch 109 only extracts sidebar shell copy.

### Patch 110 — App Shell Router Refactor Step 3

Patch 110 continues the gradual `app.py` router/shell refactor by moving the stable public header and first-use note into `ui/app_shell.py`. `app.py` remains the orchestrator for behavior, module routing, session state, scoring, receipts, downloads, and interactive controls.

Boundary preserved: Patch 110 is a UI shell extraction only. It introduces no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module routing change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.



## Patch 111 — Beginner Try This First UX

Patch 111 adds a compact beginner guide so first-time users have a safe starting path: Mirror Check, risk reading, observed reasons, repair questions, and optional local receipt download. The guide is rendered by `ui/beginner_guide.py` and wired under the public header in `app.py`.

Boundary preserved: Patch 111 is a small UX helper only. It introduces no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

## Privacy Audit Panel v1

Patch 112 makes the Privacy Boundary Audit Panel easier to maintain by moving its Streamlit rendering into `ui/privacy_audit_panel.py`. The underlying scan remains the static privacy-boundary review already used inside AI Integrity Mirror.

The panel reflects visible privacy-boundary signals in pasted artifacts: analytics hints, external network-call patterns, telemetry keywords, database-write hints, backend endpoint hints, local-only statements, and boundary tension. It provides review questions for humans.

Boundary preserved: app.py remains the orchestrator. Patch 112 does not change scoring, verdict-routing, signal-patterns, signal-weights, receipt schemas, module-routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, compliance approval, certification, enforcement, or final truth behavior. Humans keep the judgment.

## Patch 116 — App Shell Router Refactor Step 5

Patch 116 continues the gradual `app.py` reduction by extracting the stable footer banner into `ui/app_shell.py`. This is static shell extraction only. `app.py` remains the orchestrator for interactive controls, session state, module routing, scoring, receipts, downloads, and analysis behavior.

Boundary preserved: Patch 116 does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior. Humans keep the judgment.


## Patch 117 — Refactor Stabilization Checkpoint

Patch 117 pauses the app-shell router refactor sequence after Patch 116 and adds a stabilization checkpoint. It documents the refactor boundary in `docs/refactor_stabilization_checkpoint.md` and adds regression tests to verify that `ui/app_shell.py` remains a static shell-copy helper layer while `app.py` remains the orchestrator for interactive controls, session state, module routing, scoring, receipts, downloads, and analysis behavior.

Boundary preserved: no runtime behavior change, no scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior. Humans keep the judgment.

## Patch 118 — Beginner UX Polish v2

Patch 118 polishes the beginner path introduced in Patch 111. It adds a first-audit checklist, clearer “what this means / what this does not mean” copy, and stop-and-review prompts for cases involving rights, reputation, safety, legal/medical/political/institutional/financial consequences, missing evidence, or unclear receipts.

Boundary preserved: Patch 118 is static beginner UX copy and documentation only. It does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior. Humans keep the judgment.

## Patch 127 — Encoding Cleanup and Tab Icon Restore

Patch 127 repairs visible UTF-8 mojibake in the public app surface and restores the Streamlit tab icons after the late structural-refactor chain.

Scope: public UI text cleanup only. No scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, session state, privacy scan behavior, AI Integrity scan behavior, World Lens math, external calls, telemetry, analytics, storage or identity sync, privacy guarantees, certification, enforcement, or final-truth behavior changed. Human review remains required.

## Patch 128 — Public UI Text Consistency Pass

Patch 128 refines public-facing copy without changing behavior. It clarifies ALETHEIA's current stance: its strength is restraint; regulation is a floor, not the final measure of integrity; and the mirror asks where power is moving, who can appeal, what is hidden, and where human review is being weakened.

This patch updates the About / Why ALETHEIA page, Trust Package page, Evidence Lab static intro, and beginner guide copy. It is public UI text consistency only, not expansion. No scoring, routing, receipt schema, signal logic, privacy scan, AI Integrity scan, World Lens math, external call, telemetry, storage, certification, enforcement, or final-truth behavior changed. Human review remains required.

Patch 128 public wording note: the compliance mirage is a review concern, not a legal conclusion. ALETHEIA asks reviewers to look beyond paperwork toward power movement, appeal, hidden influence, and human review.

Patch 128 public wording note: regulation as a floor means compliance is not treated as the final measure of integrity; the compliance mirage remains a review concern, not a legal conclusion.

## Patch 129 — Input and Error Clarity Pass

Patch 129 is a refinement-only patch. It centralizes selected empty-input, language-calibration, and upload/read-failure messages in `ui/input_clarity.py` so user guidance is clearer without expanding ALETHEIA.

The patch clarifies that pasted AI Integrity artifacts are required, empty batch blocks are ignored, ALETHEIA is English-first and Dutch/Nederlands examples remain batch-test fixtures, not a general language-compatibility claim, and uploaded public data or CSV files may need file-type, column-name, encoding, and country/year checks. It does not change scoring, routing, receipts, signal logic, privacy scan behavior, AI Integrity scan behavior, World Lens math, external calls, telemetry, storage, certification, enforcement, or final-truth behavior. Human review remains required.
## Patch 130 — Release Candidate Freeze

Patch 130 records ALETHEIA as being in release-candidate refinement mode after the Patch 127-129 public polish sequence. The current behavior is the surface to preserve. Future work should be limited to bug fixes, copy/readability fixes, input clarity, test hygiene, documentation navigation, and small behavior-preserving cleanup.

This is not expansion. No new modules, no new scoring, no new risk states, no live model calls, no agentic review, no enterprise workflow, no telemetry, no analytics, no storage or identity sync, no certification, no enforcement, no privacy guarantee, and no final-truth claim are introduced or planned by this freeze.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
## Patch 135 - Aletheia Unit Preview v1

Status: READY FOR LOCAL REVIEW

Patch 135 adds Aletheia Unit Preview as a small first-entry preview before the full app appears. It suggests where to begin from a short pasted text, question, scenario, or receipt. It is a suggestion, not a decision, and users can still choose any module after entering ALETHEIA.

Boundary preserved: no scoring, no verdict routing, no taxonomy change, no receipt schema change, no receipt generation change, no signal regex or signal weight change, no AI Integrity scan behavior change, no Privacy Audit scan behavior change, no World Lens math change, no uploads/download behavior change, no batch behavior change, no storage, no external calls, no telemetry, no analytics, no accounts, no database, no Global ID sync, no public ledger sync, no new scoring engine, no new risk states, no final-truth claim, and no privacy guarantee. Human judgment remains required.


### Patch 137 validation alignment

Patch 137 is a test/check hygiene patch. It aligns older Start Page validation with the current Aletheia Unit Preview front door. It changes validation only; app behavior, scoring, receipts, signal logic, privacy scan behavior, AI Integrity behavior, and World Lens math remain unchanged.

### Patch 138 note: single Unit Preview entry

ALETHEIA now uses Aletheia Unit Preview as the single pre-app entry surface. The old Start Page is no longer an active gate. Unit Preview suggests where to begin; it does not score, certify, approve, reject, or replace the full modules.

## Patch 139 - Unit Preview Header Entry Hotfix

Patch 139 keeps Aletheia Unit Preview as the app's single hook before the module interface, but renders it after the public ALETHEIA header/styling. The first screen is now the polished ALETHEIA header plus Unit Preview, not a plain pre-header gate. Clicking Proceed to ALETHEIA opens the full module interface directly.

### Patch 140 orientation refinement

Aletheia Unit Preview is the first orientation surface. It now carries the practical `How to use this` guidance and short examples before the user enters the full app. After proceeding, the module tabs remain the working surface. Receipt Reader - Standard View is available as a support utility rather than a main module tab.


## Patch 160 — Why ALETHEIA + Protocol Guide Copy Polish

Patch 160 polishes the public Why ALETHEIA and Protocol Guide wording so the purpose is clearer and less doctrine-heavy. Why ALETHEIA now emphasizes why the mirror exists: systems can appear compliant, neutral, or benevolent while still hiding capture pressure, appeal failure, evidence inflation, or authority drift. Protocol Guide now reads as an operating-boundary guide rather than a command layer.

Boundary: copy/documentation only. No scoring, routing, taxonomy, receipt schema/generation, receipt parsing, empirical math, World Lens allocation, protocol logic, batch behavior, upload/download behavior, telemetry/storage, certification, enforcement, ranking, official authority, or final-truth behavior changed. Human review remains required.
