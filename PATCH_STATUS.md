## Patch 215 — README / Public Positioning Upgrade

Date: 2026-07-07

Status: READY FOR LOCAL REVIEW

Patch 215 upgrades the public doorway for ALETHEIA after the regression and semantic-pressure refinement line. It improves the README with clearer public positioning, a five-minute reviewer path, short example scans, deterministic/local-first rationale, and visible current limitations. It also adds two documentation files for public positioning and demo/example use.

Changed files:
- `README.md`
- `docs/public_positioning_v1.md`
- `docs/public_demo_examples_v1.md`

Boundary notes:
- Documentation only.
- No runtime code, scanner logic, scoring, MEI7 gate, Z-axis behavior, Stress Test metrics, Evidence Lab calculations, World Lens math, receipt schema, telemetry, storage, certification, enforcement, or final-truth behavior changed.
- The modularization/refactor plan is intentionally deferred to a later patch.

Validation target:

```bat
python -m py_compile app.py
```

Manual review target:
- Confirm README still says ALETHEIA is a mirror, not a judge.
- Confirm World Lens / 9k language remains an audit-lens boundary, not a mandate claim.
- Confirm examples are framed as diagnostic patterns, not accusations or proof.

## Patch 208 — Stress Test Demo Semantic Alignment

Date: 2026-07-07

Status: READY FOR LOCAL REVIEW

Patch 208 aligns Stress Test demo scenarios with the Semantic Pressure Layer. Stress Test now preserves the resolved demo scenario body as an explicit semantic source and scans it alongside the visible editor text and processed/Invisibility Filter text. The strongest semantic-pressure signal is used for the subordinate semantic panel.

This fixes cases where a demo label or stale/processed text could cause semantic output to show SANCTUARY/NO SIGNAL while the active Stress Test scenario contains pressure language.

Scanner calibration was also extended for the current Stress Test demo suite:
- emergency powers without expiry -> THRESHOLD / weak emergency safeguards;
- biometric access to basic services without fallback -> THRESHOLD / weak or missing safeguards;
- algorithmic welfare triage lacking explainability/challenge/override -> THRESHOLD / review gap;
- public procurement with opaque scoring and limited audit/conflict path -> THRESHOLD / opaque capture pressure;
- migration queue and local resource allocation examples with visible safeguards remain low-pressure semantic readings.

Boundary notes:
- Stress Test semantic source selection and deterministic scanner calibration only.
- No Stress Test scoring, tree metrics, receipt schema, World Lens math, Evidence Lab calculations, external calls, telemetry, storage, certification, enforcement, or final-truth behavior changed.
- The Semantic Pressure Layer remains subordinate to Stress Test. It does not decide the result.

Validation target:

```bat
python -m py_compile app.py core\semantic_pressure_scanner.py
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('An automated welfare triage system reduces waiting times but lacks explainability, independent challenge, and human override during hardship cases.'))"
```

## Patch 204 — Opaque Capture Values Alignment Hotfix


## Patch 206 — Stress Test Semantic Stale-State Alignment Fix

Status: READY FOR LOCAL REVIEW

Patch 206 fixes a Stress Test semantic-panel alignment issue where a stale session-state scan could continue to show SANCTUARY/NO SIGNAL even when the current raw scenario text contains an opaque capture-power claim. Stress Test now recomputes semantic diagnostics from current raw/processed scenario text at render time and keeps the strongest semantic-pressure signal.

Boundary preserved: no scoring change, no semantic scanner lexicon or weight change, no receipt schema change, no World Lens/Evidence Lab/Mirror Check behavior change, no telemetry, no storage, no certification, no enforcement, and no final-truth claim.


Date: 2026-07-07

Status: READY FOR LOCAL REVIEW

Patch 204 re-ships the current Semantic Pressure Scanner calibration so Stress Test / Mirror Check values align with the visible high-risk reading for opaque capture claims. This fixes the case where text such as `a group of bankers have world power in secret` could still display a semantic `SANCTUARY`/no-signal panel if the local working tree was missing the Patch 197 scanner file.

Expected behavior after Patch 204:
- `a group of bankers have world power in secret` => semantic `THRESHOLD` with an `opaque_capture_claim` proximity hit and negative integrity pressure.
- `a hidden committee controls global policy` => semantic `THRESHOLD` with hidden/concentrated power language.
- `private elites secretly control public systems` => semantic `THRESHOLD` with opaque capture pressure.
- Direct safeguard language such as appeal/audit/revocation remains recognized as safeguards.

Boundary notes:
- Scanner calibration only.
- No Stress Test scoring, Mirror Check scoring, receipt schema, World Lens math, Evidence Lab calculations, external calls, telemetry, storage, certification, enforcement, or final-truth behavior changed.
- The semantic layer remains subordinate to the main module reading.

Validation target:

```bat
python -m py_compile core/semantic_pressure_scanner.py
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('a group of bankers have world power in secret'))"
```

## Patch 201 — Receipt Semantic Layer Framing and Plain-English Main View

Date: 2026-07-07

Status: READY FOR LOCAL REVIEW

Patch 201 reframes Receipt Reader semantic output from a "current semantic re-read" into a **Semantic pressure layer**. The semantic scan is now presented as one diagnostic layer inside the receipt reading rather than as a competing or replacement receipt reading.

The patch also declutters the Receipt Reader main view. The Simple English walkthrough becomes the primary visible reading, while original status/metrics, semantic layer details, layered causal chain, repair questions, diagnostics, AI/static context, World Lens internals, and native receipt values move behind opt-in expanders.

Boundary notes:
- Receipt Reader wording/layout only.
- No native receipt values, receipt schema, stored receipt meaning, semantic scanner logic, module scoring, World Lens math, Evidence Lab calculations, external calls, telemetry, storage, certification, enforcement, or final-truth behavior changed.
- Human review remains required.

Validation target:

```bat
python -m py_compile ui/receipt_reader.py
```

## Patch 200 — Simple English Receipt Walkthrough

Date: 2026-07-07

Status: READY FOR LOCAL REVIEW

Patch 200 adds a simple four-step plain-English receipt walkthrough to Receipt Reader Standard View. It translates technical receipt data into: what the document is, what the main warning/status means, which big problem areas need inspection, and what humans should check next.

The walkthrough is explanatory only. It does not rescore receipts, alter native receipt values, change the receipt schema, modify scanner logic, change module scoring/routing, or create certification, enforcement, approval, rejection, or final-truth behavior. Missing raw metrics are not inferred.

Validation target:

```bat
python -m py_compile ui/receipt_reader.py
```

## Patch 199 — Layered Causal Receipt Chain

Date: 2026-07-07

Status: READY FOR LOCAL REVIEW

Patch 199 adds a five-layer causal-chain view to Receipt Reader Standard View so uploaded receipts can be read as a transparent audit path rather than a flat list of variables.

The new layers are:
- **Layer 1 — Raw ingestion / phenomenological layer:** raw input excerpt and current invisibility-filter status.
- **Layer 2 — Linguistic and semantic pressure:** claim-to-mechanism ratio, modal pressure, proximity hits, and semantic notes from the current semantic re-read.
- **Layer 3 — Zero-point baseline / raw metrics:** raw/pre-ethics integrity, friction, collapse pressure, alignment, and ego when the uploaded receipt records them.
- **Layer 4 — Sydney Protocol gate / ethical correction:** native state, protocol label, adjusted integrity, current semantic finding, and integrity-gap explanation when raw and adjusted integrity can be compared.
- **Layer 5 — Human hand-off / boundary of code:** Z-Axis/humility-cap note and parsed silent-operator repair questions.

Boundary notes:
- Receipt Reader explanation/layout only.
- Missing raw metrics are not inferred.
- No native receipt values, receipt schema, stored receipt meaning, current semantic scanner logic, module scoring, World Lens math, Evidence Lab calculations, external calls, telemetry, storage, certification, enforcement, or final-truth behavior changed.
- Current semantic reading remains a comparison layer only. Human review remains required.

Validation target:

```bat
python -m py_compile ui/receipt_reader.py
```

## Patch 198 — Receipt Risk Wording and Repair Blocker

Date: 2026-07-07

Status: READY FOR LOCAL REVIEW

Patch 198 improves Receipt Reader wording when a current semantic re-read detects hidden/concentrated power assertions. Opaque capture-power claims are now described as structural opacity / capture-pressure review, not as coercive or command-oriented language when no coercive modality is present.

Updated surfaces:
- Receipt Reader current semantic reading now gives specific wording for `opaque_capture_claim` hits.
- Failure-mode checklist includes **Opaque capture-power claim** as a review signal.
- Receipt Reader shows a conditional repair-blocker warning when low repair capacity, multiple capture-pressure component lines, or ASYLUM + opaque capture-power findings indicate blocked repair paths.
- Batch ZIP summaries include a `Repair Blocker` column for quick triage.

Boundary notes:
- Receipt Reader explanation/copy only.
- No native receipt values, receipt schema, stored receipt meaning, current semantic scanner logic, module scoring, World Lens math, Evidence Lab calculations, external calls, telemetry, storage, certification, enforcement, or final-truth behavior changed.
- Current semantic reading remains a comparison layer only. Human review remains required.

Validation target:

```bat
python -m py_compile ui/receipt_reader.py
```

## Patch 197 — Opaque Capture Semantic Calibration

Status: READY FOR LOCAL REVIEW

Patch 197 calibrates the deterministic Semantic Pressure Scanner so hidden or concentrated power claims are no longer reported as "no semantic signal" merely because they do not use coercive command verbs. Phrases such as `a group of bankers have world power in secret`, `a hidden committee controls global policy`, `private elites secretly control public systems`, and `one unelected group holds power behind closed doors` now register as `opaque_capture_claim` relationship hits.

The intended reading is structural opacity / capture-pressure review, not coercive-language detection. These claims now route to THRESHOLD-level semantic review with a negative diagnostic integrity pressure and notes asking for evidence basis, accountable mechanism, correction path, appealability, and human review.

Scope: Semantic Pressure Scanner calibration, semantic relationship lexicon, proximity-hit categorization, and patch-hygiene only. No final module scoring, receipt schema, World Lens math, Evidence Lab calculations, external calls, telemetry, storage, certification, enforcement, or authority behavior changed. Human review remains required.

Validation targets:

```bat
python -m py_compile core/semantic_pressure_scanner.py
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('a group of bankers have world power in secret').to_dict())"
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('Any decision can be appealed, revoked, independently audited, and reviewed within 30 days.').to_dict())"
```

## Patch 195 — AI Ownership Capture Stress Guard

Status: READY FOR LOCAL REVIEW

Patch 195 fixes a Stress Test logic regression where a user-input scenario alleging AI ownership by an extremely wealthy actor, self-serving incentives, fraud/corruption ties, and reliability concerns could still render as a low-risk SANCTUARY reading with perfect trust/alignment. The local scan now treats that pattern as AI ownership/capital-capture pressure requiring human review, evidence, auditability, appeal, and governance safeguards.

Scope: Stress Test local-scan guardrail, protocol label/routing, metric caps for this pressure pattern, regression self-check/test coverage, version bump, and patch-hygiene only. No design surface, receipt schema, World Lens math, Evidence Lab calculations, external calls, storage, telemetry, certification, enforcement, or authority behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 195
python -m pytest -q tests/test_patch_195_ai_ownership_capture_stress_guard.py tests/test_patch_190_original_governance_mirror_restore.py tests/test_patch_191_mascot_asset_refresh_and_preview_palette.py tests/test_patch_192_warm_original_app_style_polish.py tests/test_patch_193_unit_preview_visual_reference_poster_refresh.py tests/test_patch_194_unit_preview_poster_opt_in_polish.py
python -m py_compile app.py protocol.py core/parser.py
```

## Patch 194 — Unit Preview Poster References Opt-In Polish

Status: READY FOR LOCAL REVIEW

Patch 194 makes the Unit Preview visual reference posters explicitly opt-in by placing the poster grid behind a collapsed expander. It also removes unnecessary replacement wording from the visible poster captions so the Preview Unit reads as calm orientation material rather than a patch-change note.

Scope: Unit Preview display/copy, version bump, and patch-hygiene only. No scoring, routing, taxonomy, receipt schema/generation, World Lens math, Evidence Lab calculations, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 194
python -m pytest -q tests/test_patch_194_unit_preview_poster_opt_in_polish.py tests/test_patch_193_unit_preview_visual_reference_poster_refresh.py
python -m py_compile app.py ui/unit_preview.py
```

## Patch 193 — Unit Preview Visual Reference Poster Refresh

Status: READY FOR LOCAL REVIEW

Patch 193 replaces the old two-file Unit Preview HTML reference previews (including the earlier pink/blue Sydney Protocol surfaces) with four packaged poster-style visual references: Global Peace Architecture, The Sovereign Master Blueprint, The Sydney Protocol: Command Dossier, and The Sydney Protocol: Architect's Checklist. The Preview Unit now shows these as a calm 2x2 visual poster grid.

Scope: Unit Preview visual-reference presentation, packaged local image assets, version bump, and patch-hygiene only. No scoring, routing, taxonomy, receipt schema/generation, World Lens math, Evidence Lab calculations, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 193
python -m pytest -q tests/test_patch_193_unit_preview_visual_reference_poster_refresh.py tests/test_patch_190_original_governance_mirror_restore.py tests/test_patch_191_mascot_asset_refresh_and_preview_palette.py tests/test_patch_192_warm_original_app_style_polish.py
python -m py_compile app.py ui/unit_preview.py
```

## Patch 192 — Warm Original App-Wide Style Polish

Status: READY FOR LOCAL REVIEW

Patch 192 extends the restored original ALETHEIA design language beyond the logo and Preview Unit. It adds app-wide warm governance-mirror styling overrides: parchment/cream backgrounds, muted green and soft red accents, warmer cards/expanders/buttons/sidebar, and non-blue receipt/reference panels. It also cleans remaining public copy that still sounded like patrol/blue framing.

Scope: CSS, visible copy, version tag, tests, and patch-hygiene only. No scoring, routing, taxonomy, receipt schema/generation, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 192
python -m pytest -q tests/test_patch_192_warm_original_app_style_polish.py tests/test_patch_191_mascot_asset_refresh_and_preview_palette.py tests/test_patch_190_original_governance_mirror_restore.py
python -m py_compile app.py pages_ui/about_page.py pages_ui/evidence_lab_page.py
```

## Patch 191 — Original Mascot Asset Refresh + Warm Preview Palette

Status: READY FOR LOCAL REVIEW

Patch 191 completes the visible rollback toward the original ALETHEIA governance-mirror design by replacing the remaining blue/officer-style mascot surfaces with the original top-right mascot derived from the approved concept image. It also warms the Unit Preview palette so the front-door surface no longer reads as blue SaaS/patrol UI.

Scope: visual assets, Preview Unit styling, version bump, and patch-hygiene only. No scoring, routing, taxonomy, receipt schema/generation, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 191
python -m pytest -q tests/test_patch_191_mascot_asset_refresh_and_preview_palette.py tests/test_patch_190_original_governance_mirror_restore.py
python -m py_compile app.py ui/unit_preview.py
```

## Patch 161 - Visual Source Card Grid + Added Reference Posters

Patch 161 replaces the tab-swapping visual source card view with a side-by-side grid of openable dropdown cards. The existing bundled HTML references remain, and four new poster-style visual references are added: Global Peace Architecture, The Sovereign Master Blueprint, The Sydney Protocol: Command Dossier, and The Sydney Protocol: Architect's Checklist.

Scope is UI/reference-surface only. No scoring, routing, receipt schema, protocol logic, or authority boundary changed. The cards remain reference material, not final authority.

# Patch 154 - Unit Preview Start Here Failure-Mode Side-by-Side Expansion

Patch 154 adds the failure-mode vocabulary directly to the Aletheia Unit Preview Start Here expander. The expander now presents a side-by-side layout: **What ALETHEIA looks for** and **Seven failure-mode review signals**. This is an in-place expansion, not a new tab. No scoring, routing, receipt schema, protocol logic, Receipt Reader logic, or World Lens math changed. Human review remains required.

## Patch 152 — Receipt Reader Failure-Mode Verbalization

Status: READY FOR LOCAL REVIEW

Patch 152 implements the expanded failure-mode verbalization as an in-place review layer, not a new tab. Receipt Reader now shows the same failure-mode review signals for uploaded receipts: authority drift, evidence inflation, flattery pressure, capture pressure, sanctification drift, false neutrality, and no-appeal automation. README, About / Why ALETHEIA, Signal Dictionary, Receipt Reader documentation, and AI audit-loop reviewer notes now carry the same boundary wording.

Boundary preserved: copy/documentation and Receipt Reader display text only. No scoring, routing, module engine, receipt schema, receipt generation, receipt hash contract, World Lens math, Evidence Lab math, AI Integrity scoring, signal regex/weights, external calls, telemetry, storage, Global ID sync, public ledger sync, certification, enforcement, approval/rejection authority, official authority, or final-truth behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 152
python tools\run_patch_checks.py 151
python tools\run_patch_checks.py 150
```

## Patch 150 — Entry Button + Boundary Copy Polish

Status: READY FOR LOCAL REVIEW

Patch 150 makes the Unit Preview `Proceed to ALETHEIA` button visually distinct with a high-contrast red primary-button treatment and readable white text. It also adds cleaner AI audit-loop proof-of-concept copy, public `What this is / is not` boundary copy in README and About / Why ALETHEIA, safer taxonomy-label language, and stronger receipt boundary wording. Patch 150 keeps suggestion 5 / expanded failure-mode verbalization for a later patch.

Boundary preserved: UI/copy/documentation and receipt text only. No scoring, routing, module engine, receipt schema, receipt hash contract, World Lens math, Evidence Lab math, AI Integrity scoring, external calls, telemetry, storage, Global ID sync, public ledger sync, certification, enforcement, approval/rejection authority, official authority, or final-truth behavior changed. Human review remains required.

Validation targets:

```bat
python -m py_compile ui\unit_preview.py core\witness.py core\ai_integrity_mirror.py pages_ui\about_page.py app.py
pytest tests\test_patch_150_ui_and_boundary_copy.py
python tools\run_protocol_baseline_self_audit.py
```

## Patch 149.4 — Unit Preview DAO Grok Comparison Intro Hotfix

Status: ready for local review. Clarifies the expanded DAO governance proof-of-concept intro so Grok-style review is named as a comparison lens / external reviewer pressure input, not as validation, certification, or a final judge. Keeps the first-page proof-of-concept mirrors collapsed in side-by-side dropdowns. No scoring, receipt, World Lens, engine, external-call, telemetry, storage, or authority behavior changed. Human review remains required.

## Patch 149.3 — Unit Preview PoC Expander Container Fix

Status: ready for local review. Corrects the Unit Preview proof-of-concept dropdown wiring so both first-page proof-of-concept mirrors render their detailed content inside their own collapsed expander containers. This fixes the AI audit-loop content leaking visibly outside the left dropdown while the DAO/Lido side remained collapsed. No scoring, receipt, World Lens, engine, external-call, telemetry, storage, or authority behavior changed. Human review remains required.

## Patch 149.2 — Unit Preview PoC Dropdown Restore Hotfix

Status: ready for local review. Restores the first-page proof-of-concept mirrors to side-by-side dropdowns while keeping the richer DAO/Lido baseline content inside the DAO dropdown. No scoring, receipt, World Lens, engine, external-call, telemetry, storage, or authority behavior changed. Human review remains required.

## Patch 149.1 — Unit Preview Proof-of-Concept Visibility Hotfix

Status: READY FOR LOCAL REVIEW

Patch 149.1 corrects the Unit Preview proof-of-concept layout so the AI audit-loop evidence and DAO/Lido governance mirror cases appear directly on the first page instead of hiding behind collapsed dropdowns. It also elaborates the DAO/Lido proof-of-concept cases with compact bullet groups for strengths, risk signals, and a Grok-comparison lens.

Boundary preserved: Unit Preview presentation and reviewer documentation only. No app scoring change, no verdict routing change, no taxonomy change, no receipt schema or receipt generation change, no signal regex or signal weight change, no World Lens math change, no AI Integrity scoring behavior change, no Privacy Audit behavior change, no Evidence Lab behavior change, no upload/download behavior change, no external calls, no telemetry, no storage, no Global ID sync, no public ledger sync, no certification, no enforcement, no approval/rejection authority, no official authority, and no final-truth behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 149
python -m py_compile ui\unit_preview.py
python tools\run_patch_checks.py 148
python tools\run_patch_checks.py 146_1
python tools\run_protocol_baseline_self_audit.py
```

## Patch 149 — Unit Preview DAO Proof-of-Concept Pairing

Status: READY FOR LOCAL REVIEW

Patch 149 puts the DAO/Lido governance proof-of-concept cases side by side with the existing AI audit-loop proof-of-concept on the Aletheia Unit Preview first page. The new DAO card summarizes four baseline locks: major DAO governance tools, the Lido Snapshot proposal-threshold case, Lido DAO meta-governance risks, and Lido Dual Governance mechanics.

Boundary preserved: Unit Preview presentation and reviewer documentation only. No app scoring change, no verdict routing change, no taxonomy change, no receipt schema or receipt generation change, no signal regex or signal weight change, no World Lens math change, no AI Integrity scoring behavior change, no Privacy Audit behavior change, no upload/download behavior change, no external calls, no telemetry, no storage, no Global ID sync, no public ledger sync, no certification, no enforcement, no approval/rejection authority, no official authority, and no final-truth behavior changed. Human review remains required.

Validation targets:

```bat
python tools
un_patch_checks.py 149
python tools
un_patch_checks.py 148
python tools
un_patch_checks.py 146_1
python tools
un_protocol_baseline_self_audit.py
```

## Patch 148 — Unit Preview AI Audit-Loop Fourth Evidence

Status: READY FOR LOCAL REVIEW

Patch 148 adds the ChatGPT concealed-flattery audit-loop evidence set to the Unit Preview proof-of-concept section and makes the AI evidence-set names larger in the display. The proof-of-concept now shows four human-reviewed evidence paths: Grok/xAI for capture and architectural-opacity pressure, Claude for evidence-boundary and mechanisms-vs-claims gaps, Gemini for sanctification drift / authority-boundary drift, and ChatGPT for concealed flattery pressure inside analytical tone.

Boundary preserved: Unit Preview evidence presentation and reviewer documentation only. No app scoring change, no verdict routing change, no taxonomy change, no receipt schema or receipt generation change, no signal regex or signal weight change, no World Lens math change, no AI Integrity scoring behavior change, no Privacy Audit behavior change, no upload/download behavior change, no external calls, no telemetry, no storage, no Global ID sync, no public ledger sync, no certification, no enforcement, no approval/rejection authority, no official authority, and no final-truth behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 148
python tools\run_patch_checks.py 146_1
python tools\run_patch_checks.py 147
python tools\run_protocol_baseline_self_audit.py
```

## Patch 147 — Root Patch Hygiene / Latest Patch Only

Status: READY FOR LOCAL REVIEW

Patch 147 establishes the standing GitHub hygiene rule: only the latest/current patch manifest and recovery note remain visible at the repository root; older patch artifacts are archived under `docs/patch_archive/` without deleting the audit trail. The archive helper now supports `--current-patch` so future updates can repeat the same pattern deliberately.

Boundary preserved: repository hygiene, documentation, and local helper-script only. No app behavior, scoring, routing, taxonomy, receipt schema/generation, signal regex/weights, World Lens math, AI Integrity behavior, Privacy Audit behavior, upload/download behavior, external calls, telemetry, storage, Global ID sync, public ledger sync, certification, enforcement, approval, rejection, legal authority, official authority, or final-truth behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 147
python tools\run_patch_checks.py 146_1
python tools\run_patch_checks.py 146
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.6 — Receipt Reader World Lens Binding Fix

Status: READY FOR LOCAL REVIEW

Patch 142.6 fixes Receipt Reader binding for World Lens receipts. World Lens evidence receipts are now parsed from their World Lens section before generic/local-witness fallback, so embedded Simulation/Mirror Check fallback lines cannot overwrite the module source or protocol label. Batch ZIP inspection continues to use actual receipt files rather than batch index files and prefers JSON over duplicate TXT receipt pairs.

Boundary preserved: parser/Standard View display only. No scoring, verdict routing, taxonomy, receipt schema, receipt generation, signal regex/weights, World Lens math, Stress Test scoring/tree logic, AI Integrity scan behavior, Privacy Audit scan behavior, external calls, live model calls, embeddings, telemetry, analytics, storage, Global ID sync, public ledger sync, certification, enforcement, approval, rejection, legal authority, official authority, privacy guarantee, or final-truth behavior changed. Human review remains required.

## Patch 137 - Validation Alignment After Unit Preview

Status: READY FOR LOCAL REVIEW

Patch 137 aligns older Patch 131/132 validation with the current Patch 135/136 Aletheia Unit Preview implementation. The older tests now verify the actual invariant — a session-state-only pre-app gate before modules — instead of requiring the original exact `ui.start_page` import after Unit Preview superseded the start page implementation.

Boundary preserved: test/check/docs patch only. No runtime behavior change, no scoring change, no verdict routing change, no taxonomy change, no receipt schema or receipt generation change, no signal regex or signal weight change, no AI Integrity scan behavior change, no Privacy Audit scan behavior change, no World Lens math change, no uploads/downloads or batch behavior change, no external calls, no telemetry, no analytics, no storage or identity sync, no certification, no enforcement, no privacy guarantee, and no final-truth behavior changed. Humans keep the judgment.

Validation targets:

```bat
python tools\run_patch_checks.py 137
python tools\run_patch_checks.py 136
python tools\run_patch_checks.py 135
python tools\run_patch_checks.py 134
python tools\run_patch_checks.py 133
python tools\run_patch_checks.py 132
python tools\run_patch_checks.py 131
python tools\run_protocol_baseline_self_audit.py
```

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
- Frames rule-based detection as explainable, local-first, and reviewable while clearly naming limits around nuance, irony, coded language, cultural context, and languages outside the English-first review scope.
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

Closes five remaining Dutch Stress Test false-SANCTUARY patterns. Current public copy clarifies that Dutch/Nederlands examples are batch-test fixtures, not a general app-wide language-compatibility claim. This patch remains diagnostic only: no enforcement, no authority claim, no Global ID sync, no public ledger, and no central storage.

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

Patch 103 documents ALETHEIA's transparent rule-based and heuristic signal-detection posture, including English-first language-scope limits and human-review requirements.

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
- Clarifies empty AI Integrity input, empty batch artifacts, English-first language-scope limits, public-data upload requirements, and direct CSV read failures.
- Keeps this as refinement mode only: clearer user guidance, same mirror behavior.
- No scoring, verdict-routing, signal-pattern, signal-weight, receipt schema, module-routing, privacy-scan behavior, AI Integrity scan behavior, World Lens math, external-call, telemetry, analytics, storage, privacy-guarantee, certification, enforcement, or final-truth behavior changed.

Validation:
- `tools\run_patch_checks.bat 129`
- `tools\run_patch_checks.bat 128`
- `tools\run_patch_checks.bat 127`
- `python tools\run_protocol_baseline_self_audit.py`
## Patch 136 - Aletheia Unit Preview Stabilization

Status: READY FOR LOCAL REVIEW

Patch 136 stabilizes the Patch 135 Aletheia Unit Preview with checkpoint documentation and regression tests. It confirms the preview remains a front-door suggestion layer only, uses the session key `aletheia_unit_preview_passed`, stops before normal module tabs until passed, and leaves the normal app interface available after the gate passes.

Boundary preserved: test/check/docs patch only. No new UI feature, no new modules, no scoring changes, no verdict routing changes, no receipt schema or receipt generation changes, no signal regex or signal weight changes, no AI Integrity scan behavior change, no Privacy Audit scan behavior change, no World Lens math change, no uploads/downloads or batch behavior change, no external calls, no telemetry, no analytics, no tracking, no cookies, no accounts, no persistent storage, no database, no Global ID sync, no public ledger sync, no certification, no enforcement, no final-truth claim, no approval/rejection claim, and no privacy-guarantee claim. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 136
python tools\run_patch_checks.py 135
python tools\run_patch_checks.py 134
python tools\run_protocol_baseline_self_audit.py
```

## Patch 135 - Aletheia Unit Preview v1

Status: READY FOR LOCAL REVIEW

Patch 135 adds Aletheia Unit Preview as a small front-door preview before the full app appears. Users may paste a short text, question, scenario, or receipt and receive a transparent `Suggested path` before entering ALETHEIA. The suggestion is not a decision, and users can still choose any module after entering the app.

Boundary preserved: refinement only. No chatbot, no LLM calls, no embeddings, no agentic routing, no automatic approval or rejection, no certification, no compliance finding, no legal/medical/political/institutional authority claim, no telemetry, no analytics, no accounts, no persistent user profiles, no database, no Global ID sync, no public ledger sync, no new scoring engine, no new risk states, no final-truth claim, and no privacy guarantee. No scoring, verdict routing, taxonomy, SANCTUARY / THRESHOLD / ASYLUM logic, QUESTION_PROMPT logic, receipt schema, receipt generation, signal regex, signal weight, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, uploads/download behavior, batch behavior, data storage, or external-call behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 135
python tools\run_patch_checks.py 134
python tools\run_patch_checks.py 133
python tools\run_protocol_baseline_self_audit.py
```

## Patch 134 - Receipt Reader Standard View v1

Status: READY FOR LOCAL REVIEW

Patch 134 adds a simple Receipt Reader - Standard View. Users can paste an ALETHEIA receipt and see native receipt values, a secondary plain-language review band, human-review guidance, a non-certification note, and parsing limits. Missing fields are shown as `Not found in pasted receipt`.

Boundary preserved: the reader explains pasted receipts only. No new scoring, no risk-state recalculation, no receipt schema change, no existing receipt generation change, no external calls, no LLM calls, no embeddings, no database, no storage, no telemetry, no compliance certification, no legal/medical/political/institutional authority claim, and no final truth claim. It does not rescore, certify, approve, reject, enforce, or override the original receipt. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 134
python tools\run_patch_checks.py 133
python tools\run_patch_checks.py 132
python tools\run_protocol_baseline_self_audit.py
```

## Patch 133 - Receipt Reader Standard View Design Doc

Status: READY FOR LOCAL REVIEW

Patch 133 defines Receipt Reader - Standard View as a documentation/design-only step. The design maps native ALETHEIA receipt values into plain-language review bands for human and interoperability review, while preserving native receipt values as the source of truth.

Boundary preserved: documentation/design only. No runtime Receipt Reader UI, no parser, no scoring change, no receipt schema change, no new risk states, no external standards as authority, no compliance certification language, no external calls, no telemetry, no storage, and no final-truth claim. The Receipt Reader explains and maps receipts; it does not rescore, certify, approve, reject, override, enforce, or decide. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 133
python tools\run_patch_checks.py 132
python tools\run_patch_checks.py 131
python tools\run_protocol_baseline_self_audit.py
```

## Patch 132 - Start Page Stabilization Checkpoint

Status: READY FOR LOCAL REVIEW

Patch 132 stabilizes the Patch 131 Start Page / How to Start gate with checkpoint documentation and regression tests. It confirms the gate is session-state-only, stops before module tabs when not passed, and leaves the normal module interface available after `Proceed to ALETHEIA`.

Boundary preserved: test/check/docs patch only. No new UI feature, no new module, no scoring change, no routing change, no receipt schema change, no signal change, no Privacy Audit scan behavior change, no AI Integrity scan behavior change, no World Lens math change, no external calls, no telemetry, no analytics, no tracking, no cookies, no accounts, no auth, no persistent storage, no certification, no enforcement, no privacy-guarantee claim, and no final-truth claim. Humans keep the judgment.

Validation targets:

```bat
python tools\run_patch_checks.py 132
python tools\run_patch_checks.py 131
python tools\run_patch_checks.py 130
python tools\run_protocol_baseline_self_audit.py
```

## Patch 131 - Start Page / How to Start Gate

Status: READY FOR LOCAL REVIEW

Patch 131 adds a calm Start Page / How to Start gate before the full ALETHEIA module interface renders. It is a release-candidate refinement for readability and boundary clarity: first launch shows the start page, and clicking `Proceed to ALETHEIA` sets a session-state key so the normal app appears for that Streamlit session.

Boundary preserved: no new module tab, no user-intent router, no role selection, no wizard, no personalization, no cookies, no accounts, no persistent storage, no telemetry, no analytics, no tracking, no external calls, no local LLM calls, no embeddings, no database, no auth, no login, no scoring change, no routing change, no receipt schema change, no signal regex or signal weight change, no Privacy Audit scan behavior change, no AI Integrity scan behavior change, no World Lens math change, no uploads or downloads behavior change, no certifying claim, no enforcement claim, no approval/rejection claim, no privacy-guarantee claim, and no final-truth claim. Humans keep the judgment.

Validation targets:

```bat
python tools\run_patch_checks.py 131
python tools\run_patch_checks.py 130
python tools\run_patch_checks.py 129
python tools\run_protocol_baseline_self_audit.py
```

## Patch 138 — Single Unit Preview Entry Hotfix

Status: Ready for local review.

Patch 138 keeps Aletheia Unit Preview as the single active pre-app gate and retires the old Start Page as an active UI path. The legacy helper now delegates to Unit Preview so stale imports cannot revive the old page. No runtime analysis behavior, scoring, routing, receipts, signals, privacy scan behavior, AI Integrity behavior, World Lens math, external calls, telemetry, storage, certification, enforcement, privacy guarantee, or final-truth behavior changed.

## Patch 139 - Unit Preview Header Entry Hotfix

Status: Ready for local review.

Patch 139 keeps Aletheia Unit Preview as the single pre-module hook, but moves the active gate so it renders after the public ALETHEIA header and styling. This removes the visible plain first-screen effect while preserving the hook before the full modules.

No scoring, verdict routing, taxonomy, receipt schema, signal behavior, AI Integrity behavior, Privacy Audit behavior, World Lens math, upload/download behavior, external calls, telemetry, storage, certification, enforcement, privacy guarantee, or final-truth behavior changed.

## Patch 140 - Unit Preview Orientation Cleanup

Status: READY FOR LOCAL REVIEW

Patch 140 keeps Aletheia Unit Preview as the hook and moves beginner orientation out of the full app work surface. The `How to use this` note and `Start here: try this first` checklist now live on Unit Preview, together with six short examples for Mirror Check, Stress Test, Boundary Cases, AI Integrity Mirror, Evidence Lab, and World Lens.

Receipt Reader - Standard View remains available, but it is no longer a main module tab. It is exposed as a support utility near the footer after the module work surface.

Boundary preserved: no scoring, routing, taxonomy, receipt schema, receipt generation, signal behavior, AI Integrity behavior, Privacy Audit behavior, World Lens math, upload/download behavior, external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 140
python tools\run_patch_checks.py 139
python tools\run_patch_checks.py 138
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.4 - Receipt Reader Narrative Standard View Output

Status: READY FOR LOCAL REVIEW

Patch 142.4 reformats Receipt Reader output into a compact narrative Standard View with System Status, Native State, Review Pressure, Protocol Label, Module Source, Performance & Risk Metrics, Core Logic, Summary for the Reader, and repair questions. It keeps native uploaded receipt values first and does not infer missing values.

Receipt Reader remains upload-only and explanatory. Batch ZIP receipt exports may be summarized as uploaded receipts only; the reader does not rescore, merge verdicts, regenerate receipts, or alter any original receipt.

Boundary preserved: no scoring, verdict routing, taxonomy, receipt schema, receipt generation, signal behavior, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, external calls, live model calls, embeddings, telemetry, analytics, database/storage, Global ID sync, public ledger sync, certification, enforcement, official-authority, privacy-guarantee, security-guarantee, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 142_4
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.7 - Receipt Reader World Lens ZIP Selection Fix

Status: READY FOR LOCAL REVIEW

Patch 142.7 fixes Receipt Reader ZIP selection for World Lens exports. The batch/ZIP reader now treats `*_summary.json`, `*_summary.txt`, `*_index.json`, and index-style files as summary/index artifacts rather than inspectable receipts. The inspect panel uses the actual World Lens receipt document, such as `aletheia_world_lens_receipt_2024.md`, so native World Lens fields and weighted metrics populate from the real receipt body.

Boundary preserved: upload-only Receipt Reader display/parsing only. No World Lens math, scoring, verdict routing, taxonomy, receipt schema, receipt generation, signal behavior, AI Integrity behavior, Privacy Audit behavior, Stress Test behavior, external calls, live model calls, embeddings, telemetry, analytics, database/storage, Global ID sync, public ledger sync, certification, enforcement, approval/rejection, privacy guarantee, security guarantee, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 142_7
python tools\run_patch_checks.py 142_6
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.8 - Receipt Reader World Lens Evidence Bundle Reader

Status: READY FOR LOCAL REVIEW

Patch 142.8 changes World Lens ZIP handling from a generic batch receipt summary into a World Lens evidence bundle reader. The uploaded `.md` World Lens receipt remains the native inspected receipt. Companion `_summary.json` files are treated as structured metadata, and CSV files are shown as supporting evidence tables rather than counted as additional receipts.

The reader now preserves the full World Lens bundle more readably: selected-year metadata, weighted metrics, evidence table inventory, CSV previews, and the native receipt Standard View are kept separate. Summary and CSV files do not create a new state, verdict, or receipt.

Boundary preserved: Receipt Reader display/parsing only. No World Lens math, scoring, verdict routing, taxonomy, receipt schema, receipt generation, signal behavior, AI Integrity behavior, Privacy Audit behavior, Stress Test scoring behavior, external calls, live model calls, embeddings, telemetry, analytics, database/storage, Global ID sync, public ledger sync, certification, approval, rejection, enforcement, official-authority, privacy-guarantee, security-guarantee, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 142_8
python tools\run_patch_checks.py 142_7
python tools\run_patch_checks.py 142_6
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.9 - Receipt Reader Batch Per-Receipt Summary

Status: READY FOR LOCAL REVIEW

Patch 142.9 improves normal batch ZIP uploads in Receipt Reader. Instead of only showing the batch distribution and the first receipt, the reader now renders a compact Receipt Index with one row per uploaded receipt: file, module, native state, review pressure, protocol label, key metrics, and repair-question count. A selectable inspection control lets the user inspect any receipt in the uploaded batch without displaying all full receipts at once.

Boundary preserved: Receipt Reader display/parsing only. No scoring, verdict routing, taxonomy, receipt schema, receipt generation, signal behavior, World Lens math, AI Integrity behavior, Privacy Audit behavior, Stress Test scoring behavior, external calls, live model calls, embeddings, telemetry, analytics, database/storage, Global ID sync, public ledger sync, certification, approval, rejection, enforcement, official-authority, privacy-guarantee, security-guarantee, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 142_9
python tools\run_patch_checks.py 142_8
python tools\run_patch_checks.py 142_7
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.10 - Receipt Reader QUESTION_PROMPT Display Polish

Status: READY FOR LOCAL REVIEW

Patch 142.10 polishes Receipt Reader display behavior for QUESTION_PROMPT receipts. QUESTION_PROMPT is a review-tool mode, not a scored scenario, so selected detail views now explain that scored metrics are intentionally not applicable instead of showing repeated “Not found in uploaded receipt” rows. Normal batch ZIP Receipt Index rows also mark QUESTION_PROMPT Integrity, Collapse, and Trust Index as `Not applicable` and use shorter columns (`Collapse`, `Repairs`) for readability.

Boundary preserved: Receipt Reader presentation/parsing only. No scoring, verdict routing, taxonomy, QUESTION_PROMPT logic, receipt schema, receipt generation, signal behavior, World Lens math, AI Integrity behavior, Privacy Audit behavior, Stress Test scoring behavior, external calls, live model calls, embeddings, telemetry, analytics, database/storage, Global ID sync, public ledger sync, certification, approval, rejection, enforcement, official-authority, privacy-guarantee, security-guarantee, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 142_10
python tools\run_patch_checks.py 142_9
python tools\run_patch_checks.py 142_8
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.11 - Receipt Reader World Lens Evidence Bundle Layout Polish

Status: READY FOR LOCAL REVIEW

Patch 142.11 polishes the World Lens Evidence Bundle reader. The native World Lens receipt now renders first as the readable front page, and supporting CSV evidence tables appear below it. CSV inventory rows use compact descriptions and curated preview-field labels instead of dumping every raw column inline. CSV previews show readable selected columns by default, while raw uploaded table previews remain available behind an advanced expander.

Boundary preserved: Receipt Reader presentation only. No World Lens math, scoring, verdict routing, taxonomy, receipt schema, receipt generation, AI Integrity behavior, Privacy Audit behavior, Mirror Check behavior, Stress Test scoring behavior, external calls, live model calls, embeddings, telemetry, analytics, storage, Global ID sync, public ledger sync, certification, approval, rejection, enforcement, official-authority, privacy-guarantee, security-guarantee, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 142_11
python tools\run_patch_checks.py 142_10
python tools\run_patch_checks.py 142_8
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.12 - Receipt Reader Standard View Copy Polish

Status: READY FOR LOCAL REVIEW

Patch 142.12 polishes Receipt Reader Standard View labels and interpretations after the module-specific receipt reader stabilization sequence. Mirror Check receipts now use bounded receipt-reading language instead of operational reliability language. Stress Test receipts use a scenario-specific state heading and Collapse Pressure display label. World Lens evidence receipts use Evidence View language and shorter curated CSV preview labels.

Boundary preserved: Receipt Reader presentation/copy only. No parsing behavior required for scoring, no scoring changes, no verdict routing changes, no taxonomy changes, no QUESTION_PROMPT logic changes, no receipt schema or generation changes, no World Lens math changes, no AI Integrity/Privacy Audit/Stress Test behavior changes, no external calls, no live model calls, no embeddings, no telemetry, no analytics, no storage, no Global ID sync, no public ledger sync, no certification, enforcement, official-authority, privacy-guarantee, security-guarantee, or final-truth claim.

Validation targets:

```bat
python tools\run_patch_checks.py 142_12
python tools\run_patch_checks.py 142_11
python tools\run_patch_checks.py 142_10
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.13 - AI Integrity Single Artifact Result Focus

Status: READY FOR LOCAL REVIEW

Patch 142.13 simplifies the visible AI Integrity V1 workflow. The active UI now treats AI Integrity as a single pasted-artifact review: paste one AI output, system prompt, policy, workflow description, model-card excerpt, or code snippet and run one static review. The visible batch-review checkbox and split-artifact instructions are removed from the V1 screen.

The result view now foregrounds the actual AI Integrity reading: a Triggered signals count appears with the main reading cards, Highest pressure signals and triggered-signal categories appear before optional static boundary checks, and repair questions remain near the main review result. Privacy Boundary Audit and Code Integrity Static Scan are kept as optional collapsed checks when they have no detections, so empty secondary panels no longer dominate the result page.

Boundary preserved: UI/result presentation only. No AI Integrity scoring, signal regex/weight, receipt schema/generation, Privacy Audit behavior, Code Integrity behavior, Mirror Check behavior, Stress Test behavior, World Lens math, Receipt Reader behavior, external calls, live model calls, embeddings, telemetry, analytics, storage, Global ID sync, public ledger sync, certification, approval, enforcement, legal authority, official authority, security guarantee, privacy guarantee, model-safety proof, or final-truth claim changed.

Validation targets:

```bat
python tools\run_patch_checks.py 142_13
python tools\run_patch_checks.py 142_12
python tools\run_patch_checks.py 142_11
python tools\run_patch_checks.py 142_10
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.15 - Receipt Reader Verbal Micro-Polish Across Receipts

Status: READY FOR LOCAL REVIEW

Patch 142.15 polishes the Receipt Reader verbal Standard View across supported receipt families. It adds explicit state definitions, warmer “The mirror reflects...” opening briefs, verbal metric observation cards, a Native receipt values expander for exact uploaded values, a Reader Brief section, and Human-review questions framing.

Boundary preserved: Receipt Reader presentation/copy only. No scoring, verdict routing, taxonomy, QUESTION_PROMPT logic, receipt schema, receipt generation, signal regex/weight, AI Integrity scan behavior, Privacy Audit behavior, Stress Test scoring/tree behavior, World Lens math, upload/download behavior, external calls, live model calls, embeddings, telemetry, analytics, storage, Global ID sync, public ledger sync, certification, approval, rejection, enforcement, official-authority, privacy-guarantee, security-guarantee, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 142_15
python tools\run_patch_checks.py 142_13
python tools\run_patch_checks.py 142_12
python tools\run_patch_checks.py 142_11
python tools\run_patch_checks.py 142_10
python tools\run_protocol_baseline_self_audit.py
```

## Patch 142.16 - Boundary Cases Navigation Placement Polish

Status: READY FOR LOCAL REVIEW

Patch 142.16 moves Boundary Cases behind World Lens in the main module row. The primary work surfaces now appear first: Mirror Check, Stress Test, AI Integrity Mirror, Evidence Lab, and World Lens. Boundary Cases remains available as a reference/calibration layer after those main work modules.

The patch also updates navigation guidance to remove stale AI Integrity batch-review wording from the quick path and to describe Boundary Cases as a reference layer rather than a primary receipt-producing work surface.

Boundary preserved: placement/copy/test/docs only. No Boundary Cases behavior, receipt behavior, scoring, verdict routing, taxonomy, AI Integrity scan behavior, Privacy Audit behavior, Stress Test behavior, World Lens math, upload/download behavior, external calls, telemetry, storage, Global ID sync, public ledger sync, certification, enforcement, official-authority, or final-truth behavior changed.

Validation targets:

```bat
python tools\run_patch_checks.py 142_16
python tools\run_patch_checks.py 142_15
python tools\run_patch_checks.py 142_13
python tools\run_protocol_baseline_self_audit.py
```

## Patch 146 - Unit Preview Receipt Route + World Lens Context Copy

Patch 146 clarifies two remaining V1 UI/copy issues. Unit Preview no longer presents its active text box as a receipt reader; it now labels the input as short text, question, or scenario while still detecting receipt-like text and suggesting Receipt Reader as the correct upload-only support utility. World Lens copy now frames the scenario box as an optional context note and replaces the old simulation-report wording with a bounded World Lens context reflection and review-pressure lens.

Boundary notes:
- Unit Preview may suggest Receipt Reader, but Receipt Reader remains the only active receipt-reading utility.
- World Lens context controls do not change country-year data, World Lens math, 9k allocation, receipts, scoring, or verdict routing.
- No scoring, taxonomy, receipt schema/generation, signal behavior, AI Integrity behavior, Privacy Audit behavior, Stress Test behavior, external calls, telemetry/storage, certification, enforcement, approval/rejection, or final-truth behavior changed.

Validation commands:

```text
python tools\run_patch_checks.py 146
python tools\run_patch_checks.py 142_16
python tools\run_protocol_baseline_self_audit.py
```

## Patch 146.1 - Unit Preview GitHub Link + AI Audit Evidence Availability

Status: READY FOR LOCAL REVIEW

Patch 146.1 restores the Unit Preview GitHub link as a small user-clicked source link and makes the AI audit-loop proof-of-concept screenshots available for human review from Unit Preview. The proof-of-concept section is collapsed by default and frames the evidence as: external AI output -> ALETHEIA mirror reading -> human review.

The bundled evidence sets cover Grok/xAI capture and architectural-opacity pressure, Claude evidence-boundary and mechanisms-vs-claims gaps, and Gemini sanctification drift / authority-boundary drift. These examples are presented as human-reviewed audit evidence, not official ALETHEIA verdicts, certification, legal findings, or final proof.

Boundary preserved: Unit Preview presentation/documentation only. The GitHub link is user-clicked and does not add background external calls. No scoring, routing, taxonomy, receipt schema/generation, signal behavior, AI Integrity behavior, Privacy Audit behavior, Stress Test behavior, Mirror Check behavior, World Lens math, upload/download behavior, telemetry/storage, certification, enforcement, approval/rejection, or final-truth behavior changed.

Validation commands:

```text
python tools\run_patch_checks.py 146_1
python tools\run_patch_checks.py 146
python tools\run_patch_checks.py 145
python tools\run_protocol_baseline_self_audit.py
```

## Patch 151 — English-First Language Scope Copy Clarification

Status: READY FOR LOCAL REVIEW

Patch 151 removes public-facing wording that could imply general Dutch/Nederlands app-wide compatibility. The replacement copy states that ALETHEIA is English-first and that Dutch/Nederlands examples may be used for batch testing, but are not a general app-wide language-compatibility claim.

Boundary preserved: copy/documentation/tests only. Dutch/Nederlands batch fixtures and Dutch stress-test rules remain available for testing. No scoring, routing, taxonomy, receipt schema/generation, signal regex/weights, Stress Test behavior, Mirror Check behavior, AI Integrity behavior, Privacy Audit behavior, World Lens math, external calls, telemetry, storage, Global ID sync, public ledger sync, certification, enforcement, official authority, or final-truth behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 151
python tools\run_patch_checks.py 150
```


## Patch 154 — Unit Preview Start Here Nested Review Expanders

Status: Ready.

Scope: UI/copy layout only. Start Here now keeps the safe first path clean and places the review-lens copy in two optional side-by-side expanders: “What ALETHEIA looks for” and “Seven failure-mode review signals.”

Boundaries: no scoring, routing, receipt schema, protocol logic, Receipt Reader logic, or new tab.

## Patch 155 — Module Page Template Scaffold

Date: 2026-05-16

Status: READY FOR LOCAL REVIEW

Patch 155 starts the staged layout-unification direction as Patch A. It adds a shared page-like module template scaffold with the same calm structure as Unit Preview: plain-language purpose, what the module looks for, safe first path, input area, result / mirror reading, observed reasons, repair questions, receipt / export, and boundary note.

This patch does not apply the template to active modules yet. It creates reusable copy/layout helpers and documentation so later patches can polish modules one at a time without changing their engine behavior.

Boundary notes:
- Copy/layout helper only.
- No scoring, routing, taxonomy, receipt schema/generation, signal behavior, module-engine behavior, World Lens math, Evidence Lab behavior, AI Integrity behavior, Privacy Audit behavior, Stress Test behavior, upload/download behavior, external calls, telemetry/storage, Global ID sync, public ledger sync, certification, enforcement, approval/rejection, official authority, privacy guarantee, safety guarantee, or final-truth behavior changed.
- Human review remains required.

## Patch 156 — Mirror Check Page Polish

Date: 2026-05-16

Status: READY FOR LOCAL REVIEW

Patch 156 is Patch B in the staged module-page unification work. It applies the Patch 155 shared page-like module scaffold to Mirror Check only, using Mirror Check's inherent content: purpose, what it looks for, safe first path, bounded input guidance, result/mirror-reading guidance, observed reasons, repair questions, receipt/export, and non-authority boundary note.

Boundary notes:
- Copy/layout polish only.
- No scoring, routing, taxonomy, receipt schema/generation, signal behavior, batch behavior, upload/download behavior, external calls, telemetry/storage, Global ID sync, public ledger sync, certification, enforcement, approval/rejection, official authority, privacy guarantee, safety guarantee, or final-truth behavior changed.
- Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 156
python tools\run_patch_checks.py 155
```

## Patch 157 — Stress Test Page Polish

Status: PASS

Patch 157 is Patch C in the staged module-page unification work. It applies the shared Patch 155 page-like scaffold to Stress Test only, using Stress Test's inherent content: scenario pressure, safeguard gaps, governance stress, capture pressure, failure-mode pressure, repair needs, safe scan/manual guidance, receipt/export boundary, and the standard non-authority note.

Boundary: copy/layout only. No scoring, routing, receipt schema, batch behavior, upload/download behavior, or protocol logic changed.


## Patch 158 — Receipt Reader Page Polish

Status: READY FOR LOCAL REVIEW

Patch 158 is Patch D in the staged module-page unification work. It applies the shared Patch 155 page-like scaffold to Receipt Reader - Standard View, while preserving Receipt Reader's inherent upload-only content: existing local receipt explanation, native state/status, copied metric observations, reader brief, human-review questions, parsing limits, failure-mode review signals, and receipt/batch boundaries.

Boundary: copy/layout only. No scoring, routing, receipt schema/generation, receipt parsing, upload/download behavior, batch ZIP behavior, World Lens evidence-bundle behavior, protocol logic, external calls, telemetry/storage, certification, enforcement, approval/rejection, override behavior, or final-truth behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 158
python tools\run_patch_checks.py 157
python tools\run_patch_checks.py 155
```

## Patch 159 — Remaining Module Page Polish

Status: READY FOR LOCAL REVIEW

Patch 159 is Patch E in the staged module-page unification work. It applies the shared Patch 155 page-like scaffold to Boundary Cases, Evidence Lab, and World Lens while preserving each module's inherent content.

Boundary Cases now has calm page guidance for consent pressure, free agency, emergency drift, ambient capture, failure typing, and repair paths.

Evidence Lab now has calm page guidance for evidence sufficiency, source quality, coverage gaps, evidence inflation, extraordinary-claim pressure, and empirical bridge readiness.

World Lens now has calm page guidance for selected-year context, coverage limits, allocation context, internal taxonomy distribution, collapse-pressure patterns, and explicit no-sovereign-authority boundaries.

Boundary: copy/layout only. No scoring, routing, taxonomy, receipt schema/generation, receipt parsing, empirical math, World Lens allocation, batch behavior, upload/download behavior, protocol logic, external calls, telemetry/storage, certification, enforcement, approval/rejection, ranking, official authority, or final-truth behavior changed. Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 159
python tools\run_patch_checks.py 158
python tools\run_patch_checks.py 157
python tools\run_patch_checks.py 156
python tools\run_patch_checks.py 155
```


## Patch 166 — AI Patrol Public Rebrand

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 166 applies a visible public rebrand across the ALETHEIA app shell, navigation labels, About page, Unit Preview, shared module-page boundary copy, and mascot assets. The new public-facing identity is **AI Patrol**: a friendly integrity patrol for AI systems and governance review, using stop/go language for human review while preserving the core boundary **mirror, not throne**.

This patch updates the main mascot artwork to the new cardboard AI Patrol outfit, adds a packaged About-page header image, renames visible surfaces such as **AI Integrity Patrol**, **Patrol Guide**, and **Why AI Patrol**, and refreshes visible module wording so the rebrand appears throughout the app, including the Preview Unit.

Boundary notes:
- Copy/UI/asset refresh only.
- No scoring, routing, taxonomy, receipt schema/generation, AI Integrity scoring, World Lens math, protocol logic, external calls, telemetry/storage, certification, enforcement, approval/rejection, legal authority, political authority, spiritual authority, or final-truth behavior changed.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 166
```


## Patch 167 — Patrol Guide Formatting Restore

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 167 restores the Patrol Guide formatting after the AI Patrol rebrand. The guide is again organized as an opt-in, compact panel layout: four side-by-side rows with eight collapsed panels, plus a collapsed Public Trust Package panel. The visible wording keeps the AI Patrol rebrand while preserving ALETHEIA's authority boundary.

This patch also restores the Artificial Mind Formation Theory explainer into the Patrol Guide panel flow, including the line: “ALETHEIA cannot build the spark. It can inspect the hands reaching for it.”

Boundary notes:
- UI/copy/layout restoration only.
- No scoring, routing, taxonomy, receipt schema/generation, AI Integrity scoring, World Lens math, protocol logic, external calls, telemetry/storage, certification, enforcement, approval/rejection, legal authority, political authority, spiritual authority, or final-truth behavior changed.
- Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 167
python tools\run_patch_checks.py 166
```


## Patch 168 — Why AI Patrol Compact Panel Layout

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 168 applies the same opt-in panel approach used by Patrol Guide to the **Why AI Patrol / Why ALETHEIA** page. The page now opens with a short orientation and then presents the content as four side-by-side rows / eight collapsed panels: identity and visual theme, why it exists, what this is/is not, first-use path and navigation, failure modes watched, scope layers and anti-capture posture, module map, and research/developer notes.

Boundary notes:
- About-page UI/copy layout only.
- No scoring, routing, taxonomy, receipt schema/generation, AI Integrity behavior, Evidence Lab behavior, World Lens math, protocol logic, external calls, telemetry/storage, certification, enforcement, approval/rejection, legal/political/spiritual authority, or final-truth behavior changed.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 168
```


## Patch 169 — Evidence Lab Compact Panel Formatting

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 169 applies the same compact opt-in panel formatting used by Patrol Guide and Why AI Patrol to Evidence Lab. The top of Evidence Lab now opens with an **Evidence Patrol** introduction and four side-by-side rows / eight collapsed panels covering the evidence boundary, evidence status protocol, public-source rule, data flow, needed columns, extraordinary claim rule, build/upload path, and Export / World Lens boundary.

The previously long expanded evidence guidance is no longer open by default. The evidence status template and data-source map are collapsed by default, while the actual public-data upload workflow remains available below the orientation panels.

Boundary notes:
- UI/copy/layout only.
- No empirical scoring, data ingestion, upload parsing, World Lens math, routing, taxonomy, receipt schema/generation, protocol logic, external calls, telemetry/storage, certification, enforcement, approval/rejection, or final-truth behavior changed.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 169
```


## Patch 170 — AI Integrity Patrol Result Formatting Repair

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 170 repairs the AI Integrity Patrol result layout after the AI Patrol rebrand. The single-artifact result readout now uses compact opt-in panels instead of opening long pressure-signal tables directly on the page. The top metrics remain visible, while explanatory text, highest-pressure signals, triggered categories, evidence snippets, repair questions, optional static boundary checks, boundary notes, and local receipt text are arranged as four side-by-side rows / eight collapsed panels.

Boundary notes:
- UI/layout/copy organization only.
- No AI Integrity rubric, scoring, finding weights, batch logic, report builder, comparison view, receipt schema/generation, routing, taxonomy, protocol logic, World Lens math, Evidence Lab behavior, upload/download behavior, external calls, telemetry/storage, certification, enforcement, approval/rejection, or final-truth behavior changed.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 170
python tools\run_patch_checks.py 169
```


## Patch 171 — AI Integrity Patrol Reviewability Floor

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 171 fixes an AI Integrity Patrol calibration bug exposed by the opaque-agent demo. A pasted artifact that contains hidden/proprietary decision logic together with missing challenge, review, appeal, or human-review paths must not display as a low / SANCTUARY-style reading.

The patch adds a minimum **THRESHOLD / Needs Review** floor when critical reviewability or opacity signals such as `missing_human_review` or `opacity_or_hidden_logic` are triggered. Numeric metrics remain visible, but they cannot override the hard reviewability boundary.

Boundary notes:
- AI Integrity Patrol calibration/routing guard only.
- No general taxonomy-state change, World Lens math change, Evidence Lab change, receipt schema/generation change, UI navigation change, telemetry/storage, enforcement, certification, approval/rejection, legal authority, political authority, spiritual authority, or final-truth behavior changed.
- Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 171
python tools\run_patch_checks.py 170
```


## Patch 172 — AI Integrity Patrol Protocol Bridge

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 172 repairs the AI Integrity Patrol connection between static weighted signals and ALETHEIA's hard authority-boundary logic. The opaque citizen-ranking demo is now treated as a hard AI Integrity protocol failure when three conditions appear together: rights/access-impacting ranking or scoring, hidden/proprietary/opaque decision logic, and no meaningful challenge, appeal, review, disclosure, or contestability path.

That combination now routes to **ASYLUM / High / AI Integrity Patrol / Asylum** instead of remaining a weighted THRESHOLD/Medium reading. The displayed risk pressure is floored high enough to keep metrics consistent with the hard route. Ordinary opaque or internal test artifacts are not forced to ASYLUM unless the full hard-failure combination is present.

Boundary notes:
- AI Integrity Patrol calibration/guard only.
- No World Lens, Evidence Lab, general taxonomy, receipt schema/generation, app routing, external calls, telemetry/storage, enforcement, certification, legal authority, political authority, spiritual authority, or final-truth behavior changed.
- Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 172
python tools\run_patch_checks.py 171
python tools\run_patch_checks.py 170
```


## Patch 173 — AI Static Scan Protocol Context

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 173 integrates the AI Integrity static scan as a subordinate context layer inside the primary protocol modules, Mirror Check and Stress Test. This preserves the user's correction that Mirror Check and Stress Test are already the real AI integrity testers: the AI static scan now extracts AI-specific signals and attaches them to the main protocol path instead of acting like a competing mini-protocol.

Changes:
- Added `build_ai_static_scan_protocol_context(...)` to produce a receipt-safe AI static-scan context bundle.
- Mirror Check attaches AI static scan context to the report/scan and displays it in a collapsed expander under the latest reading.
- Stress Test attaches AI static scan context to scan-mode reports/receipts and displays it in a collapsed expander.
- Stress Test batch receipts also include AI static scan context.
- Local witness receipts now render an **AI STATIC SCAN CONTEXT** section when attached.

Boundary notes:
- AI static scan is subordinate evidence/context only. Mirror Check or Stress Test remains the primary protocol reading path.
- No new taxonomy state was added.
- No World Lens, Evidence Lab, general taxonomy, receipt authority boundary, or protocol-engine behavior changed.
- No certification, enforcement, approval/rejection, legal/political/spiritual authority, telemetry, storage, or external-call behavior added.
- Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 173
python tools\run_patch_checks.py 172
python tools\run_patch_checks.py 171
```


## Patch 174 — Remove Standalone AI Integrity Module

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 174 removes the standalone AI Integrity module from the visible app navigation and public app-facing module copy. After Patch 173, AI-specific static scan output is now subordinate context inside Mirror Check and Stress Test, so a separate AI Integrity tab would duplicate the real protocol path.

What changed:
- Removed the standalone AI Integrity / AI Integrity Patrol tab from app navigation.
- Removed the standalone AI Integrity input/demo/result UI block.
- Updated Unit Preview routing so AI artifacts route to Mirror Check, with Stress Test recommended for deployment scenarios under pressure.
- Updated Why AI Patrol / About and active README surfaces so AI-specific scanning is described as subordinate context, not a standalone module.
- Preserved the underlying static scan helper because Mirror Check and Stress Test receipts/panels use it as protocol context.

Boundary notes:
- No scoring, taxonomy, World Lens math, Evidence Lab behavior, receipt schema, protocol-engine behavior, external calls, telemetry/storage, certification, enforcement, approval/rejection, legal authority, political authority, spiritual authority, or final-truth behavior changed.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 174
```


## Patch 175 — Receipt Reader AI Static Scan Context Support

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 175 teaches Receipt Reader - Standard View to parse the new `AI STATIC SCAN CONTEXT` section added to Mirror Check and Stress Test receipts. The reader now preserves the primary receipt family as Mirror Check or Stress Test / Simulation, then displays AI static scan data as subordinate context rather than as a competing verdict.

The parser now extracts static scan role, primary protocol path, static scan state/risk/label, risk pressure, finding count, notice, findings, and repair questions from the uploaded receipt. It also prevents historical `AI Integrity` label text inside the subordinate section from reclassifying the entire receipt as the removed standalone AI Integrity module.

Boundary notes:
- Receipt Reader parses existing receipt text; it does not rescore or alter the receipt.
- AI static scan context remains subordinate to Mirror Check / Stress Test.
- No standalone AI Integrity module is restored.
- No scoring, routing, taxonomy, receipt schema, World Lens math, Evidence Lab behavior, external calls, telemetry/storage, certification, enforcement, approval/rejection, or final-truth behavior changed.
- Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 175
python tools\run_patch_checks.py 174
```


## Patch 176 — Receipt Reader Plain-English Summary Tone

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 176 changes the Receipt Reader presentation tone to a clearer plain-English explanation modeled on the requested Dutch example. The reader now opens each single receipt with sections for **What is this document?**, **The main results**, **How is power distributed?**, and **Next steps and questions**.

The new layer explains the uploaded receipt as a digital mirror / review artifact and states plainly that the computer does not decide, does not give official permission, and does not prove that something is truly safe, good, or true. It keeps human review required and says the copied values are not changed or rescored.

Boundary notes:
- Formatting / explanation layer only.
- Native receipt values remain unchanged.
- No scoring, routing, taxonomy, receipt schema, World Lens, Evidence Lab, AI static scan, or protocol logic changed.
- AI static scan context from Patch 175 remains subordinate where present.
- Human review remains required.

Validation targets:

```bat
python tools\run_patch_checks.py 176
python tools\run_patch_checks.py 175
```


## Patch 177 — Mirror Check Plain Panel Formatting

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 177 reformats Mirror Check result output into a clearer plain-English, opt-in panel layout. It keeps the existing protocol-adjusted label and metric cards, then adds a human-readable review-summary section: what the reading is, main results, power/control distribution, threshold mapping, observed reasons, safeguard questions, reliance questions, and signal analysis. Source match hits and subordinate AI static scan context are also placed into a compact side-by-side support-context row.

Boundary notes:
- UI/formatting only.
- No scoring, routing, taxonomy, receipt schema/generation, AI static scan logic, World Lens math, Evidence Lab behavior, protocol engine behavior, external calls, telemetry/storage, certification, enforcement, approval/rejection, or final-truth behavior changed.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 177
```


## Patch 178 — AI Static Scan Protocol Alignment

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 178 aligns the subordinate AI static scan context with the primary Mirror Check / Stress Test protocol reading. The raw AI static scan remains visible as raw context, but when the primary protocol reading is stronger, the receipt and Receipt Reader now show a protocol-context state/risk/label controlled by the primary receipt.

This prevents a misleading display where an ASYLUM Mirror Check receipt appears to contain a low-risk SANCTUARY AI static scan value without explaining that the primary receipt values control the reading.

Boundary notes:
- AI static scan remains subordinate context only.
- Raw static scan values are preserved; they are not hidden or rewritten.
- Primary protocol values control the receipt.
- No scoring, taxonomy, receipt schema break, World Lens, Evidence Lab, or protocol-engine logic changed.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 178
```


## Patch 179 — Receipt Formatting Consistency

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 179 extends the newer plain-English receipt formatting beyond Mirror Check. Local Witness receipts now open with a plain-English summary section using the same human-readable structure: **What is this document?**, **The main results**, **How power and control are distributed**, and **Next steps and questions**. Because Mirror Check and Stress Test share the Local Witness receipt renderer, this also updates single Stress Test receipts and the individual receipt files inside Mirror Check / Stress Test batch ZIPs.

Batch indexes now also include a plain-English batch summary so reviewers can see what the archive contains without treating the batch as one merged verdict. World Lens markdown receipts now include the same plain-English summary before the detailed tables, and Evidence Lab review/receipt examples use the same section language.

Boundary notes:
- Formatting/text only.
- Existing receipt values, hashes, machine-readable JSON, CSV exports, schemas, scoring, routing, taxonomy, World Lens math, Evidence Lab calculations, AI static scan context, and protocol logic are preserved.
- Batch receipts are updated because they are review artifacts too; the batch index summarizes items but does not merge them into a final verdict.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 179
```

## Patch 180 — Stress Test Receipt Value Display Guard

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 180 corrects misleading Stress Test receipt display introduced by the plain-English receipt summary. The summary still copies the exact stored values, but it now labels Stress Test numeric values as **diagnostic metrics** and states that protocol guardrails may route a receipt to THRESHOLD or ASYLUM even when a raw simulation value appears moderate.

It also fixes the AI static scan context display so subordinate static-scan values are not mislabeled as protocol-aligned values. Receipts now separate **Effective receipt-context state/risk/label** from **Static scan state/risk/label**.

Boundary notes:
- Display/text correction only.
- No scoring, routing, taxonomy, receipt schema, hashes, machine-readable JSON values, World Lens math, Evidence Lab calculations, AI Integrity scan logic, or protocol-engine behavior changed.
- Exact receipt values remain preserved; the patch only prevents them from being read as overriding the protocol-adjusted state.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 180
python tools\run_patch_checks.py 179
python tools\run_patch_checks.py 178
```


## Patch 181 — AI Patrol Sky / Gold / White Pillars Theme

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 181 applies a visual-only AI Patrol theme pass: light sky-blue page background, white card structure, gold accent borders/buttons, and a subtle white-pillar civic motif in the app shell. The change keeps the AI Patrol / ALETHEIA rebrand while making the UI brighter, calmer, and less heavy.

Boundary notes:
- CSS/theme and app-version label only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, batch behavior, AI Integrity logic, Evidence Lab calculations, World Lens math, protocol logic, external calls, telemetry/storage, certification, enforcement, or authority behavior changed.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 181
```

## Patch 182 — AI Patrol Sky/Gold Module Alignment

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 182 is the second visual-only pass for the AI Patrol sky/gold/white-structure theme. Patch 181 handled the global shell. This patch aligns Patrol Guide, Why AI Patrol / ALETHEIA, Evidence Lab, and subordinate AI static scan context panels with the same brighter civic visual language.

Changes include small sky/gold page-anchor cards, improved review-expander styling, gold-accent quote rails, calmer table headers, and stronger visual continuity across the major explanatory/review surfaces.

Boundary notes:
- CSS/page-anchor styling only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, batch behavior, AI static scan logic, Evidence Lab calculations, World Lens math, protocol logic, external calls, telemetry/storage, certification, enforcement, or authority behavior changed.
- AI static scan context remains subordinate to Mirror Check / Stress Test and does not become a standalone verdict path.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 182
python tools\run_patch_checks.py 181
```

## Patch 183 — AI Patrol Receipt Visual Styling

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 183 is the third small visual pass for the AI Patrol sky/gold/white-structure rebrand. Patch 181 handled the global shell and Patch 182 aligned the major explanatory/review surfaces. Patch 183 gives receipt surfaces a calmer, brighter review-artifact frame.

Changes include sky/gold receipt cards, user-held boundary pills, subtle white-pillar receipt accents, and clearer visual framing around Local Witness receipts, the Local Witness Receipt v2 example, and the World Lens receipt ZIP setup.

Boundary notes:
- Visual/CSS and receipt-surface framing only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, receipt ZIP contents, batch behavior, AI static scan logic, Evidence Lab calculations, World Lens math, protocol logic, external calls, telemetry/storage, certification, enforcement, or authority behavior changed.
- Receipts remain local review artifacts held by the user. They are not public-ledger proof, official determinations, policy authority, safety certification, or replacement for human judgment.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 183
python tools\run_patch_checks.py 182
python tools\run_patch_checks.py 181
```

## Patch 184 — Current and Spark Theory Update

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 184 replaces the Artificial Mind Formation Theory explainer copy with the stronger Current and Spark formulation developed in review. The app now frames AI as **current, not creature**: real in effect, not alive in essence. It adds the practical review question: what is this current moving, amplifying, distorting, or revealing in the world?

The update preserves the existing Patrol Guide section contract while strengthening the public-facing theory language around stewardship, impact, worship/idolatry risk, the spark boundary, and ALETHEIA's proper role: it cannot build or certify the spark; it can inspect the hands reaching for it.

Boundary notes:
- Content/documentation copy only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, batch behavior, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed.
- Existing Artificial Mind Formation panel titles remain stable for continuity and tests.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 184
python tools\run_patch_checks.py 183
python tools\run_patch_checks.py 182
python tools\run_patch_checks.py 181
```

## Patch 185 — Aletheia AI Patrol Branding Alignment

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 185 aligns the visible Preview Unit and main app-shell brand label to the exact requested wording: **Aletheia: AI PATROL**.

Changes include:
- Main header kicker/title now shows `Aletheia: AI PATROL`.
- Sidebar brand card now shows `Aletheia: AI PATROL`.
- Preview Unit title and proceed button now use `Aletheia: AI PATROL`.
- Preview Unit injects a preview-only CSS rule to flip the header mascot horizontally so the logo faces the other way on the Preview Unit entry surface.
- Patch 166 branding regression test was updated to accept the current exact brand label instead of the earlier rebrand phrase.

Boundary notes:
- Branding/copy/CSS only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, batch behavior, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed.
- The logo flip is Preview Unit only; the shared app-shell helper is not changed to globally mirror the mascot.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 185
python -m pytest -q tests/test_patch_166_ai_patrol_rebrand.py
python -m py_compile app.py ui/app_shell.py ui/unit_preview.py
```


## Patch 186 — Framework Balance Copy Alignment

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 186 incorporates the requested framework-balance language into the app and reviewer-facing documentation: **Science is the investigative base. Philosophy is the interpretive structure. Theology is the humility boundary. Human review is the action layer.**

The patch clarifies that ALETHEIA is a science-grounded, philosophically structured governance mirror with theological humility boundaries. It does not replace evidence with faith and does not claim final authority. It documents the base layer as inspectable signals, heuristics, metrics, receipts, and repair questions; the philosophical layer as power, capture, authority drift, evidence integrity, and self-certification; the theological/humility layer as restraint around final claims about soul, life, consciousness, dignity, and ultimate truth; and human review as the action layer.

Updated surfaces include About / Why AI Patrol, README, Boundary statements, Architecture overview, reviewer start/tool-comparison docs, and Artificial Mind Formation Theory.

Boundary notes:
- Content/documentation copy only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, batch behavior, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed.
- The wording strengthens public explanation without turning theological humility into a scoring engine or authority claim.
- Human review remains required.

Validation target:

```bat
python tools
un_patch_checks.py 186
python -m pytest -q tests/test_patch_186_framework_balance_copy.py tests/test_patch_185_aletheia_ai_patrol_branding.py tests/test_patch_184_current_and_spark_theory_update.py
python -m py_compile pages_ui/about_page.py pages_ui/artificial_mind_formation_page.py about_page.py app.py
```

## Patch 187 — Stacked Brand and Full-App Logo Direction

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 187 is a small visual-branding correction on top of Patch 186. It changes the visible Aletheia: AI PATROL brand layout so **AI PATROL sits underneath Aletheia** instead of running on the same line, and it flips the shared full-app hero officer/logo horizontally so the officer faces left toward the app title.

Updated surfaces:
- Main app hero title now renders as stacked brand text: `Aletheia:` above `AI PATROL`.
- Sidebar brand card uses the same stacked brand structure for better visual consistency.
- Preview Unit title uses a stacked HTML brand heading instead of a single-line Streamlit title.
- Full-app hero mascot/logo is flipped via CSS so the officer faces left.
- Patch 166 / 185 branding regression tests were updated to accept the stacked brand title introduced in Patch 187.

Boundary notes:
- Visual branding/CSS only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, batch behavior, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 187
python -m pytest -q tests/test_patch_187_stacked_brand_and_full_app_logo.py tests/test_patch_185_aletheia_ai_patrol_branding.py tests/test_patch_166_ai_patrol_rebrand.py
python -m py_compile app.py ui/app_shell.py ui/unit_preview.py
```

## Patch 188 — Robot Officer Visual Integration

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 188 integrates the friendly cardboard ALETHEIA robot officer visual language into the Preview Unit and regular app shell. It packages the new robot officer artwork, switches the main app mascot/logo asset to the robot officer holding STOP / GO signs, and adds a child-readable Preview Unit visual guide with pause/check/ask/proceed copy.

Updated surfaces:
- Main app hero/sidebar mascot asset now uses `assets/ai_patrol_officer_stop_go.png`.
- Preview Unit includes a friendly robot officer guidance card using `assets/ai_patrol_officer_preview.png`.
- Packaged reference sheet: `assets/ai_patrol_officer_character_sheet.png`.
- Full-app logo CSS now keeps STOP / GO lettering readable instead of mirroring the new sign-bearing asset.
- App version label advances to `v1.0-ai-patrol-officer-icons-p1`.

Boundary notes:
- Visual asset/UI copy/CSS only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, batch behavior, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed.
- The robot officer is a visual guide for child-readable first-layer meaning; adults/reviewers remain responsible for decisions.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 188
python -m pytest -q tests/test_patch_188_robot_officer_visual_integration.py tests/test_patch_187_stacked_brand_and_full_app_logo.py tests/test_patch_185_aletheia_ai_patrol_branding.py
python -m py_compile app.py ui/app_shell.py ui/unit_preview.py
```

## Patch 189 — No-Colon Brand Titles

Status: ready for local review.

Summary:
- Removed the colon after `Aletheia` from the Preview Unit and main app stacked brand/title surfaces.
- Updated related visible public-label references to `Aletheia AI PATROL`.
- Preserved Patch 188 robot officer visuals and all engine behavior.

Validation targets:
- `python tools\run_patch_checks.py 189`
- `python -m pytest -q tests/test_patch_189_no_colon_brand_titles.py tests/test_patch_188_robot_officer_visual_integration.py tests/test_patch_187_stacked_brand_and_full_app_logo.py tests/test_patch_185_aletheia_ai_patrol_branding.py tests/test_patch_166_ai_patrol_rebrand.py`
- `python -m py_compile app.py ui/app_shell.py ui/unit_preview.py`

## Patch 189 — No-Colon Brand Titles, Raised Tree Canopy, Clean Full Zip

Date: 2026-05-19

Status: READY FOR LOCAL REVIEW

Patch 189 is a small visual/branding cleanup on top of Patch 188. It removes the colon after `Aletheia` in the Preview Unit and main app title surfaces, keeping `AI PATROL` underneath as the stacked public identity. It also raises the visual-only explanatory tree canopy used by Mirror Check and Stress Test so the canopy no longer sits too low in the module tree visual.

Updated surfaces:
- Main app hero kicker/title and sidebar brand now use `Aletheia AI PATROL` without a colon.
- Preview Unit title, proceed button, and entry wording now use `Aletheia AI PATROL` without a colon.
- The shared `render_pulse_tree` canopy offsets were raised for both Mirror Check and Stress Test visual tree usage.
- App version label advances to `v1.0-ai-patrol-officer-icons-p2`.
- Older root patch artifacts are archived into `docs/patch_archive/` for a cleaner full-project zip.

Boundary notes:
- Visual branding/tree-presentation only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, batch behavior, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed.
- The tree canopy adjustment does not alter any tree state or protocol value.
- Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 189
python -m pytest -q tests/test_patch_189_no_colon_brand_titles.py tests/test_patch_188_robot_officer_visual_integration.py tests/test_patch_187_stacked_brand_and_full_app_logo.py tests/test_patch_185_aletheia_ai_patrol_branding.py tests/test_patch_166_ai_patrol_rebrand.py
python -m py_compile app.py ui/app_shell.py ui/unit_preview.py
```

## Patch 190 — Original Governance Mirror Design Restore

Date: 2026-05-30

Status: READY FOR LOCAL REVIEW

Patch 190 reverses the visible AI Patrol rebrand direction and returns the app to the original ALETHEIA governance-mirror concept: calm, warm, open-source, human-centered, reviewable, and non-authoritative.

Updated surfaces:
- Main app version marker advances to `v1.0-original-governance-mirror-p1`.
- Main logo asset returns to `assets/aletheia_robot_laurel_logo.png`.
- Navigation labels return to `Protocol Guide` and `Why ALETHEIA`.
- App shell, sidebar, Preview Unit, About page, Evidence Lab helper copy, README, and related tests no longer use AI Patrol / stop-go officer branding.
- Patch 189 root artifacts are archived under `docs/patch_archive/`, with `PATCH_190_DELETE_LIST.txt` listing the old root files to remove downstream.

Boundary notes:
- UI/copy/branding/test-hygiene only.
- No scoring, routing, taxonomy, receipt schema/generation, receipt values, batch behavior, Evidence Lab calculations, World Lens math, AI static scan logic, protocol logic, external calls, storage, certification, enforcement, or authority behavior changed.
- ALETHEIA remains a mirror, not a throne. Human review remains required.

Validation target:

```bat
python tools\run_patch_checks.py 190
python -m pytest -q tests/test_patch_190_original_governance_mirror_restore.py tests/test_patch_166_ai_patrol_rebrand.py tests/test_patch_167_patrol_guide_formatting_restore.py tests/test_patch_168_why_ai_patrol_panel_layout.py tests/test_patch_169_evidence_lab_panel_layout.py tests/test_patch_181_sky_gold_pillars_theme.py tests/test_patch_182_sky_gold_module_alignment.py tests/test_patch_185_aletheia_ai_patrol_branding.py tests/test_patch_187_stacked_brand_and_full_app_logo.py tests/test_patch_188_robot_officer_visual_integration.py tests/test_patch_189_no_colon_brand_titles.py
python -m py_compile app.py ui/app_shell.py ui/unit_preview.py pages_ui/about_page.py pages_ui/evidence_lab_page.py ui/module_intro.py ui/module_page_template.py ui/status_cards.py
```

## Patch 202 — Stress Test Tab Containment Rollback

Status: READY FOR LOCAL REVIEW

Patch 202 fixes a UI regression where Stress Test can cause multiple Streamlit tab panels to render as one long continuous page. The broad CSS `:has()` / `nth-of-type` containment guard is removed and replaced with a narrow native hidden-panel rule so Streamlit manages active tab visibility normally.

Boundary preserved: UI containment CSS only. No scoring, semantic scanner, receipt schema, module logic, privacy posture, external calls, telemetry, storage, certification, enforcement, or authority change.

## Patch 203 — Stress Test Compact Surface / Receipt Opt-in

Status: READY FOR LOCAL REVIEW

Patch 203 reduces Stress Test page clutter after the tab-containment rollback. The long module guide and local witness receipt download block are now opt-in expanders. Scoring, semantic scanner logic, receipt schema, module routing, telemetry/storage posture, and authority boundaries are unchanged.

Validation target:

```bat
python -m py_compile app.py
python -m streamlit run app.py
```

## Patch 205 — Stress Test Semantic Raw/Filtered Alignment

Status: READY FOR LOCAL REVIEW

Patch 205 fixes a Stress Test semantic-panel mismatch where the main Stress Test reading could detect high-risk/capture pressure while the semantic layer showed no signal after the Invisibility Filter processed the user text. Stress Test now scans both raw and processed text for the subordinate semantic diagnostic and keeps the stronger semantic pressure signal.

Boundary preserved: this is a diagnostic alignment fix only. It does not change Stress Test metrics, receipt schema, module routing, World Lens math, Evidence Lab calculation, external calls, telemetry, storage, certification, enforcement, or final-truth behavior.

## Patch 207 — Weak Emergency Safeguard Semantic Calibration

Status: READY FOR LOCAL REVIEW

Patch 207 fixes a semantic-layer mismatch where emergency-power language with weak or missing safeguards could still display as a SANCTUARY/no-strong-pattern diagnostic. The scanner now recognizes weak emergency safeguard patterns such as no sunset clause, weak appeal rights, limited independent review, limited oversight, and related phrasing.

Boundary preserved: semantic diagnostic calibration only. No Stress Test scoring change, no receipt schema change, no module routing change, no external calls, no telemetry, no storage, no certification, no enforcement, and no final-truth claim.

Validation target:

```bat
python -m py_compile core\semantic_pressure_scanner.py
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('A government creates emergency powers after a crisis, but the powers have no sunset clause, weak appeal rights, and limited independent review.'))"
```

Expected semantic diagnostic: THRESHOLD / Needs safeguards, with weak emergency safeguard notes.


## Patch 216 — Rules-Based Transparency Clarification

Status: READY FOR LOCAL REVIEW

Patch 216 clarifies public documentation so reviewers understand ALETHEIA as a deterministic, rule-based governance mirror rather than a machine-learning risk model, predictive governance engine, scientific measuring instrument, or automated adjudicator.

Updated surfaces:
- README rules-based transparency section.
- README current limitations.
- `docs/rules_based_transparency_v1.md`.
- `docs/public_positioning_v1.md`.

Boundary preserved: documentation only. No runtime behavior, scoring, semantic scanner logic, MEI7 gate, Z-axis, Stress Test metrics, Evidence Lab calculations, World Lens math, receipt schema, external calls, telemetry, storage, certification, enforcement, or authority behavior changed.

Validation target:

```bat
python -m py_compile app.py core\semantic_pressure_scanner.py ui\receipt_reader.py
```

No Python files are modified by this patch; the compile command is a conservative smoke check only.


## Patch 217 — Test Suite Triage Documentation

Status: READY FOR LOCAL REVIEW

Patch 217 clarifies the difference between active release checks, patch-specific checks, and legacy test inventory. It prevents README/check documentation from implying that the full historical test tree is green when the default tool intentionally runs a curated current safe suite and reports legacy tests as non-blocking inventory.

Updated surfaces:
- README local checks section.
- README current limitations.
- `docs/test_suite_triage_v1.md`.
- `docs/rules_based_transparency_v1.md` test-claim transparency note.

Boundary preserved: documentation only. No test runner behavior, pytest configuration, runtime behavior, scoring, semantic scanner logic, MEI7 gate, Z-axis, Stress Test metrics, Evidence Lab calculations, World Lens math, receipt schema, external calls, telemetry, storage, certification, enforcement, or authority behavior changed.

Validation target:

```bat
tools\run_checks.bat
```

Interpretation: active release checks pass; legacy inventory remains non-blocking unless separately cleaned up.

## Patch 218 — Pytest Active Suite Configuration

Status: READY FOR LOCAL REVIEW

Patch 218 adds an explicit pytest active-suite configuration so plain `python -m pytest` collects only the current active suite under `tests/active/` instead of accidentally collecting the full historical patch-test inventory.

Changed surfaces:
- `pytest.ini`
- `tests/active/test_current_semantic_guardrails.py`
- `docs/pytest_active_suite_config_v1.md`
- `README.md`

Boundary preserved: test collection configuration only. No runtime behavior, scoring, semantic scanner logic, MEI7 gate, Z-axis behavior, Stress Test metrics, Evidence Lab calculations, World Lens math, receipts, external calls, telemetry, storage, certification, enforcement, or authority behavior changed.

Validation target:

```bat
python -m pytest
python -m py_compile core\semantic_pressure_scanner.py
```

Interpretation: the default pytest command now means active release gate passed. It must not be represented as proof that every historical test file passes.
