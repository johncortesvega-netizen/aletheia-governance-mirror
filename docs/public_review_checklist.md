# ALETHEIA Public Review Checklist

**Created for:** Patch 113 — Public Trust Package Consolidation  
**Last updated:** 2026-05-13

This checklist helps a reviewer inspect ALETHEIA before relying on a reading, running a local audit, adapting the code, or contributing a patch.

It is a checklist, not a certification. Completing it does not prove truth, safety, legality, ethics, privacy, security, compliance, or legitimacy.

## 1. Boundary check

- Did the reviewed text preserve **mirror, not throne** language?
- Does the app avoid claiming legal, political, institutional, medical, religious, ethical, or automated authority?
- Are outputs framed as readings, signals, or review prompts rather than verdicts or certifications?
- Is human review explicitly required?

## 2. Privacy and hosting check

- Is local use recommended for sensitive audits?
- Does the wording avoid promising a privacy guarantee?
- Are hosted deployment caveats visible?
- Does the reviewed change avoid telemetry, analytics, central storage, Global ID sync, public ledger sync, and external model calls unless explicitly reviewed?

## 3. Signal-basis check

- Are rule-based and heuristic limits visible?
- Are English/Dutch calibration limits visible where relevant?
- Are possible false positives and missed nuance acknowledged?
- Are signal outputs treated as internal governance-risk readings rather than verdicts or certifications?

## 4. Evidence and repair check

- Can a reviewer inspect the input, snippets, reasons, and repair questions?
- Are evidence gaps marked as review needs rather than proof of wrongdoing?
- Are repair questions framed as prompts for human judgment?

## 5. Contributor and patch check

- Is the change small enough to review?
- Are manifest and recovery notes present?
- Are patch-specific tests present?
- Does the patch preserve scoring, verdict routing, signal patterns, signal weights, receipt schema, module routing, and privacy boundaries unless the patch explicitly states otherwise?

## 6. Public trust check

- Does `docs/public_trust_package.md` point to the relevant boundary, privacy, signal, architecture, beginner, and patch-history documents?
- Does the trust package state that it is not a certification package?
- Does the public language avoid final-truth, enforcement, compliance approval, and vendor-certification claims?

## Closing rule

If a reviewer cannot answer a checklist item, the right outcome is not automatic rejection or automatic trust. The right outcome is more human review.

**ALETHEIA surfaces signals. Humans keep the judgment.**
