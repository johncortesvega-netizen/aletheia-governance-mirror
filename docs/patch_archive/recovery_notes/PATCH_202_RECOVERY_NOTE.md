# Patch 202 — Stress Test Tab Containment Rollback

## What this patch fixes

A UI regression could make the app render multiple tab panels as one long continuous page after entering or using Stress Test. This made the module surface look like a continuous wall of text instead of one active tab.

## Root cause

A previous CSS containment guard used broad `:has()` / `nth-of-type` selectors to force inactive Streamlit tab panels hidden. In some Streamlit/browser combinations, and especially with nested tab surfaces, this can interact badly with Streamlit's own tab rendering.

## What changed

The broad containment guard has been removed. The app now keeps only a narrow rule that hides panels already marked hidden by Streamlit.

## Validation

Run:

```bat
python -m py_compile app.py
python -m streamlit run app.py
```

Manual check:
1. Open the app.
2. Enter main ALETHEIA tools.
3. Click Stress Test.
4. Run a Stress Test input.
5. Switch between tabs.
6. Confirm only the selected module is visible and the page is not one long continuous stack.

## Boundary

This patch changes UI containment CSS only. It does not change scores, scanners, receipt values, module logic, privacy posture, or authority boundaries.
