# Patch 32.1 — Plain Repair Question Bank Routing

Type: UI / repair-loop routing polish.

## Goal
Use the plain-language Repair Questions v2 bank as the default small question set for normal Mirror Check reviews.

## Behavior
- Embed the 50 plain repair questions in `app.py`.
- Route by risk family instead of showing a generic or overly broad question set.
- Select 3–7 questions; current UI uses 5.
- Keep questions reflective, not commanding.
- Keep uploaded question banks classified as `QUESTION_PROMPT / Review Tool`.

## Hard boundaries
No product authority added:
- no Global ID sync
- no public ledger
- no automatic enforcement
- no push-warning layer
- no centralized truth authority
- no user/person classification as malicious

ALETHEIA remains a mirror. People decide.

## Acceptance test

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_32_1_plain_repair_question_routing.py -q
```

Expected:

```text
6 passed
```
