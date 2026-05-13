# ALETHEIA Public Release Polish v1

**Patch:** 114 — Public Release Polish v1  
**Purpose:** make the public entry path clearer after the Public Trust Package consolidation.  
**Runtime effect:** none.

ALETHEIA is a **mirror, not a throne**. It surfaces governance-risk signals and review questions for human judgment. It does not decide, enforce, certify, approve, punish, or replace human review.

## Public entry path

A first-time public reviewer should be able to follow this path without reading the full patch history first:

1. Read the short project summary in `README.md`.
2. Read the boundary statement in `docs/BOUNDARY.md`.
3. Check privacy and hosted-use limits in `docs/privacy_boundary.md` and `docs/hosting_limits.md`.
4. Review the signal basis in `docs/signal_detection.md` and `docs/SIGNAL_DICTIONARY.md`.
5. Try the beginner path in `docs/beginner_ux.md`.
6. Use `docs/public_trust_package.md` as the central review map.
7. Use `docs/public_review_checklist.md` before relying on any reading.

## Public wording standard

Use this wording when introducing ALETHEIA:

> ALETHEIA is a free, open-source governance mirror. It helps people review pressure around power, consent, evidence, appeal, capture risk, privacy posture, and human review. Its outputs are internal governance-risk readings and repair prompts, not verdicts or certifications.

Avoid wording that implies ALETHEIA is a neutral authority, final evaluator, compliance engine, legal/medical/political/religious advisor, safety guarantee, privacy guarantee, or final-truth system.

## Recommended public links

Prefer direct repository and documentation links over shortened links. Direct links are easier for reviewers to inspect, archive, and trust.

## local-first public note

For public demos, hosted Streamlit is useful for light review. For sensitive audits, run ALETHEIA locally. hosted deployments may have platform-level logs outside ALETHEIA's application-code boundary.

## Release boundary

This patch polishes public framing only. It does not change app behavior, scoring, routing, signal patterns, receipts, external calls, telemetry, analytics, storage, certification, enforcement, or authority boundaries.

**ALETHEIA surfaces signals. Humans keep the judgment.**
