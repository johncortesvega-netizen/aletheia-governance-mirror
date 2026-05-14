# ALETHEIA Public Trust Package

**Version:** v1.0  
**Consolidated for:** Patch 114 — Public Release Polish v1  
**Base consolidation:** Patch 113 — Public Trust Package Consolidation  
**Last updated:** 2026-05-13

This is the central review map for people who want to inspect, run, adapt, or contribute to ALETHEIA. It collects the trust-relevant documents added across the structural improvement sequence without turning them into a certification package.

ALETHEIA is a **mirror, not a throne**. It surfaces governance-risk signals and review questions around power, consent, evidence, appeal, capture risk, privacy posture, and human review. It does not decide, enforce, certify, approve, punish, or replace human judgment.

## What this package is

This package is a review path. It helps reviewers find the project boundaries, signal-detection limits, privacy/local-first posture, architecture notes, beginner path, patch history, and public-review checklist.

## What this package is not

This package is not a trust guarantee, security audit, privacy guarantee, compliance approval, vendor audit, legal opinion, ethics certification, institutional authorization, or proof of final truth. It does not certify truth, safety, legality, ethics, privacy, security, or legitimacy.

## Recommended review order

### 1. Boundary and authority

Read:

- `docs/BOUNDARY.md`
- `docs/scope_layers.md`
- `docs/ethics.md`

Review question: does the project preserve the non-authority boundary and keep human judgment outside the system?

### 2. Privacy and hosted-use posture

Read:

- `docs/privacy_boundary.md`
- `docs/hosting_limits.md`
- `docs/go_live_privacy_review_statement.md`
- `docs/privacy_audit_panel_v1.md`

Key wording:

> ALETHEIA is local-first by design. For sensitive audits, run ALETHEIA locally. Hosted deployments may have platform-level logs outside ALETHEIA's application-code boundary.

Review question: is the material sensitive enough that it should only be reviewed locally?

### 3. Signal detection and limits

Read:

- `docs/signal_detection.md`
- `docs/SIGNAL_DICTIONARY.md`

Review question: are the visible signals useful as review prompts, while remembering that rule-based and heuristic detection may miss nuance, irony, coded language, cultural context, domain shorthand, or languages outside the strongest English/Dutch calibration path?

### 4. Architecture and maintainability

Read:

- `docs/architecture.md`
- `docs/structural_improvement_entrypoint.md`
- `docs/new_contributor_start_here.md`
- `CONTRIBUTING.md`

Review question: does the project remain reviewable as a Streamlit app whose `app.py` is being reduced gradually through small behavior-preserving shell extractions?

### 5. Beginner path

Read:

- `docs/beginner_ux.md`
- `ui/beginner_guide.py`

Review question: can a first-time reviewer understand the safe path from Mirror Check to risk reading, observed reasons, repair questions, and optional local receipt download?

### 6. Patch history

Read:

- `docs/patch_index.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- latest `PATCH_*_MANIFEST.txt`
- latest `PATCH_*_RECOVERY_NOTE.md`

Review question: can a reviewer inspect one patch at a time without treating patch history as proof of correctness?

### 7. Public-review checklist

Read:

- `docs/public_review_checklist.md`

Review question: did the reviewer check the boundary, privacy posture, signal basis, evidence basis, repair questions, and human-review requirements before relying on any reading?

## Current structural sequence

| Patch | Trust layer | Runtime effect |
| --- | --- | --- |
| 102 | Architecture and contributor entry point | No runtime behavior change |
| 103 | Signal-detection transparency | No runtime behavior change |
| 104 | Boundary, privacy, and hosted-use transparency | No Streamlit page wiring change |
| 105 | Patch-history and trust navigation | No runtime behavior change |
| 106 | Signal dictionary and glossary | No runtime behavior change |
| 107 | Boundary/privacy UI wiring | Narrow UI wiring only |
| 108 | App shell refactor step 1 | Static shell extraction only |
| 109 | App shell refactor step 2 | Static shell extraction only |
| 110 | App shell refactor step 3 | Static shell extraction only |
| 111 | Beginner try-this-first UX | Static UX helper only |
| 112 | Privacy Audit Panel v1 | Static pasted-artifact review UI only |
| 113 | Public Trust Package consolidation | Documentation/navigation only |
| 114 | Public release polish and public entry path | Documentation/release-surface only |
| 115 | App shell refactor step 4 sidebar tuning copy | Static shell extraction only |

## Local run path

For sensitive audits, run ALETHEIA locally:

```bash
git clone https://github.com/johncortesvega-netizen/aletheia-governance-mirror.git
cd aletheia-governance-mirror
pip install -r requirements.txt
streamlit run app.py
```

Hosted deployments are useful for public demonstration and light review, but they may involve platform-level logs outside ALETHEIA's application-code boundary.

## Manual verification before relying on a reading

Before relying on an ALETHEIA reading, manually inspect:

- the input text or uploaded artifact;
- the visible evidence basis;
- the signal categories and snippets;
- the repair questions;
- the boundary statement;
- the local-vs-hosted privacy posture;
- the limits of rule-based/heuristic detection;
- whether a human reviewer with domain context is needed.

## Final boundary

This package organizes review evidence. It does not create authority.

**ALETHEIA surfaces signals. Humans keep the judgment.**

## Patch 116 note — footer shell extraction

Patch 116 moves the stable footer banner into `ui/app_shell.py` so public shell copy is easier to inspect alongside the other app-shell helpers. This is not a trust certification and does not change scoring, routing, receipts, signal logic, privacy posture, or authority boundaries.


## Patch 117 note — refactor stabilization checkpoint

Patch 117 adds `docs/refactor_stabilization_checkpoint.md` and a focused regression test for the app-shell refactor sequence. This helps public reviewers see that the recent `app.py` reduction is still bounded: `ui/app_shell.py` is static shell copy, and `app.py` remains responsible for interactive controls, session state, module routing, scoring, receipts, downloads, and analysis behavior.

This checkpoint is not a certification, privacy guarantee, compliance approval, enforcement mechanism, or final-truth claim. It is review evidence only. Humans keep the judgment.

## Patch 118 note — beginner UX polish

Patch 118 strengthens the beginner path by adding a first-audit checklist, clearer meaning/non-meaning language, and stop-and-review prompts to `ui/beginner_guide.py` and `docs/beginner_ux.md`. This helps public reviewers understand how a first-time user is guided toward human review rather than automatic reliance.

The guide remains static copy. It is not a certification workflow, approval workflow, privacy guarantee, enforcement mechanism, or final-truth claim. Humans keep the judgment.
## Receipt Reader - Standard View Design

Patch 133 adds `docs/receipt_reader_standard_view.md` as a design-only note for a future Receipt Reader - Standard View. The intended reader explains pasted ALETHEIA receipts by keeping native receipt values as source of truth and mapping them secondarily into plain-language review bands for interoperability.

This design is not a certification path. It does not add runtime UI, parsing code, scoring, receipt schema changes, new risk states, external standards as authority, external calls, telemetry, storage, compliance certification language, or final-truth claims. Human review remains required.
