# Patch 163 Recovery Note — Artificial Mind Formation Boundary-Officer Rebrand

Patch 163 is a small copy/documentation/test patch layered on Patch 162.

## Purpose

Reframe the Artificial Mind Formation Theory explainer so ALETHEIA can be
understood as police-officer-like at the AI boundary without becoming a judge.

## Intended meaning

ALETHEIA may:
- observe;
- inspect;
- preserve evidence;
- warn;
- route concerns to human review;
- escalate to human reviewers.

ALETHEIA may not:
- judge final truth;
- decide guilt;
- decide consciousness, personhood, soul, life, legal standing, safety, or worth;
- punish;
- command;
- approve or reject;
- enforce;
- certify;
- claim legal, spiritual, institutional, or final authority.

## Recovery / rollback

To roll back Patch 163 only, restore these files from the Patch 162 state:
- `pages_ui/artificial_mind_formation_page.py`
- `docs/artificial_mind_formation_theory.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

Then remove:
- `tests/test_patch_163_artificial_mind_boundary_officer_rebrand.py`
- `PATCH_163_MANIFEST.txt`
- `PATCH_163_RECOVERY_NOTE.md`

## Validation

Run:

```bat
python tools\run_patch_checks.py 163
```

This patch must remain copy-only and must not change scoring, taxonomy, World
Lens logic, routing, receipt generation, external calls, telemetry/storage, or
any authority/certification behavior.
