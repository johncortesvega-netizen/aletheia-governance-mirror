# Patch 196 — Receipt Reader Automatic Semantic Reading

## Status
READY FOR LOCAL REVIEW

## What changed
Receipt Reader now attaches and renders a current semantic reading automatically for uploaded receipts instead of requiring an optional button-triggered re-read.

## Why
Receipt Reader should show the semantic comparison consistently across every receipt surface so users can compare the original receipt with the current Semantic Pressure Scanner v1 reading without hunting for a manual action.

## Scope
Changed `ui/receipt_reader.py` only.

## Preserved boundaries
- The current semantic reading is not part of the original receipt.
- Native receipt fields remain copied, not inferred.
- Standard View remains the receipt interpretation layer.
- The current semantic reading does not rescore, modify, certify, approve, reject, or override the uploaded receipt.
- Batch ZIP summaries include semantic findings for each receipt, but no merged verdict is created.

## Validation
Run:

```bat
python -m py_compile ui\receipt_reader.py
python -m py_compile app.py core\semantic_pressure_scanner.py ui\receipt_reader.py ui\unit_preview.py
```

Manual checks:
1. Upload one receipt and verify `Current semantic reading` appears automatically.
2. Upload a ZIP of receipts and verify the index has a `Current Semantic` column for every receipt.
3. Inspect a selected receipt from the batch and verify the current semantic reading appears once, not twice.
4. Confirm native values and audit data remain unchanged.
5. Confirm debug details require the explicit checkbox.
