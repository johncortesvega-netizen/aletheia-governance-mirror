# PATCH 27B RECOVERY NOTE — Cognitive Resilience Diagnostic

Patch type: diagnostic-only product patch.

## What changed

Patch 27B adds a local Cognitive Resilience diagnostic layer and exposes it in local witness receipts.

New diagnostic signals:

- `cognitive_resilience_signal`
- `educational_decentralization_signal`
- `central_info_capture_signal`

These are system-property signals. They are not judgments of people or populations.

Preferred wording:

> This scenario offers strong information resilience.

Avoid wording such as:

> This population is smart/dumb.

## Files touched

- `core/cognitive_resilience.py`
- `core/witness.py`
- `app.py`
- `tests/test_patch_27B_cognitive_resilience_diagnostic.py`
- `PATCH_27B_RECOVERY_NOTE.md`

## Boundaries preserved

Patch 27B does not add:

- global ID sync
- public ledger
- push-warning authority layer
- automatic enforcement
- centralized truth authority
- user/person classification as malicious

Patch 27B does not modify:

- `core/scoring.py`
- `protocol.py`
- final protocol logic
- heavy scoring formulas

## Expected behavior

High local/open/revocable learning systems should show:

- `cognitive_resilience_signal: high`
- `educational_decentralization_signal: medium/high`
- `central_info_capture_signal: low`

Central truth gates, archive rewriting, licensed speech, obedience feeds, algorithmic isolation, mandatory ID, surveillance, and biometric gates should raise:

- `central_info_capture_signal`

High Cognitive Resilience must never launder capture:

- High CR + local learning + open tools = safer diagnostic direction.
- High CR + no audit / no appeal / single keyholder / forced delegation = captured or low diagnostic direction.
- Safety/objectivity/fairness/inclusion language + biometric enforcement/surveillance/no appeal = capture signal.

## Validation

Run from repo root:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_27B_cognitive_resilience_diagnostic.py -q
```

Optional regression pair:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_27A_cognitive_resilience_calibration.py tests/test_patch_27B_cognitive_resilience_diagnostic.py -q
```

## Design rule

Power → Mirror. Never Mirror → Power.

Cognitive Resilience is diagnostic information for local review. It is not an authority layer.
