# Patch Notes

## Patch 251 — Evidence Lab Bridge Removal Import Hotfix

Patch 251 fixes a missing import introduced by the Evidence Lab bridge-removal refactor. The extracted page uses `hashlib.sha256()` to build an active-input signature but did not import `hashlib` locally.

Changed:
- `ui/pages/evidence_lab.py` now imports `hashlib` explicitly.

Not changed:
- scanner logic
- scoring
- MEI7 gate
- Z-axis
- Evidence Lab calculations
- World Lens math
- receipts
- telemetry/storage
- authority-boundary behavior
