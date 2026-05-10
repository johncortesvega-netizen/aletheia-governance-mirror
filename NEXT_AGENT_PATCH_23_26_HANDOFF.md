# NEXT AGENT HANDOFF — ALETHEIA PATCHES 23–26

Current base:
- Stable through Patch 22.1.
- Patch 22.1 makes contextual ethics visible in Mirror Check receipts and applies ethics-calibrated integrity only when there is meaningful ethics pressure.
- Keep the build patch-by-patch. Do not combine 23–26 into one patch.

Hard constraints:
- ALETHEIA is a mirror, not a throne.
- No Global ID sync.
- No public ledger.
- No push-warning authority layer.
- Keep raw metrics available whenever adjusted metrics are shown.
- Preserve local witness receipts.
- Keep tests and recovery notes with every patch.

## Patch 23 — Nonlinear Ego Penalty

Goal:
Make ego/grip pressure more realistic: low ego should be manageable, but concentrated control should rise sharply near a tipping point.

Recommended implementation:
- Add a bounded nonlinear ego penalty layer.
- Use the instruction as a starting point, but clamp it:
  `ego_penalty = ego_weight * (ego ** 1.5)`
- Do not blindly subtract `ego ** 1.5` from every score without scale checks.
- Preserve raw/pre-penalty metrics in the report.

Suggested affected files:
- core/scoring.py or core/ethics.py, depending where the current Mirror Check metric calibration is centralized.
- tests/test_patch_23_nonlinear_ego_penalty.py
- PATCH_23_RECOVERY_NOTE.md

Expected tests:
- low ego does not over-penalize.
- medium ego creates visible caution.
- high ego sharply lowers integrity/stability and raises collapse probability.
- grip markers still remain a protocol/ethics hard signal.

Do not touch:
- batch UI
- Global Grid
- Evidence Lab
- witness hash mechanics except to add raw/adjusted fields if needed

## Patch 24 — Trust Gap / Collapse Calibration

Goal:
Increase collapse probability when alignment is high but trust is low. This catches systems that look coherent on paper but lack human confidence.

Recommended implementation:
- Calculate `trust_gap = max(0, alignment - trust_index)`.
- Increase collapse_probability with a bounded curve, for example:
  `collapse_probability += trust_gap ** 1.35 * weight`
- Increase trust_friction when trust_gap is meaningful.
- Preserve raw collapse_probability before adjustment.

Suggested affected files:
- core/scoring.py or core/ethics.py if Mirror Check calibration remains there.
- core/witness.py only if adding receipt fields.
- tests/test_patch_24_trust_gap_collapse.py
- PATCH_24_RECOVERY_NOTE.md

Expected tests:
- high alignment + high trust remains stable.
- high alignment + low trust raises collapse probability.
- low alignment + low trust should not fake stability.
- trust_gap appears in receipts or report metadata.

## Patch 25 — Repair Question Routing

Goal:
Avoid audit fatigue. Do not show all 50 questions by default. Route 3–7 relevant repair questions based on risk family.

Recommended implementation:
- Tag the 50 repair questions by family:
  - #Sovereignty
  - #Ego
  - #Systemic
  - #Appeal
  - #Surveillance
  - #MicroSovereignty
  - #TrustGap
  - #Evidence
- Let the report or judgment expose a compact risk profile, for example:
  `risk_families = ["Ego", "Appeal", "MicroSovereignty"]`
- Match questions by these families.
- Keep full question set optional, not default.

Suggested affected files:
- protocol.py or a new `core/repair_questions.py`
- app.py only if UI display needs a small label
- tests/test_patch_25_repair_question_routing.py
- PATCH_25_RECOVERY_NOTE.md

Expected tests:
- no appeal -> appeal/sovereignty questions.
- high ego -> ego/throne questions.
- central grid/universal ID -> micro-sovereignty/surveillance questions.
- safe local program -> light monitoring questions only.

## Patch 26 — V-Axis Dashboard

Goal:
Make the complex metrics visible in the botanical civic UI style without making ALETHEIA feel authoritative.

Recommended UI:
- Use existing botanical civic palette:
  - cream background
  - plum headings
  - sage safe signals
  - soft gold baseline
  - rose warnings
- Show:
  - Integrity
  - Friction
  - Ego pressure
  - Trust gap
  - Collapse probability
  - Micro sovereignty
- Use labels like:
  "Pattern view"
  "What needs review"
  "ALETHEIA reflects. People decide."

Suggested affected files:
- app.py
- tests/test_patch_26_v_axis_dashboard_contract.py
- PATCH_26_RECOVERY_NOTE.md

Do not do in Patch 26:
- no new scoring formulas
- no protocol verdict changes
- no new data flows
- no external sync

## Strategic note
The sequence matters:
1. Patch 23: Ego penalty.
2. Patch 24: Trust gap collapse.
3. Patch 25: repair-question routing.
4. Patch 26: V-Axis visual dashboard.

Keep each patch small and reversible.
