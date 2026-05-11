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
