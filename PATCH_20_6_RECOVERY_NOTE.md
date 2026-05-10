# ALETHEIA PATCH 20.6 RECOVERY NOTE

Patch: 20.6
Name: Batch Question Set Classification
Type: batch classification / receipt wording guardrail

Intent:
- Treat uploaded/pasted audit question banks as review tools, not policy proposals.
- Prevent Dutch or English audit questions from becoming OUT_OF_SCOPE or ASYLUM just because they mention risk terms.
- Keep the Batch Testing panel separate from the normal tree scanner.

Touched files:
- app.py
- core/witness.py
- tests/test_patch_20_6_question_set_classification.py
- PATCH_20_6_RECOVERY_NOTE.md

Do not touch:
- protocol.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/empirical.py
- verdict formulas
- witness hash mechanics
- Global Grid logic

Expected behavior:
- Numbered question banks are detected as QUESTION_SET / QUESTION_PROMPT.
- Batch summary rows show QUESTION_PROMPT / Review Tool for audit questions.
- Real scenario batches still use the normal local Mirror Check path.
- Each batch item still gets its own local receipt and ZIP archive.

Rollback:
- Revert app.py and core/witness.py to Patch 20.5.
- Remove this recovery note and the Patch 20.6 test file.

Validation:
- python -m py_compile app.py core/witness.py
- python -m pytest tests -q
