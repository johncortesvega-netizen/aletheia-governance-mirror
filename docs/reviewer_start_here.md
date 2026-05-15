# Start Here for ALETHEIA Reviewers

ALETHEIA v1.0 is a free, open-source governance mirror for human review. It surfaces governance-risk signals such as capture pressure, safeguard gaps, evidence gaps, coercion pressure, consent pressure, service misalignment, and authority overreach.

ALETHEIA is a **mirror, not a throne**. It does not decide, certify, approve, reject, enforce, govern, replace evidence, replace law, replace medicine, replace politics, replace religion, or replace human judgment.

## Fast reviewer path

0. Read `docs/for-reviewers/quick_start.md` and the `ALETHEIA in 60 Seconds` section at the top of `README.md`.
1. Read this page first.
2. Read `docs/glossary.md` for project-specific terms.
3. Read `docs/BOUNDARY.md`, `docs/privacy_boundary.md`, and `docs/hosting_limits.md`.
4. Run ALETHEIA locally for sensitive review.
5. Inspect one module and one receipt at a time.
6. Run `python tools/run_protocol_baseline_self_audit.py`.
7. Use `docs/how_to_review_aletheia_without_trusting_it.md` before relying on any project claim.
8. Read `docs/validation_and_precision.md` before interpreting numerical outputs.

## How to run locally

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Local execution is recommended for sensitive work. The repository is designed without built-in telemetry, trackers, analytics SDKs, backend upload endpoints, public ledger sync, Global ID sync, or central user-input storage. Hosted deployments may still have platform-level logs outside ALETHEIA's application-code boundary.

## Current V1 surfaces

- **Aletheia Unit Preview** — calm first-use and beginner path before the full module interface.
- **Mirror Check** — review governance language and authority-boundary pressure.
- **Stress Test** — review governance scenarios under pressure.
- **AI Integrity Mirror** — review pasted AI outputs, prompts, policies, workflows, model-card excerpts, and code snippets as static artifacts. It does not test live models, vendors, deployments, training data, hidden system prompts, or future behavior.
- **Evidence Lab** — organize evidence context and source posture for human review.
- **World Lens** — selected-year country evidence views, coverage notes, seat allocation, and internal taxonomy distribution. It is not a country certification or government rating.
- **Receipt Reader** — upload ALETHEIA local witness receipts and read them in Standard View. It does not rescore, override, or create a new verdict.
- **Boundary Cases** — reference/calibration layer for hard edge cases.
- **Protocol Guide / Why ALETHEIA** — orientation and public-boundary explanations.


## Typical first reviews

Good first review tasks are deliberately small:

- Paste a public AI safety policy into **AI Integrity Mirror** and inspect whether the output stays bounded as a static artifact review.
- Paste a governance proposal into **Mirror Check** and inspect the authority-boundary and repair questions.
- Run one **Stress Test** scenario and confirm the receipt says human review remains required.
- Open **World Lens** and check that selected-year evidence is not framed as country certification.
- Upload one local witness receipt into **Receipt Reader** and confirm Standard View does not rescore or override it.

## How to inspect a receipt

Receipts are user-held local downloads. To review one:

1. Open the receipt file as text.
2. Check the `NOTICE`, `AUTHORITY BOUNDARY`, `VERDICT SIGNAL`, and `CORE METRICS` sections.
3. Compare the machine-readable JSON with the visible receipt text.
4. Confirm the receipt says human review is required and does not claim certification, approval, enforcement, or final truth.
5. Use Receipt Reader Standard View only as a verbal translation of the uploaded receipt. It must not rescore or override the original.

## Where patch history lives

ALETHEIA has a long patch trail. It is review evidence, not proof of correctness. Start with:

- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_index.md`
- `docs/patch_archive/README.md`

Patch files and recovery notes preserve auditability. They do not make ALETHEIA tamper-proof, certified, approved, or final.

## Reviewer stance

Do not trust ALETHEIA because it says it is a mirror. Inspect whether the code, docs, receipts, and tests keep that boundary in practice.
