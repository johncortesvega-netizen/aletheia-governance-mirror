# ALETHEIA Patch Status

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

