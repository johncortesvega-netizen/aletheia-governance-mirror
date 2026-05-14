## Patch 118 Notes — Beginner UX Polish v2

Patch 118 polishes the beginner guide introduced in Patch 111. It adds a first-audit checklist, clearer “what this means / what this does not mean” copy, and stop-and-review prompts for high-consequence or unclear cases.

This is static UX copy and documentation only. It does not change runtime behavior, scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 117 — Refactor Stabilization Checkpoint

Status: READY FOR LOCAL REVIEW

Patch 117 adds a stabilization checkpoint after the app-shell refactor sequence through Patch 116. It documents the boundary of the refactor and adds tests to verify that `ui/app_shell.py` remains a static shell-copy helper layer while `app.py` remains the orchestrator for interactive controls, session state, module routing, scoring, receipts, downloads, and analysis behavior.

Scope: documentation and regression tests only. No runtime behavior change, no scoring, no verdict-routing, no signal-pattern or signal-weight change, no receipt schema change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 116 — App Shell Router Refactor Step 5

Status: READY FOR LOCAL TESTING

Patch 116 continues the gradual app-shell refactor by extracting the stable footer banner into `ui/app_shell.py`. The change is static shell extraction only. `app.py` remains responsible for interactive controls, session state, module routing, scoring, receipts, downloads, and analysis behavior.

Boundary preserved: no scoring, verdict-routing, signal-pattern, signal-weight, receipt schema, module-routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantee, certification, enforcement, or final-truth behavior changed. Humans keep the judgment.

# ALETHEIA Progress Database

This file tracks current project progress inside the repo so patch continuity is not dependent on chat history alone.

## Current Status

Current patch: Patch 49 — Full Test Suite / Legacy Test Cleanup.

Patch 47 is treated as passed. Patch 48 adds the v0.1 release-candidate gate: included modules, explicit exclusions, manual smoke-test steps, automated checks, and release readiness criteria.

## Current Patch Map

- Patch 33 — Baseline v0.1 + Safe Language + Eternal Baseline — passed.
- Patch 34 — Boundary Cases Matrix — passed.
- Patch 35 — Failure Classification — passed.
- Patch 36 — Patch Automation Toolkit — passed.
- Patch 36.1 — Automation Script Hotfix + Safe Check Workflow — passed.
- Patch 37 — Consent-Audit Engine — passed.
- Patch 38 — Mechanism-vs-Claim Scanner — passed.
- Patch 39 — Self-Audit Mode — passed.
- Patch 40 — Evidence Lab + Extraordinary Claim Protocol — passed.
- Patch 41 — Local Witness Receipt v2 — passed.
- Patch 42 — World Lens Simulation — passed.
- Patch 43 — Protocol Guide Consolidation — passed.
- Patch 44 — Progress Database + Patch Status Hardening — passed.
- Patch 45 — Public README + Limitations Polish — passed.
- Patch 46 — Sample Reports / Example Audits — passed.
- Patch 47 — App Navigation + Smoke Test Cleanup — passed.
- Patch 48 — Release Candidate Checklist — passed.
- Patch 49 — Full Test Suite / Legacy Test Cleanup — current.

## Current Architecture Direction

User input → optional actor-bias reduction → Mirror Check / Stress Test → Boundary Cases → Failure Classification → Consent-Audit Engine → Mechanism-vs-Claim Scanner → Self-Audit Mode → Evidence Lab / Extraordinary Claim Protocol → World Lens Simulation → Protocol Guide consolidation → sample reports / examples → repair questions → Local Witness Receipt v2 → human judgment.

## Module Map

| Module | Purpose | Authority Boundary |
|---|---|---|
| Baseline v0.1 | Defines what ALETHEIA may and may not do | Mirror only; no command authority |
| Safe Language Layer | Replaces enforcement language with review language | No leader removal, no AI decision claims |
| Eternal Baseline | Versioned ethical continuity layer | Reference layer, not a command layer |
| Boundary Cases Matrix | Stress-tests hard edge cases | Calibration for human review |
| Failure Classification | Separates Actor, Policy, Implementation, and Data Failure | Repair targeting, not blame engine |
| Consent-Audit Engine | Checks whether refusal is realistically possible | Reflects consent pressure; no legal judgment |
| Mechanism-vs-Claim Scanner | Separates value claims from real safeguards | Does not infer bad faith |
| Self-Audit Mode | Lets ALETHEIA audit its own language and assumptions | Does not prove correctness |
| Evidence Lab | Marks evidence levels and parks extraordinary claims | Does not validate spiritual authority |
| Local Witness Receipt v2 | Creates local user-held fingerprints | No ledger, no Global ID sync, no central storage |
| World Lens Simulation | Reviews possible population impact | Simulation only; no real governance mechanism |
| Protocol Guide | Explains how modules connect | Documentation only |
| Progress Database | Tracks local roadmap and patch state | Developer continuity only |
| Public Release Limits | Documents limitations, ethics, release scope, and archive caution | Explanation only; no authority |
| Sample Reports | Shows example audit, boundary case, self-audit, and receipt formats | Demonstration only; no authority |
| Legacy Test Cleanup | Separates current patch checks from older test cleanup | Developer workflow only; no governance authority |

## Patch Workflow

1. Apply patched items over the working project folder.
2. Run the current patch command, for example:

```bat
tools\run_patch_checks.bat 46
```

3. For the safe default check, run:

```bat
tools\run_checks.bat
```

4. If checks pass, continue with the next patch.

5. Return only patched or added files, not the whole app, unless recovery requires a full archive.

See `docs/patch_workflow.md` for the full workflow.

## Next-Patch Convention

When the user says `next patch`, it means the previous patch succeeded and development should continue with the next logical patch.

## Notes

Full pytest collection is not used as the default automation target until older duplicate test paths and legacy collection issues are cleaned up.

## Patch 41 Notes

Patch 41 adds Local Witness Receipt v2: document fingerprint, processed-document fingerprint, report fingerprint, receipt fingerprint, app/rubric/prompt versions, active modules, and explicit no-ledger/no-Global-ID-sync/no-central-storage/no-authority boundaries.

## Patch 42 Notes

Patch 42 adds World Lens Simulation as a non-sovereign population-impact mirror. It reviews affected groups, power gains, protection losses, basic-rights risk, minority-rights risk, ambient capture risk, appealability, exit, and repair. It uses simulated threshold signal language only and explicitly avoids real Global ID, real 9k selection, World Leader logic, automatic resets, central storage, enforcement, or governance mandates.

## Patch 43 Notes

Patch 43 consolidates the v0.1 logic from patches 33–42 into `docs/protocol_guide.md` and the app Protocol Guide. It connects the Baseline, Safe Language Layer, Eternal Baseline, Boundary Cases Matrix, Failure Classification, Consent-Audit Engine, Mechanism-vs-Claim Scanner, Self-Audit Mode, Evidence Lab, Local Witness Receipt v2, and World Lens Simulation into one user-facing operating guide. It adds no governance authority and preserves mirror-not-throne, human-review-required language.

## Patch 44 Notes

Patch 44 hardens continuity by adding `docs/patch_workflow.md`, expanding this progress database, and updating `PATCH_STATUS.md` with the current patch, check command, safe default check, and next-patch pointer. It adds no governance logic; it makes the development workflow easier to continue safely.


## Patch 45 Notes

Patch 45 adds `docs/limitations.md`, `docs/ethics.md`, and `docs/public_release_notes.md`. It polishes the README and app/about language for a public v0.1 release posture: ALETHEIA is a research and review prototype, not legal advice, political authority, religious authority, medical authority, a sovereign system, an election mechanism, or automated enforcement. It also preserves the archive caution that historical AI-flattery artifacts are development context, not founder validation.

## Patch 46 Notes

Patch 46 adds `docs/sample_reports.md` and four public-safe example artifacts under `examples/`: a sample policy audit, a sample boundary-case report, a sample self-audit, and a sample local witness receipt. These examples show report structure before users upload their own documents. They are demonstration artifacts only and do not create legal, political, religious, medical, or governance authority.

## Next Logical Patch

Patch 50 — v0.1 Release Package.


## Patch 47 Notes

Patch 47 adds `docs/app_navigation_smoke.md` and centralizes the visible navigation labels in `app.py` through `APP_NAVIGATION_LABELS`. The visible v0.1 path is Mirror Check, Stress Test, Boundary Cases, Evidence Lab, World Lens, Protocol Guide, and Why ALETHEIA. The patch adds smoke-test coverage so local checks can confirm the app navigation remains discoverable and non-authoritative after the release-hardening patches.

Patch 47 adds no governance authority, no Global ID sync, no real 9k selection, no automatic reset, no World Leader logic, no public ledger, and no spiritual validation.


## Patch 48 Notes

Patch 48 adds `docs/release_candidate_checklist.md`. It defines the v0.1 release-candidate gate: included modules, explicit out-of-scope features, safe and forbidden output language, a manual smoke-test path, automated check commands, and readiness criteria. It keeps ALETHEIA framed as a testable mirror package, not a truth claim or authority system.

Patch 48 adds no governance authority, no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no public ledger, no neural data, no memory extraction, no spiritual validation, and no automated enforcement.


## Patch 49 Notes

Patch 49 separates the current safe check workflow from legacy full-suite cleanup. The default `tools\run_checks.bat` now runs the latest patch-specific test chain and compile checks, then prints a non-blocking legacy inventory. `tools\run_full_checks.bat` remains available for explicit full-suite work, but legacy blockers are documented in `docs/legacy_test_cleanup.md` rather than allowed to break the current patch workflow.

Known legacy blockers include the nested duplicate `tests/tests/test_patch_29_hard_capture_receipt_trace.py`, the old Patch 20 batch upload test that imports `combine_witness_text_uploads`, and `tests/test_scoring_repair_questions.py`, which imports `repair_prompts_from_report`. These are cleanup candidates, not current Patch 33+ blockers.

Patch 49 adds no governance authority, no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no public ledger, no neural data, no memory extraction, no spiritual validation, and no automated enforcement.

## Next Logical Patch

Patch 50 — v0.1 Release Package.

## Patch 50 — v0.1 Release Package

Status: Current

Purpose: package ALETHEIA v0.1 as a clean public MVP without adding authority claims.

Added:

- `docs/v01_release_package.md`
- v0.1 module list
- public interpretation rule
- explicit out-of-scope list
- quickstart commands
- release readiness checklist

Boundary:

Patch 50 is packaging only. It does not activate real Global ID, real 9k selection, World Leader logic, neural data, public ledger, automatic reset, legal authority, religious authority, or automated enforcement.

Next logical patch: Patch 51 — Git Diff Workflow Setup.


## Patch 51 Notes

Patch 51 adds the optional Git Diff Workflow. Future patches may be delivered as `.diff` files when the local project is committed and clean. The workflow supports `git apply --check`, `git apply`, local status inspection through `tools\check_git_status.bat`, and local diff export through `tools\export_patch_diff.bat`.

The patched-items-only zip workflow remains valid. Git diff workflow is a developer convenience and does not create governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger, neural validation, religious validation, legal authority, or automated enforcement.

## Next Logical Patch

Patch 54 — Example Audit Runner / Demo Inputs.


## Patch 52 Notes

Patch 52 adds optional UX polish after the v0.1 release-hardening sequence. It shortens navigation descriptions, adds a first-use path, updates About / Why ALETHEIA copy, and documents the UX boundary in `docs/ux_polish.md`.

The first-use path is: Mirror Check for documents, Stress Test for scenarios, Boundary Cases for ethical edge cases, Evidence Lab for claim/source review, World Lens for non-sovereign population-impact framing, Protocol Guide for rules, and Why ALETHEIA for context.

Patch 52 adds no doctrine, no scoring authority, no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no public ledger, no neural validation, no religious validation, no legal authority, and no automated enforcement.

## Next Logical Patch

Patch 54 — Example Audit Runner / Demo Inputs.


## Patch 53 — Final v0.1 Smoke Release

Status: Current / release-smoke patch

Purpose: verify that v0.1 release materials are coherent and still framed as a reviewable governance mirror.

Added:

- `docs/final_v01_smoke_release.md`
- `tests/test_patch_53_final_v01_smoke_release.py`

Checks:

```bat
tools\run_patch_checks.bat 53
tools\run_checks.bat
```

Boundary: no new doctrine, no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no public ledger, no neural validation, no religious validation, no legal authority, and no automated enforcement.

Next logical patch: Patch 54 — Example Audit Runner / Demo Inputs.


## Patch 55 — GitHub Cleanup Package

Status: Current / ready for local verification

Purpose: prepare ALETHEIA v0.1 for public repository review without expanding authority.

Added:

- `docs/github_cleanup_package.md`
- `docs/contributing.md`
- `docs/repository_map.md`
- `tests/test_patch_55_github_cleanup.py`

Updated:

- `README.md`
- `about_page.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

Boundary: Patch 55 is documentation and repository packaging only. It adds no governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger authority, neural validation, religious validation, legal authority, or automated enforcement.

Next logical patch: Patch 56 — v0.2 Planning Document.


## Patch 56–60 — v1 Finalization Bundle

Status: Current / final v1 package

Purpose: mark ALETHEIA as v1.0 public MVP complete while preserving the mirror-not-throne boundary.

Added:

- `docs/v02_roadmap.md`
- `docs/feature_backlog.md`
- `docs/out_of_scope_future_modules.md`
- `docs/report_export_polish.md`
- `docs/manual_evidence_attachment.md`
- `docs/rubric_weighting_confidence.md`
- `docs/deployment_prep.md`
- `docs/v1_release_complete.md`
- `tests/test_patch_56_60_v1_finalization.py`

v1.0 status: finished public MVP package.

Next work: v0.2 planning, report export implementation, manual evidence attachment implementation, confidence notes, or public deployment only after human review.

Boundary: no governance authority, no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no public ledger authority, no neural validation, no religious validation, no legal authority, and no automated enforcement.

## Patch 61A — Asylum Repair Questions

Status: ready for local verification.

Adds a high-risk repair-question guard so ASYLUM / High / Malicious Leadership outputs include Silent Operator repair questions instead of an empty repair path. This remains mirror-only and human-review-only.

Check command:

```bat
tools\run_patch_checks.bat 61A
```



## Patch 61B — Malicious Leadership Metric Calibration

Status: Current / ready for local verification

Purpose: align visible metrics with malicious leadership / ASYLUM signals so hostile leadership prompts do not display perfect trust, perfect alignment, or near-zero ego without concrete safeguards.

Added:

- `docs/malicious_leadership_metric_calibration.md`
- `tests/test_patch_61b_malicious_leadership_metrics.py`

Updated:

- `protocol.py`
- `app.py`
- `README.md`
- `about_page.py`
- `PATCH_STATUS.md`

Boundary: mirror-only calibration. No governance authority, no leader removal, no AI command, no legal/political authority, no Global ID sync, no public ledger, and no automated enforcement.

Check:

```bat
tools\run_patch_checks.bat 61B
```


## Patch 61C Notes — Country-Year Available-Year Filter

Patch 61C hardens World Lens / Evidence Lab country-year selection. The Country-Year Explorer now computes available years for the selected country/ISO3 only, displays country-specific availability wording, and documents that ALETHEIA must not silently fall back to a stale previous country, global/default year, or invented country-year row.


## Patch 61D — Missing Raw Trust Display

Patch 61D clarifies World Lens trust interpretation by separating observed raw trust evidence from neutral trust-prior fallback values. Missing raw trust is displayed as `not available`, and neutral priors are labeled as `0.500 neutral default`.

Check:

```bat
tools\run_patch_checks.bat 61D
```

## Patch 61E — World Lens Value Guards

Patch 61E adds a deterministic selected-year guard for World Lens. It verifies selected-year seat totals, focus-country values, no-stale-year behavior, verdict-seat derivation, and clear trust-prior interpretation.

Check:

```bat
tools\run_patch_checks.bat 61E
```

Boundary: diagnostic only; no governance authority, no Global ID sync, no public ledger, no automatic reset, and no enforcement.


## Patch 62 — Post-61 Regression Smoke Test

Status: ready for local verification.

Patch 62 is a consolidation smoke/regression patch after the split Patch 61 calibration series. It checks that Simulation and World Lens still work together after Asylum repair questions, malicious leadership metric calibration, country-scoped available years, explicit raw-trust fallback wording, and selected-year value guards.

Files added:

- `docs/post_61_regression_smoke.md`
- `tests/test_patch_62_post_61_regression_smoke.py`

Boundary: diagnostic only; no governance authority, no Global ID sync, no public ledger, no automatic reset, and no enforcement.

Check:

```bat
tools\run_patch_checks.bat 62
```


## Patch 63 — Post-62 Release Refresh

Patch 63 records the post-62 release state in project documentation. It ties the completed Patch 61A–61E calibration series and Patch 62 smoke regression back into the public README, About page, release notes, and status files.

Current post-62 stable modules:

- Simulation repair path: ASYLUM / High-risk outputs include repair questions.
- Simulation metric calibration: malicious-leadership prompts cannot display perfect trust/alignment without safeguards.
- World Lens country-year filtering: years are selected per country with no silent fallback.
- World Lens trust interpretation: observed raw trust and neutral trust-prior fallback are visibly separate.
- World Lens value guards: selected-year seats, focus country, verdict seats, and trust-prior wording are regression-checked.

Boundary: diagnostic only, mirror-only, human-review required.

## Patch 64 — Mirror Check Batch Baseline Validation

Patch 64 records three official Mirror Check batch baselines:

- `examples/batch_questions/plain_language_questions_nl.txt`
- `examples/batch_questions/boundary_case_questions_nl.txt`
- `examples/batch_questions/world_lens_release_questions_nl.txt`

Each set contains 50 numbered audit questions. The expected batch mode is `QUESTION_PROMPT`, with `Risk: Review Tool` and `Protocol label: Audit Question / Review Tool`. Normal governance scoring should remain suppressed because these inputs are audit questions, not governance mechanisms.

Authority boundary remains unchanged: local receipt only, no public ledger, no Global ID sync, no central storage, no authority claim, and human review required.

Check:

```bat
tools\run_patch_checks.bat 64
```

## Patch 65 — Stress Test Prompting Guide + Batch Baseline

Patch 65 extends Stress Test validation after the Mirror Check batch baselines. It adds:

- `docs/stress_test_prompting_guide.md`
- `docs/stress_test_batch_baselines.md`
- `examples/batch_scenarios/stress_test_scenarios_en_v1.txt`
- an explicit opt-in Stress Test batch runner in `app.py`

Expected behavior: Simulation receipts remain local, authority-safe, human-review required, and high-risk scenarios preserve repair questions.

Boundary: diagnostic only; no governance authority, no Global ID sync, no public ledger, no central storage, no automated reset, and no enforcement.

## Patch 66 — Stress Test Risk Sensitivity Calibration

Status: Delivered

Patch 66 raises Stress Test sensitivity for subtle governance-risk scenarios. The official 50-scenario Stress Test baseline should now route to mostly THRESHOLD / Needs Safeguards, with hard capture cases still reaching ASYLUM / High. This patch does not add authority, enforcement, public ledger, Global ID sync, or central storage.

Check:

```bat
tools\run_patch_checks.bat 66
```

## Patch 67 — Stress Test Threshold Repair + Metric Softening

Patch 67 completes the second Stress Test calibration layer after Patch 66. Stress scenarios that route to `THRESHOLD / Needs Safeguards` now receive repair questions and a light metric softening guard: trust and alignment are capped below perfect values, while ego/ego-pressure receive a small review-pressure floor. This makes medium-risk results more useful without turning ALETHEIA into an authority system.

Boundary: diagnostic only; no enforcement, no automatic reset, no public ledger, no Global ID sync, no central storage, and no authority claim.

## Patch 67.1 — Dutch Stress Test Lexicon + Threshold Receipt Enforcement

Status: Ready for local verification.

Adds Dutch Stress Test risk triggers so Dutch governance scenarios with noodbevoegdheden, biometrische toegang tot basisdiensten, ontbrekende data/fallback-waarden, geen audit-trail, founder/oprichter control, forced consent, surveillance, and human-review-without-power are routed to THRESHOLD / Needs Safeguards instead of SANCTUARY.

Check command:

```bat
tools\run_patch_checks.bat 67_1
```

## Patch 67.2 — Dutch Stress Lexicon Gap Fix + App-Wide Input Scope

Patch 67.2 closes the remaining Dutch Stress Test calibration gaps discovered after Patch 67.1. The following Dutch stress patterns now route to `THRESHOLD / Needs Safeguards` rather than `SANCTUARY`:

- DAO / tokenholder voting concentration with no appeal process.
- Emergency committee bypassing normal law with no audit trail.
- Reform or transition movement removing term limits.
- Humanitarian aid prioritizing efficiency over appeal rights.
- Revolutionary leadership promising repair without independent audit trail.

The patch also adds app-wide input-language scope wording: English and Nederlands/Dutch are calibrated across the app. Other languages may be pasted as text but are not validated by the calibrated risk lexicon.

Boundary unchanged: local mirror only, no authority claim, no enforcement, no public ledger, no Global ID sync, no central storage, and human review required.

Check:

```bat
tools\run_patch_checks.bat 67_2
```

## Patch 68 — Advanced English Stress Lexicon + Asylum Metric Enforcement

Adds advanced English Stress Test calibration for predictive sentencing, biometric/identity coercion, divine-authority wallet capture, founder-keyword mirror capture, pre-emptive arrests, loyalty-to-state baseline capture, archive deletion, unaudited mirror code, and similar high-risk governance patterns. Advanced English stress scenarios route to `THRESHOLD / Needs Safeguards` or `ASYLUM / High` instead of washing into Sanctuary. Asylum metric enforcement now applies to non-malicious Asylum labels so receipts do not retain perfect trust/alignment or zero ego.

## Patch 69 — Stress Test Question Prompt Detection

Status: completed.

Finding: the Stress Test batch runner could process a formal doctrine repair-question baseline as ordinary Simulation scenarios, producing normal SANCTUARY / THRESHOLD / ASYLUM verdicts instead of recognizing the inputs as audit prompts.

Fix: Stress Test batch mode now checks whether the batch is a question set. If so, each audit / repair question is stored as a Simulation `QUESTION_PROMPT` local witness receipt with `Risk: Review Tool` and `Protocol label: Audit Question / Review Tool`.

Reminder file used by the user: `formal doctrine repair-question baseline.txt`.
Repo baseline copy: `examples/batch_questions/formal_doctrine_repair_questions_nl.txt`.

## Patch 69.1 — Stress Batch Scenario-vs-Question Detection

Status: Ready for local verification.

After Patch 69, uploaded Stress Test `.txt` scenario batches could be classified too broadly as question-prompt review tools. Patch 69.1 separates two batch types:

- Declarative scenario batches remain Simulation `USER_INPUT` and receive normal Stress Test verdicts.
- Formal audit/repair-question banks become `QUESTION_PROMPT / Review Tool` receipts with metrics suppressed.

This keeps advanced English scenario upload consistent with paste-input behavior while preserving formal doctrine question-bank handling.

Safety boundary unchanged: no authority claim, no public ledger, no Global ID sync, no central storage, and human review required.

Check: `tools\run_patch_checks.bat 69_1`


## Patch 68.1 — Asylum Label / Metric Consistency

Status: Ready for local verification.

Patch 68.1 fixes a consistency gap found in advanced English Stress Test receipts: some patterns reached `protocol_adjusted_state: ASYLUM` and `Risk: High`, but still displayed a `Needs Safeguards` label with THRESHOLD-style metrics.

New rule: if final state is ASYLUM, the label is normalized to `/ Asylum`, trust is capped at 0.80, alignment at 0.85, and ego is raised to at least 0.10. Repair questions remain present and the authority boundary stays unchanged: local receipt only, no public ledger, no Global ID sync, no central storage, and human review required.

Check: `tools\run_patch_checks.bat 68_1`

## Patch 70 — Mirror + Stress Tree Visual Calibration

Status: Ready for local verification.

Patch 70 updates the tree visual used by Mirror Check and Stress Test. It keeps scoring logic unchanged while making the UI clearer:

- Mirror Check tree: audit/review mirror with human review, evidence, accountability, safeguards, appeal, transparency, repair, basic rights, and non-coercion.
- Stress Test tree: scenario-pressure mirror with human dignity, consent, exit, appeal, time limits, independent review, evidence clarity, and basic rights.
- QUESTION_PROMPT: Review Tool Mode, not a Sanctuary/Threshold/Asylum score.
- Visual tree score is labeled separately from protocol-adjusted integrity in the receipt.

Boundary unchanged: no authority claim, no enforcement, no public ledger, no Global ID sync, no central storage, and human review required.

## Patch 70.1 — Negated Safeguard Strength Calibration

Date: 2026-05-11
Status: Ready for local verification

### Trigger

Patch 70 tree visual review showed that the tree and final ASYLUM receipt were correct for a high-risk single-ruler scenario, but the ethics diagnostics could still display positive strengths when safeguard words appeared inside negated phrases such as `no oversight` or `no public review`.

### Change

Patch 70.1 adds a narrow positive-credit negation filter in `core/ethics.py`. Positive safeguard terms near English or Dutch negation prefixes are no longer counted as transparency, accountability, fairness, or dignity strengths. Risk and grip-marker detection are not weakened.

### Verification target

`tests/test_patch_70_1_negated_safeguard_strengths.py` confirms:

- `no oversight` and `no public review` do not become strengths.
- normal positive safeguard wording still receives strength credit.
- Dutch negated safeguard wording does not become strength credit.
- Patch manifest, recovery note, status, and progress notes are present.

### Boundary

No authority expansion. ALETHEIA remains local, non-enforcing, human-review-only, and does not claim legal, political, institutional, religious, medical, or automated authority.

## Patch 71 — Batch File Repository Consolidation

Date: 2026-05-11
Status: Ready for local verification

### Trigger

After Patch 70.1, the repository still contained a mix of older batch filenames and renamed user-facing batch files. This could confuse local validation, README references, and public documentation.

### Change

Patch 71 adds `docs/batch_file_catalog.md` as the official registry for batch fixtures and adds/verifies the official batch filenames:

- `examples/batch_questions/repair_questions_v2_nl.txt`
- `examples/batch_questions/formal_doctrine_repair_questions_nl.txt`
- `examples/batch_questions/plain_language_questions_nl.txt`
- `examples/batch_questions/boundary_case_questions_nl.txt`
- `examples/batch_questions/world_lens_release_questions_nl.txt`
- `examples/batch_scenarios/stress_test_scenarios_en_v1.txt`
- `examples/batch_scenarios/stress_test_scenarios_nl_v1.txt`
- `examples/batch_scenarios/governance_language_stress_test_en.txt`

Question banks are documented as `QUESTION_PROMPT / Review Tool` fixtures with metrics suppressed. Scenario batches are documented as Stress Test / Simulation fixtures.

### Latest verified scenario distributions

- `governance_language_stress_test_en`: THRESHOLD 29 / ASYLUM 21 / SANCTUARY 0
- `stress_test_scenarios_en_v1`: THRESHOLD 46 / ASYLUM 4 / SANCTUARY 0
- `stress_test_scenarios_nl_v1`: THRESHOLD 50 / ASYLUM 0 / SANCTUARY 0

### Verification target

`tests/test_patch_71_batch_file_catalog.py` confirms official file presence, exact 50-line batch integrity, catalog references, expected distribution documentation, and README/About references to official names.

### Boundary

No scoring, receipt, tree, storage, or authority behavior changed. ALETHEIA remains a local mirror only: no authority claim, no enforcement, no public ledger, no Global ID sync, no central storage, and human review required.

## Patch 71.1 — Module Demo Label Isolation

Date: 2026-05-11
Status: Ready for local verification

### Trigger

After Patch 71, UI review showed that the Stress Test tab could display demo labels and/or a load-button label associated with Mirror Check, creating confusion about which module owned the selected demo scenario.

### Change

Patch 71.1 separates module demo libraries in `app.py`:

- `MIRROR_CHECK_DEMO_SCENARIOS` powers the Mirror Check scenario-demo dropdown.
- `STRESS_TEST_DEMO_SCENARIOS` powers the Stress Test scenario-demo dropdown.
- Stress Test now displays `Stress Test demo examples` and `Load Stress Test scenario demo`.
- Mirror Check now displays `Mirror Check scenario demo examples` and `Load Mirror Check scenario demo`.

The old `SCENARIOS` name remains as a compatibility alias to the Mirror Check demo map so older references do not break, while active module UI paths use module-specific maps.

### Verification target

`tests/test_patch_71_1_module_demo_label_isolation.py` confirms that the two demo maps exist, their titles do not overlap, Stress Test uses the Stress Test map and button label, Mirror Check uses the Mirror Check map and button label, and manifest/recovery/status/progress files are present.

### Boundary

No scoring, receipt, tree, batch-catalog, storage, or authority behavior changed. ALETHEIA remains a local mirror only: no authority claim, no enforcement, no public ledger, no Global ID sync, no central storage, and human review required.

## Patch 71.2 — Tree Canopy + Caption Visual Polish

Date: 2026-05-11
Status: Ready for local verification

### Trigger

Post-Patch 71.1 UI review showed that the tree canopy looked like disconnected circles and the explanatory caption appeared inside/over the dark tree visual instead of below it.

### Change

Patch 71.2 updates `render_pulse_tree` in `app.py`:

- Replaces the old loose circle canopy stack with a layered ellipse canopy.
- Keeps the branches visually connected to the canopy and trunk.
- Adds a small state-aware canopy sag for visual pressure only.
- Moves the explanatory caption below the SVG visual using a dedicated caption class.

### Verification target

`tests/test_patch_71_2_tree_canopy_caption_visual_polish.py` confirms that the caption renders below the SVG, the old circle stack is removed, the layered canopy exists, and Patch 71.2 remains UI-only.

### Boundary

No scoring, receipt, taxonomy, batch, demo-library, storage, or authority behavior changed. ALETHEIA remains a local mirror only: no authority claim, no enforcement, no public ledger, no Global ID sync, no central storage, and human review required.


## Patch 71.3 — Stress Test Missing-Safeguard Negation + Tree Canopy Tune

Date: 2026-05-11
Status: Ready for local verification

### Trigger

Post-Patch 71.2 UI/receipt review showed that the Stress Test demo `Algorithmic welfare triage under pressure` was rendered as SANCTUARY with near-perfect trust/alignment even though the scenario explicitly says the automated triage system lacks explainability, independent challenge, and human override. The same review also showed that the tree canopy still sat too high and felt visually disconnected from the trunk.

### Change

Patch 71.3 adds deterministic missing-safeguard negation handling:

- Detects phrases such as `lacks explainability`, `lacks independent challenge`, `lacks human override`, `without appeal`, `no independent review`, and related patterns.
- Routes these cases to `Missing Safeguard Negation / Needs Safeguards`.
- Prevents negated safeguards from being counted as positive transparency/accountability signals in the local scanner.
- Applies a bridge calibration in Stress Test scan mode to prevent perfect Sanctuary-like trust/alignment/ego metrics when explicit safeguard gaps are present.
- Tunes the explanatory tree canopy lower and more compactly so it connects visually with the trunk/branches.

### Verification target

`tests/test_patch_71_3_missing_safeguard_negation_and_tree.py` confirms that missing-safeguard negation is detected, the local scanner lowers transparency/oversight, threshold metric calibration catches the pattern, the app wires the bridge override, the tuned canopy constants are present, and manifest/recovery/status/progress files exist.

### Boundary

This patch does not make ALETHEIA an authority and does not change storage or enforcement behavior. Authority claim remains false; human review remains required; public ledger remains false; Global ID sync remains false; central storage remains false. The tree remains explanatory; local witness receipts remain canonical.

## Patch 71.4 — Missing-Safeguard Verdict Enforcement

Date: 2026-05-11

Patch 71.4 closes the remaining Stress Test gap found after Patch 71.3. The algorithmic welfare triage demo explicitly says the system lacks explainability, independent challenge, and human override. That language must not remain SANCTUARY/Low with perfect trust/alignment.

Implemented behavior:
- Missing-safeguard negation is detected in the visible Stress Test path and batch path.
- The final UI/receipt route enforces THRESHOLD / Medium with label `Missing Safeguard Negation / Needs Safeguards`.
- Trust and alignment are capped below perfect values.
- Ego, friction, trust friction, and collapse pressure receive non-zero review pressure.
- Repair questions are injected before the local witness receipt is built.

Invariant preserved:
- ALETHEIA remains a mirror, not a throne.
- No legal, political, institutional, religious, medical, or automated authority is claimed.
- Public ledger, Global ID sync, and central storage remain false.
- Dataflow remains Power -> Mirror, never Mirror -> Power.

Files:
- app.py
- protocol.py
- tests/test_patch_71_4_missing_safeguard_verdict_enforcement.py
- PATCH_71_4_MANIFEST.txt
- PATCH_71_4_RECOVERY_NOTE.md


## Patch 71.5 — Boundary Cases Missing-Safeguard Cleanup

Date: 2026-05-11

Patch 71.5 aligns the Boundary Cases tab with Patch 71.4. After missing-safeguard Stress Test scenarios were correctly routed to THRESHOLD / Needs Safeguards, the Boundary Cases templates also needed to name the same concepts so users do not see outdated or incomplete edge-case guidance.

Implemented:
- Added `Automated Triage Missing Safeguards` boundary template.
- Added `Biometric Gate Without Fallback` boundary template.
- Added `Question Prompt vs Risk State` boundary template.
- Updated report templates to name explainability, independent challenge, human override, fallback paths, public audit, and meaningful appeal.
- Updated Consent-Audit and Mechanism-vs-Claim examples to reflect missing-safeguard review language.

Invariant preserved:
- This is a UI/template cleanup only.
- No scoring logic, Stress Test routing logic, Mirror Check logic, receipt storage, tree rendering, or World Lens math changed.
- ALETHEIA remains a mirror, not a throne.
- Public ledger, Global ID sync, and central storage remain false.

Files:
- app.py
- tests/test_patch_71_5_boundary_cases_missing_safeguards_cleanup.py
- PATCH_71_5_MANIFEST.txt
- PATCH_71_5_RECOVERY_NOTE.md


## Patch 71.6 — Tree Central Glow Removal

Date: 2026-05-11

Patch 71.6 is a visual-only tree cleanup following user review of the Stress Test / Mirror Check tree. The large central glow/blob behind the canopy made the tree read like it had a big circle in the center instead of a clean layered canopy.

Implemented:
- Removed the central alignment glow ellipse from `render_pulse_tree`.
- Kept canopy leaves, trunk, branches, ground shadow, fallen leaves, caption, and state color behavior.
- Added a patch-specific regression test confirming the central glow is removed while core tree elements remain.

Invariant preserved:
- No scoring logic changed.
- No receipt logic changed.
- No Stress Test, Mirror Check, Boundary Cases, World Lens, storage, or authority-boundary logic changed.
- ALETHEIA remains a mirror, not a throne.

Files:
- app.py
- tests/test_patch_71_6_tree_central_glow_removal.py
- PATCH_71_6_MANIFEST.txt
- PATCH_71_6_RECOVERY_NOTE.md


## Patch 71.7 — Threshold Review Band Display

Date: 2026-05-11

Patch 71.7 adds user-friendly nuance inside the canonical THRESHOLD state without expanding the receipt or protocol taxonomy.

Display labels:
- Needs Repair: closer to Asylum, but still repairable.
- Needs Review: mixed or incomplete safeguards.
- Near Sanctuary: mostly stable, but not fully safe yet.

Implementation:
- Added `review_band_for_state(...)` in `app.py`.
- Stress Test result card shows the review band for THRESHOLD outputs.
- Stress Test batch summary includes a Review band column.

Invariant preserved:
- Canonical taxonomy remains ASYLUM / THRESHOLD / SANCTUARY.
- No receipt schema change.
- No scoring, verdict-routing, tree visual, Boundary Cases, World Lens, storage, or authority-boundary logic changed.

Files:
- app.py
- tests/test_patch_71_7_threshold_review_band_display.py
- PATCH_71_7_MANIFEST.txt
- PATCH_71_7_RECOVERY_NOTE.md


## Patch 71.8 — Stress Test Review Band Card Polish

Date: 2026-05-11

Patch 71.8 is a small display-only follow-up to Patch 71.7. The Stress Test result card now displays the review band on its own line so `Safety risk` and `Review band` do not wrap awkwardly.

Implemented:
- Replaced the one-line helper text with a two-line HTML helper in `app.py`.
- Added a patch-specific regression test.

Invariant preserved:
- No receipt schema change.
- No scoring logic change.
- No verdict-routing change.
- No taxonomy expansion.
- No Mirror Check, tree visual, Boundary Cases, World Lens, storage, or authority-boundary logic changed.

Files:
- app.py
- tests/test_patch_71_8_stress_review_band_card_polish.py
- PATCH_71_8_MANIFEST.txt
- PATCH_71_8_RECOVERY_NOTE.md


## Patch 71.9 — Mirror Check Review Band Display

Date: 2026-05-11

Patch 71.9 extends the display-only Threshold review band from Stress Test to Mirror Check latest-reading cards.

Implemented:
- `render_chat_judgment` now accepts optional simulation metrics.
- Mirror Check latest-reading cards pass `latest.get("sim")` into `render_chat_judgment`.
- THRESHOLD Mirror Check outputs can display Needs Repair, Needs Review, or Near Sanctuary.

Invariant preserved:
- Canonical taxonomy remains ASYLUM / THRESHOLD / SANCTUARY.
- No receipt schema change.
- No scoring logic change.
- No verdict-routing change.
- No tree visual change.
- No Stress Test, Boundary Cases, World Lens, storage, or authority-boundary logic changed.

Files:
- app.py
- tests/test_patch_71_9_mirror_check_review_band_display.py
- PATCH_71_9_MANIFEST.txt
- PATCH_71_9_RECOVERY_NOTE.md


## Patch 71.10 - Mirror Check HTML Rendering Fix

Date: 2026-05-11

Patch 71.10 fixes a Mirror Check UI regression introduced during review-band display work. The local fallback/result card was showing raw HTML code because the Streamlit Markdown block could interpret indented HTML as literal code.

Implemented:
- Added `textwrap` import.
- Built the Mirror Check judgment card as `judgment_card_html`.
- Rendered the card with `textwrap.dedent(judgment_card_html).strip()` and `unsafe_allow_html=True`.
- Precomputed the review-band detail line outside the HTML template.

Invariant preserved:
- No receipt schema change.
- No scoring logic change.
- No verdict-routing change.
- No taxonomy expansion.
- No tree visual, Stress Test, Boundary Cases, World Lens, storage, or authority-boundary logic changed.

Files:
- app.py
- tests/test_patch_71_10_mirror_check_html_rendering.py
- PATCH_71_10_MANIFEST.txt
- PATCH_71_10_RECOVERY_NOTE.md

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

Patch 73.1 keeps the layered scope clarification introduced in Patch 73 but makes the UI lighter by collapsing the Scope Layers expander by default in both the integrated Why ALETHEIA tab and standalone About page.

Implemented:
- About remains the correct place for the longer current-tool / research / vision / out-of-scope distinction.
- First-view UI no longer opens the full scope block automatically.
- The actual scope boundary copy remains intact and reviewable.
- No new disclaimers were spread across Mirror Check, Stress Test, Boundary Cases, Evidence Lab, or World Lens.

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

Patch 74 converts the public-review concern "test it on concrete inputs" into a small, reviewable example layer.

Implemented:
- Created `examples/evaluation_cases/` with eight public cases covering procurement favoritism, healthcare consent pressure, AI authority overreach, extraordinary policy claims, AI-governance capture, emergency powers without sunset clauses, visionary-language boundary tension, and police accountability review gaps.
- Created `docs/evaluation_method.md` to explain the evaluation posture: cases are review prompts, not proof of correctness.
- Created `docs/public_test_cases.md` as a compact catalog.
- Updated README with pointers to the case pack and evaluation method.
- Added `tests/test_patch_74_public_evaluation_case_pack.py` to verify case structure, risk coverage, documentation links, and patch ledger entries.

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

Status: Implemented.

Patch 75 follows directly from the Patch 74 evaluation workflow. A Mirror Check receipt showed an ASYLUM / High internal reading with uncapped trust/alignment/ego metrics. The patch keeps the reading non-authoritative but makes the metric layer consistent with the protocol-adjusted ASYLUM state.

Changes:
- Mirror Check post-judgment path applies ASYLUM metric consistency caps.
- Local witness receipts apply a defensive ASYLUM / High cap at receipt-build time.
- Protocol summary language now avoids `audit result` and `final label` wording.

Design boundary:
- This is display/receipt calibration only.
- It does not change the purpose of ALETHEIA: mirror, not throne.
- It does not add enforcement, public ledger, Global ID sync, central storage, legal authority, political authority, religious authority, medical authority, or automated authority.

Check:

```bat
tools\run_patch_checks.bat 75
```

## Patch 76 - Differentiation / Comparison Framing

Date: 2026-05-12

### Purpose

Patch 76 responds to external positioning feedback comparing ALETHEIA with enterprise AI governance platforms and technical fairness/open-source tooling. The goal is to make ALETHEIA's actual niche clearer without expanding the claim.

### Implemented

- Added `docs/comparison_positioning.md`.
- Added README section: `Differentiation from other governance tools`.
- Added collapsed About/Why ALETHEIA positioning expander in `app.py` and `about_page.py`.
- Framed ALETHEIA as qualitative governance-risk reflection: corruption-pattern signals, consent pressure, capture risk, evidence gaps, authority-overreach language, weak accountability, and repair questions for human review.
- Added explicit free/open-source commitment: ALETHEIA is free/open-source code and is intended to remain free.

### Boundary preserved

ALETHEIA remains a mirror, not a throne. Patch 76 does not claim enterprise readiness, regulatory compliance automation, legal authority, technical fairness replacement, institutional certification, enforcement, or final judgment. No scoring, routing, receipt, data, World Lens, Evidence Lab, or engine behavior changed.

### Verification

Run:

```bat
tools\run_patch_checks.bat 76
```

## Patch 77 - Capture Risk Signals Framework

Date: 2026-05-12

### Purpose

Patch 77 turns the anti-capture framing into an explicit public framework. It clarifies that ALETHEIA is anti-capture by design and capture-risk-detecting by function.

### Implemented

- Added `docs/capture_risk_framework.md`.
- Added a regulatory-capture / revolving-door evaluation case.
- Updated README and About with a collapsed capture-risk framework pointer.
- Updated `docs/public_test_cases.md` to include the new case.
- Added `tests/test_patch_77_capture_risk_framework.py`.

### Boundary preserved

Patch 77 is documentation/copy/test only. It does not add a new app module, change scoring, change verdict routing, change witness receipts, change evidence/data pipelines, or add enforcement. ALETHEIA continues to reflect capture-risk signals for human review only.

### Verification

Run:

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

Patch 79 adds a minimal Android WebView wrapper under `android_webview/` so ALETHEIA can be packaged as an APK that opens the live Streamlit app.

Implemented:
- Added an Android project named **ALETHEIA Mirror**.
- Added a WebView `MainActivity` that opens `https://aletheialive.streamlit.app/`.
- Requested only the Android `INTERNET` permission.
- Disabled cleartext traffic and file/content access inside the WebView.
- Added `docs/android_apk_wrapper.md` with build and distribution notes.
- Updated README with an Android wrapper section.
- Added `tests/test_patch_79_android_webview_wrapper.py`.

Boundary preserved:

The Android wrapper is an access shell, not a new authority layer and not a native rewrite. It does not change ALETHEIA scoring, routing, receipts, data processing, Mirror Check, Stress Test, Evidence Lab, World Lens, or authority boundaries. It does not add ads, trackers, analytics SDKs, push notifications, public ledger sync, Global ID sync, central storage, enforcement, certification, punishment, or final judgment.

Verification:

Run:

```bat
tools\run_patch_checks.bat 79
```

## Patch 80 - Signed Release APK Build Guide

Status: Ready for local verification.

Patch 80 follows Patch 79 by adding a safe signed-release path for the optional ALETHEIA Mirror Android WebView wrapper.

Key additions:
- `docs/signed_release_apk.md` explains keystore generation, local signing properties, release APK build commands, sharing cautions, and recovery steps.
- `android_webview/signing.properties.example` provides a template without storing real secrets.
- `.gitignore` excludes Android signing secrets and local release artifacts.
- `android_webview/app/build.gradle` can sign release builds when local `signing.properties` exists.

Boundary preserved:
- The wrapper remains a WebView shell for `https://aletheialive.streamlit.app/`.
- ALETHEIA remains free/open-source, anti-capture by design, capture-risk-detecting by function, and a mirror for human review.
- No local keystore or signing secret is included in the repo.
- No authority, enforcement, central storage, public ledger, Global ID sync, or native rewrite claim is introduced.

## Patch 81 - Android WebView Hello Android Guard / Troubleshooting

Status: Ready for local verification.

Patch 81 responds to the Android APK symptom where a built app opens to a default `Hello Android!` screen instead of the live ALETHEIA web app. The current wrapper source already uses a Java WebView activity, so this patch adds a hard source guard and a focused troubleshooting document to prevent wrong-folder/default-template builds.

Implemented:
- Added `docs/android_webview_troubleshooting.md` with Android Studio clean/rebuild steps and correct project-folder guidance.
- Updated README and `docs/android_apk_wrapper.md` with a direct troubleshooting pointer.
- Added `tests/test_patch_81_android_webview_hello_android_guard.py` to fail if default Android template markers are committed or if the WebView entry point stops loading `https://aletheialive.streamlit.app/`.

Boundary preserved:
- No Streamlit engine change.
- No scoring formula change.
- No verdict-routing change.
- No witness receipt schema change.
- No Evidence Lab or World Lens data model change.
- No native rewrite or offline mobile claim.
- No keystore, private key, password, or signed APK is committed.
- No new Android permissions beyond internet access.
- No ads, trackers, analytics SDKs, push notifications, public ledger sync, Global ID sync, central storage, enforcement, certification, punishment, legal authority, political authority, religious authority, or final judgment.

Verification:

```bat
tools\run_patch_checks.bat 81
```

## Patch 82 - Android App Icon / WebView Template Purge

Patch 82 follows the Android wrapper signing/troubleshooting work by adding the ALETHEIA launcher icon and hardening the wrapper source against stale default-template builds. The Android manifest now binds `@mipmap/ic_launcher` and `@mipmap/ic_launcher_round`, and the launcher resources use ALETHEIA mascot/logo-derived assets instead of the default Android icon.

Implementation notes:
- The active launcher activity remains `android_webview/app/src/main/java/net/johncortesvega/aletheia/MainActivity.java`.
- The stale `V1/Aletheia/MainActivity.kt` Android template source is neutralized so it cannot show `Hello Android!`.
- The wrapper build config is Java/WebView-only; Compose template dependencies are removed from the Groovy build path.
- Kotlin Gradle mirror files are aligned to the same package for clarity if Android Studio inspects them.

Boundary preserved: this is an Android wrapper polish and guard patch only. It changes no ALETHEIA scoring, receipts, World Lens data model, Evidence Lab logic, public ledger behavior, Global ID sync, central storage, enforcement, authority claim, or signed-key handling.

Verification: `tools\run_patch_checks.bat 82` and `tools\run_patch_checks.bat 81`.

## Patch 83 Notes

Patch 83 fixes the Android WebView wrapper Gradle configuration so Android Studio can resolve `com.android.application` during signed APK builds. The project root now declares the Android Gradle Plugin version with `apply false`, the app module applies the plugin locally, and settings files define the required plugin repositories. This is a build-configuration-only patch: no Streamlit engine change, no scoring change, no receipt change, no authority-boundary change, no new Android permissions, no keystore, and no signed APK are included.

## Patch 84 Notes

Patch 84 fixes Android release-build resource linking for the optional ALETHEIA Mirror WebView wrapper. The previous launcher-icon resource placement exposed `<adaptive-icon>` XML to Android API levels below 26 while the wrapper keeps `minSdk 23`; Android then failed `processReleaseResources`.

Implemented:
- Added `mipmap-anydpi-v26/ic_launcher.xml` and `mipmap-anydpi-v26/ic_launcher_round.xml` for API 26+ adaptive icons.
- Replaced unqualified `mipmap-anydpi/ic_launcher.xml` and `mipmap-anydpi/ic_launcher_round.xml` with non-adaptive bitmap fallback icons.
- Added `docs/android_adaptive_icon_resource_fix.md`.
- Updated the Patch 82 icon test and added `tests/test_patch_84_android_adaptive_icon_resource_fix.py`.

Boundary preserved: no Streamlit engine change, no scoring change, no receipt change, no WebView URL change, no new Android permissions, no keystore, no signed APK, no public ledger, no Global ID sync, no central storage, no enforcement, and no authority claim.

Verification:

```bat
tools\run_patch_checks.bat 84
tools\run_patch_checks.bat 82
```

## Patch 85 - AI Integrity Mirror Scaffold

Patch 85 adds **AI Integrity Mirror** to the existing ALETHEIA app as a static, local-first governance-integrity review module for AI/code artifacts.

Implemented:
- `core/ai_integrity_mirror.py` static analyzer.
- New `🤖 AI Integrity Mirror` app tab.
- Review support for AI outputs, system prompts/policies, agent workflows/specs, model-card/safety claims, and code snippets.
- Deterministic detection for final-authority claims, automated enforcement, missing review/appeal, opacity, manipulation pressure, surveillance/identity capture, exposed secrets, and unsafe code-execution markers.
- Internal taxonomy label, risk, integrity, collapse pressure, repair questions, and local witness receipt download.
- `docs/ai_integrity_mirror.md`, `PATCH_85_MANIFEST.txt`, `PATCH_85_RECOVERY_NOTE.md`, and `tests/test_patch_85_ai_integrity_mirror.py`.

Boundary preserved:
- AI Integrity Mirror is a review mirror, not a model-certification authority.
- No live model benchmarking, external calls, repository crawler, public ledger, Global ID sync, central storage, enforcement, or final safety claim.
- No scoring change to Mirror Check, Stress Test, Evidence Lab, or World Lens.

Verification:

```bat
tools\run_patch_checks.bat 85
```

## Patch 86 - AI Integrity Mirror Copy & Receipt Polish

AI Integrity Mirror does not certify AI systems, vendors, prompts, agents, codebases, or outputs.

Patch 86 follows Patch 85 by tightening the AI Integrity Mirror language around its strongest boundary: static pasted-artifact review, not model certification.

Implemented:
- Updated the AI Integrity rubric version to `ai-integrity-v0.2-static-receipt-polish`.
- Added scope, receipt, and reliance notes to analyzer output.
- Propagated non-certification copy into scan/report metadata so local receipts carry the same boundary as the UI.
- Changed UI metric language to risk reading, integrity reading, and capture pressure.
- Added a "How to read this result" expander to reduce overinterpretation of internal metrics.
- Updated `docs/ai_integrity_mirror.md`, `PATCH_86_MANIFEST.txt`, `PATCH_86_RECOVERY_NOTE.md`, and `tests/test_patch_86_ai_integrity_copy_receipt_polish.py`.

Boundary preserved:
- AI Integrity Mirror remains a review mirror for pasted artifacts only.
- No live model benchmarking, external calls, repository crawler, public ledger, Global ID sync, central storage, enforcement, certification, vendor approval, or final safety claim.
- No scoring-math or verdict-routing change to any ALETHEIA module.

Verification:

```bat
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```
## Patch 87 - AI Integrity Mirror Demo Examples and Static Smoke Coverage

Patch 87 follows the AI Integrity Mirror scaffold/copy work by improving example discipline. Demo examples now live in the analyzer module as shared metadata rather than an app-only dictionary, and tests audit every demo example directly.

Implemented:
- Added `AI_INTEGRITY_DEMO_EXAMPLES` with title, artifact kind, review focus, and text.
- Updated the app to load demo examples from the shared metadata.
- Added user-facing demo focus captions.
- Removed duplicated non-certification sentence from the app info copy.
- Added `tests/test_patch_87_ai_integrity_demo_examples.py`.

Boundary preserved:
- Static pasted-artifact review only.
- No live model benchmarking, external calls, repository crawler, certification, enforcement, public ledger, Global ID sync, central storage, scoring-math change, or verdict-routing change.

Verification:

```bat
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```


## Patch 88 - AI Integrity Mirror Signal Evidence Snippets

Patch 88 extends the Patch 85-87 AI Integrity Mirror line with clearer review evidence. Triggered findings now include a category and local evidence snippet so users can see why a signal fired without treating the reading as certification.

Implemented:
- Signal-category metadata for AI Integrity findings.
- Short evidence snippets from the pasted artifact for each triggered rule.
- Redaction of credential-like values and private-key blocks before snippets appear in UI/metadata.
- UI table columns for Category and Evidence snippet.
- `tests/test_patch_88_ai_integrity_signal_evidence.py`.

Boundary preserved:
- AI Integrity Mirror remains a static review mirror for pasted artifacts only.
- Evidence snippets support human review; they do not prove truth, safety, legality, or alignment.
- No live model benchmarking, external calls, repository crawler, public ledger, Global ID sync, central storage, enforcement, certification, vendor approval, scoring-math change, or verdict-routing change.

Verification:

```bat
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Patch 89 — Privacy Boundary Visibility

Patch 89 makes the no-built-in-data-collection boundary visible and testable. It adds privacy-by-design copy to the app surface, sidebar, AI Integrity Mirror, About page, README, and `docs/privacy_boundary.md`.

Safe claim: ALETHEIA's repository includes no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Inputs are processed in the running app session and receipts are user-held downloads.

Deployment caution: third-party hosting layers may still keep server logs, access logs, crash logs, request metadata, or operational monitoring outside ALETHEIA's app-code boundary. Public deployment claims must review the host as well as the repository.

Boundary preserved: no scoring-math change, no verdict-routing change, no AI Integrity rubric change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger, no Global ID sync, no enforcement, no certification, and no authority claim.

Verification:

```bat
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Patch 90 — AI Integrity Batch Review Scaffold

Patch 90 turns AI Integrity Mirror from single-artifact review into a small pasted-batch review workflow while keeping the same static, local-first boundary.

Implemented:
- Simple delimiter splitter for pasted batch items using lines such as `---`, `===`, or `###`.
- Batch analyzer that reuses `audit_ai_integrity_artifact` for each item rather than adding a separate scoring route.
- Batch summary with artifact count, risk-reading distribution, highest-pressure item, category counts, and redacted excerpts.
- AI Integrity tab batch-mode checkbox and review table.
- Patch-specific tests in `tests/test_patch_90_ai_integrity_batch_review.py`.

Boundary preserved: pasted artifacts only; no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger, no Global ID sync, no enforcement, no vendor ranking, no model certification, no approval, no final safety claim, and no scoring-math or verdict-routing change.

Verification:

```bat
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Patch 91 — AI Integrity Receipt Export Polish

Patch 91 makes AI Integrity Mirror receipt downloads more useful for human review while preserving the static mirror boundary.

Implemented:
- AI Integrity receipt version marker: `ai-integrity-receipt-polish-v0.5`.
- Receipt context builder for AI Integrity-specific metadata.
- Readable receipt context renderer.
- App receipt export prefix containing static review scope, privacy boundary, non-certification note, reliance boundary, finding summary, redacted evidence snippets, repair questions, and optional batch summary.
- Patch-specific tests in `tests/test_patch_91_ai_integrity_receipt_export_polish.py`.

Boundary preserved: receipt export polish only. No scoring-math change, no verdict-routing change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, no vendor ranking, no model certification, no approval, and no final safety claim.

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

## Patch 92 — AI Integrity Rubric Documentation

Patch 92 makes the AI Integrity Mirror rubric explicit without changing runtime behavior.

Implemented:
- New `docs/ai_integrity_rubric.md` documentation page.
- Reviewable table of signal categories, signal names, review questions, and current weight ranges.
- Documentation for positive review signals, evidence snippets, redaction, single/batch mode, receipt scope, privacy boundary, and out-of-scope claims.
- README and AI Integrity documentation updated to point reviewers to the rubric.
- Patch-specific regression tests in `tests/test_patch_92_ai_integrity_rubric_documentation.py`.

Boundary preserved: documentation only. No scoring-math change, no signal-pattern change, no signal-weight change, no verdict-routing change, no UI behavior change, no receipt-generation change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, no vendor ranking, no model certification, no approval, and no final safety claim.

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

## Patch 93 — AI Integrity Batch Demo Pack

Patch 93 adds a ready-to-use static demo pack for AI Integrity Mirror.

Implemented:
- `examples/ai_integrity/bounded_ai_answer.txt` for bounded, reviewable AI-answer behavior.
- `examples/ai_integrity/authority_overclaim.txt` for final-authority and certification-overclaim pressure.
- `examples/ai_integrity/opaque_agent_workflow.txt` for hidden-criteria and weak-reviewability pressure.
- `examples/ai_integrity/code_secret_example.txt` for credential-like strings and unsafe execution/network markers.
- `examples/ai_integrity/central_identity_capture_claim.txt` for Global ID, biometric tracking, central registry, continuous monitoring, and blacklist pressure.
- `examples/ai_integrity/batch_demo_v1.txt` as a separator-delimited batch-mode demo.
- `docs/ai_integrity_demo_pack.md`, README pointer, AI Integrity Mirror documentation pointer, manifest, recovery note, and patch-specific tests.

Boundary preserved: examples/docs/tests only. No analyzer scoring change, no signal-pattern change, no signal-weight change, no verdict-routing change, no UI behavior change, no receipt-generation change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, no vendor ranking, no model certification, no approval, and no final safety claim.

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

## Patch 94 — AI Integrity UI Review Table Polish

Patch 94 improves the AI Integrity Mirror result display for faster human review.

Implemented:
- Highest pressure signals now appear above the detailed review table.
- Batch review keeps compact summary cards and adds a clearer compact review table heading.
- Batch results include category grouping and collapsible item-level evidence snippets.
- Single-artifact findings are grouped by category.
- Evidence snippets are collapsed by category instead of crowding the main table.
- Repair questions are shown as prominent human-review prompts.
- Empty-state copy explicitly says no-trigger output is not a safety guarantee, approval, certification, or proof.
- Patch-specific regression tests in `tests/test_patch_94_ai_integrity_ui_review_table_polish.py`.

Boundary preserved: UI/result presentation only. No analyzer scoring change, no signal-pattern change, no signal-weight change, no verdict-routing change, no receipt-generation change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, no vendor ranking, no model certification, no approval, and no final safety claim.

Verification:

```bat
tools\run_patch_checks.bat 94
tools\run_patch_checks.bat 93
tools\run_patch_checks.bat 92
```


## Patch 95 — Code Integrity Static Scan v1

Patch 95 adds a code-specific static scan layer for pasted code artifacts.

Implemented:
- `CODE_INTEGRITY_SCAN_VERSION = code-integrity-static-scan-v0.1`.
- `scan_code_integrity_static()` for deterministic pasted-code review.
- Detection categories for exposed secrets, dangerous execution, hardcoded admin bypass, unsafe deletion, outbound network calls, telemetry/tracking, central logging / identity sync, and missing human-review gates in automated decision code.
- Redacted evidence snippets, severity counts, category counts, and review questions.
- AI Integrity Mirror display section for Code Integrity Static Scan metadata.
- Documentation in `docs/code_integrity_static_scan.md` and docs/README pointers.
- Patch-specific regression tests in `tests/test_patch_95_code_integrity_static_scan.py`.

Boundary preserved: static pasted-code scan only. No analyzer scoring change, no verdict-routing change, no code execution, no dependency audit, no repository crawler, no external calls, no live model benchmarking, no penetration test, no security guarantee, no vulnerability certification, no compliance approval, no model certification, no enforcement, no approval, and no final safety claim.

Verification:

```bat
tools\run_patch_checks.bat 95
tools\run_patch_checks.bat 94
tools\run_patch_checks.bat 93
```

## Patch 96 — Privacy Boundary Audit Panel

Patch 96 adds a static Privacy Boundary Audit Panel to AI Integrity Mirror.

Implemented:
- `PRIVACY_BOUNDARY_SCAN_VERSION = privacy-boundary-audit-v0.1`.
- `scan_privacy_boundary_static()` for deterministic pasted-artifact privacy-boundary review.
- Detection categories for analytics packages, external network call patterns, telemetry keywords, database write hints, backend endpoint hints, and local-only statement markers.
- Boundary tension indicator when local-only/no-data-collection wording appears beside analytics, network, telemetry, database, or backend evidence.
- Local-only statement and hosting caveat surfaced in the AI Integrity Mirror result view.
- Redacted evidence snippets, category counts, and privacy boundary review questions.
- Documentation in `docs/privacy_boundary_audit_panel.md` and docs/README pointers.
- Patch-specific regression tests in `tests/test_patch_96_privacy_boundary_audit_panel.py`.

Boundary preserved: static pasted-artifact review only. No analyzer scoring change, no verdict-routing change, no runtime monitoring, no host-log inspection, no dependency crawl, no repository crawler, no external calls, no live model benchmarking, no privacy guarantee, no compliance approval, no vendor audit, no hosting audit, no certification, and no proof that no data is collected.

Verification:

```bat
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
tools\run_patch_checks.bat 94
```


## Patch 97 — AI Integrity Comparison View v1

Patch 97 adds artifact-level **AI Integrity Comparison View** for AI Integrity batch results.

Implemented:
- `AI_INTEGRITY_COMPARISON_VERSION = ai-integrity-comparison-view-v0.1`.
- `build_ai_integrity_comparison()` for side-by-side comparison metadata.
- Batch UI section showing artifact count, review needed count, authority pressure, missing review, signal counts, boundary-risk comparison, category totals, and artifact-level review needed notes.
- Documentation in `docs/ai_integrity_comparison_view.md` and AI Integrity/README pointers.
- Patch-specific regression tests in `tests/test_patch_97_ai_integrity_comparison_view.py`.

Boundary preserved: static pasted-artifact comparison only. No analyzer scoring change, no signal-pattern change, no signal-weight change, no verdict-routing change, no receipt-generation change, no live model benchmarking, no external calls, no repository crawler, no storage layer, no public ledger sync, no Global ID sync, no enforcement, not model-wide certification, not a vendor ranking, and not a final truth claim.

Verification:

```bat
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
```

## Patch 98 — AI Integrity Red Team Prompt Pack v1

Patch 98 adds a static/manual red-team prompt pack for AI Integrity Mirror adoption testing.

Implemented:
- `examples/ai_integrity/red_team_prompt_pack_v1.txt` with prompt categories for authority overreach, legal/medical/political false authority, manipulation pressure, privacy extraction, surveillance/capture, false certainty, no-appeal automation, unsafe code request, refusal quality, and bounded-answer control.
- `docs/ai_integrity_red_team_prompt_pack.md` with usage workflow and boundary language.
- README and AI Integrity Mirror documentation pointers.
- Patch-specific regression tests in `tests/test_patch_98_red_team_prompt_pack.py`.

Boundary preserved: static prompt examples/docs/tests only. ALETHEIA does not run prompts, call live models, benchmark live models, rank vendors, certify models, certify code safety, guarantee truth, guarantee security, enforce decisions, publish to a public ledger, sync Global ID, create central user-input storage, or make model-wide certification claims. Outputs remain pasted artifacts for human review.

Verification:

```bat
tools\run_patch_checks.bat 98
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
```


## Patch 99 — AI Integrity Report Builder v1

Patch 99 adds a compact AI Integrity Report Builder for delimiter-separated batch results. The builder summarizes existing static artifact-level readings into an executive summary, artifact count, risk distribution, state distribution, top triggered categories, highest-pressure artifacts, selected redacted evidence snippets, repair questions, non-certification note, and privacy note.

Files touched include `core/ai_integrity_mirror.py`, `app.py`, `docs/ai_integrity_report_builder.md`, `docs/ai_integrity_mirror.md`, `README.md`, `PATCH_STATUS.md`, `PATCH_99_MANIFEST.txt`, `PATCH_99_RECOVERY_NOTE.md`, and `tests/test_patch_99_ai_integrity_report_builder.py`.

Boundary: static pasted-artifact report only. No scoring change, no verdict-routing change, no live model calls, no external calls, no repository crawl, no vendor ranking, no model-wide certification, no safety guarantee, no security guarantee, no privacy guarantee, no enforcement, and no final truth claim.

## Patch 100 — Release Stabilization / Public Adoption Package

Patch 100 marks the AI Integrity work from patches 85-99 as **ALETHEIA v1.0 AI Integrity Preview**.

Implemented:
- Public adoption guide for the AI Integrity Preview.
- Release notes for the AI Integrity Preview milestone.
- Screenshot/caption guidance that preserves non-authority language.
- README and AI Integrity docs pointers for the first-use path.
- About page copy pointing to demo files, report builder, privacy/code boundary checks, comparison view, and red-team prompt outputs.
- Patch-specific regression tests.

Boundary preserved: stabilization and public-facing polish only. No scoring change, no verdict-routing change, no live model calls, no external calls, no repository crawler, no vendor ranking, no model-wide certification, no security guarantee, no privacy guarantee, no legal/medical/political/religious authority, no enforcement, and no final truth claim.

Suggested verification:

```bat
tools\run_patch_checks.bat 100
tools\run_patch_checks.bat 99
tools\run_patch_checks.bat 98
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
```


## Patch 101 — Human-Auditable Protocol Baseline Self-Audit

Patch 101 adds a local hash-based self-audit for selected protocol, release-boundary, and AI Integrity files. It creates a human-readable way to see whether watched files match the known local baseline or require human review before release.

Implemented:
- `core/protocol_baseline_self_audit.py` with SHA-256 comparison helpers and text/JSON rendering.
- `tools/run_protocol_baseline_self_audit.py` CLI wrapper.
- `data/protocol_baseline_manifest.json` listing watched baseline files and expected hashes.
- `docs/protocol_baseline_self_audit.md` with usage and boundary language.
- `docs/go_live_privacy_review_statement.md` recording the final static privacy-boundary review statement.
- Patch-specific tests.

Boundary preserved: human-auditable review evidence only. The audit is not tamper-proof, not automated approval, not certification, not a security guarantee, not a privacy guarantee, not enforcement, and not final truth. Human review remains required before release.

Verification:

```bat
tools\run_patch_checks.bat 101
python tools\run_protocol_baseline_self_audit.py
tools\run_patch_checks.bat 100
```


## Patch 102 — Structural Improvement Entry Point

Patch 102 starts the external-review improvement path with documentation architecture rather than a risky immediate code refactor. The review advice identified a large `app.py`, rule-based signal limits, Streamlit hosting limits, contributor complexity, and local-first/no-external-call tradeoffs. Structurally, the right first move is to document the intended architecture, contributor path, and staged refactor order before changing runtime behavior.

Implemented:
- `docs/structural_improvement_entrypoint.md` with the staged strategy: boundary/contributor docs, signal transparency, privacy/hosting limits, patch-history navigation, then gradual `app.py` extraction.
- `docs/architecture.md` with plain-language module architecture and the shared-protocol-logic wording.
- `docs/new_contributor_start_here.md` with the shortest safe onboarding path.
- `CONTRIBUTING.md` with safe contribution areas, high-review areas, prohibited authority-drift directions, patch workflow, and local-first privacy note.
- README pointer to the structural path.
- Patch-specific tests for the new structural documentation and authority/privacy boundaries.
- Updated Patch 101 baseline manifest hashes for changed watched documentation files.

Boundary preserved: documentation and tests only. No scoring change, no verdict-routing change, no receipt schema change, no Streamlit behavior change, no LLM calls, No external calls, No telemetry, no central storage, no Global ID sync, no public ledger authority, no certification claim, no enforcement, and no final truth claim. Human review remains required.

Verification:

```bat
tools\run_patch_checks.bat 102
tools\run_patch_checks.bat 101
```

## Patch 103 — Signal Detection Transparency Documentation

Patch 103 documents the signal-detection posture identified in external review: ALETHEIA uses transparent rule-based and heuristic signal detection in key review paths. The patch makes this a trust asset rather than a hidden limitation.

Implemented:
- Added `docs/signal_detection.md` with the signal basis, strengths, known limits, English/Dutch calibration note, suggested receipt language, and contributor rule.
- Updated README with a public pointer to signal transparency.
- Updated `docs/architecture.md` to point to the dedicated signal-basis document.
- Updated `CONTRIBUTING.md` with signal-detection contribution boundaries.
- Added patch-specific tests in `tests/test_patch_103_signal_detection_transparency.py`.
- Updated Patch 101 baseline manifest hashes for changed watched documentation files.

Boundary preserved: documentation and tests only. No scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no Streamlit behavior change, no `app.py` refactor, no live model calls, no external calls, no telemetry, no central storage, no Global ID sync, no public ledger sync, no certification claim, no enforcement, and no final truth claim. Human review remains required.

Verification:

```bat
tools\run_patch_checks.bat 103
tools\run_patch_checks.bat 102
tools\run_patch_checks.bat 101
```



## Patch 102 — Structural Improvement Entry Point

Patch 102 started the reviewable structural path with docs-first architecture/onboarding work before any `app.py` refactor. It added contributor and architecture entry points while preserving all runtime behavior and authority boundaries.

## Patch 103 — Signal Detection Transparency Documentation

Patch 103 documented ALETHEIA's transparent rule-based and heuristic signal-detection basis. It clarified explainability/privacy strengths, English/Dutch calibration limits, and the requirement that signal outputs remain internal governance-risk readings rather than verdicts or certifications.

## Patch 104 — Boundary, Privacy, and Hosted-Use Transparency

Patch 104 adds a central public boundary statement and hosted-use caveat before larger UI or `app.py` refactors.

Implemented:
- `docs/BOUNDARY.md` for non-authority, scope, privacy, AI Integrity, footer, and Dutch-summary boundary language.
- `docs/hosting_limits.md` for Streamlit/hosted deployment caveats and local-first guidance.
- `core/boundary.py` for reusable boundary text.
- `core/privacy_panel.py` for reusable privacy/local-first panel text.
- Documentation updates in README, CONTRIBUTING, architecture, and privacy-boundary docs.
- Patch-specific regression tests.

Boundary preserved: no runtime UI wiring, no `app.py` refactor, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no live model calls, no telemetry, no analytics, no backend upload endpoint, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no security guarantee, no certification, no enforcement, and no final truth claim.

Suggested verification:

```bat
tools\run_patch_checks.bat 104
tools\run_patch_checks.bat 103
tools\run_patch_checks.bat 102
tools\run_patch_checks.bat 101
```

## Patch 105 — Patch History and Public Trust Navigation

Patch 105 responds to the external-review observation that ALETHEIA's long patch trail can feel overwhelming for new reviewers and contributors. It adds a documentation navigation layer instead of changing runtime behavior.

Implemented:
- `docs/patch_index.md` as a structured map for patch categories, structural sequence, contributor entry, and patch-file conventions.
- `docs/public_trust_package.md` as a compact review path for boundary, privacy, hosting, signal-detection, architecture, contributor, and patch-history documents.
- `examples/Trust_Package_README.md` as a quick pointer for public trust-package review.
- README, CONTRIBUTING, and architecture updates pointing to the navigation layer.
- Patch-specific tests for navigation, non-certification wording, and behavior-preserving boundaries.

Boundary preserved: documentation and tests only. No runtime behavior change, no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no Streamlit page wiring change, no `app.py` refactor, no external calls, no live model calls, no telemetry, no analytics, no backend upload endpoint, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no security guarantee, no certification, no enforcement, and no final truth claim. Human review remains required.

Suggested verification:

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

## Patch 106 — Signal Dictionary and Glossary

Patch 106 adds a reviewer-facing signal dictionary / glossary after the Patch 103 signal-detection transparency layer and the Patch 105 public-trust navigation layer.

Files added:
- `docs/SIGNAL_DICTIONARY.md`
- `tests/test_patch_106_signal_dictionary_glossary.py`
- `PATCH_106_MANIFEST.txt`
- `PATCH_106_RECOVERY_NOTE.md`

Files updated:
- `docs/signal_detection.md`
- `docs/public_trust_package.md`
- `docs/patch_index.md`
- `examples/Trust_Package_README.md`
- `CONTRIBUTING.md`
- `README.md`
- `PATCH_STATUS.md`
- `data/protocol_baseline_manifest.json`

Purpose:
- Explain signal families in reviewer-facing language.
- Clarify typical cues, false positives, and repair directions.
- Preserve the rule-based / heuristic posture as transparent and reviewable.

Boundary preserved:
- Documentation-only.
- No runtime behavior change.
- No scoring change.
- No verdict-routing change.
- No signal-pattern or signal-weight change.
- No receipt schema change.
- No Streamlit wiring or `app.py` refactor.
- No external calls, telemetry, analytics, storage, certification, enforcement, or final-truth claim.

Principle retained: ALETHEIA surfaces signals. Humans keep the judgment.


## Patch 107 — Boundary and Privacy UI Wiring

Patch 107 makes the boundary/privacy trust layer visible inside the running Streamlit app. The sidebar now renders the existing privacy/local-first expander and compact boundary footer from `core/privacy_panel.py` and `core/boundary.py`.

Scope: narrow runtime UI wiring only. No scoring change, no verdict-routing change, no signal-pattern or signal-weight change, no receipt schema change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required.


## Patch 108 — App Shell Router Refactor Step 1

Patch 108 begins the gradual app.py router/shell refactor. It extracts the stable top-of-app boundary notices into `ui/app_shell.py` and keeps `app.py` responsible for orchestration. This is the first small maintainability step after the documentation, privacy, trust, and signal-glossary foundation.

Scope: app shell extraction only. No scoring change, no verdict-routing change, no signal-pattern or signal-weight change, no receipt schema change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required.

## Patch 109 Notes — App Shell Router Refactor Step 2

Patch 109 continues the gradual app.py router/shell refactor after Patch 108. It extracts the stable sidebar identity card and sidebar context copy into `ui/app_shell.py` while keeping `app.py` as the orchestrator.

This is a shell extraction only. Interactive controls, session state, module routing, analysis calls, scoring, receipt generation, and downloads remain in `app.py`.

Boundary preserved: no scoring change, no verdict-routing change, no signal-pattern change, no signal-weight change, no receipt schema change, no external calls, no live model calls, no telemetry, no analytics, no central storage, no Global ID sync, no public ledger sync, no privacy guarantee, no certification, no enforcement, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.


App.py remains the orchestrator for behavior; Patch 109 only extracts sidebar shell copy.

## Patch 110 Notes — App Shell Router Refactor Step 3

Patch 110 continues the gradual app.py router/shell refactor after Patches 108 and 109. It extracts the stable public header and first-use note into `ui/app_shell.py` while keeping `app.py` as the orchestrator.

This is a static shell-copy extraction only. It does not touch scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior.

App.py remains the orchestrator for behavior; Patch 110 only extracts public header and first-use note copy.



## Patch 111 Notes — Beginner Try This First UX

Patch 111 starts the beginner UX layer after app-shell refactor steps 108-110. It adds `ui/beginner_guide.py`, wires a compact "Start here: try this first" guide into `app.py`, and documents the first safe path in `docs/beginner_ux.md`.

The guide points new users toward Mirror Check, a risk reading, observed reasons, repair questions, and optional local receipt download. It is static UI guidance only. It does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.


## Patch 112 Notes — Privacy Audit Panel v1

Patch 112 starts the privacy audit panel roadmap item in the current structural sequence. It extracts the Privacy Boundary Audit Panel renderer into `ui/privacy_audit_panel.py` while preserving the existing static privacy-boundary scan inside AI Integrity Mirror.

The panel reflects pasted-artifact signals such as analytics hints, external network-call patterns, telemetry keywords, database-write hints, backend endpoint hints, local-only statements, and boundary tension. It presents review questions, not guarantees.

This is a UI/rendering extraction only. It does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, compliance approval, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 113 Notes — Public Trust Package Consolidation

Patch 113 consolidates the public trust package after the boundary, signal, privacy, onboarding, patch-navigation, app-shell, beginner UX, and Privacy Audit Panel v1 sequence. It rewrites `docs/public_trust_package.md` as the central review map and adds `docs/public_review_checklist.md` for public reviewers.

The checklist covers boundary, privacy/hosting, signal basis, evidence/repair, contributor/patch, and public-trust review questions. It is not a certification checklist; unresolved items require more human review, not automatic trust or automatic rejection.

This is documentation/navigation only. It does not change runtime behavior, app.py, scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, compliance approval, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.



## Patch 114 Notes — Public Release Polish v1

Patch 114 polishes the public entry path after Patch 113. It adds `docs/public_release_polish_v1.md` and updates the README, public release notes, trust package, patch index, architecture, and trust-package README so public reviewers can begin with boundary, privacy/local-first posture, hosted-use caveats, signal basis, beginner path, public trust map, and public-review checklist.

This is documentation/release-surface polish only. It does not change app.py, runtime behavior, scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.


## Patch 115 Notes — App Shell Router Refactor Step 4

Patch 115 resumes Option A after the Patch 114 public release polish. It extracts static sidebar tuning-section headings and captions from `app.py` into `ui/app_shell.py`.

Interactive controls, session state, module routing, scoring, verdict routing, signal patterns, signal weights, receipt schemas, downloads, and analysis behavior remain in `app.py`. This patch is static shell extraction only.

Boundary preserved: no external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantee, certification, enforcement, or final-truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 119 Notes — App Shell Router Refactor Step 6

Patch 119 continues the app-shell router refactor after the Patch 117 stabilization checkpoint and Patch 118 beginner UX polish. It adds `ui/module_intro.py` and extracts one small Stress Test module intro note from `app.py`.

This is copy-only. Interactive widgets, session state, module routing, scoring, verdict routing, signal patterns, signal weights, receipt schemas, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior remain in `app.py`.

Boundary preserved: no external calls, live model calls, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 120 Notes — Module Intro Extraction Step 2

Patch 120 continues the module-intro extraction sequence. It adds two more copy-only helpers to `ui/module_intro.py`: one for the Boundary Cases calibration note and one for the Consent-Audit Engine intro.

This is copy-only. Interactive widgets, session state, module routing, scoring, verdict routing, signal patterns, signal weights, receipt schemas, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior remain in `app.py`.

Boundary preserved: no external calls, live model calls, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 121 Notes — Shared Status / Notice Cards

Patch 121 starts the shared status/notice-card layer by adding `ui/status_cards.py`. It extracts the static AI Integrity boundary caption group into `render_ai_integrity_boundary_cards`.

This is copy-only. Interactive widgets, session state, module routing, scoring, verdict routing, signal patterns, signal weights, receipt schemas, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior remain in `app.py`.

Boundary preserved: no external calls, live model calls, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 122 Notes - Refactor Stabilization Checkpoint 2

Patch 122 pauses the app-shell router refactor after Patch 119, Patch 120, and Patch 121. It adds `docs/refactor_stabilization_checkpoint_2.md` and a checkpoint test suite for helper importability, `app.py` wiring, copy-only helper boundaries, non-authoritative language, and repair-note hygiene.

This is documentation and regression testing only. Interactive widgets, session state, module routing, scoring, verdict routing, signal patterns, signal weights, receipt schemas, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior remain in `app.py`.

Boundary preserved: no external calls, live model calls, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 123 Notes - About / Public Info Page Extraction

Patch 123 starts the low-risk page extraction phase after the second refactor stabilization checkpoint. It moves the in-app `Why ALETHEIA` / About tab copy from `app.py` into `pages_ui/about_page.py`.

This is a page-level display extraction only. `app.py` still owns tab orchestration and optional header image resolution. The older root-level `about_page.py` remains in place for standalone About-page compatibility and historical tests.

Interactive widgets, session state, module routing, scoring, verdict routing, signal patterns, signal weights, receipt schemas, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior remain outside the new page helper.

Boundary preserved: no external calls, live model calls, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 124 Notes - Trust Package Page Extraction

Patch 124 continues the low-risk page extraction phase by adding `pages_ui/trust_package_page.py`. The helper exposes the public trust package review route inside the Protocol Guide tab while keeping `docs/public_trust_package.md` and `docs/public_review_checklist.md` as the source of truth.

This is a page-level display extraction only. `app.py` still owns tab orchestration, widgets, session state, module routing, scoring, receipts, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, and analysis behavior.

Boundary preserved: no external calls, live model calls, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 125 Notes - Evidence Lab Static UI Extraction

Patch 125 starts the Evidence Lab static UI extraction by adding `pages_ui/evidence_lab_page.py`. It moves stable Evidence Lab intro copy and public-data build guidance out of `app.py`.

This is static UI copy extraction only. `app.py` still owns Evidence Lab upload widgets, build buttons, dataframe processing, public upload diagnostics, scoring, validation, downloads, receipts, session state, Evidence Lab / World Lens synchronization, and analysis behavior.

Boundary preserved: no evidence processing, upload handling, dataframe logic, scoring, routing, receipt schema, session-state, privacy scan, AI Integrity scan, World Lens math, external calls, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 126 Notes - Final Structural Simplification Freeze

Patch 126 records the corrected roadmap posture. ALETHEIA is not in expansion mode. It is in refinement mode.

Allowed work is limited to moving existing UI code into clearer files, removing duplication, consolidating repeated copy, improving documentation navigation, tightening regression tests, and locking existing behavior. The current behavior is treated as the release-candidate surface to preserve.

This is documentation and regression-test only. `app.py` is not changed.

Boundary preserved: no app runtime behavior, new module, scoring, routing, panel, analysis mode, intelligence, receipt schema, session-state, privacy scan, AI Integrity scan, World Lens math, external calls, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.


## Patch 126 Local-Review Stabilization Note

During review of Patches 119-126, stale regression expectations were corrected. Patch 119 no longer requires an old exact import string after grouped module-intro imports. Patch 122 now recognizes the current app-shell helper signatures and confirms that the static privacy boundary scan remains owned by `core/ai_integrity_mirror.py`. The protocol baseline manifest was resaved as UTF-8 without BOM and refreshed to the current watched-file hashes.

This is test/manifest hygiene only. No app runtime behavior, scoring, routing, receipt schema, signal pattern, signal weight, privacy scan behavior, AI Integrity scan behavior, World Lens math, external call, telemetry, analytics, storage, identity sync, privacy guarantee, certification, enforcement, or final truth behavior changed. Human review remains required.

## Patch 127 Notes - Encoding Cleanup and Tab Icon Restore

Patch 127 repairs visible UTF-8 mojibake in the public app surface after the late structural-refactor sequence. It restores the app tab icons and normal Unicode punctuation in app-facing text and public progress notes.

This is a public UI text cleanup only. It does not add a new feature, module, panel, analysis mode, or intelligence. It only restores readable text where corrupted symbols appeared.

Boundary preserved: no scoring, routing, receipt schema, signal pattern, signal weight, session-state, upload handling, download handling, privacy scan, AI Integrity scan, World Lens math, external call, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final-truth behavior changed.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

## Patch 128 Notes - Public UI Text Consistency Pass

Patch 128 is a public copy refinement patch. It updates the extracted About, Trust Package, Evidence Lab intro, and beginner-guide copy so the app explains ALETHEIA's current stance more consistently: restraint is a strength, regulation is a floor, and the mirror asks where power moves, who can appeal, what is hidden, and where human review is weakened.

This is not expansion. It does not add a new module, panel, analysis mode, intelligence layer, scoring behavior, routing behavior, receipt schema, signal pattern, signal weight, privacy scan behavior, AI Integrity scan behavior, World Lens math, external call, telemetry, analytics, storage or identity sync, privacy guarantee, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.

Patch 128 public wording note: the compliance mirage is a review concern, not a legal conclusion. ALETHEIA asks reviewers to look beyond paperwork toward power movement, appeal, hidden influence, and human review.

Patch 128 public wording note: regulation as a floor means compliance is not treated as the final measure of integrity; the compliance mirage remains a review concern, not a legal conclusion.

## Patch 129 Notes - Input and Error Clarity Pass

Patch 129 adds a small copy-only input clarity layer. The patch centralizes selected empty-input, language-calibration, and upload/read-failure messages in `ui/input_clarity.py` and wires those helpers into `app.py` where the same input checks already existed.

Structural intent: refinement, not expansion. The patch improves the way ALETHEIA explains missing pasted artifacts, empty batch blocks, English/Dutch calibration limits, public-data upload requirements, and CSV read failures. It does not change scoring, routing, receipts, signal logic, privacy scan behavior, AI Integrity scan behavior, World Lens math, external calls, telemetry, storage, certification, enforcement, or final-truth behavior. Human review remains required.
## Patch 130 — Release Candidate Freeze

Patch 130 records ALETHEIA as being in release-candidate refinement mode after the Patch 127-129 public polish sequence. The current behavior is the surface to preserve. Future work should be limited to bug fixes, copy/readability fixes, input clarity, test hygiene, documentation navigation, and small behavior-preserving cleanup.

This is not expansion. No new modules, no new scoring, no new risk states, no live model calls, no agentic review, no enterprise workflow, no telemetry, no analytics, no storage or identity sync, no certification, no enforcement, no privacy guarantee, and no final-truth claim are introduced or planned by this freeze.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
## Patch 134 Notes - Receipt Reader Standard View v1

Current patch: Patch 134 - Receipt Reader Standard View v1.

Patch 134 implements the design from Patch 133 as a simple pasted-receipt reader. It shows native receipt values first, then a secondary Standard View band. Missing fields are shown as `Not found in pasted receipt`.

Boundary preserved: no new scoring, no recalculation of risk state, no receipt schema change, no modification to existing receipt generation, no external calls, no LLM calls, no embeddings, no database, no storage, no telemetry, no compliance certification, no authority claim, and no final truth claim. Human review remains required.

## Patch 133 Notes - Receipt Reader Standard View Design Doc

Current patch: Patch 133 - Receipt Reader Standard View Design Doc.

Patch 133 defines Receipt Reader - Standard View before implementation. Native receipt values remain the source of truth; Standard View is a secondary interoperability mapping into plain-language review bands: SANCTUARY to low review pressure, THRESHOLD to elevated review pressure, ASYLUM to high review pressure / escalation review required, and QUESTION_PROMPT to not scored / review-tool mode.

Boundary preserved: documentation/design only. No runtime Receipt Reader UI, no parser, no scoring, no receipt schema change, no new risk states, no external standards as authority, no compliance certification language, no external calls, no telemetry, no storage, and no final-truth claim. Human review remains required.

## Patch 132 Notes - Start Page Stabilization Checkpoint

Current patch: Patch 132 - Start Page Stabilization Checkpoint.

Patch 132 is a test/check/docs checkpoint for the Patch 131 Start Page / How to Start gate. It verifies that the gate remains session-state-only, uses no cookies/accounts/persistent storage, stops before the module interface until passed, and leaves the normal app interface available after `Proceed to ALETHEIA`.

Boundary preserved: no new UI feature, no new modules, no scoring, no routing, no receipt schema, no signal behavior, no Privacy Audit scan behavior change, no AI Integrity scan behavior change, no World Lens math change, no external calls, no telemetry, no analytics, no tracking, no auth, no storage, no certification, no enforcement, no privacy-guarantee claim, and no final-truth claim. Humans keep the judgment.

## Patch 131 Notes - Start Page / How to Start Gate

Current patch: Patch 131 - Start Page / How to Start Gate.

Patch 130 passed and placed ALETHEIA in release-candidate refinement mode. Patch 131 adds a calm first-entry Start Page / How to Start gate so users do not land directly inside the full module interface. The gate is session-state only: clicking `Proceed to ALETHEIA` sets `aletheia_start_gate_passed` for the current Streamlit session and reveals the existing app.

Boundary preserved: no new module tab, no user-intent router, no role selection, no wizard, no personalization, no cookies, no accounts, no persistent storage, no telemetry, no analytics, no tracking, no external calls, no local LLM calls, no embeddings, no database, no auth, no login, no scoring change, no routing change, no receipt schema change, no signal regex or signal weight change, no Privacy Audit scan behavior change, no AI Integrity scan behavior change, no World Lens math change, and no uploads or downloads behavior change. Humans keep the judgment.
