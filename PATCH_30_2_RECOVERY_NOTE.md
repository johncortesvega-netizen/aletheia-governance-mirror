# PATCH 30.2 — Positive CR Verdict Stabilizer + EDD Receipt Guard

## Purpose

Patch 30.2 addresses the calibration issue found after batch-testing the 40 Cognitive Resilience scenarios:

- Group 1 positive Cognitive Resilience scenarios were diagnostically recognized as high CR, but still landed too often in THRESHOLD or ASYLUM.
- Group 2 and Group 3 were improved by Patch 30.1 and must not be loosened.
- Patch 30 Education Defense diagnostics must remain visible in local witness receipts.

## Design rule

High Cognitive Resilience may only stabilize a verdict when all of the following are true:

- `cognitive_resilience_signal == "high"`
- `educational_decentralization_signal` is `medium` or `high`
- `central_info_capture_signal == "low"`
- `education_defense_signal == "protected"`
- `capture_architecture_signal` is not present
- `high_cr_laundering_blocked` is false
- contextual capture count is 0
- grip marker count is 0
- central info capture terms are absent
- capture/relinquish terms are absent

If any capture architecture exists, the stabilizer does nothing.

## Files touched

- `core/cognitive_resilience.py`
- `app.py`
- `tests/test_patch_30_2_positive_cr_verdict_stabilizer.py`
- `PATCH_30_2_RECOVERY_NOTE.md`

## What changed

### `core/cognitive_resilience.py`

Added `positive_cr_baseline_stabilizer(judgment, report)`.

This function can soften an over-hard local Mirror Check result only for safe positive CR baseline scenarios. It does not change scoring formulas, does not create enforcement, and does not classify people.

Capture still blocks stabilization.

### `app.py`

- Imports the Patch 30.2 stabilizer.
- Applies it after local/LLM judgment inside Mirror Check.
- Updates `APP_VERSION` to `v9.6.9-patch30-2-cr-verdict-stabilizer`.

### Tests

Added tests for:

1. Positive CR baseline can stabilize an over-hard ASYLUM result.
2. High education + capture architecture is not laundered.
3. Safety/objectivity capture is not overridden.
4. Education Defense diagnostics remain visible in witness receipts.

## Verification

Patch-only test:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_30_2_positive_cr_verdict_stabilizer.py -q
```

Expected:

```text
4 passed
```

Combined CR/capture chain:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_27A_cognitive_resilience_calibration.py tests/test_patch_27B_cognitive_resilience_diagnostic.py tests/test_patch_28_educational_decentralization_scoring.py tests/test_patch_28_1_safety_objectivity_capture_multiplier.py tests/test_patch_29_hard_capture_receipt_trace.py tests/test_patch_29_1_demo_input_receipt_guard.py tests/test_patch_30_education_defense.py tests/test_patch_30_1_cr_contextual_capture_calibration.py tests/test_patch_30_2_positive_cr_verdict_stabilizer.py -q
```

Observed locally:

```text
131 passed, 17 xfailed, 23 xpassed
```

## Boundary check

Patch 30.2 does not add:

- Global ID sync
- public ledger
- push-warning authority layer
- automatic enforcement
- centralized truth authority
- user/person classification as malicious

Power → Mirror. Never Mirror → Power.
