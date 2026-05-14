## Patch 130 — Release Candidate Freeze

Status: READY FOR LOCAL REVIEW

Patch 130 records ALETHEIA as being in release-candidate refinement mode. The current app behavior is the surface to preserve; future work should be limited to bug fixes, public-copy/readability fixes, input clarity, test hygiene, documentation navigation, and small behavior-preserving cleanup.

Boundary preserved: documentation and regression-test only. No runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern or signal-weight change, no receipt schema change, no module-routing change, no privacy scan behavior change, no AI Integrity scan behavior change, no World Lens math change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final-truth behavior changed. Humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 130
tools\run_patch_checks.bat 129
tools\run_patch_checks.bat 128
python tools\run_protocol_baseline_self_audit.py
```

## Patch 118 — Beginner UX Polish v2

Status: READY FOR LOCAL REVIEW

Patch 118 polishes the beginner path from Patch 111 by adding a first-audit checklist, clearer “what this means / what this does not mean” copy, and stop-and-review prompts for rights, reputation, safety, missing evidence, legal/medical/political/institutional/financial consequences, and unclear receipts.

Boundary preserved: static beginner UX copy and documentation only. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 118
tools\run_patch_checks.bat 117
tools\run_patch_checks.bat 116
tools\run_patch_checks.bat 115
python tools\run_protocol_baseline_self_audit.py
```

## Patch 117 — Refactor Stabilization Checkpoint

Status: READY FOR LOCAL REVIEW

Patch 117 pauses the app-shell router refactor after Patch 116 and adds a stabilization checkpoint. It documents the refactor boundary and adds tests proving that `ui/app_shell.py` remains a static shell-copy helper layer while `app.py` remains the orchestrator for interactive controls, session state, module routing, scoring, receipts, downloads, and analysis behavior.

Boundary preserved: no runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

Validation targets:

```bat
tools
un_patch_checks.bat 117
tools
un_patch_checks.bat 116
tools
un_patch_checks.bat 115
tools
un_patch_checks.bat 114
python tools
un_protocol_baseline_self_audit.py
```

## Patch 116 — App Shell Router Refactor Step 5

Status: READY FOR LOCAL TESTING

Summary:
- Extracts the stable footer banner into `ui/app_shell.py` as a copy-only app-shell helper.
- Updates `app.py` to call `render_app_footer_banner(APP_VERSION, st)` while keeping runtime orchestration in `app.py`.
- Keeps this as static shell extraction only: no interactive controls, session state, module routing, scoring, receipts, downloads, or analysis behavior moved.
- No scoring, verdict-routing, signal-pattern, signal-weight, receipt schema, module-routing, external-call, live-model-call, telemetry, analytics, central-storage, Global ID sync, public ledger sync, privacy-guarantee, certification, enforcement, or final-truth behavior changed.

Validation:
- `tools\run_patch_checks.bat 116`
- `tools\run_patch_checks.bat 115`
- `tools\run_patch_checks.bat 114`
- `python tools\run_protocol_baseline_self_audit.py`

# ALETHEIA Patch Status

## Patch 115 — App Shell Router Refactor Step 4

Status: READY FOR LOCAL TESTING

Summary:
- Extracts static sidebar tuning-section headings and explanatory captions into `ui/app_shell.py`.
- Updates `app.py` to call the new app-shell helpers while keeping all interactive sidebar controls in place.
- Keeps `app.py` as the orchestrator for session state, module routing, scoring, receipts, downloads, and analysis behavior.
- No scoring, verdict-routing, signal-pattern, signal-weight, receipt schema, module-routing, external-call, live-model-call, telemetry, analytics, central-storage, Global ID sync, public ledger sync, privacy-guarantee, certification, enforcement, or final-truth behavior changed.

Validation:
- `tools\run_patch_checks.bat 115`
- `tools\run_patch_checks.bat 114`
- `tools\run_patch_checks.bat 113`
- `python tools\run_protocol_baseline_self_audit.py`

## Patch 114 — Public Release Polish v1

Status: READY FOR LOCAL TESTING

Summary:
- Adds `docs/public_release_polish_v1.md` as the public wording and first-review entry note.
- Updates README, public release notes, public trust package, patch index, architecture, and trust-package README.
- Clarifies that ALETHEIA outputs are internal governance-risk readings and repair prompts, not verdicts or certifications.
- Keeps public links direct and reviewable rather than relying on shortened links.
- No app.py change, no runtime behavior change, no scoring, verdict-routing, signal-pattern, signal-weight, receipt schema, module-routing, external-call, live-model-call, telemetry, analytics, central-storage, Global ID sync, public ledger sync, privacy-guarantee, certification, enforcement, or final-truth behavior changed.

Validation:
- `tools\run_patch_checks.bat 114`
- `tools\run_patch_checks.bat 113`
- `tools\run_patch_checks.bat 112`
- `tools\run_patch_checks.bat 111`
- `python tools\run_protocol_baseline_self_audit.py`

## Patch 111 — Beginner Try This First UX

Status: READY FOR LOCAL TESTING

Summary:
- Adds `ui/beginner_guide.py` with a compact first-run "Start here: try this first" guide.
- Wires the guide under the public header in `app.py` without changing module routing, scoring, receipts, or signal logic.
- Adds `docs/beginner_ux.md` to document the beginner path and its boundaries.
- Keeps `app.py` as the orchestrator for behavior.
- No scoring, verdict-routing, signal-pattern, signal-weight, receipt schema, module-routing, external-call, telemetry, analytics, storage, certification, enforcement, privacy-guarantee, or final-truth behavior changed.

Validation:
- `tools\run_patch_checks.bat 111`
- `tools\run_patch_checks.bat 110`
- `tools\run_patch_checks.bat 109`
- `tools\run_patch_checks.bat 108`
- `tools\run_patch_checks.bat 107`
- `tools\run_patch_checks.bat 106`
- `python tools\run_protocol_baseline_self_audit.py`


## Patch 103 — Signal Detection Transparency Documentation

Status: READY FOR LOCAL TESTING

Summary:
- Adds `docs/signal_detection.md` to document ALETHEIA's transparent rule-based and heuristic signal-detection posture.
- Frames rule-based detection as explainable, local-first, and reviewable while clearly naming limits around nuance, irony, coded language, cultural context, and languages outside the strongest English/Dutch calibration path.
- Updates README, architecture, and contributor docs with the signal-basis pointer.
- Updates the Patch 101 baseline manifest hashes for changed watched docs so the human-auditable baseline remains explicit and reviewable.
- No scoring, verdict-routing, signal-pattern, signal-weight, receipt schema, Streamlit behavior, external-call, telemetry, storage, or authority-boundary logic changed.

Validation:
- `tools\run_patch_checks.bat 103`
- `tools\run_patch_checks.bat 102`
- `tools\run_patch_checks.bat 101`

## Patch 102 — Structural Improvement Entry Point

Status: READY FOR LOCAL TESTING

Summary:
- Adds a documentation-first structural improvement path before any `app.py` refactor.
- Adds architecture and new-contributor entry docs so later refactors have a reviewable boundary.
- Adds `CONTRIBUTING.md` with safe contribution areas, high-review areas, and prohibited authority-drift directions.
- Updates README with the structural path.
- Updates the Patch 101 baseline manifest hashes for changed watched docs so the human-auditable baseline self-audit remains explicit and reviewable.
- No scoring, verdict-routing, receipt schema, Streamlit behavior, external calls, telemetry, storage, or authority-boundary logic changed.

Validation:
- `tools\run_patch_checks.bat 102`
- `tools\run_patch_checks.bat 101`

## Patch 83 — Android Gradle Plugin Resolution Fix

Status: READY FOR LOCAL TESTING

Summary:
- Fixed Android wrapper Gradle plugin resolution for signed APK builds.
- Project-level Gradle files now declare `com.android.application` with a version and `apply false`.
- App-module Gradle files apply the Android application plugin only inside `android_webview/app`.
- Settings files define `google()`, `mavenCentral()`, and `gradlePluginPortal()` repositories without duplicate includes.
- No Streamlit engine change, no scoring change, no new Android permissions, no keystore, and no signed APK included.

Validation:
- `tools\run_patch_checks.bat 83`

## Patch 71.10 - Mirror Check HTML Rendering Fix

Status: READY FOR LOCAL TESTING

Summary:
- Fixed Mirror Check result card rendering where HTML appeared as literal code.
- The judgment card now uses dedented HTML before `st.markdown(..., unsafe_allow_html=True)`.
- Review-band card line is precomputed outside the HTML template.
- Display-only fix: no receipt schema, scoring, verdict-routing, taxonomy, tree, Stress Test, Boundary Cases, World Lens, storage, or authority-boundary changes.

Validation:
- `tools\run_patch_checks.bat 71_10`


## Patch 71.9 — Mirror Check Review Band Display

Status: READY FOR LOCAL TESTING

Summary:
- Mirror Check latest-reading cards now use the same display-only Threshold review band helper as Stress Test.
- THRESHOLD Mirror Check outputs can show Needs Repair, Needs Review, or Near Sanctuary.
- No receipt schema, scoring, verdict-routing, taxonomy, tree, Stress Test, Boundary Cases, World Lens, storage, or authority-boundary changes.

Validation:
- `tools\run_patch_checks.bat 71_9`


## Patch 71.8 — Stress Test Review Band Card Polish

Status: READY FOR LOCAL TESTING

Summary:
- Stress Test result card now shows the review band on its own line for THRESHOLD outputs.
- Display-only polish: no receipt schema, scoring, verdict-routing, taxonomy, Mirror Check, tree, Boundary Cases, World Lens, storage, or authority-boundary changes.

Validation:
- `tools\run_patch_checks.bat 71_8`


## Patch 71.7 — Threshold Review Band Display

Status: READY FOR LOCAL TESTING

Summary:
- Added a display-only Review band for THRESHOLD outputs: Needs Repair, Needs Review, Near Sanctuary.
- Canonical taxonomy remains ASYLUM / THRESHOLD / SANCTUARY.
- Stress Test result card and batch summary can show the user-friendly band.
- No receipt schema, scoring, verdict-routing, tree, Boundary Cases, World Lens, storage, or authority-boundary logic changed.

Validation:
- `tools\run_patch_checks.bat 71_7`


## Patch 71.6 — Tree Central Glow Removal

Status: READY FOR LOCAL TESTING

Summary:
- Removed the large central glow/blob from the explanatory tree visual.
- Preserved canopy leaves, trunk, branches, fallen leaves, state color, and caption placement.
- This is visual-only; no scoring, receipt, Stress Test, Mirror Check, Boundary Cases, World Lens, storage, or authority-boundary logic changed.

Validation:
- `tools\run_patch_checks.bat 71_6`


## Patch 71.5 — Boundary Cases Missing-Safeguard Cleanup

Status: READY FOR LOCAL TESTING

Summary:
- Boundary Cases now reflects Patch 71.4 missing-safeguard behavior.
- Added templates for automated triage missing explainability/challenge/override, biometric gates without fallback/audit/appeal, and QUESTION_PROMPT as review-tool mode.
- Consent-Audit and Mechanism-vs-Claim templates now include explainability, independent challenge, human override, fallback paths, public audit, and meaningful appeal.
- No scoring, Stress Test, Mirror Check, tree, World Lens, storage, or authority-boundary changes.

Validation:
- `tools\run_patch_checks.bat 71_5`


## Patch 71.4 — Missing-Safeguard Verdict Enforcement

Status: READY FOR LOCAL TESTING

Summary:
- Stress Test now applies a final missing-safeguard guard before visible metrics and local witness receipts are produced.
- Explicit phrases such as `lacks explainability`, `lacks independent challenge`, and `lacks human override` route to THRESHOLD / Medium instead of SANCTUARY / Low.
- Trust and alignment are capped below perfect values, friction/collapse pressure become non-zero, and repair questions are added.
- Authority boundary remains unchanged: mirror only, local receipt only, human review required.

Validation:
- `tools\run_patch_checks.bat 71_4`


This file is the compact local patch ledger for ALETHEIA v0.1. Longer implementation notes live in `docs/progress_database.md`.

| Patch | Name | Status |
|---|---|---|
| 33 | Baseline v0.1 + Safe Language + Eternal Baseline | Passed |
| 34 | Boundary Cases Matrix | Passed |
| 35 | Failure Classification | Passed |
| 36 | Patch Automation Toolkit | Passed |
| 36.1 | Automation Script Hotfix + Safe Check Workflow | Passed |
| 37 | Consent-Audit Engine | Passed |
| 38 | Mechanism-vs-Claim Scanner | Passed |
| 39 | Self-Audit Mode | Passed |
| 40 | Evidence Lab + Extraordinary Claim Protocol | Passed |
| 41 | Local Witness Receipt v2 | Passed |
| 42 | World Lens Simulation | Passed |
| 43 | Protocol Guide Consolidation | Passed |
| 44 | Progress Database + Patch Status Hardening | Passed |
| 45 | Public README + Limitations Polish | Passed |
| 46 | Sample Reports / Example Audits | Passed |
| 47 | App Navigation + Smoke Test Cleanup | Passed |
| 48 | Release Candidate Checklist | Passed |
| 49 | Full Test Suite / Legacy Test Cleanup | Passed |
| 50 | v0.1 Release Package | Passed |
| 51 | Git Diff Workflow Setup | Passed |
| 52 | Optional UX Polish | Passed |
| 53 | Final v0.1 Smoke Release | Passed |
| 54 | Example Audit Runner / Demo Inputs | Passed |
| 55 | GitHub Cleanup Package | Passed |
| 56–60 | v1 Finalization Bundle | Passed |
| 61A | Asylum Repair Questions | Passed |
| 61B | Malicious Leadership Metric Calibration | Passed |
| 61C | Country-Year Available-Year Filter | Passed |
| 61D | Missing Raw Trust Display | Passed |
| 61E | World Lens Value Guards | Passed |
| 62 | Post-61 Regression Smoke Test | Current |

| 68.1 | Asylum Label / Metric Consistency | Ready for local verification |

## Current Patch

Patch 62 — Post-61 Regression Smoke Test

## Current Check Command

```bat
tools\run_patch_checks.bat 62
```

## Safe Default Check

```bat
tools\run_checks.bat
```

## Next Logical Patch

Patch 63 — optional GitHub-ready cleanup / deployment smoke, or hold v1 if no new issue is found.

## Workflow Rule

When the user says `next patch`, treat the previous patch as passed and continue from the latest working project state.

## Patch 55 Boundary

Patch 55 is public repository packaging only. It does not add governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger authority, neural validation, religious validation, legal authority, or automated enforcement.


## Patch 56–60 Boundary

Patch 56–60 finalizes ALETHEIA v1.0 as a public MVP package and adds future-planning documentation. It does not add governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger authority, neural validation, religious validation, legal authority, or automated enforcement.

## Patch 61A — Asylum Repair Questions

Status: Passed.

Adds a high-risk repair-question guard so ASYLUM / High / Malicious Leadership outputs include Silent Operator repair questions instead of an empty repair path. This remains mirror-only and human-review-only.

Check command:

```bat
tools\run_patch_checks.bat 61A
```

## Patch 61B — Malicious Leadership Metric Calibration

Status: Passed.

Caps perfect trust/alignment and raises the ego signal for malicious leadership scenarios unless concrete safeguards are present. This is metric calibration only; it adds no enforcement or authority.

Check command:

```bat
tools\run_patch_checks.bat 61B
```

## Patch 61C — Country-Year Available-Year Filter

Status: Passed.

Scopes the Country-Year Explorer year dropdown to the selected country only. Prevents stale/global/default year fallback and adds clear country-specific available-year wording.

Check command:

```bat
tools\run_patch_checks.bat 61C
```

## Patch 61D — Missing Raw Trust Display

Status: Passed.

Clarifies World Lens trust interpretation by separating observed raw trust evidence from neutral trust-prior fallback values. Missing raw trust is displayed as `not available`, and neutral priors are labeled as `0.500 neutral default`.

Check command:

```bat
tools\run_patch_checks.bat 61D
```

## Patch 61E — World Lens Value Guards

Status: Passed.

Adds deterministic selected-year guards for World Lens. It verifies selected-year seat totals, focus-country values, no-stale-year behavior, verdict-seat derivation, and clear trust-prior interpretation.

Check command:

```bat
tools\run_patch_checks.bat 61E
```

## Patch 62 — Post-61 Regression Smoke Test

Status: ready for local verification.

Consolidates 61A–61E with one regression smoke test across Simulation and World Lens. Confirms ASYLUM repair questions, malicious-leadership metric calibration, country-year filtering, missing raw-trust labeling, selected-year 9k seat guards, and Netherlands 2024 fixture stability.

Check command:

```bat
tools\run_patch_checks.bat 62
```


## Patch 63 — Post-62 Release Refresh

Status: Ready for local verification.

Updates README, About, public release notes, progress database, and release-refresh docs after Patch 61A–61E and Patch 62. This is release-surface hardening only; it adds no governance authority or enforcement.

Check command:

```bat
tools\run_patch_checks.bat 63
```

## Patch 64 — Mirror Check Batch Baseline Validation

Status: Ready for local verification.

Records three 50-question Mirror Check batch baselines and documents the expected `QUESTION_PROMPT` receipt contract: 50 receipts, 50 JSON receipts, no scenario-hash mismatches, no normal scoring, and authority boundary preserved.

Check command:

```bat
tools\run_patch_checks.bat 64
```

## Patch 65 — Stress Test Prompting Guide + Batch Baseline

Status: Ready for local verification.

Adds Stress Test scenario-writing guidance, an official 50-scenario Stress Test baseline, and an explicit opt-in local Stress Test batch tester. The batch runner produces local Simulation receipts only and preserves the authority boundary.

Check command:

```bat
tools\run_patch_checks.bat 65
```

## Patch 66 — Stress Test Risk Sensitivity Calibration

Status: Delivered

Raises Stress Test sensitivity for missing appeal, no term limits, biometric access pressure, consent under pressure, fallback-data confusion, founder control, surveillance, and non-meaningful human review. Subtle stress cases now route to `THRESHOLD / Needs Safeguards`; hard capture remains `ASYLUM / High`.

## Patch 67 — Stress Test Threshold Repair + Metric Softening

Status: Delivered

Adds repair questions and light metric softening for `THRESHOLD / Needs Safeguards` Stress Test outputs. Medium-risk scenarios no longer display perfect trust/alignment and zero ego while still requiring safeguards. ASYLUM behavior remains unchanged.

Check:

```bat
tools\run_patch_checks.bat 67
```

## Patch 67.1 — Dutch Stress Test Lexicon + Threshold Receipt Enforcement

Status: Ready for local verification.

Dutch Stress Test calibration added. Dutch stress scenarios now trigger Threshold / Needs Safeguards for missing appeal, no sunset, biometric basic-service access, forced consent, fallback-data confusion, founder control, no audit trail, surveillance, and human review without power.

Check command:

```bat
tools\run_patch_checks.bat 67_1
```

## Patch 67.2 — Dutch Stress Lexicon Gap Fix + App-Wide Input Scope

Status: Ready for local verification.

Closes five remaining Dutch Stress Test false-SANCTUARY patterns and adds app-wide English/Nederlands input-scope wording in the header/control surface. This patch remains diagnostic only: no enforcement, no authority claim, no Global ID sync, no public ledger, and no central storage.

Check command:

```bat
tools\run_patch_checks.bat 67_2
```

## Patch 68 — Advanced English Stress Lexicon + Asylum Metric Enforcement

Adds advanced English Stress Test calibration for predictive sentencing, biometric/identity coercion, divine-authority wallet capture, founder-keyword mirror capture, pre-emptive arrests, loyalty-to-state baseline capture, archive deletion, unaudited mirror code, and similar high-risk governance patterns. Advanced English stress scenarios route to `THRESHOLD / Needs Safeguards` or `ASYLUM / High` instead of washing into Sanctuary. Asylum metric enforcement now applies to non-malicious Asylum labels so receipts do not retain perfect trust/alignment or zero ego.

## Patch 69 — Stress Test Question Prompt Detection — completed

Stress Test batch mode now recognizes formal audit / repair-question banks as `QUESTION_PROMPT` review tools instead of scoring them as ordinary governance scenarios. The regression baseline file is `examples/batch_questions/formal_doctrine_repair_questions_nl.txt`, copied from the user-used `formal doctrine repair-question baseline.txt`.

## Patch 69.1 — Stress Batch Scenario-vs-Question Detection

Status: Ready for local verification.

Fixes the Stress Test `.txt` upload path so uploaded declarative scenario batches remain Simulation `USER_INPUT` items instead of being suppressed as `QUESTION_PROMPT`. Formal audit/repair-question banks still become `QUESTION_PROMPT / Review Tool` receipts.

Check command:

```bat
tools\run_patch_checks.bat 69_1
```

## Patch 70 — Mirror + Stress Tree Visual Calibration

Status: Ready for local verification.

Clarifies the tree visual in both Mirror Check and Stress Test. The tree now presents itself as a visual state explainer rather than a second protocol metric. It distinguishes `Visual tree score` from receipt `protocol-adjusted integrity`, adds separate Mirror Check and Stress Test tree language, and treats `QUESTION_PROMPT` as Review Tool Mode rather than a fourth risk state.

Check command:

```bat
tools\run_patch_checks.bat 70
```

## Patch 70.1 — Negated Safeguard Strength Calibration

Status: Ready for local verification.

Patch 70.1 fixes a diagnostic false positive found during Patch 70 tree review: phrases such as `no oversight` and `no public review` must not be reported as transparency or accountability strengths. The change filters positive-credit safeguard terms when they are locally negated, including English and Dutch negation forms.

Scoring boundary unchanged: ASYLUM, grip-marker, local witness receipt, repair-question, and authority-boundary behavior remain intact. ALETHEIA remains a mirror only: no authority claim, no enforcement, no public ledger, no Global ID sync, no central storage, and human review required.

Check:

```bat
tools\run_patch_checks.bat 70_1
```

## Patch 71 — Batch File Repository Consolidation

Status: Ready for local verification.

Patch 71 makes the renamed batch files official in the repository and documents them in `docs/batch_file_catalog.md`. It validates the EN/NL question and scenario fixtures, records the expected QUESTION_PROMPT behavior for question banks, and records the latest verified Stress Test distributions:

- `examples/batch_scenarios/stress_test_scenarios_en_v1.txt`: THRESHOLD 46 / ASYLUM 4 / SANCTUARY 0
- `examples/batch_scenarios/stress_test_scenarios_nl_v1.txt`: THRESHOLD 50 / ASYLUM 0 / SANCTUARY 0
- `examples/batch_scenarios/governance_language_stress_test_en.txt`: THRESHOLD 29 / ASYLUM 21 / SANCTUARY 0

Legacy names may remain as compatibility aliases, but README, About, and the catalog now point to the official Patch 71 names. No scoring, tree, receipt, or authority-boundary logic changed.

Check:

```bat
tools\run_patch_checks.bat 71
```

## Patch 71.1 — Module Demo Label Isolation

Status: Ready for local verification.

Patch 71.1 separates the visible demo libraries used by Mirror Check and Stress Test. Stress Test now uses Stress Test-specific scenario demos and the button label `Load Stress Test scenario demo`; Mirror Check keeps its own scenario demo library and `Load Mirror Check scenario demo` label.

No scoring, tree, receipt, batch-catalog, storage, or authority-boundary logic changed.

Check:

```bat
tools\run_patch_checks.bat 71_1
```

## Patch 71.2 — Tree Canopy + Caption Visual Polish

Status: Ready for local verification.

Patch 71.2 improves the explanatory tree visual after UI review showed that the canopy looked disconnected and the explanatory caption sat inside the tree image. The tree now uses a layered ellipse canopy connected to the trunk/branches, and the caption is placed below the SVG visual.

No scoring, receipt, tree-state, batch-catalog, demo-library, storage, or authority-boundary logic changed. The tree remains an explanatory visual signal; receipt integrity and protocol-adjusted state remain canonical.

Check:

```bat
tools\run_patch_checks.bat 71_2
```


## Patch 71.3 — Stress Test Missing-Safeguard Negation + Tree Canopy Tune

Status: Ready for local verification.

Patch 71.3 fixes a Stress Test calibration gap found in the `Algorithmic welfare triage under pressure` demo. Phrases such as `lacks explainability`, `lacks independent challenge`, and `lacks human override` are now treated as missing-safeguard review signals, not as positive transparency/accountability features. The bridge guardrail prevents these cases from displaying perfect Sanctuary-like trust/alignment metrics.

Patch 71.3 also tunes the explanatory tree canopy placement so the crown sits lower, connects more naturally to the trunk/branches, and leaves the caption outside the SVG visual.

No receipt storage, authority-boundary, batch-catalog, public-ledger, Global ID sync, or central-storage behavior changed.

Check:

```bat
tools\run_patch_checks.bat 71_3
```

## Patch 71.11 - Mirror Check Stress Label Row Render Fix

Date: 2026-05-11

Patch 71.11 fixes the remaining Mirror Check latest-reading card regression where the `Stress label` row could still appear as literal code after Patch 71.10.

Implemented:
- Kept the Patch 71.10 `judgment_card_html` + `textwrap.dedent(...).strip()` render path.
- Built the result-card detail rows as inline HTML blocks joined into `detail_rows_html`.
- Escaped dynamic display text before inserting it into `unsafe_allow_html=True` markup.
- Rendered the detail rows inline so Streamlit Markdown no longer treats the final row as code.

Invariant preserved:
- No receipt schema change.
- No scoring logic change.
- No verdict-routing change.
- No taxonomy expansion.
- No tree visual, Stress Test, Boundary Cases, World Lens, storage, or authority-boundary logic changed.

Check:

```bat
tools\\run_patch_checks.bat 71_11
```

## Patch 71.12 - Mirror Check Review Band Row Render Fix

Date: 2026-05-11

Patch 71.12 fixes the remaining THRESHOLD-specific Mirror Check latest-reading card regression where the visual review-band line could still appear as literal HTML/code.

Implemented:
- Built the THRESHOLD review-band visual line as inline HTML instead of an indented triple-quoted block.
- Removed the obsolete `review_band_detail_line` fragment from the render path.
- Preserved the Patch 71.11 inline detail rows and HTML escaping for Safety risk, Review band, and Stress label.

Invariant preserved:
- No receipt schema change.
- No scoring logic change.
- No verdict-routing change.
- No taxonomy expansion.
- No tree visual, Stress Test, Boundary Cases, World Lens, storage, or authority-boundary logic changed.

Check:

```bat
tools\run_patch_checks.bat 71_12
```

## Patch 72 - Threshold Mapping Layer

Date: 2026-05-11

Patch 72 adds a receipt-only Threshold Mapping Layer to clarify the middle zone between captured logic and distributed resilience.

Implemented:
- Added `threshold_mapping_layer` to local witness receipts.
- Added `threshold_direction`, `z_axis_position`, `integrity_gap`, and `repair_index`.
- Added component readings for Power balance, Correction, and Access.
- Added Asylum pressure signals and Sanctuary growth signals.
- Printed `THRESHOLD MAPPING LAYER` between Raw Metrics Before Ethics and Scanner Features in readable receipts.
- Added documentation in `docs/threshold_mapping_layer.md`.

Invariant preserved:
- Canonical taxonomy remains SANCTUARY / THRESHOLD / ASYLUM.
- No scoring logic change.
- No verdict-routing change.
- No UI tree visual change.
- No Stress Test, Boundary Cases, World Lens, storage, public ledger, Global ID sync, central storage, or authority-boundary logic changed.

Check:

```bat
tools\run_patch_checks.bat 72
```

## Patch 72.1 - Threshold Mapping UI Preview

Date: 2026-05-11

Patch 72.1 surfaces the Patch 72 Threshold Mapping Layer in the live Mirror Check latest-reading UI.

Implemented:
- Added public `build_threshold_mapping_layer(...)` wrapper in `core/witness.py`.
- Passed scanner features into `render_chat_judgment(...)`.
- Added expandable `Threshold mapping preview` below the core metrics.
- Displayed Threshold direction, Z-axis, Repair index, component readings, pressure signals, and growth signals.
- Marked the preview as receipt-only and not a new verdict/enforcement path.

Invariant preserved:
- Canonical taxonomy remains SANCTUARY / THRESHOLD / ASYLUM.
- No scoring logic change.
- No verdict-routing change.
- No receipt authority change beyond Patch 72's receipt mapping.
- No tree visual, Stress Test, Boundary Cases, World Lens, storage, public ledger, Global ID sync, central storage, or authority-boundary logic changed.

Check:

```bat
tools\run_patch_checks.bat 72_1
```

## Patch 72.1 Hotfix - Threshold Mapping Card Summary

Date: 2026-05-11

Patch 72.1 Hotfix makes the Threshold Mapping UI visibly confirmable in the main Mirror Check judgment card.

Implemented:
- Added a compact `Threshold mapping` line to the card itself.
- Displayed threshold direction, Z-axis, and repair index before the metrics.
- Reused the same mapping object for the expandable Threshold mapping preview below the metrics.
- Kept the full Patch 72.1 preview intact.

Invariant preserved:
- Canonical taxonomy remains SANCTUARY / THRESHOLD / ASYLUM.
- No scoring logic change.
- No verdict-routing change.
- No receipt schema change.
- No tree visual, Stress Test, Boundary Cases, World Lens, storage, public ledger, Global ID sync, central storage, or authority-boundary logic changed.

Check:

```bat
tools\run_patch_checks.bat 72_1_hotfix
```

## Patch 72.2 - Mirror Check Input Change Reset

Date: 2026-05-11

Patch 72.2 fixes a Mirror Check UI-state issue where a previous assessment/receipt could stay active after the user changed the input text.

Implemented:
- Added `mirror_active_input_signature(...)` for stable current-input matching.
- Stored `audit_active_input_signature` only after an explicit `Review idea` run.
- Rendered the latest reading and local receipt only when the current text still matches the last reviewed input.
- Added a closed-assessment notice when the input changes, asking the user to click Review idea again.
- Preserved previous readings as history without treating them as the current draft.

Invariant preserved:
- No scoring logic change.
- No verdict-routing change.
- No receipt schema change.
- No Threshold Mapping logic change.
- No tree visual, Stress Test, Boundary Cases, World Lens, storage, public ledger, Global ID sync, central storage, or authority-boundary logic changed.

Check:

```bat
tools\run_patch_checks.bat 72_2
```

## Patch 72.3 - Humility Protocol / Sanctuary Asymptote

Date: 2026-05-11

Patch 72.3 adds the Humility Protocol: Sanctuary as Asymptote.

Implemented:
- Redefined the Threshold Mapping Z-axis as proximity to the boundary of human/system authority, not progress toward perfection.
- Capped human/system Z-axis values at `0.9999`.
- Marked `Z=1.0000` as `OUTSIDE SYSTEM CLAIM`.
- Added `asymptote_note`, `outside_system_claim_note`, and `nine_k_threshold_steward_note` to the Threshold Mapping Layer.
- Printed ASYMPTOTE NOTE and 9K THRESHOLD STEWARD NOTE in readable receipts.
- Updated the Mirror Check Threshold Mapping UI to show Z-axis against the 0.9999 cap and state that Z=1.0000 is outside system claim.
- Updated `docs/threshold_mapping_layer.md` with The Humility Protocol: Sanctuary as Asymptote.

Invariant preserved:
- Canonical taxonomy remains SANCTUARY / THRESHOLD / ASYLUM.
- No scoring logic change.
- No verdict-routing change.
- No religious, legal, political, medical, institutional, or automated authority claim.
- No tree visual, Stress Test, Boundary Cases, World Lens, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_3
```

## Patch 72.4 - Friendly Humility Copy Refresh

Date: 2026-05-11

Patch 72.4 refreshes user-facing text so the app is neutral, friendly, and current with Patch 72.3's Humility Protocol / Sanctuary Asymptote.

Implemented:
- Added friendly UI labels for Threshold Mapping directions.
- Updated Mirror Check plain words to clarify that Sanctuary is low risk inside the prototype, not final safety.
- Updated Z-axis copy to emphasize the human/system boundary and the 0.9999 cap.
- Updated Threshold Mapping preview labels to Capture-pressure and Repair/growth signals.
- Updated About, README, and Threshold Mapping docs with neutral Humility Protocol language.
- Updated receipt notes to say ultimate questions and final authority remain outside ALETHEIA.

Invariant preserved:
- No scoring logic change.
- No verdict-routing change.
- No receipt schema change.
- No Threshold Mapping math change.
- No tree visual, Stress Test, Boundary Cases, World Lens, storage, public ledger, Global ID sync, central storage, or authority-boundary logic changed.

Check:

```bat
tools\run_patch_checks.bat 72_4
```

## Patch 72.4 - Neutral Text Refresh

Date: 2026-05-11

Patch 72.4 refreshes user-facing copy so the app is neutral, friendly, and current with Patches 72-72.3.

Implemented:
- Updated Z-axis language to describe the boundary of what human/system tools may responsibly claim.
- Reframed Z=1.0000 as outside ALETHEIA's claim.
- Reframed 9k as an anti-tyranny scaffold / threshold steward without final-safety or final-legitimacy language.
- Added a friendly Humility Protocol / Z-axis boundary section to the Protocol Guide.
- Updated README, About, core receipt notes, and Threshold Mapping docs.
- Removed or softened wording that could sound like perfection, final authority, or doctrinal validation in user-facing copy.

Invariant preserved:
- No scoring logic change.
- No verdict-routing change.
- No receipt schema change.
- No Threshold Mapping math change.
- No tree visual, Stress Test, Boundary Cases, World Lens, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_4
```

## Patch 72.5 - Boundary Cases Neutral Text Refresh

Date: 2026-05-11

Patch 72.5 refreshes Boundary Cases copy so it is neutral, friendly, and current with Patch 72.4.

Implemented:
- Replaced older metaphorical authority wording with direct calibration-only language.
- Replaced "before any Sanctuary reading" with "before any low-risk internal reading".
- Replaced "approach Sanctuary" with "approach the review boundary".
- Replaced spiritual-validation wording with extraordinary-claim / unverified-authority wording.
- Kept Boundary Cases as human-review calibration only.

Invariant preserved:
- No scoring logic change.
- No verdict-routing change.
- No receipt schema change.
- No Threshold Mapping math change.
- No tree visual, Stress Test, Evidence Lab, World Lens, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_5
```

## Patch 72.6 - Why ALETHEIA Neutral Text Refresh

Date: 2026-05-11

Patch 72.6 refreshes the Why ALETHEIA / About page so it is neutral, friendly, and current with Patches 72-72.5.

Implemented:
- Updated About intro to say ALETHEIA reviews risk, evidence gaps, and safeguard needs without deciding, enforcing, validating final truth, or replacing human judgment.
- Updated Humility Protocol copy to frame the Z-axis as the boundary of what human/system tools may responsibly claim.
- Updated 9k copy as representation/exposure review support, not final safety, final legitimacy, or authority.
- Updated Audit, Boundary Cases, Evidence Lab, sample-report, navigation, World Lens, and caution copy to match the neutral text standard.

Invariant preserved:
- No scoring logic change.
- No verdict-routing change.
- No receipt schema change.
- No Threshold Mapping math change.
- No tree visual, Stress Test, Boundary Cases, Evidence Lab, World Lens, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_6
```

## Patch 72.7 - Repair Capacity Mapping Guard

Date: 2026-05-11

Patch 72.7 separates generated repair questions from confirmed repair capacity in the Threshold Mapping Layer.

Implemented:
- Added `repair_question_index`.
- Added `confirmed_repair_capacity`.
- Kept `repair_index` as confirmed repair capacity for backward display compatibility.
- Guarded ASYLUM component readings so they do not present as `Threshold +` while canonical state is ASYLUM.
- Updated receipt text to print repair questions available and confirmed repair capacity separately.
- Updated UI preview to show Repair questions and Confirmed repair separately.
- Neutralized old "outside Sanctuary", "Divine Bias", and "Divine Treasury" wording.

Invariant preserved:
- No scoring logic change.
- No verdict-routing change.
- No canonical taxonomy change.
- No receipt authority change.
- No tree visual, Stress Test batch structure, Evidence Lab, Boundary Cases, World Lens, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_7
```

## Patch 72.8 - Stress Batch Input Reset and Protocol Capture Risk Presentation

Date: 2026-05-11

Patch 72.8 fixes Stress Test batch UI carry-over and clarifies protocol capture risk in receipts.

Implemented:
- Added a stable Stress batch input signature.
- Stored the active Stress batch signature only after an explicit `Run Stress Batch`.
- Hid old batch results/downloads when the uploaded or pasted batch input changes.
- Added a closed-batch notice and optional last-closed-batch preview.
- Added `protocol_capture_risk` and `protocol_capture_risk_note` to local witness receipt verdict blocks.
- Printed `Protocol capture risk` separately from raw simulation `Collapse risk`.

Invariant preserved:
- No scoring logic change.
- No verdict-routing change.
- No canonical taxonomy change.
- No Threshold Mapping math change.
- No tree visual, Stress Test scoring, Evidence Lab, Boundary Cases, World Lens, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_8
```

## Patch 72.9 - Evidence Lab Build/Explorer State Guard

Date: 2026-05-11

Patch 72.9 prevents Evidence Lab country/year selection and CSV downloads from re-scoring the same active uploaded/generated master.

Implemented:
- Added stable active-input signature for Evidence Lab scoring.
- Cached prepared and scored Evidence Lab tables in session state.
- Reused cached active scored table when source signature matches.
- Added explicit generated-master download key and explanatory caption.
- Clarified upload diagnostics: individual source files may show 0 valid country-year rows before merge; the merged master is the scoring source of truth.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No World Lens logic change.
- No receipt schema change.
- No Evidence Lab data model, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_9
```

## Patch 72.10 - Trust Upload Auto-Normalizer

Date: 2026-05-11

Patch 72.10 lets Evidence Lab accept common public trust uploads without requiring manual ALETHEIA-ready CSV conversion.

Implemented:
- Auto-maps `Entity`, `Code`, and `Year` identity columns already supported by the empirical frame.
- Added trust aliases including `Trust in others`, `trust_in_others`, `trust_others`, and `trust_in_other_people`.
- Normalizes 0-100 trust percentages to 0-1 `wvs_generalized_trust`.
- Preserves already-normalized 0-1 trust values.
- Adds `_aletheia_trust_upload_note` for transparent diagnostics.
- Exposes the trust transform note through `public_upload_diagnostics`.
- Applies the same behavior to the Streamlit fallback module `core_empirical.py`.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No World Lens logic change.
- No receipt schema, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_10
```

## Patch 72.11 - Mascot Logo Replacement

Date: 2026-05-11

Patch 72.11 replaces the dove corner logos with the new Aletheia cardboard robot mascot wearing a green leaf/laurel crown.

Implemented:
- Added `assets/aletheia_robot_laurel_logo.png`.
- Added a small data-URI asset helper for HTML-embedded image badges.
- Replaced the header right circular dove emblem with the mascot logo.
- Replaced the sidebar top circular dove emblem with the mascot logo.
- Preserved the existing visual frame, copy, layout, and authority boundary.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No Evidence Lab, Stress Test, Mirror Check, Boundary Cases, World Lens, receipt schema, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_11
```

## Patch 72.12 - Mascot Asset Refresh

Date: 2026-05-11

Patch 72.12 refreshes the app mascot asset with the updated Aletheia robot image while preserving the Patch 72.11 header/sidebar mascot wiring.

Implemented:
- Replaced `assets/aletheia_robot_laurel_logo.png` with the updated mascot artwork.
- Preserved the existing mascot embedding path in `app.py`.
- Added a patch test to verify the refreshed asset file, size, and hash.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No Evidence Lab, Stress Test, Mirror Check, Boundary Cases, World Lens, receipt schema, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_12
```

## Patch 72.13 - Evidence Lab Year Selector and Trust Diagnostic Guard

Date: 2026-05-11

Patch 72.13 fixes two Evidence Lab UI/diagnostic issues.

Implemented:
- Country-Year Explorer uses the synced evidence year only as an initial seed for a country-specific year widget.
- Manual year selections are no longer overwritten on every Streamlit rerun.
- Direct merged-upload diagnostics now label `empirical_trust_prior` as `Trust prior (derived)` instead of a missing upload source.
- The unscored merged evidence-table message now explains that raw trust is read from `wvs_generalized_trust` and trust prior is derived during scoring.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No World Lens logic change.
- No Evidence Lab data model, receipt schema, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_13
```

## Patch 72.14 - World Lens Value Guard Fallback

Date: 2026-05-11

Patch 72.14 prevents World Lens from crashing when `selected_year_value_guard` is unavailable in an older/partial deployment.

Implemented:
- Replaced the direct value-guard call with a safe callable lookup.
- Added a local diagnostic-only fallback for selected-year, total-seat, stale-year-row, and focus-row checks.
- Preserved selected-year wording and full/partial 9k view behavior.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab data model, receipt schema, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_14
```

## Patch 72.15 - World Lens Year and Focus Guard

Date: 2026-05-11

Patch 72.15 fixes World Lens year-selection and value-guard runtime issues.

Implemented:
- World Lens uses the Evidence Lab synced year only as the initial seed for the year widget.
- Manual World Lens evidence-year selections are no longer overwritten on every rerun.
- Defined `focus_iso3` safely before the selected-year value guard call.
- Added a prototype-branch allocation heading so prototype mode does not depend on empirical-branch variables.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab data model, receipt schema, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_15
```

## Patch 72.16 - World Lens Comparison Packet Summary Columns

Date: 2026-05-11

Patch 72.16 adds explicit selected-year summary columns to the World Lens comparison packet export.

Implemented:
- Added visible overview/coverage card values to `comparison_export`.
- Added selected-year countries, displayed rows, zero-seat diagnostics, weighted friction, average empirical coverage, raw trust coverage, trust-prior fallback coverage, WGI coverage, V-Dem coverage, missing-source counts, trust-prior counts, and verdict seat totals.
- Added `trust_prior_interpretation_note` to distinguish fallback/model continuity coverage from observed raw survey coverage.
- Included the new fields in the selected-year comparison packet CSV download.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab data model, receipt schema, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_16
```

## Patch 72.17 - World Lens Sanctuary Display Humility Guard

Date: 2026-05-11

Patch 72.17 aligns World Lens / Evidence Lab country-year display with the Humility Protocol: Sanctuary as Asymptote.

Implemented:
- Changed the country-year card from `Empirical verdict` to `Empirical pattern`.
- Displays internal `SANCTUARY` rows as `Low-risk internal reading`.
- Adds a caption preserving `Internal taxonomy label: SANCTUARY` while clarifying that this is not a final safety, final Sanctuary, or authority claim.
- Updates empirical overlay text to `Low-risk evidence pattern` for high-integrity/low-collapse rows.
- Rewrites legacy uploaded `SANCTUARY evidence pattern` overlay text in the UI display layer.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab data model, receipt schema, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_17
```

## Patch 72.18 - World Lens Receipt Naming and Sanctuary Humility Export Guard

Date: 2026-05-11

Patch 72.18 updates World Lens receipt naming and neutralizes old absolute Sanctuary narrative text in receipt/export rows.

Implemented:
- Renamed complete receipt UI from Grid receipt to World Lens receipt.
- Updated receipt ZIP filename to `aletheia_world_lens_receipt_<year>.zip`.
- Updated internal ZIP filenames to `aletheia_world_lens_receipt_<year>_*`.
- Added `_sanitize_world_lens_receipt_text(...)`.
- Sanitized `comparison_export` after World Lens diagnostic alignment so receipt/export narrative fields use low-risk/internal-taxonomy language instead of final Sanctuary wording.
- Preserved raw/internal `SANCTUARY` taxonomy values for compatibility and aggregation.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_18
```

## Patch 72.19 - Evidence Lab Humility Alignment

Date: 2026-05-11

Patch 72.19 aligns Evidence Lab technical displays and methodology copy with the Humility Protocol / Sanctuary-as-Asymptote standard.

Implemented:
- Renamed `Group averages by result` to `Group averages by internal taxonomy`.
- Added humble display fields to Evidence Lab UI tables: `empirical_pattern_display`, `internal_taxonomy_label`, and `humility_note`.
- Sanitized old SANCTUARY narrative text in protocol-detail and full empirical UI tables.
- Updated methodology copy so SANCTUARY is described as a low-risk internal reading, not final safety, final Sanctuary, or authority.
- Applied the same methodology update to `core_empirical.py` fallback.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_19
```

## Patch 72.20 - Evidence Humility Helper Scope Fix

Date: 2026-05-11

Patch 72.20 fixes the runtime `NameError` from Patch 72.19 by moving `_empirical_humility_display_df(...)` into top-level app scope before Evidence Lab calls it.

Implemented:
- Helper is now defined before Evidence Lab group-average and technical table rendering.
- Patch 72.19 humility display behavior is preserved.
- Added a scope regression test.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_20
```

## Patch 72.24 - World Lens Public Display Taxonomy Guard

Date: 2026-05-11

Patch 72.24 centralizes World Lens public taxonomy display.

Implemented:
- Added `_world_lens_public_display_df(...)`.
- Added `_world_lens_taxonomy_label(...)`.
- World Lens comparison tables now display `empirical_pattern_display`, `internal_taxonomy_label`, and `humility_note`.
- Renamed public result distribution views to internal taxonomy distribution.
- Changed selected-year CSV public naming from Global Grid to World Lens.
- Updated receipt-readiness wording from Global Grid to World Lens.
- Display-guarded receipt verdict summaries and all-rows output.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_24
```

## Patch 72.25 - World Lens Receipt Table Completion

Date: 2026-05-11

Patch 72.25 completes World Lens receipt/table display alignment after Patch 72.24.

Implemented:
- Public display helper now detects `internal_taxonomy_label`, `raw_aletheia_verdict`, and `raw_verdict`.
- Tables already using `internal_taxonomy_label` now receive `empirical_pattern_display` and `humility_note`.
- Remaining THRESHOLD/ASYLUM final interpretation strings are converted to internal-reading wording.
- Receipt distribution CSV is renamed from verdict distribution to taxonomy distribution.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_25
```

## Patch 72.26 - World Lens Live UI Table Guard

Date: 2026-05-12

Patch 72.26 aligns live World Lens UI tables with the Humility Protocol display guideline.

Implemented:
- Added `_world_lens_ui_table_df(...)`.
- Live UI tables now show `empirical_pattern_display`, `internal_taxonomy_label`, and `humility_note` first.
- Live UI tables hide raw compatibility columns by default while preserving raw/internal fields in downloads.
- Applied the UI helper to World Lens comparison/detail/report tables.
- Removed remaining old public World Lens copy using Global Grid / Grid year / verdict distribution language.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No 9k allocation formula change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_26
```

## Patch 72.27 - Mirror Stress Live UI Taxonomy Guard

Date: 2026-05-12

Patch 72.27 extends live UI taxonomy/humility display alignment to Mirror Check, Stress Test, and Audit self-check views.

Implemented:
- Added generic protocol display helpers for Mirror/Stress/Audit tables and metric cards.
- Guarded Sydney Protocol self-check result tables.
- Guarded Mirror and Stress batch summary tables.
- Stress Test main result card now displays a public protocol reading first and the raw internal taxonomy underneath.
- Mirror Check judgment card now displays a public protocol reading first, the raw internal taxonomy underneath, and a humility note.
- Reworded the guarded public-system self-check label from final-Sanctuary language to low-risk eligibility language.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_27
```

## Patch 72.28 - Shared Copy Humility Polish

Date: 2026-05-12

Patch 72.28 applies the small copy-polish backlog from Mirror Check, Stress Test, Boundary Cases, and Evidence Lab screenshot review.

Implemented:
- Shared state labels now use `Selected case / scenario` and `Evidence basis`.
- Mirror Check review-band copy now uses `Near low-risk boundary`.
- Mirror Check question expander now says `Questions before relying on this reading`.
- Evidence Lab schema help uses `Helpful empirical columns`, hides duplicate `population` from the helpful list, and adds `Scale expectations`.
- Evidence Lab disclaimer now says `enforcement authority`.
- Evidence Lab method note now uses empirical evidence-audit / internal authority-boundary review wording.
- Evidence source and field mapping copy now uses CPI-style/corruption-capture wording and `vulnerable groups`.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_28
```

## Patch 72.29 - World Lens Copy Humility Polish

Date: 2026-05-12

Patch 72.29 gives World Lens the same copy/humility polish applied to the other modules.

Implemented:
- Replaced remaining public `verdict signal` language with `internal taxonomy signal`.
- Replaced remaining distribution copy with internal-taxonomy wording.
- Replaced report-packet phrasing with review-packet phrasing.
- Updated World Lens Simulation copy to use `final review remains human`, `enforcement authority`, and `real 9k body` wording.
- Updated receipt markdown labels to `World Lens source state` and `Evidence allocation status`.
- Replaced legacy receipt module note title with `Module alignment note`.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_29
```

## Patch 72.30 - Protocol Guide Copy Humility Polish

Date: 2026-05-12

Patch 72.30 gives Protocol Guide the same copy/humility treatment applied to the rest of the app.

Implemented:
- Protocol Guide identity now says ALETHEIA v1.0 — Governance Mirror.
- `keep final judgment human` changed to `keep final review human`.
- Old Protocol Guide `Global Grid` public copy changed to World Lens.
- 9k copy now says human anti-tyranny scaffold / threshold steward.
- `Sanctuary / Threshold / Asylum labels` changed to `Internal taxonomy labels`.
- Internal taxonomy descriptions now explicitly state that SANCTUARY is not final safety, final Sanctuary, or authority.
- Release/history copy avoids `final smoke release`, real 9k selection, and old final-truth wording where it could sound too absolute.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_30
```

## Patch 72.31 - Why ALETHEIA Copy Humility Polish

Date: 2026-05-12

Patch 72.31 gives Why ALETHEIA / About the same copy-humility treatment applied to the rest of the app.

Implemented:
- Why ALETHEIA intro now says ALETHEIA reflects; people decide.
- Mirror Check description now uses public reading plus raw/internal taxonomy label wording.
- Evidence Lab description now says empirical evidence-audit workflow and rejects proof-engine/oracle framing.
- World Lens description now uses comparison/exposure model language and rejects Global ID, real 9k body, sovereign body, and political mandate readings.
- Protocol Guide description uses Humility / Z-axis boundary language instead of V-Axis Compass.
- Research caution says outputs are internal review readings.
- Standalone `about_page.py` received matching copy polish.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 72_31
```

## Patch 73 - Layered Scope Clarification

Date: 2026-05-12

Patch 73 clarifies the public scope distinction between ALETHEIA's current tool layer, research layer, long-term vision layer, and out-of-scope boundary.

Implemented:
- README now frames ALETHEIA's current operational layer as a corruption-pattern and governance-risk detection framework for human review.
- Added `docs/scope_layers.md` to separate current capability, research hypotheses, theoretical horizon, and non-authority exclusions.
- Why ALETHEIA / About now includes a visible Scope Layers expander in both `app.py` and standalone `about_page.py`.
- The incorruptible-system language is explicitly framed as a theory horizon, not a present capability, mandate, or authority claim.
- Out-of-scope copy states that ALETHEIA does not govern, enforce, allocate authority, select representatives, create a real 9k body, issue mandates, validate spiritual or political authority, or replace human judgment.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 73
```


## Patch 73.1 - Scope Copy Trim / UI Minimalism

Date: 2026-05-12

Patch 73.1 keeps Patch 73's scope clarification while reducing first-view UI weight in About / Why ALETHEIA.

Implemented:
- The Scope Layers expander in integrated `app.py` Why ALETHEIA is now collapsed by default.
- The matching Scope Layers expander in standalone `about_page.py` is now collapsed by default.
- The layered-scope copy remains available and unchanged for readers who open it.
- No module-level disclaimer spread was added; longer scope framing stays concentrated in About/docs/README.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model, authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 73_1
```

## Patch 74 - Public Evaluation Case Pack

Date: 2026-05-12

Patch 74 adds a modest public evaluation case pack so reviewers can test ALETHEIA on concrete inputs instead of judging only the vision layer.

Implemented:
- Added eight copy/paste public evaluation cases under `examples/evaluation_cases/`.
- Added `docs/evaluation_method.md` to explain how to test for mirror behavior, evidence awareness, repair questions, and non-authority boundaries.
- Added `docs/public_test_cases.md` as a catalog of the case pack.
- Added README pointers to the evaluation cases and method docs.
- Added a patch-specific structure/coverage test.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model change.
- No app UI change.
- No authority boundary, storage, public ledger, Global ID sync, central storage, or enforcement behavior changed.

Check:

```bat
tools\run_patch_checks.bat 74
```

## Patch 75 - Mirror Check ASYLUM Metric Cap + Copy Polish

Date: 2026-05-12

Patch 75 fixes a Mirror Check consistency regression found while testing Patch 74 evaluation cases: ASYLUM / High readings could still show THRESHOLD-style trust/alignment/ego metrics in the Mirror Check UI/receipt path.

Implemented:
- Mirror Check now applies `enforce_asylum_metric_consistency` after final judgment generation.
- Mirror Check normalizes ASYLUM protocol labels with `normalize_asylum_protocol_label`.
- Mirror Check keeps ASYLUM repair questions available for high-risk readings.
- Local witness receipt construction now defensively caps ASYLUM / High metrics even if the caller passes an uncapped sim object.
- Protocol summary copy now uses humility language: `Protocol reading`, `internal taxonomy label`, and `ALETHEIA does not enforce action`.

Invariant preserved:
- No authority claim.
- No enforcement path.
- No public ledger.
- No Global ID sync.
- No central storage.
- No Evidence Lab or World Lens data model change.
- Raw pre-ethics metrics remain available in receipts when present.

Check:

```bat
tools\run_patch_checks.bat 75
```

## Patch 76 - Differentiation / Comparison Framing

Date: 2026-05-12

Patch 76 clarifies ALETHEIA's public niche relative to adjacent governance and AI-audit tool categories while preserving the narrow mirror boundary.

Implemented:
- Added `docs/comparison_positioning.md` to define ALETHEIA as qualitative governance-risk reflection rather than enterprise compliance, legal tooling, institutional GRC, or technical fairness tooling.
- Added README positioning text that distinguishes enterprise AI governance workflows, technical fairness libraries, and ALETHEIA's corruption-pattern / power-analysis mirror.
- Added a short collapsed About/Why ALETHEIA positioning expander in both app and standalone about page.
- Added the free/open-source commitment: ALETHEIA is free/open-source code and is intended to remain free, without turning access or code into authority.
- Added a patch-specific test covering comparison framing, free/open-source wording, and anti-overclaim boundaries.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No app engine change.
- No competitor pricing claims.
- No claim that ALETHEIA replaces enterprise governance, technical fairness testing, compliance review, legal review, or human judgment.

Check:

```bat
tools\run_patch_checks.bat 76
```

## Patch 77 - Capture Risk Signals Framework

Date: 2026-05-12

Patch 77 makes ALETHEIA's anti-capture logic explicit as a public framework while preserving the mirror boundary.

Implemented:
- Added `docs/capture_risk_framework.md` with the core statement: ALETHEIA is anti-capture by design and capture-risk-detecting by function.
- Defined capture-risk signal categories: power concentration, weak or missing appeal paths, hidden influence / information asymmetry, evidence gaps or selective evidence, consent pressure, authority overreach, and service misalignment.
- Added a copy/paste capture-risk audit prompt and usage guidance.
- Added `examples/evaluation_cases/regulatory_capture_revolving_door_en.txt` to test hidden influence, revolving-door incentives, evidence gaps, and public-accountability safeguards.
- Added README and About pointers to the capture-risk framework.
- Updated the public test-case catalog.
- Added a patch-specific test covering framework content, boundary wording, evaluation-case structure, About/README links, and patch ledgers.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No app engine change.
- No new module.
- No enforcement, certification, punishment, legal authority, political authority, religious authority, public ledger, Global ID sync, central storage, or final judgment.

Check:

```bat
tools\run_patch_checks.bat 77
```

## Patch 78 - Capture Risk Checklist / Prompt Pack

Date: 2026-05-12

Patch 78 turns the Patch 77 capture-risk framework into a practical checklist and copy/paste prompt pack.

Implemented:
- Added `docs/capture_risk_checklist.md` as a one-page practical checklist for power concentration, appeal paths, hidden influence, evidence integrity, consent pressure, authority boundary, and service alignment.
- Added `examples/capture_risk_prompts/` with five copy/paste prompts for general capture-risk review, policy proposals, institution self-audit, AI governance, and evidence/consent pressure.
- Added README and About pointers to the checklist/prompt pack.
- Linked the practical companion from `docs/capture_risk_framework.md`.
- Added a patch-specific test covering prompt-pack structure, boundary language, README/About links, and patch ledgers.

Invariant preserved:
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model change.
- No new app module.
- No enforcement, certification, punishment, legal authority, political authority, religious authority, public ledger, Global ID sync, central storage, or final judgment.

Check:

```bat
tools\run_patch_checks.bat 78
```

## Patch 79 - Android WebView APK Wrapper

Date: 2026-05-12

Patch 79 adds an optional lightweight Android wrapper so people can install an APK that opens the live ALETHEIA Streamlit app.

Implemented:
- Added `android_webview/`, a minimal Android WebView project named **ALETHEIA Mirror**.
- The wrapper opens `https://aletheialive.streamlit.app/`.
- Added `docs/android_apk_wrapper.md` with Android Studio and command-line build notes.
- Added README documentation clarifying that the APK wrapper is not a native rewrite and not an offline mobile version.
- Added a patch-specific test covering wrapper structure, live URL, internet-only permission posture, no dangerous permissions, boundary wording, and patch ledgers.

Invariant preserved:
- No Streamlit engine change.
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model change.
- No native rewrite or offline mobile claim.
- No ads, trackers, analytics SDKs, push notifications, public ledger, Global ID sync, central storage, enforcement, certification, punishment, legal authority, political authority, religious authority, or final judgment.

Check:

```bat
tools\run_patch_checks.bat 79
```

## Patch 80 - Signed Release APK Build Guide

Date: 2026-05-12

Patch 80 adds a safe local release-signing workflow for the optional ALETHEIA Mirror Android WebView wrapper.

Implemented:
- Added `docs/signed_release_apk.md` with keystore creation, signed release build, sharing, and recovery notes.
- Added `android_webview/signing.properties.example` as a local-only template.
- Updated `android_webview/app/build.gradle` to support release signing from local `signing.properties` when present.
- Updated `.gitignore` to exclude local Android signing secrets and release artifacts.
- Updated README and `docs/android_apk_wrapper.md` to point to the signed-release guide.
- Added a patch-specific test covering signing docs, secret exclusion, release build configuration, and patch ledgers.

Invariant preserved:
- No keystore, private key, password, or signed APK is committed.
- No Streamlit engine change.
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model change.
- No native rewrite or offline mobile claim.
- No ads, trackers, analytics SDKs, push notifications, public ledger, Global ID sync, central storage, enforcement, certification, punishment, legal authority, political authority, religious authority, or final judgment.

Check:

```bat
tools\run_patch_checks.bat 80
```

## Patch 81 - Android WebView Hello Android Guard / Troubleshooting

Status: READY FOR LOCAL TESTING

Patch 81 adds a troubleshooting guard for APK builds that accidentally show a default `Hello Android!` template screen instead of the ALETHEIA WebView.

Summary:
- Added `docs/android_webview_troubleshooting.md`.
- Linked the troubleshooting guide from README and `docs/android_apk_wrapper.md`.
- Added a patch-specific test that verifies `MainActivity.java` is a WebView activity, points to `https://aletheialive.streamlit.app/`, and contains no default Android template markers.
- No Streamlit engine change, no scoring change, no receipt change, no native rewrite, no new permissions, no keystore, and no signed APK included.

Validation:
- `tools\run_patch_checks.bat 81`

## Patch 82 - Android App Icon / WebView Template Purge

Status: READY FOR LOCAL TESTING

Patch 82 adds the ALETHEIA launcher icon to the Android WebView wrapper and removes remaining stale Android default-template risk from the wrapper project.

Summary:
- Added ALETHEIA mascot/logo launcher resources for adaptive and legacy Android icons.
- Added `android:icon` and `android:roundIcon` to the Android manifest.
- Replaced the stale default-template Kotlin activity with a neutral placeholder so it cannot show `Hello Android!`.
- Simplified the Groovy Android Gradle config to Java WebView only, with no Compose dependency path.
- Aligned Kotlin Gradle mirror files to the same WebView package in case Android Studio reads them.
- Updated Android wrapper and troubleshooting docs.
- Added a patch-specific test for launcher icons, manifest icon bindings, WebView package alignment, and no default-template markers.

Boundary preserved:
- No Streamlit engine change.
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No native rewrite or offline mobile claim.
- No new Android permissions beyond internet access.
- No keystore, private key, password, or signed APK is committed.
- No ads, trackers, analytics SDKs, push notifications, public ledger sync, Global ID sync, central storage, enforcement, certification, punishment, legal authority, political authority, religious authority, or final judgment.

Verification:

```bat
tools\run_patch_checks.bat 82
tools\run_patch_checks.bat 81
```

## Patch 84 - Android Adaptive Icon Resource Fix

Status: READY FOR LOCAL TESTING

Patch 84 fixes Android release resource linking for the optional WebView wrapper when the build reports:

```text
<adaptive-icon> elements require a sdk version of at least 26
```

Summary:
- Moved adaptive launcher icon XML into `mipmap-anydpi-v26/`.
- Replaced unqualified `mipmap-anydpi/` launcher XML with non-adaptive bitmap fallbacks.
- Preserved `minSdk 23` instead of raising the minimum Android version.
- Updated the Patch 82 icon test expectations so older patch checks align with the resource-placement fix.
- Added `docs/android_adaptive_icon_resource_fix.md` and a patch-specific guard test.

Boundary preserved:
- No Streamlit engine change.
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model change.
- No WebView URL change.
- No new Android permissions.
- No keystore, password, private key, or signed APK is included.
- No ads, trackers, analytics SDKs, push notifications, public ledger sync, Global ID sync, central storage, enforcement, certification, punishment, legal authority, political authority, religious authority, or final judgment.

Verification:

```bat
tools\run_patch_checks.bat 84
tools\run_patch_checks.bat 82
```

## Patch 85 - AI Integrity Mirror Scaffold

Status: READY FOR LOCAL TESTING

Patch 85 adds **AI Integrity Mirror** as a new static review tab inside the existing ALETHEIA app.

Summary:
- Added `core/ai_integrity_mirror.py` with deterministic static audit logic for pasted AI outputs, prompts, agent specs, model-card claims, and code snippets.
- Added a new `🤖 AI Integrity Mirror` app tab.
- Added authority-overreach, no-review, enforcement, opacity, coercion, surveillance, exposed-secret, and unsafe-code signal checks.
- Added internal taxonomy label, risk, integrity, collapse pressure, triggered-signal display, repair questions, and local witness receipt download.
- Added `docs/ai_integrity_mirror.md` and a patch-specific test.

Boundary preserved:
- No live model benchmarking.
- No external model calls, web calls, repository scanning, public ledger, Global ID sync, central storage, or certification.
- No Mirror Check, Stress Test, Evidence Lab, or World Lens scoring change.
- No enforcement, punishment, legal authority, political authority, religious authority, medical authority, moral finality, vendor approval, or final safety claim.

Verification:

```bat
tools\run_patch_checks.bat 85
```

## Patch 86 - AI Integrity Mirror Copy & Receipt Polish

Status: READY FOR LOCAL TESTING

AI Integrity Mirror does not certify AI systems, vendors, prompts, agents, codebases, or outputs.

Patch 86 polishes the Patch 85 AI Integrity Mirror scaffold so the UI, analyzer metadata, and local receipt context consistently describe a static risk reading rather than certification.

Summary:
- Updated AI Integrity Mirror copy to emphasize static review, pasted-artifact scope, and non-certification.
- Added explicit scope, receipt, and reliance notes to `core/ai_integrity_mirror.py`.
- Carried boundary notes into scan/report metadata for local witness receipts.
- Added a "How to read this result" expander and clearer metric labels: risk reading, integrity reading, and capture pressure.
- Updated AI Integrity documentation and added a patch-specific test.

Boundary preserved:
- No scoring-math change.
- No verdict-routing change.
- No Mirror Check, Stress Test, Evidence Lab, World Lens, or Boundary Cases logic change.
- No live model benchmarking, external calls, repository crawler, public ledger, Global ID sync, central storage, enforcement, punishment, model certification, vendor approval, legal authority, political authority, religious authority, medical authority, moral finality, or final safety claim.

Verification:

```bat
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```
## Patch 87 - AI Integrity Mirror Demo Examples and Static Smoke Coverage

Status: READY FOR LOCAL TESTING

Patch 87 improves AI Integrity Mirror usability and regression safety by centralizing demo examples and testing that each example remains auditable as a static pasted artifact.

Summary:
- Added shared `AI_INTEGRITY_DEMO_EXAMPLES` metadata to `core/ai_integrity_mirror.py`.
- Updated the AI Integrity Mirror app tab to load demo text from the shared examples.
- Added demo-focus captions so users understand what each example is meant to illustrate.
- Removed duplicated non-certification copy in the AI Integrity intro.
- Added patch-specific tests that audit every demo example without external calls.

Boundary preserved:
- No scoring-math change.
- No verdict-routing change.
- No Mirror Check, Stress Test, Evidence Lab, World Lens, or Boundary Cases logic change.
- No live model benchmarking, external calls, repository crawler, public ledger, Global ID sync, central storage, enforcement, punishment, model certification, vendor approval, legal authority, political authority, religious authority, medical authority, moral finality, or final safety claim.

Verification:

```bat
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```


## Patch 88 - AI Integrity Mirror Signal Evidence Snippets

Status: READY FOR LOCAL TESTING

Patch 88 makes AI Integrity Mirror findings easier to review by adding human-readable signal categories and short evidence snippets for each triggered rule. Credential-like values are redacted before snippets are shown in the UI table or carried in analyzer metadata.

Summary:
- Added category metadata to AI Integrity findings.
- Added bounded local evidence snippets for triggered signals.
- Added credential/private-key redaction for evidence snippets.
- Updated the triggered-signal table with Category and Evidence snippet columns.
- Added patch-specific tests and documentation updates.

Boundary preserved:
- Evidence snippets are review aids, not proof, certification, model approval, vendor approval, or final safety claims.
- Static pasted-artifact review only.
- No scoring-math change.
- No verdict-routing change.
- No live model benchmarking, external calls, repository crawler, public ledger, Global ID sync, central storage, enforcement, punishment, legal authority, political authority, religious authority, medical authority, moral finality, or certification.

Verification:

```bat
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Patch 89 - Privacy Boundary Visibility

Status: READY FOR LOCAL TESTING

Patch 89 makes ALETHEIA's no-built-in-data-collection boundary visible in the app, About page, README, and documentation. This supports adoption and user trust without turning privacy language into a certification or infrastructure guarantee.

Summary:
- Added app-visible privacy-by-design copy near the top-level guidance.
- Added a sidebar privacy boundary caption.
- Added AI Integrity Mirror-specific data-boundary copy for pasted artifacts.
- Added an About-page privacy expander.
- Added `docs/privacy_boundary.md` with safe public wording and deployment caution.
- Updated README and AI Integrity documentation.
- Added patch-specific static tests for visible privacy copy and absence of common telemetry/backend-upload imports in Python app code.

Boundary preserved:
- The claim is limited to ALETHEIA's repository/app-code design.
- Third-party hosts may still keep their own server/access logs outside ALETHEIA's code boundary.
- No scoring-math change.
- No verdict-routing change.
- No AI Integrity rubric change.
- No live model benchmarking, external calls, repository crawler, storage layer, public ledger, Global ID sync, enforcement, certification, or authority claim.

Verification:

```bat
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Patch 90 - AI Integrity Batch Review Scaffold

Status: READY FOR LOCAL TESTING

Patch 90 adds a small static batch-review layer to AI Integrity Mirror. Users can paste multiple AI outputs, prompts, agent specs, model-card excerpts, policy claims, or code snippets and separate them with delimiter lines such as `---`, `===`, or `###`.

Summary:
- Added `split_ai_integrity_batch_input`, `summarize_ai_integrity_batch`, and `audit_ai_integrity_batch` to the AI Integrity analyzer.
- Added an app checkbox for AI Integrity batch review mode.
- Added an **AI Integrity Batch Summary** with artifact count, Low / Medium / High risk-reading counts, highest-pressure item, per-item readings, category summary, and collapsed item details.
- Added patch-specific tests for delimiter splitting, per-item batch readings, UI copy, and ledger/docs coverage.

Boundary preserved:
- Batch review uses pasted artifacts only.
- No scoring-math change.
- No verdict-routing change.
- No live model benchmarking, external calls, repository crawler, storage layer, public ledger, Global ID sync, enforcement, vendor ranking, model certification, approval, or final safety claim.
- Batch comparison is artifact-level review support only, not a model-wide benchmark or certification.

Verification:

```bat
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Patch 91 - AI Integrity Receipt Export Polish

Status: READY FOR LOCAL TESTING

Patch 91 polishes AI Integrity Mirror receipt exports. Downloaded receipts now begin with an AI Integrity-specific context section before the generic local witness receipt.

Summary:
- Added `AI_INTEGRITY_RECEIPT_VERSION`.
- Added a receipt context builder and renderer in `core/ai_integrity_mirror.py`.
- Added app receipt export prefix with static review scope, privacy boundary, non-certification note, reliance boundary, redacted evidence snippets, and repair questions.
- Batch-mode receipt context can include batch summary metadata without becoming a model ranking, benchmark, approval, or certification.
- Added patch-specific tests for receipt context, batch receipt context, app wiring, and docs/ledger coverage.

Boundary preserved:
- Static pasted-artifact review only.
- No scoring-math change.
- No verdict-routing change.
- No live model benchmarking, external calls, repository crawler, storage layer, public ledger sync, Global ID sync, enforcement, vendor ranking, model certification, model approval, or final safety claim.

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

## Patch 92 - AI Integrity Rubric Documentation

Status: READY FOR LOCAL TESTING

Patch 92 publishes the AI Integrity Mirror rubric as a reviewable documentation artifact. It makes the signal categories, signal names, review questions, current weight ranges, positive review signals, evidence-snippet/redaction behavior, batch boundaries, receipt scope, privacy boundary, and out-of-scope claims explicit.

Summary:
- Added `docs/ai_integrity_rubric.md`.
- Updated `docs/ai_integrity_mirror.md` with a Patch 92 rubric-documentation section.
- Updated README with AI Integrity Mirror scope and rubric links.
- Added patch-specific tests for rubric transparency and boundary preservation.

Boundary preserved:
- Documentation only.
- No scoring-math change.
- No signal-pattern change.
- No signal-weight change.
- No verdict-routing change.
- No UI behavior change.
- No receipt-generation change.
- No live model benchmarking, external calls, repository crawler, storage layer, public ledger sync, Global ID sync, enforcement, vendor ranking, model certification, approval, or final safety claim.

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

## Patch 93 - AI Integrity Batch Demo Pack

Status: READY FOR LOCAL TESTING

Patch 93 adds ready-to-use AI Integrity Mirror demo artifacts so reviewers can test single-artifact and batch review paths without inventing examples.

Summary:
- Added `examples/ai_integrity/bounded_ai_answer.txt`.
- Added `examples/ai_integrity/authority_overclaim.txt`.
- Added `examples/ai_integrity/opaque_agent_workflow.txt`.
- Added `examples/ai_integrity/code_secret_example.txt`.
- Added `examples/ai_integrity/central_identity_capture_claim.txt`.
- Added separator-delimited `examples/ai_integrity/batch_demo_v1.txt`.
- Added `docs/ai_integrity_demo_pack.md`.
- Updated README and AI Integrity Mirror docs to point to the demo pack.
- Added patch-specific tests for demo existence, batch delimiters, boundary language, coverage, and no live/certification expansion.

Boundary preserved:
- Examples/docs/tests only.
- No analyzer scoring change.
- No signal-pattern change.
- No signal-weight change.
- No verdict-routing change.
- No UI behavior change.
- No receipt-generation change.
- No live model benchmarking, external calls, repository crawler, storage layer, public ledger sync, Global ID sync, enforcement, vendor ranking, model certification, approval, or final safety claim.

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

## Patch 94 - AI Integrity UI Review Table Polish

Status: READY FOR LOCAL TESTING

Patch 94 makes AI Integrity Mirror results easier to scan while preserving the static pasted-artifact boundary.

Summary:
- Keeps compact summary cards for AI Integrity batch counts and highest-pressure item.
- Shows highest pressure signals above the detailed review table.
- Groups triggered findings by category.
- Moves evidence snippets into collapsed expanders.
- Shows repair questions more prominently as human-review prompts.
- Improves empty-state copy so no-trigger output is not mistaken for approval, certification, or a safety guarantee.
- Updates AI Integrity docs, README, progress database, manifest, recovery note, and patch-specific tests.

Boundary preserved:
- UI/result presentation only.
- No analyzer scoring change.
- No signal-pattern change.
- No signal-weight change.
- No verdict-routing change.
- No receipt-generation change.
- No live model benchmarking, external calls, repository crawler, storage layer, public ledger sync, Global ID sync, enforcement, vendor ranking, model certification, approval, or final safety claim.

Verification:

```bat
tools\run_patch_checks.bat 94
tools\run_patch_checks.bat 93
tools\run_patch_checks.bat 92
```


## Patch 95 - Code Integrity Static Scan v1

Status: READY FOR LOCAL TESTING

Patch 95 adds a code-specific static scan layer for pasted code artifacts inside AI Integrity Mirror.

Summary:
- Added `scan_code_integrity_static()` and `CODE_INTEGRITY_SCAN_VERSION` in `core/ai_integrity_mirror.py`.
- Detects exposed secrets, dangerous subprocess/eval usage, hardcoded admin bypass markers, unsafe deletion patterns, outbound network calls, telemetry-like endpoints, central logging / identity sync hints, and missing human-review gates in automated decision code.
- Adds redacted evidence snippets, severity counts, category counts, and code review questions.
- Surfaces Code Integrity Static Scan metadata in the AI Integrity Mirror result view.
- Added `docs/code_integrity_static_scan.md` plus AI Integrity docs / README pointers.
- Added patch-specific tests in `tests/test_patch_95_code_integrity_static_scan.py`.

Boundary preserved:
- Static pasted-code scan only.
- No analyzer scoring change.
- No verdict-routing change.
- No code execution.
- No dependency audit.
- No repository crawler.
- No external calls.
- No live model benchmarking.
- No penetration test.
- No security guarantee.
- No vulnerability certification.
- No compliance approval.
- No model certification, enforcement, approval, or final safety claim.

Verification:

```bat
tools\run_patch_checks.bat 95
tools\run_patch_checks.bat 94
tools\run_patch_checks.bat 93
```

## Patch 96 - Privacy Boundary Audit Panel

Status: READY FOR LOCAL TESTING

Patch 96 adds a static Privacy Boundary Audit Panel inside AI Integrity Mirror.

Summary:
- Added `scan_privacy_boundary_static()` and `PRIVACY_BOUNDARY_SCAN_VERSION` in `core/ai_integrity_mirror.py`.
- Detects analytics packages, external network call patterns, telemetry keywords, database write hints, backend endpoint hints, and local-only statement markers.
- Flags privacy-boundary tension when local-only/no-data-collection wording appears beside analytics, network, telemetry, database, or backend evidence.
- Adds local-only statement, hosting caveat, redacted evidence snippets, category counts, and privacy review questions.
- Surfaces the Privacy Boundary Audit Panel in AI Integrity Mirror results.
- Added `docs/privacy_boundary_audit_panel.md` plus AI Integrity docs / README pointers.
- Added patch-specific tests in `tests/test_patch_96_privacy_boundary_audit_panel.py`.

Boundary preserved:
- Static pasted-artifact review only.
- No analyzer scoring change.
- No verdict-routing change.
- No runtime monitoring.
- No host-log inspection.
- No dependency crawl.
- No repository crawler.
- No external calls.
- No live model benchmarking.
- No privacy guarantee.
- No compliance approval.
- No vendor audit.
- No hosting audit.
- No certification.
- No proof that no data is collected.

Verification:

```bat
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
tools\run_patch_checks.bat 94
```


## Patch 97 - AI Integrity Comparison View v1

Status: READY FOR LOCAL TESTING

Patch 97 adds an artifact-level **AI Integrity Comparison View** for delimiter-separated batch results.

Summary:
- Added `AI_INTEGRITY_COMPARISON_VERSION` and `build_ai_integrity_comparison()` in `core/ai_integrity_mirror.py`.
- Added side-by-side comparison metadata for risk readings, signal counts, code detections, privacy-boundary signals, boundary-risk comparison, and review needed notes.
- Added AI Integrity Comparison View UI inside the batch result area.
- Added `docs/ai_integrity_comparison_view.md` plus README and AI Integrity docs pointers.
- Added patch-specific tests in `tests/test_patch_97_ai_integrity_comparison_view.py`.

Boundary preserved:
- Static pasted-artifact comparison only.
- No analyzer scoring change.
- No signal-pattern change.
- No signal-weight change.
- No verdict-routing change.
- No receipt-generation change.
- No live model benchmarking.
- No external calls.
- No repository crawler.
- No storage layer.
- No public ledger sync.
- No Global ID sync.
- No enforcement.
- Comparison is artifact-level.
- It is not model-wide certification.
- It is not a vendor ranking.
- It is not a final truth claim.

Verification:

```bat
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
```

## Patch 98 - AI Integrity Red Team Prompt Pack v1

Status: READY FOR LOCAL TESTING

Patch 98 adds a static/manual **AI Integrity Red Team Prompt Pack v1**.

Summary:
- Added `examples/ai_integrity/red_team_prompt_pack_v1.txt`.
- Added manual prompts for authority overreach, legal/medical/political false authority, manipulation pressure, privacy extraction, surveillance/capture, false certainty, no-appeal automation, unsafe code request, refusal quality, and bounded-answer control.
- Added `docs/ai_integrity_red_team_prompt_pack.md` plus README and AI Integrity docs pointers.
- Added patch-specific tests in `tests/test_patch_98_red_team_prompt_pack.py`.

Boundary preserved:
- Static prompt examples only.
- No analyzer scoring change.
- No signal-pattern change.
- No signal-weight change.
- No verdict-routing change.
- No UI behavior change.
- No receipt-generation change.
- No live model calls.
- No live model benchmarking.
- No external calls.
- No repository crawler.
- No storage layer.
- No public ledger sync.
- No Global ID sync.
- No enforcement.
- Not model-wide certification.
- Not a vendor ranking.
- Not a final truth claim.
- Not a security guarantee.

Verification:

```bat
tools\run_patch_checks.bat 98
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
```


## Patch 99 - AI Integrity Report Builder v1

Status: READY FOR LOCAL TESTING

Patch 99 adds a compact **AI Integrity Report Builder v1** for AI Integrity batch results.

Summary:
- Added `AI_INTEGRITY_REPORT_VERSION`, `build_ai_integrity_report()`, and `render_ai_integrity_report_text()` in `core/ai_integrity_mirror.py`.
- Added an AI Integrity batch UI report section with executive summary, artifact count, risk distribution, top triggered categories, selected redacted evidence snippets, repair questions, non-certification note, privacy note, preview, and local text download.
- Added `docs/ai_integrity_report_builder.md` plus README and AI Integrity docs pointers.
- Added patch-specific tests in `tests/test_patch_99_ai_integrity_report_builder.py`.

Boundary preserved:
- Static pasted-artifact report only.
- No analyzer scoring change.
- No signal-pattern change.
- No signal-weight change.
- No verdict-routing change.
- No code execution.
- No live model calls.
- No external calls.
- No repository crawler.
- No vendor ranking.
- No model-wide certification.
- No safety guarantee.
- No security guarantee.
- No privacy guarantee.
- No final truth claim.

Verification:

```bat
tools\run_patch_checks.bat 99
tools\run_patch_checks.bat 98
tools\run_patch_checks.bat 97
```

## Patch 100 - Release Stabilization / Public Adoption Package

Status: READY FOR LOCAL TESTING

Patch 100 stabilizes the public-facing **ALETHEIA v1.0 AI Integrity Preview** release surface.

Summary:
- Added `docs/ai_integrity_preview_public_adoption.md`.
- Added `docs/ai_integrity_preview_release_notes.md`.
- Added `docs/ai_integrity_screenshots_guidance.md`.
- Updated README and AI Integrity documentation with a first-use path for demos, batch review, comparison, red-team prompt outputs, code/privacy boundary review, and report exports.
- Updated About page release copy for the AI Integrity Preview milestone.
- Added patch-specific tests in `tests/test_patch_100_release_stabilization_public_adoption.py`.

Boundary preserved:
- Release-surface stabilization only.
- No analyzer scoring change.
- No signal-pattern change.
- No signal-weight change.
- No verdict-routing change.
- No receipt-generation change.
- No live model calls.
- No external calls.
- No repository crawler.
- No vendor ranking.
- No model-wide certification.
- No safety guarantee.
- No security guarantee.
- No privacy guarantee.
- No legal, medical, political, religious, or official authority.
- No public ledger sync.
- No Global ID sync.
- No central storage.
- No enforcement.
- No final truth claim.

Verification:

```bat
tools\run_patch_checks.bat 100
tools\run_patch_checks.bat 99
tools\run_patch_checks.bat 98
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
```


## Patch 101 - Human-Auditable Protocol Baseline Self-Audit

Status: READY FOR LOCAL TESTING

Patch 101 adds a local protocol baseline self-audit and go-live static privacy review statement.

Summary:
- Added `core/protocol_baseline_self_audit.py` and `tools/run_protocol_baseline_self_audit.py`.
- Added `data/protocol_baseline_manifest.json` with SHA-256 hashes for selected core protocol, release-boundary, and AI Integrity files.
- Added `docs/protocol_baseline_self_audit.md`.
- Added `docs/go_live_privacy_review_statement.md`.
- Added patch-specific tests in `tests/test_patch_101_protocol_baseline_self_audit.py`.

Boundary preserved:
- Local static hash comparison only.
- Human-auditable review evidence only.
- No automated approval.
- Not tamper-proof.
- No security guarantee.
- No privacy guarantee.
- No certification.
- No enforcement.
- No live model calls.
- No external calls.
- No scoring or verdict-routing changes.

Verification:

```bat
tools\run_patch_checks.bat 101
python tools\run_protocol_baseline_self_audit.py
tools\run_patch_checks.bat 100
```


## Patch 102 - Structural Improvement Entry Point

Status: PASSED BY USER / READY FOR NEXT PATCH

Patch 102 starts the structural improvement path with documentation-first onboarding and architecture mapping before any `app.py` refactor.

Boundary preserved: documentation/tests only; no runtime behavior, scoring, verdict routing, receipt schema, telemetry, storage, external-call behavior, or authority-claim changes.

## Patch 103 - Signal Detection Transparency Documentation

Status: PASSED BY USER / READY FOR NEXT PATCH

Patch 103 documents ALETHEIA's transparent rule-based and heuristic signal-detection posture, including English/Dutch calibration limits and human-review requirements.

Boundary preserved: documentation/tests only; no scoring, verdict routing, signal-pattern, signal-weight, receipt schema, telemetry, storage, external-call behavior, or authority-claim changes.

## Patch 104 - Boundary, Privacy, and Hosted-Use Transparency

Status: PASSED BY USER / READY FOR NEXT PATCH

Patch 104 adds a central boundary statement, hosted-use caveat, and small reusable helper modules for future UI use.

Summary:
- Added `docs/BOUNDARY.md`.
- Added `docs/hosting_limits.md`.
- Added `core/boundary.py`.
- Added `core/privacy_panel.py`.
- Updated README, CONTRIBUTING, architecture, and privacy-boundary docs.
- Added patch-specific tests in `tests/test_patch_104_boundary_privacy_hosting.py`.

Boundary preserved:
- No scoring change.
- No verdict-routing change.
- No signal-pattern change.
- No signal-weight change.
- No receipt schema change.
- No Streamlit page wiring change.
- No app.py refactor.
- No external calls.
- No live model calls.
- No telemetry.
- No analytics.
- No backend upload endpoint.
- No central storage.
- No Global ID sync.
- No public ledger sync.
- No privacy guarantee.
- No security guarantee.
- No certification.
- No enforcement.
- No final truth claim.

Verification:

```bat
tools\run_patch_checks.bat 104
tools\run_patch_checks.bat 103
tools\run_patch_checks.bat 102
tools\run_patch_checks.bat 101
```

## Patch 105 - Patch History and Public Trust Navigation

Status: READY FOR LOCAL TESTING

Patch 105 adds a documentation navigation layer so reviewers and contributors can inspect ALETHEIA's boundary, privacy, hosting, signal-detection, architecture, and patch-history documents without being overwhelmed by the full patch trail.

Summary:
- Added `docs/patch_index.md`.
- Added `docs/public_trust_package.md`.
- Added `examples/Trust_Package_README.md`.
- Updated README, CONTRIBUTING, architecture, status, and progress docs.
- Added patch-specific tests in `tests/test_patch_105_patch_index_trust_navigation.py`.

Boundary preserved:
- No runtime behavior change.
- No scoring change.
- No verdict-routing change.
- No signal-pattern change.
- No signal-weight change.
- No receipt schema change.
- No Streamlit page wiring change.
- No app.py refactor.
- No external calls.
- No live model calls.
- No telemetry.
- No analytics.
- No backend upload endpoint.
- No central storage.
- No Global ID sync.
- No public ledger sync.
- No privacy guarantee.
- No security guarantee.
- No certification.
- No enforcement.
- No final truth claim.

Verification:

```bat
tools
un_patch_checks.bat 105
tools
un_patch_checks.bat 104
tools
un_patch_checks.bat 103
tools
un_patch_checks.bat 102
tools
un_patch_checks.bat 101
python tools
un_protocol_baseline_self_audit.py
```

## Patch 106 - Signal Dictionary and Glossary

Status: READY FOR LOCAL TESTING

Patch 106 adds `docs/SIGNAL_DICTIONARY.md`, a reviewer-facing glossary for signal families, review questions, typical cues, possible false positives, and repair directions.

Summary:
- Added `docs/SIGNAL_DICTIONARY.md`.
- Linked the dictionary from signal-detection, public-trust, patch-index, contributor, trust-package, and README surfaces.
- Added patch-specific tests in `tests/test_patch_106_signal_dictionary_glossary.py`.

Boundary preserved:
- No runtime behavior change.
- No scoring change.
- No verdict-routing change.
- No signal-pattern change.
- No signal-weight change.
- No receipt schema change.
- No Streamlit page wiring change.
- No app.py refactor.
- No external calls.
- No live model calls.
- No telemetry.
- No analytics.
- No backend upload endpoint.
- No central storage.
- No Global ID sync.
- No public ledger sync.
- No privacy guarantee.
- No security guarantee.
- No certification.
- No enforcement.
- No final truth claim.

Verification:

```bat
tools\run_patch_checks.bat 106
tools\run_patch_checks.bat 105
tools\run_patch_checks.bat 104
tools\run_patch_checks.bat 103
tools\run_patch_checks.bat 102
tools\run_patch_checks.bat 101
python tools\run_protocol_baseline_self_audit.py
```


## Patch 107 - Boundary and Privacy UI Wiring

Status: READY FOR LOCAL TESTING

Patch 107 wires the existing Patch 104 boundary/privacy helpers into the Streamlit sidebar. This is narrow runtime UI wiring only: it makes the local-first / hosted-use caveat and compact "mirror, not throne" footer visible in the app.

Boundary preserved:
- No scoring change.
- No verdict-routing change.
- No signal-pattern change.
- No signal-weight change.
- No receipt schema change.
- No external calls.
- No live model calls.
- No telemetry.
- No analytics.
- No backend upload endpoint.
- No central storage.
- No Global ID sync.
- No public ledger sync.
- No privacy guarantee.
- No security guarantee.
- No certification.
- No enforcement.
- No final truth claim.

Verification:

```bat
tools\run_patch_checks.bat 107
tools\run_patch_checks.bat 106
python tools\run_protocol_baseline_self_audit.py
```


## Patch 108 - App Shell Router Refactor Step 1

Status: READY FOR LOCAL TESTING

Patch 108 starts the gradual app.py router/shell refactor by extracting the top-of-app boundary notices into `ui/app_shell.py`. The app now calls `render_app_boundary_notices(SUPPORTED_INPUT_LANGUAGE_NOTE, st)` instead of keeping those static notices inline.

Boundary preserved:
- No scoring change.
- No verdict-routing change.
- No signal-pattern change.
- No signal-weight change.
- No receipt schema change.
- No external calls.
- No live model calls.
- No telemetry.
- No analytics.
- No backend upload endpoint.
- No central storage.
- No Global ID sync.
- No public ledger sync.
- No privacy guarantee.
- No security guarantee.
- No certification.
- No enforcement.
- No final truth claim.

Verification:

```bat
tools\run_patch_checks.bat 108
tools\run_patch_checks.bat 107
tools\run_patch_checks.bat 106
python tools\run_protocol_baseline_self_audit.py
```

## Patch 109 — App Shell Router Refactor Step 2

Status: READY FOR LOCAL TESTING

Summary:
- Continues the gradual app.py router/shell refactor started in Patch 108.
- Extracts the stable sidebar identity card and sidebar context copy into `ui/app_shell.py`.
- Keeps `app.py` as the orchestrator for navigation, interactive controls, session state, scoring calls, receipt generation, downloads, and module routing.
- Adds patch-specific tests proving the new helpers are copy-only and boundary-safe.

Boundary preserved: no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module routing change, no navigation change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required.

Validation:
- `tools\run_patch_checks.bat 109`
- `tools\run_patch_checks.bat 108`
- `tools\run_patch_checks.bat 107`
- `tools\run_patch_checks.bat 106`
- `python tools\run_protocol_baseline_self_audit.py`


App.py remains the orchestrator for behavior; Patch 109 only extracts sidebar shell copy.

## Patch 110 — App Shell Router Refactor Step 3

Status: READY FOR LOCAL REVIEW

Patch 110 continues the gradual `app.py` router/shell refactor by extracting the stable public header and first-use note into `ui/app_shell.py`. `app.py` remains the orchestrator for behavior, module routing, session state, scoring, receipts, downloads, and interactive controls.

Validation targets:

- `tools\run_patch_checks.bat 110`
- `tools\run_patch_checks.bat 109`
- `tools\run_patch_checks.bat 108`
- `tools\run_patch_checks.bat 107`
- `tools\run_patch_checks.bat 106`
- `python tools\run_protocol_baseline_self_audit.py`

Boundary preserved: no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module routing change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.


## Patch 112 — Privacy Audit Panel v1

Status: READY FOR LOCAL REVIEW

Patch 112 extracts the Privacy Boundary Audit Panel rendering into `ui/privacy_audit_panel.py` and documents the panel in `docs/privacy_audit_panel_v1.md`. The underlying scan remains the static privacy-boundary audit used by AI Integrity Mirror for pasted artifacts.

App.py remains the orchestrator for behavior, module routing, session state, scoring, receipts, downloads, and interactive controls.

Boundary preserved: no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no compliance approval, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 112
tools\run_patch_checks.bat 111
tools\run_patch_checks.bat 110
tools\run_patch_checks.bat 109
python tools\run_protocol_baseline_self_audit.py
```

## Patch 113 — Public Trust Package Consolidation

Status: READY FOR LOCAL REVIEW

Patch 113 consolidates the public trust package and adds a concise public review checklist. `docs/public_trust_package.md` is now the central review map for boundary statements, privacy/local-first posture, hosted-use limits, signal detection, the signal dictionary, architecture, beginner UX, Privacy Audit Panel v1, patch history, and the public-review checklist.

Boundary preserved: documentation/navigation only. No app.py change, no runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no compliance approval, no certification, no enforcement, and no final truth claim. Humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 113
tools\run_patch_checks.bat 112
tools\run_patch_checks.bat 111
tools\run_patch_checks.bat 110
python tools\run_protocol_baseline_self_audit.py
```

## Patch 119 — App Shell Router Refactor Step 6

Status: READY FOR LOCAL REVIEW

Patch 119 continues the gradual app.py shell/router refactor. It adds `ui/module_intro.py` and extracts exactly one small static/non-interactive UI copy block: the Stress Test "Scan my idea" note now renders through `render_stress_test_scan_intro(st)`.

Boundary preserved: copy-only module intro extraction. `app.py` remains the orchestrator for mode choice, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 119
tools\run_patch_checks.bat 118
tools\run_patch_checks.bat 117
python tools\run_protocol_baseline_self_audit.py
```

## Patch 120 — Module Intro Extraction Step 2

Status: READY FOR LOCAL REVIEW

Patch 120 continues the static module-intro extraction path started in Patch 119. It extends `ui/module_intro.py` with `render_boundary_cases_intro` and `render_consent_audit_intro`, replacing two small inline copy blocks in `app.py`.

Boundary preserved: copy-only module intro extraction. `app.py` remains the orchestrator for mode choice, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 120
tools\run_patch_checks.bat 119
tools\run_patch_checks.bat 118
python tools\run_protocol_baseline_self_audit.py
```

## Patch 121 — Shared Status / Notice Cards

Status: READY FOR LOCAL REVIEW

Patch 121 starts the shared status/notice-card layer. It adds `ui/status_cards.py` and moves the AI Integrity boundary caption group into `render_ai_integrity_boundary_cards`.

Boundary preserved: copy-only status/notice card extraction. `app.py` remains the orchestrator for mode choice, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 121
tools\run_patch_checks.bat 120
tools\run_patch_checks.bat 119
python tools\run_protocol_baseline_self_audit.py
```

## Patch 122 - Refactor Stabilization Checkpoint 2

Status: READY FOR LOCAL REVIEW

Patch 122 stabilizes the app-shell router refactor after Patch 119, Patch 120, and Patch 121. It adds `docs/refactor_stabilization_checkpoint_2.md` and regression tests that verify helper importability, `app.py` helper wiring, copy-only helper boundaries, non-authoritative language, and repair-note hygiene.

Boundary preserved: documentation and regression tests only. `app.py` remains the orchestrator for mode choice, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. No runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 122
tools\run_patch_checks.bat 121
tools\run_patch_checks.bat 120
python tools\run_protocol_baseline_self_audit.py
```

## Patch 123 - About / Public Info Page Extraction

Status: READY FOR LOCAL REVIEW

Patch 123 starts the low-risk page extraction phase. It moves the in-app `Why ALETHEIA` / About tab copy from `app.py` into `pages_ui/about_page.py`, leaving `app.py` responsible for opening the tab, resolving the optional header image, and calling the page renderer.

Boundary preserved: page-level display extraction only. The older root-level `about_page.py` remains available for standalone About-page compatibility. `app.py` remains the orchestrator for mode choice, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. No runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no session-state change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Patch 123 also aligns the Patch 122 checkpoint test with the existing privacy-audit helper name. This is test-only and does not change app behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 123
tools\run_patch_checks.bat 122
tools\run_patch_checks.bat 121
python tools\run_protocol_baseline_self_audit.py
```

## Patch 124 - Trust Package Page Extraction

Status: READY FOR LOCAL REVIEW

Patch 124 exposes the public trust package review route inside the Protocol Guide tab through `pages_ui/trust_package_page.py`. The helper renders document pointers and review prompts only; the source of truth remains `docs/public_trust_package.md`, `docs/public_review_checklist.md`, and the linked boundary, privacy, signal, architecture, beginner, and patch-history docs.

Boundary preserved: page-level display extraction only. `app.py` remains the orchestrator for tabs, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior. No runtime analysis behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no session-state change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 124
tools\run_patch_checks.bat 123
tools\run_patch_checks.bat 122
python tools\run_protocol_baseline_self_audit.py
```

## Patch 125 - Evidence Lab Static UI Extraction

Status: READY FOR LOCAL REVIEW

Patch 125 starts the Evidence Lab static UI extraction. It adds `pages_ui/evidence_lab_page.py` and moves stable Evidence Lab intro copy plus public-data build guidance out of `app.py`.

Boundary preserved: static UI copy extraction only. `app.py` remains the orchestrator for Evidence Lab upload widgets, build buttons, dataframe processing, public upload diagnostics, scoring, validation, downloads, receipts, session state, Evidence Lab / World Lens synchronization, and analysis behavior. No evidence processing change, no upload handling change, no dataframe logic change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no session-state change, no privacy scan change, no AI Integrity scan change, no World Lens math change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 125
tools\run_patch_checks.bat 124
tools\run_patch_checks.bat 123
python tools\run_protocol_baseline_self_audit.py
```

## Patch 126 - Final Structural Simplification Freeze

Status: READY FOR LOCAL REVIEW

Patch 126 records the corrected project posture. ALETHEIA is not in expansion mode. It is in refinement mode.

Allowed work from this point is limited to moving existing UI code into clearer files, removing duplication, consolidating repeated copy, improving documentation navigation, tightening regression tests, and locking existing behavior. The current behavior is treated as the release-candidate surface to preserve.

Boundary preserved: documentation and regression-test only. `app.py` is unchanged. No app runtime behavior change, no new module, no new scoring, no new panel, no new analysis mode, no new intelligence, no receipt schema change, no module-routing change, no session-state change, no privacy scan change, no AI Integrity scan change, no World Lens math change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 126
tools\run_patch_checks.bat 125
tools\run_patch_checks.bat 124
python tools\run_protocol_baseline_self_audit.py
```


### Patch 126 local-review stabilization note

Patch 126 also repairs stale regression expectations found during local review of Patches 119-126. The changes are test/manifest hygiene only: grouped imports are accepted, current helper signatures are recognized, privacy-scan ownership remains in the core layer, and the protocol baseline manifest is UTF-8 without BOM. No app runtime behavior change, no new scoring, no new panel, no new analysis mode, no external calls, and no authority expansion. Human review remains required.

## Patch 127 - Encoding Cleanup and Tab Icon Restore

Status: READY FOR LOCAL REVIEW

Patch 127 repairs visible UTF-8 mojibake in the public app surface after the late structural-refactor sequence. It restores tab icons and normal Unicode punctuation where broken broken emoji bytes, broken dashes, and broken bullets appeared in the app UI or public progress notes.

Boundary preserved: public UI text cleanup only. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no session-state change, no upload handling change, no download handling change, no privacy scan change, no AI Integrity scan change, no World Lens math change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final-truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 127
tools\run_patch_checks.bat 126
python tools\run_protocol_baseline_self_audit.py
```

## Patch 128 - Public UI Text Consistency Pass

Status: READY FOR LOCAL REVIEW

Patch 128 refines public UI copy after the page-extraction and encoding-cleanup sequence. It incorporates the current positioning that ALETHEIA's strength is restraint: it does not follow the normal AI-governance trend of adding more automation, more intelligence, and more institutional control.

The public pages now state more clearly that regulation is a floor, not the final measure of integrity; compliance workflows can miss capture pressure, consent erosion, hidden influence, weak appeal paths, and authority drift; and ALETHEIA asks where power is moving, who can appeal, what is hidden, and where human review is being weakened.

Boundary preserved: public UI text consistency only. This is refinement, not expansion. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no module-routing change, no session-state change, no upload handling change, no download handling change, no privacy scan change, no AI Integrity scan change, no World Lens math change, no external calls, no telemetry, no analytics, no storage or identity sync, no privacy guarantee, no certification, no enforcement, and no final-truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Validation targets:

```bat
tools\run_patch_checks.bat 128
tools\run_patch_checks.bat 127
python tools\run_protocol_baseline_self_audit.py
```

Patch 128 public wording note: the compliance mirage is a review concern, not a legal conclusion. ALETHEIA asks reviewers to look beyond paperwork toward power movement, appeal, hidden influence, and human review.

Patch 128 public wording note: regulation as a floor means compliance is not treated as the final measure of integrity; the compliance mirage remains a review concern, not a legal conclusion.

## Patch 129 — Input and Error Clarity Pass

Status: READY FOR LOCAL TESTING

Summary:
- Adds `ui/input_clarity.py` as a copy-only helper for selected input and upload messages.
- Clarifies empty AI Integrity input, empty batch artifacts, English/Dutch language-calibration limits, public-data upload requirements, and direct CSV read failures.
- Keeps this as refinement mode only: clearer user guidance, same mirror behavior.
- No scoring, verdict-routing, signal-pattern, signal-weight, receipt schema, module-routing, privacy-scan behavior, AI Integrity scan behavior, World Lens math, external-call, telemetry, analytics, storage, privacy-guarantee, certification, enforcement, or final-truth behavior changed.

Validation:
- `tools\run_patch_checks.bat 129`
- `tools\run_patch_checks.bat 128`
- `tools\run_patch_checks.bat 127`
- `python tools\run_protocol_baseline_self_audit.py`
