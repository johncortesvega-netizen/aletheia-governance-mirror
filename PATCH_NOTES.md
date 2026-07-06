# Patch S3.2 — Semantic debug hard-hide

Changed file:
- app.py

Purpose:
- Keep semantic panels useful for normal review while preventing raw debug machinery from dominating World Lens, Stress Test, Mirror Check, or Evidence Lab.

Changes:
- Replaced the always-rendered nested "Developer/debug details" expander with an explicit checkbox:
  - "Show developer/debug details"
- Default is OFF.
- When OFF, the UI does not render:
  - contextual proximity hits table
  - normalized text area
  - plain-text semantic report
- When ON, the same diagnostics are still available for calibration/troubleshooting.

No changes to:
- semantic scanner logic
- scores
- receipts
- World Lens flags
- Stress Test/Evidence Lab calculations
