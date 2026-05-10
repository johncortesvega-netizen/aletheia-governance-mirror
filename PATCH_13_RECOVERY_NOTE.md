# ALETHEIA PATCH RECOVERY NOTE

Patch: 13
Name: Code Hygiene + Language Consistency
Type: Cleanup / low-risk refactor

## Intent

Keep the working Patch 12 build clean before adding new intelligence layers.
This patch removes minor technical debt and aligns repair-loop text with the
English app voice introduced in Patch 10.

## Touched files

- `app.py`
- `protocol.py`
- `core/parser.py`
- `requirements.txt`
- `requirements-llm.txt`
- `tests/test_protocol_repair_loop.py`
- `tests/test_patch_13_hygiene_contract.py`
- `PATCH_13_RECOVERY_NOTE.md`

## What changed

- Removed duplicate `import hashlib` from `app.py`.
- Converted `protocol_repair_questions(...)` from Dutch to English.
- Made OpenAI optional in `core/parser.py`; local scan remains the fallback.
- Moved `openai>=1.30` into `requirements-llm.txt` so local/core builds stay lighter.
- Added tests for cleanup and language consistency.

## Not touched

- No scoring formulas changed.
- No verdict logic changed.
- No capture-marker logic changed.
- No witness hashing changed.
- No UI layout changed.
- No empirical validation claims added.
- No Global ID sync, public ledger, or push-warning behavior added.

## Recovery

If this patch causes trouble:

1. Restore the duplicate-safe import section from Patch 12 `app.py` if needed.
2. Restore the previous `protocol_repair_questions(...)` text block if Dutch output was intentional.
3. Move `openai>=1.30` back into `requirements.txt` if the deployment expects AI Deep Scan as a hard dependency.
4. Remove `requirements-llm.txt` and `tests/test_patch_13_hygiene_contract.py`.

## Validation

Run:

```bash
python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py
python -m pytest tests -q
```
