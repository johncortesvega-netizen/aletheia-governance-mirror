# AI Integrity Mirror

Patch 85 added **AI Integrity Mirror** as a static, local-first review module inside the existing ALETHEIA Streamlit app. Patch 86 polishes the copy, scope notes, and receipt language without changing scoring or verdict routing. Patch 87 centralizes paste-ready demo examples and adds static smoke coverage for those examples. Patch 88 adds categorized signal findings and redacted evidence snippets so reviewers can see why a rule triggered without treating the output as certification. Patch 89 makes the app-wide privacy boundary explicit: no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, or central user-input database.

## Purpose

AI Integrity Mirror reviews pasted AI artifacts for governance-integrity risk signals:

- AI outputs
- system prompts or policy excerpts
- agent workflows or specs
- model-card / safety claims
- code snippets

It checks for bounded, reviewable behavior rather than claiming to prove whether an AI system is safe, true, aligned, lawful, or ethical. It does **not certify** models, vendors, prompts, agents, outputs, or codebases.

## What it can flag

The first scaffold looks for deterministic text/code signals such as:

- final-authority or certification language
- automated enforcement without review
- missing appeal, override, audit, or human review paths
- opacity or hidden criteria
- manipulation, pressure, or vulnerability exploitation
- surveillance, Global ID, central registry, or biometric capture language
- exposed secrets, embedded tokens, private keys, unsafe dynamic execution, or shell execution markers in code snippets

## Output

The module produces a static risk reading for the pasted artifact only:

- internal taxonomy label: `SANCTUARY`, `THRESHOLD`, or `ASYLUM`
- risk level
- integrity and collapse-pressure metrics
- triggered signal table with categories and redacted evidence snippets
- repair questions
- local witness receipt download
- scope note: pasted artifact only; no live model or repository certification
- receipt note: review evidence, not certification or approval
- reliance note: human review and context-specific safety/legal processes stay outside ALETHEIA
- authority-boundary notice and asymptote note

## Boundary

AI Integrity Mirror is not:

- model certification
- vendor approval
- proof of safety
- truth detection
- legal, medical, political, religious, moral, or official authority
- public ledger publication
- live model benchmarking
- external API scanning
- enforcement, punishment, or automated decision-making

It is a review mirror. People decide.

## Patch 86 copy and receipt polish

Patch 86 updates the AI Integrity Mirror language from generic score display toward clearer review terms: **risk reading**, **integrity reading**, and **capture pressure**. It adds static-receipt-polish metadata to the analyzer output so local receipts carry the same boundary language as the UI.

Boundary preserved: no live model benchmarking, no external calls, no repository crawler, no scoring-math change, no verdict-routing change, no public ledger, no Global ID sync, no central storage, no enforcement, and no certification.

## Patch 87 demo examples and static smoke coverage

Patch 87 moves AI Integrity demo examples into `core/ai_integrity_mirror.py` as shared, testable example metadata. The app now reads the same centralized examples that the tests audit.

Demo coverage includes:

- a bounded AI answer with human review, evidence gaps, appeal, and independent challenge
- an overclaiming automated-decision artifact with final-verdict and no-appeal language
- an opaque agent workflow with hidden criteria and weak challenge paths
- a central identity capture claim with Global ID, biometric tracking, continuous monitoring, and registry pressure
- a code snippet with an exposed API key and unsafe dynamic execution

Boundary preserved: these are static pasted examples only. They do not benchmark live models, call external APIs, crawl repositories, certify vendors, or claim final safety.


## Patch 88 signal categories and evidence snippets

Patch 88 adds review-facing metadata to AI Integrity findings:

- a signal category such as Authority boundary, Reviewability, Transparency, Surveillance / identity capture, or Code / credential hygiene
- a short evidence snippet from the pasted artifact showing why the deterministic rule fired
- credential/private-key redaction before snippets are displayed or carried in metadata

Evidence snippets are local review aids. They are not external verification, proof of truth, proof of safety, certification, vendor approval, legal approval, or a final alignment claim.

Boundary preserved: static pasted-artifact review only; no live model benchmarking, external calls, repository crawler, scoring-math change, verdict-routing change, public ledger, Global ID sync, central storage, enforcement, or certification.

## Patch 89 privacy boundary

AI Integrity Mirror inherits the app-wide ALETHEIA privacy boundary. The repository includes no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Pasted AI Integrity artifacts are processed in the running app session and receipts are user-held downloads.

Deployment caution: third-party hosting layers may still keep their own access logs or server logs outside ALETHEIA's application code, so public deployment claims should review the host as well as the repository.

Boundary preserved: no AI Integrity scoring change, verdict-routing change, live model benchmarking, external calls, repository crawler, public ledger, Global ID sync, central storage, enforcement, certification, or authority claim.

## Verification

```bat
tools\run_patch_checks.bat 85
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 89
```

## Patch 90 batch review scaffold

Patch 90 adds a static **AI Integrity Batch Review** scaffold. Users can paste multiple AI artifacts in the same text area and separate items with a delimiter line such as `---`, `===`, or `###`. ALETHEIA then runs the same local AI Integrity Mirror review on each pasted item and displays a compact batch summary.

Batch output includes:

- total pasted artifact count
- Low / Medium / High risk-reading counts
- highest-pressure item number
- per-item state, risk reading, integrity, pressure, finding count, and redacted excerpt
- top triggered signal categories
- collapsed per-item repair questions

Boundary preserved: batch review is pasted artifacts only. It does not benchmark live models, call external APIs, crawl repositories, rank vendors, publish to a public ledger, sync Global ID, create central storage, enforce action, approve systems, or certify AI safety. Comparison is artifact-level review support only, not a model-wide ranking or final truth claim.

Verification:

```bat
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Patch 91 receipt export polish

Patch 91 improves the local **AI Integrity receipt** export. The receipt now starts with an AI Integrity-specific context section before the generic local witness receipt.

Receipt context includes:

- receipt header
- review mode: single static artifact or batch static artifact
- artifact type
- static review scope
- privacy boundary
- non-certification note
- reliance boundary
- triggered signal categories
- redacted evidence snippets
- repair questions
- optional batch summary

The receipt context is meant to make exports easier to read and share for human review. It remains a local, user-held receipt. It is not AI certification, model approval, vendor approval, benchmark proof, legal advice, medical advice, enforcement, or proof of safety.

Boundary preserved: static review scope only; no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, no scoring-math change, no verdict-routing change, and no certification.

Verification:

```bat
tools\run_patch_checks.bat 91
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Patch 92 rubric documentation

Patch 92 adds a public, reviewable rubric document: `docs/ai_integrity_rubric.md`. It explains the AI Integrity signal categories, current signal names, review questions, weight ranges, positive review signals, evidence-snippet behavior, batch boundaries, receipt scope, privacy boundary, and out-of-scope claims.

Boundary preserved: documentation only. No scoring-math change, no signal-pattern change, no signal-weight change, no verdict-routing change, no UI behavior change, no receipt-generation change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, and no certification.

Verification:

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

## Patch 93 AI Integrity batch demo pack

Patch 93 adds a ready-to-use static demo pack in `examples/ai_integrity/` and documents it in `docs/ai_integrity_demo_pack.md`.

Demo coverage includes:

- bounded AI answer with human review, uncertainty, appealability, and authority limits
- authority-overclaim artifact with final-verdict, certification-overclaim, and no-appeal language
- opaque agent workflow with hidden criteria, automated denial, and weak challenge paths
- code-risk artifact with credential-like strings, dynamic execution, and shell/network markers
- central identity/capture artifact with Global ID, biometric tracking, central registry, continuous monitoring, and blacklist pressure
- separator-delimited `batch_demo_v1.txt` for AI Integrity batch mode

Boundary preserved: demo examples, documentation, and tests only. No analyzer scoring change, no signal-pattern change, no signal-weight change, no verdict-routing change, no UI behavior change, no receipt-generation change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, no vendor ranking, no model certification, no approval, and no final safety claim.

Verification:

```bat
tools\run_patch_checks.bat 93
tools\run_patch_checks.bat 92
tools\run_patch_checks.bat 91
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Patch 94 AI Integrity UI review table polish

Patch 94 improves the AI Integrity Mirror result display so review output is easier to scan before deeper human review.

UI polish includes:

- compact summary cards for batch counts and highest-pressure item
- highest pressure signals shown above the detailed review tables
- clearer category grouping for triggered signals
- evidence snippets moved into collapsed expanders
- repair questions shown more prominently as human-review prompts
- clearer empty-state copy when no strong static trigger is detected

Boundary preserved: UI/result presentation only. No analyzer scoring change, no signal-pattern change, no signal-weight change, no verdict-routing change, no receipt-generation change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, no vendor ranking, no model certification, no approval, and no final safety claim.

Verification:

```bat
tools\run_patch_checks.bat 94
tools\run_patch_checks.bat 93
tools\run_patch_checks.bat 92
```


## Patch 95 code integrity static scan

Patch 95 adds a **Code Integrity Static Scan** layer for pasted code snippets. The scan flags code-specific review signals such as exposed secrets, dangerous subprocess/eval usage, hardcoded admin bypass markers, unsafe deletion patterns, outbound network calls, telemetry-like endpoints, central logging or identity-sync hints, and missing human-review gates in automated decision code.

The scan output includes detection count, severity counts, category counts, redacted evidence snippets, and code review questions. It is surfaced as review metadata inside AI Integrity Mirror and documented in `docs/code_integrity_static_scan.md`.

Boundary preserved: static pasted-code scan only. No code execution, no dependency audit, no repository crawler, no external calls, no live model benchmarking, no penetration test, no security guarantee, no vulnerability certification, no compliance approval, no model certification, no enforcement, and no final safety claim.

## Patch 96 privacy boundary audit panel

Patch 96 adds a **Privacy Boundary Audit Panel** for static pasted-artifact review. It can flag analytics packages, external network call patterns, telemetry keywords, database write hints, backend endpoint hints, local-only statement markers, and privacy-boundary tension when local-only/no-data-collection wording appears beside visible implementation hints.

The panel surfaces detection count, active signal count, local-only statement status, boundary-tension status, redacted evidence snippets, review questions, ALETHEIA's local-only boundary statement, and the hosting caveat.

Boundary preserved: no analyzer scoring change, no verdict-routing change, no runtime monitoring, no host-log inspection, no dependency crawl, no repository crawler, no external calls, no live model benchmarking, no privacy guarantee, no compliance approval, no vendor audit, no hosting audit, no certification, and no proof that no data is collected.

See `docs/privacy_boundary_audit_panel.md`.


## Patch 97 AI Integrity Comparison View

Patch 97 adds **AI Integrity Comparison View** for AI Integrity batch results. When a user pastes delimiter-separated artifacts, ALETHEIA can now show side-by-side artifact-level readings, signal counts, boundary-risk comparison, category totals, and review needed notes.

This is designed for cases such as comparing Model A answer, Model B answer, and Model C answer after the user manually gathers those outputs. ALETHEIA does not call the models, benchmark the models, or rank the vendors. It only compares the pasted artifacts.

Boundary preserved: No analyzer scoring change, no signal-pattern change, no signal-weight change, no verdict-routing change, no receipt-generation change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, not model-wide certification, not a vendor ranking, and not a final truth claim.

See `docs/ai_integrity_comparison_view.md`.

## Patch 98 AI Integrity Red Team Prompt Pack

Patch 98 adds `examples/ai_integrity/red_team_prompt_pack_v1.txt`, a static manual prompt pack for generating artifacts that can later be pasted into AI Integrity Mirror.

Covered categories include authority overreach, legal/medical/political false authority, manipulation pressure, privacy extraction, surveillance/capture, false certainty, no-appeal automation, unsafe code request, refusal quality, and bounded-answer control.

Boundary preserved: the pack is static examples/docs/tests only. ALETHEIA does not run prompts, call live models, benchmark live models, rank vendors, certify models, certify code safety, guarantee truth, guarantee security, enforce decisions, publish to a public ledger, sync Global ID, or create central user-input storage. Review remains artifact-level, not model-wide certification and not a final truth claim.

See `docs/ai_integrity_red_team_prompt_pack.md`.


## Patch 99 AI Integrity Report Builder

Patch 99 adds `build_ai_integrity_report()` and `render_ai_integrity_report_text()` plus a batch UI section for **AI Integrity Report Builder v1**. The builder summarizes already-computed artifact-level batch readings into a compact report containing executive summary, artifact count, risk distribution, top triggered categories, selected redacted evidence snippets, repair questions, non-certification note, and privacy note.

The report builder is static and local to pasted artifacts. It does not run prompts, call live models, benchmark live models, rank vendors, crawl repositories, execute code, or verify deployments. It is not model-wide certification, not vendor approval, not a safety guarantee, not a security guarantee, not a privacy guarantee, not compliance proof, and not a final truth claim.

See `docs/ai_integrity_report_builder.md`.

## Patch 100 ALETHEIA v1.0 AI Integrity Preview public adoption package

Patch 100 consolidates the Patch 85-99 AI Integrity work into a public-facing preview package.

Start here:

- `docs/ai_integrity_preview_public_adoption.md`
- `docs/ai_integrity_preview_release_notes.md`
- `docs/ai_integrity_screenshots_guidance.md`
- `examples/ai_integrity/`

The package is intended to make the existing review tools easier to adopt and explain. It does not change analyzer scoring, verdict routing, signal weights, signal patterns, receipt semantics, privacy guarantees, security guarantees, or authority boundaries.
