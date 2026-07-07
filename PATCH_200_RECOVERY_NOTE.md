# Patch 200 — Simple English Receipt Walkthrough

## Status
READY FOR LOCAL REVIEW

## What changed
Patch 200 adds a simple four-step translation layer to Receipt Reader Standard View. It turns the technical receipt into a basic-English path for non-technical readers:

1. **What is this document?** Explains that the receipt is a private/local ALETHEIA review support artifact, not a legal document or real-world decision.
2. **Main warning/status.** Explains the native receipt state in plain language and, when available, describes the raw-to-adjusted integrity gap without inventing missing raw metrics.
3. **Big problems to inspect.** Translates receipt pressure into simple review areas: central control, correction path, conditional access/safety, and transparency.
4. **Next steps for humans.** Shows simple human hand-off questions and the existing repair-blocker note when present.

The view also adds a three-sentence plain-English summary tailored to the native receipt state and current semantic re-read.

## Boundary preserved
- Explanation/layout only.
- Missing raw metrics are not inferred.
- Native receipt values remain unchanged.
- Current semantic re-read remains diagnostic and does not override the original receipt.
- No receipt schema change.
- No scanner logic change.
- No scoring/routing change.
- No World Lens or Evidence Lab calculation change.
- No external calls, telemetry, storage, certification, enforcement, approval, rejection, or final-truth claim.

## Validation target

```bat
python -m py_compile ui/receipt_reader.py
```
