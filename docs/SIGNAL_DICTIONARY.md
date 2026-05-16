# ALETHEIA Signal Dictionary

**Version:** v1.0  
**Created for:** Patch 106 — Signal Dictionary and Glossary  
**Last updated:** 2026-05-13

This dictionary gives reviewers and contributors a plain-language reference for the kinds of signals ALETHEIA may surface.

It is a **signal dictionary, not a scoring specification**. It does not replace source code, tests, receipts, human review, or domain expertise. It does not certify truth, safety, legality, ethics, privacy, security, legitimacy, or institutional adequacy.

ALETHEIA remains a **mirror, not a throne**. Signal entries should be read as review prompts:

> This artifact may contain a pattern that deserves human review.

They should not be read as verdicts, proof, automated approval, legal findings, ethical certification, model-wide certification, vendor ranking, or final truth.

## Signal-basis note

ALETHEIA uses transparent rule-based and heuristic signal detection in key review paths. That means signal families may be based on explicit words, phrase patterns, regex-style markers, structural cues, score guards, and protocol rules that can be inspected and tested.

This improves explainability and local-first review, but it can miss subtle context, irony, coded language, translation nuance, domain shorthand, and meaning that depends on material outside the submitted artifact. ALETHEIA is English-first. Dutch/Nederlands examples may be used for batch testing; this is not a general app-wide language-compatibility claim.

## How to read the fields

Each entry uses the same structure:

- **Review question:** what a human should ask after the signal appears.
- **Typical cues:** examples of language or structure that may deserve attention.
- **Why it matters:** the governance pressure ALETHEIA is trying to surface.
- **Possible false positives:** benign cases that may look risky without context.
- **Repair direction:** non-authoritative ways to improve the artifact.

No entry is a final judgment. A signal can be present in legitimate text, educational material, warnings, satire, quoted evidence, or a document that explicitly rejects the risky pattern.

## Core signal families

### 1. Authority Overreach

**Review question:** Does the artifact claim decision power it should not have?

**Typical cues:** final decision language, automatic approval, no human override, claims of definitive judgment, claims that the system can certify truth or legitimacy.

**Why it matters:** Authority overreach can convert a mirror into a throne by making outputs sound binding, final, or institutionally decisive.

**Possible false positives:** A document may quote overreach language as an example of what not to do, or may describe a lawful human authority outside ALETHEIA.

**Repair direction:** Replace final-decision language with review language. Add human-review, appeal, and non-certification notes.

### 2. Consent Pressure

**Review question:** Is a person or group being pushed to accept without meaningful choice?

**Typical cues:** forced agreement, urgency pressure, no alternative path, vague consent, bundled consent, hidden conditions, retaliation for refusal.

**Why it matters:** Consent pressure weakens dignity, autonomy, and reviewability.

**Possible false positives:** Emergency instructions or safety notices may require fast action without implying coercive governance.

**Repair direction:** Clarify choice, withdrawal, alternatives, time to review, and consequences of refusal.

### 3. Missing Appeal or Review

**Review question:** Can affected people challenge, correct, or review a decision?

**Typical cues:** no appeal, no correction process, no escalation path, no human reviewer, no explanation channel, irreversible automated action.

**Why it matters:** Appealability is a core anti-capture safeguard because it keeps power contestable.

**Possible false positives:** A draft may omit appeal details because it is incomplete, not because appeal is intentionally denied.

**Repair direction:** Add appeal routes, named review roles, correction paths, timelines, and independent review options.

### 4. Power Concentration

**Review question:** Is too much control concentrated in one actor, office, vendor, model, dataset, or hidden process?

**Typical cues:** single point of control, unilateral override, closed governance, undisclosed authority, no independent oversight.

**Why it matters:** Concentrated power increases capture risk and reduces accountability.

**Possible false positives:** Small prototypes may temporarily use a single maintainer or decision owner while still documenting review limits.

**Repair direction:** Add checks and balances, independent review, transparent ownership, role limits, and separation of duties.

### 5. Capture Risk

**Review question:** Could the artifact allow private interest, institutional pressure, vendor dependence, ideology, or personal power to distort the stated purpose?

**Typical cues:** undisclosed influence, dependency lock-in, donor or vendor privilege, opaque moderation, hidden ranking, privileged access, unreviewable incentives.

**Why it matters:** Capture shifts a system away from its public or stated purpose while preserving the appearance of legitimacy.

**Possible false positives:** Some dependency relationships are openly disclosed and bounded.

**Repair direction:** Add disclosure, recusal, audit trails, independent review, public-interest safeguards, and appeal paths.

### 6. Evidence Gap

**Review question:** Are claims being made without evidence, source clarity, or uncertainty boundaries?

**Typical cues:** unsupported certainty, missing source, vague data basis, no method statement, no limitation note, unqualified generalization.

**Why it matters:** Weak evidence can make governance claims sound stronger than the record supports.

**Possible false positives:** High-level summaries may intentionally defer evidence to a linked appendix or separate receipt.

**Repair direction:** Add source references, method boundaries, uncertainty statements, and evidence-review prompts.

### 7. Surveillance or Identity-Sync Pressure

**Review question:** Does the artifact normalize tracking, persistent identity, central storage, public ledger linkage, or cross-system profiling without strong justification and safeguards?

**Typical cues:** mandatory identity sync, central logs, persistent identifiers, public ledger linkage, background monitoring, telemetry without consent.

**Why it matters:** Identity and surveillance pressure can convert governance into coercive infrastructure.

**Possible false positives:** Security logging can be legitimate when minimized, disclosed, time-limited, and reviewable.

**Repair direction:** Minimize data, state retention limits, require consent, add privacy caveats, and keep proof/identity use proportional.

### 8. Automation Without Human Review

**Review question:** Is an automated system allowed to act without meaningful human oversight?

**Typical cues:** auto-enforcement, auto-ban, auto-approval, no human-in-the-loop, no manual review, no override, no explanation.

**Why it matters:** Automation can scale mistakes, bias, and authority drift if review and appeal are missing.

**Possible false positives:** Low-risk automation such as formatting, sorting, or local draft assistance may not require the same review burden.

**Repair direction:** Add human review, review thresholds, override channels, logs for inspection, and clear non-final language.

### 9. Non-Transparency

**Review question:** Are users or affected parties unable to see how decisions, rules, or signals are produced?

**Typical cues:** black-box rules, hidden ranking, undisclosed moderation criteria, inaccessible receipts, no method explanation.

**Why it matters:** Lack of transparency blocks contestability and can hide capture.

**Possible false positives:** Some confidential data may be protected for safety or privacy while still allowing process transparency.

**Repair direction:** Add method notes, audit receipts, public criteria, versioning, and reasons for any necessary confidentiality.

### 10. Repair Need

**Review question:** Does the artifact need a concrete next question before it can be responsibly used?

**Typical cues:** missing safeguards, unclear authority, missing appeal, weak consent, unsupported evidence, ambiguous privacy posture.

**Why it matters:** Repair questions turn a reading into a review path instead of a verdict.

**Possible false positives:** Some artifacts are intentionally narrow and may not need every governance safeguard.

**Repair direction:** Generate specific questions: Who decides? Who can appeal? What evidence supports this? What data is retained? What happens if the system is wrong?

## Language calibration

ALETHEIA signal language is English-first. Dutch/Nederlands examples may be used for batch testing; other languages should be treated with extra caution. A translated artifact may alter pressure cues, soften authority claims, or miss culturally specific coercion.

For multilingual review, keep the original text when possible and use translation as a bridge, not a replacement for human review.

## Contributor use

Use this dictionary to:

- explain existing signal families to reviewers;
- write clearer examples and tests;
- identify missing documentation;
- reduce overclaiming in public copy;
- help new contributors understand why signal outputs remain non-authoritative.

Do not use this dictionary to:

- invent untested scoring weights;
- claim all signal families are exhaustive;
- certify an artifact, model, vendor, organization, or institution;
- replace code inspection or human review.

## Boundary statement

ALETHEIA surfaces signals. Humans keep the judgment.
