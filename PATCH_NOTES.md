# Patch — Semantic No-Signal Disconnect Fix

## Purpose
Fixes a UI mismatch where the semantic diagnostic panel could display `SANCTUARY` even when it had detected no semantic relationship at all, while the primary module reading showed `THRESHOLD` or `ASYLUM`.

## Change
- Keeps the scanner's internal output unchanged.
- Updates only the semantic panel display layer in `app.py`.
- If the semantic scan has no claims, no mechanisms, no modal pressure, no reversibility signal, no fail-closed flag, no proximity hits, and zero integrity pressure, the panel now displays:
  - `Semantic finding: NO SIGNAL`
  - `No semantic pressure relationship detected. This does not lower or override the main module reading.`
- Renames the visible card label from `State` to `Semantic finding` to make clear it is subordinate to the main module reading.

## Boundary
No scoring, scanner logic, receipts, taxonomy labels, or module readings are changed. This is a UI interpretation fix only.

## Validation
Run:

```bat
python -m py_compile app.py
python -m streamlit run app.py
```

Test with a main-reading high-risk or threshold case that has no semantic pressure terms. The main reading may remain ASYLUM/THRESHOLD, while the semantic panel should show `NO SIGNAL`, not `SANCTUARY`.
