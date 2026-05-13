# New Contributor Start Here

This file gives the shortest safe entry path into ALETHEIA.

## What ALETHEIA is

ALETHEIA is a bounded governance-risk mirror. It helps humans review power, consent, appeal, evidence, capture pressure, and authority-overreach signals.

## What ALETHEIA is not

ALETHEIA is not a throne, judge, oracle, compliance engine, legal tool, medical tool, political authority, religious authority, AI-system certifier, security scanner, privacy certifier, or final truth machine.

## Run locally

Install dependencies and run the app with Streamlit:

```bat
pip install -r requirements.txt
streamlit run app.py
```

For sensitive audits, local use is recommended over hosted use.

## Understand the project shape

Start with:

- `README.md` for public framing;
- `docs/architecture.md` for module structure;
- `docs/structural_improvement_entrypoint.md` for the maintainability path;
- `PATCH_STATUS.md` for the current patch ledger;
- `docs/progress_database.md` for longer continuity notes.

## Understand the signal posture

ALETHEIA uses transparent rule-based and heuristic signal detection in key places. That makes the system explainable and reviewable, but not all-knowing. It may miss nuance, implicit context, irony, culturally specific meaning, or language outside the strongest English/Dutch calibration.

## Understand the patch files

The many `PATCH_*_MANIFEST.txt` and `PATCH_*_RECOVERY_NOTE.md` files are intentional. They preserve a local audit trail of what changed and what boundary was protected. Future documentation should index them better, not erase them.

## First safe edits

Good first edits are usually docs, tests, copy clarity, local setup notes, or behavior-preserving UI polish. Avoid scoring, verdict routing, privacy posture, and authority-boundary logic until you understand the tests and prior patches.
