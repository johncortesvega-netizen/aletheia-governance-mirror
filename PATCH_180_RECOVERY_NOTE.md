# PATCH 180 Recovery Note

## Summary
Patch 180 is a display/text correction for Local Witness receipts, especially Stress Test receipts and batch receipt files. It does not change stored values, scoring, routing, taxonomy, receipt schema, hashes, JSON exports, World Lens math, Evidence Lab calculations, AI Integrity scan logic, or protocol-engine behavior.

## What changed
- Plain-English receipt summaries now label Stress Test metrics as diagnostic metrics.
- The summary explains that protocol guardrails may route a receipt to THRESHOLD or ASYLUM even when raw simulation diagnostics look moderate.
- AI static scan context now separates effective receipt-context state/risk/label from raw static scan state/risk/label.

## Recovery
If this patch needs to be reverted, restore `core/witness.py` and the listed tests from the previous patch state, then rerun:

```bat
python tools\run_patch_checks.py 180
python tools\run_patch_checks.py 179
python tools\run_patch_checks.py 178
```

Human review remains required.
