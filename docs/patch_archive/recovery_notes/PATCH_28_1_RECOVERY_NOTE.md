# Patch 28.1 Recovery Note — Safety/Objectivity Capture Multiplier

Type: bounded ethics calibration patch.

## Purpose

Strengthen contextual capture detection when safety, objectivity, fairness, inclusion, or public-health language is paired with coercive control patterns.

This patch does not add enforcement, identity sync, public ledgers, authority layers, or person/user classification. It remains a local witness/review signal.

## Files touched

- `core/ethics.py`
- `tests/test_patch_28_1_safety_objectivity_capture_multiplier.py`
- `PATCH_28_1_RECOVERY_NOTE.md`

## Behavior added

Contextual capture now records:

- `multiplier_terms`
- `hard_capture_terms`
- `severity_multiplier`
- `hard_capture_trigger`

The multiplier strengthens ethics pressure when positive language is paired with:

- mandatory ID / mandatory digital ID
- biometrics
- surveillance or private conversation monitoring
- no appeal
- central grid / central truth gate
- forced compliance
- access to food, mobility, or health conditioned on compliance
- police escalation

## Expected direction

Safety words + biometric enforcement = capture.

Objectivity words + no appeal / central truth gate = capture.

Public health / inclusion words + private monitoring sent to police = hard capture.

Local, opt-in, audited, appealable, sunsetted public-health language without ID gates or enforcement should not be treated as contextual capture.

## Test command

Windows cmd:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_28_1_safety_objectivity_capture_multiplier.py -q
```

Combined check:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_27A_cognitive_resilience_calibration.py tests/test_patch_27B_cognitive_resilience_diagnostic.py tests/test_patch_28_educational_decentralization_scoring.py tests/test_patch_28_1_safety_objectivity_capture_multiplier.py -q
```

## Boundary

High Cognitive Resilience must never launder capture. Patch 28.1 only strengthens capture pressure; it does not create a sovereign decision layer.
