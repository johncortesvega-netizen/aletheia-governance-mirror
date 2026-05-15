# PATCH 29.1 — Demo Input Receipt Guard

Type: receipt clarity / auditability patch.

## Purpose

Patch 29.1 makes bundled demo/sample receipts visibly non-evaluative without changing scoring, protocol classification, ethics logic, Cognitive Resilience logic, or app enforcement behavior.

## Change

When a local witness receipt is built with `input_status="DEMO_INPUT"` or `input_type="DEMO_INPUT"`, the receipt now includes:

- `demo_mode: true`
- `demo_warning: "Demo/sample input: this receipt is for interface review only and should not be treated as a real scenario assessment."`

The rendered plain-text receipt also shows:

```text
Demo mode: True
Demo warning: Demo/sample input: this receipt is for interface review only and should not be treated as a real scenario assessment.
```

Regular user receipts keep `demo_mode: false`, `demo_warning: null`, and do not display the demo warning block.

## Hard boundaries preserved

This patch does not add:

- Global ID sync
- Public ledger
- Push-warning authority layer
- Automatic enforcement
- Centralized truth authority
- User/person classification as malicious

ALETHEIA remains local-first, witness-based, reviewable, non-sovereign, and mirror-only.

Power → Mirror. Never Mirror → Power.

## Files touched

- `core/witness.py`
- `tests/test_patch_29_1_demo_input_receipt_guard.py`
- `PATCH_29_1_RECOVERY_NOTE.md`

## Verification

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_29_1_demo_input_receipt_guard.py -q
```

Expected:

```text
4 passed
```
