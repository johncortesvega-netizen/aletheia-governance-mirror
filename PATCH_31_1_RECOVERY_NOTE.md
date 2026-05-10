# PATCH 31.1 RECOVERY NOTE — Strategic Regression Contract Pack

Type: test/regression contract only.

Patch 31.1 does not add new product logic. It locks the accepted behavior from
Patch 28.1 through Patch 31 so future edits do not silently disconnect the core
ALETHEIA logic.

## Protected behavior

1. Safety/objectivity/fairness/inclusion/public-health language paired with
   coercive architecture must still trigger contextual capture.
2. Clean high Cognitive Resilience scenarios may stabilize toward SANCTUARY / Low.
3. High Cognitive Resilience must never launder capture architecture.
4. Education Defense diagnostics must remain visible.
5. Local witness receipts must expose hard capture trace evidence.
6. World Lens must remain connected to Evidence Lab empirical country-year data
   while marking Mirror Check text-scenario diagnostics as not assessed unless
   actual policy/scenario text is present.

## Hard boundaries

Do not add:

- Global ID sync
- public ledger
- push-warning authority layer
- automatic enforcement
- centralized truth authority
- user/person classification as malicious

ALETHEIA remains local-first, witness-based, reviewable, non-sovereign, and
mirror-not-throne.

Power -> Mirror. Never Mirror -> Power.

## Validation

Run:

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_31_1_regression_contract.py -q
```

Expected:

```text
6 passed
```
