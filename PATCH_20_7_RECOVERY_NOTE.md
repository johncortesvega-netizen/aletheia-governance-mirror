# ALETHEIA PATCH 20.7 RECOVERY NOTE

Patch: 20.7
Name: Batch Results UI Polish
Type: UI display polish only

## Intent
Make the Batch Testing result table easier to read after Patch 20.6 question-set classification.

## Touched files
- app.py
- tests/test_patch_20_7_batch_results_ui_polish.py
- PATCH_20_7_RECOVERY_NOTE.md

## Do not touch
- protocol.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/witness.py
- core/empirical.py
- verdict formulas
- witness hashes
- batch receipt generation
- Global Grid logic

## Expected behavior
- Stored batch summary values remain machine-readable.
- The visible table maps:
  - State -> Type
  - Risk -> Role
  - Label -> Reading
  - QUESTION_PROMPT -> Question
  - Review Tool -> Review
  - Audit Question / Review Tool -> Audit question
- The ZIP contents and receipt JSON are unchanged.

## Rollback
Remove this patch and revert only the batch-summary display block in app.py. No backend rollback should be needed.

## Validation
- python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py
- python -m pytest tests -q
