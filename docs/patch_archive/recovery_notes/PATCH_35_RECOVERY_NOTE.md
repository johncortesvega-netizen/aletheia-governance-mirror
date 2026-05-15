# Patch 35 — Failure Classification

Status: recovery checkpoint

## What changed

Added a public-safe Failure Classification layer so ALETHEIA can distinguish where a serious governance-risk issue appears to originate.

## Added

- `docs/failure_classification.md`
- `prompts/failure_classification_prompt.md`
- `tests/test_patch_35_failure_classification.py`

## Updated

- `README.md`
- `about_page.py`
- `app.py`

## Logic added

Four diagnostic failure modes are now documented and surfaced:

1. Actor Failure
2. Policy Failure
3. Implementation Failure
4. Data Failure

## Safety boundary

Failure Classification is diagnostic only.
It does not assign final blame, create enforcement authority, remove leaders, decide guilt, or replace human review.

## Recovery note

If this patch causes problems, remove the Failure Classification docs/prompt/test and revert the small UI/README/About references. No core enforcement logic was added.
