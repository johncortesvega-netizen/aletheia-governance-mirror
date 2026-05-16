# Signal Detection Transparency

Patch 103 documents ALETHEIA's signal-detection posture so reviewers and contributors understand what the mirror can and cannot see before deeper refactors begin.

ALETHEIA uses transparent rule-based and heuristic signal detection in key review paths. This means many signals are surfaced through explicit phrases, regex-style markers, keyword families, bounded scoring rules, and protocol guardrails that can be inspected by humans.

## Why rule-based signals are used

The rule-based posture is intentional. It supports:

- explainability: reviewers can inspect why a signal may have appeared;
- local-first operation: readings do not require live model calls;
- privacy: pasted text does not need to leave the running app session for external AI analysis;
- regression testing: signal families can be checked through small repeatable tests;
- authority restraint: ALETHEIA does not hide final judgment inside an opaque model.

This is a mirror design choice, not a claim that simple rules understand all language.

## What the signals can do

The signal system can help surface review pressure around:

- power concentration;
- consent pressure;
- weak appeal paths;
- missing safeguards;
- capture-risk language;
- surveillance or identity-sync pressure;
- authority-overreach claims;
- evidence gaps;
- repair-question needs.

These are internal governance-risk readings, not verdicts or certifications. They are not proof of harm, not proof of safety, not proof of corruption, not proof of legitimacy, legal findings, ethical certifications, or final truth.

## Known limits

Rule-based and heuristic detection can miss or misread:

- irony, sarcasm, and coded language;
- indirect coercion or implied threats;
- cultural context not present in the text;
- domain-specific shorthand;
- long multi-document arguments where meaning depends on context outside the pasted material;
- benign uses of words that usually indicate pressure;
- languages outside the strongest calibration path.

ALETHEIA is English-first. Dutch/Nederlands examples may be used for batch testing, but this is not a general app-wide language-compatibility claim. Other languages may produce incomplete, noisy, or less reliable readings and require extra human review.

## Why ALETHEIA does not simply replace this with LLM analysis

LLMs can sometimes interpret nuance more flexibly, but they can also introduce opacity, hallucination risk, hidden prompt sensitivity, external-call privacy concerns, and false authority. ALETHEIA's current rule-based posture favors reviewability, reproducibility, and local-first restraint.

Future optional language-assistance layers, if ever added, should remain subordinate to the protocol boundary. They must not become automatic approval, live model certification, vendor ranking, hidden scoring authority, or a replacement for human review.

## How to read a signal

A signal should be read as:

> This text may contain a pattern that deserves human review.

It should not be read as:

> ALETHEIA has decided what is true or what must happen.

## Suggested receipt language

When showing or documenting signal results, use language like:

> Signal basis: transparent rule-based heuristic detection. This reading may miss subtle, ironic, culturally specific, multilingual, or context-dependent meaning. Human review remains required.

Avoid language like:

- AI verdict;
- final determination;
- certified safe;
- certified ethical;
- proven corrupt;
- legally invalid;
- automatic decision.

## Contributor rule

Contributors may improve signal coverage, examples, tests, and documentation, but should not hide the signal basis or make the mirror sound more capable than it is.

Any change to signal patterns, signal weights, verdict routing, ASYLUM / THRESHOLD / SANCTUARY taxonomy, or receipt wording should include explicit tests and human review.


## Signal dictionary

Patch 106 adds `docs/SIGNAL_DICTIONARY.md` as a reviewer-facing glossary of signal families. The dictionary explains common review questions, typical cues, possible false positives, and repair directions. It is a signal dictionary, not a scoring specification, and it does not replace source code, tests, receipts, or human review.

## Boundary statement

ALETHEIA surfaces signals. Humans keep the judgment.
