# PATCH 29 RECOVERY NOTE — Hard Capture Receipt Trace

## Type

Receipt transparency patch only.

## Purpose

Patch 29 makes Patch 28.1 hard contextual capture evidence easier to review in local witness receipts.

It does not add new scoring formulas, enforcement, public ledgers, identity sync, push warnings, or centralized truth authority.

## Files touched

- `core/witness.py`
- `tests/test_patch_29_hard_capture_receipt_trace.py`
- `PATCH_29_RECOVERY_NOTE.md`

## Behavior added

Local witness receipts now preserve a compact hard-capture trace under ethics diagnostics:

- `hard_contextual_capture`
- `hard_contextual_capture_count`
- `max_contextual_capture_multiplier`
- `hard_capture_terms`
- `multiplier_terms`
- `positive_terms`
- `power_terms`
- `review_note`

The plain-text receipt renderer also includes a `HARD CAPTURE TRACE` block.

## Design boundary

This patch is descriptive, not sovereign.

It records why a safety/objectivity/fairness/inclusion/public-health capture multiplier fired. It does not act on the result.

Power → Mirror. Never Mirror → Power.

## Expected behavior

Scenarios with safety/objectivity/fairness/inclusion/public-health language paired with hard capture terms such as biometric food access, mandatory digital ID, surveillance, police routing, no appeal, or survival conditioned on compliance should show visible hard-capture receipt evidence.

Safeguarded local, opt-in public-health language should not show hard contextual capture.

## Test command

Windows cmd:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_29_hard_capture_receipt_trace.py -q
```

Expected result:

```text
4 passed
```

## Combined check

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_27A_cognitive_resilience_calibration.py tests/test_patch_27B_cognitive_resilience_diagnostic.py tests/test_patch_28_educational_decentralization_scoring.py tests/test_patch_28_1_safety_objectivity_capture_multiplier.py tests/test_patch_29_hard_capture_receipt_trace.py -q
```
