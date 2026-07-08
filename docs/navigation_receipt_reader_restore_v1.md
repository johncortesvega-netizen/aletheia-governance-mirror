# Patch 235 — Receipt Reader Navigation Restore

Patch 226 moved the app to single-module navigation so inactive Streamlit tab bodies no longer render in the background. After that change, Receipt Reader remained available only as a support utility under Why ALETHEIA, which made it appear removed from the primary module surface.

Patch 235 restores Receipt Reader as a first-class top-level module in the single-module navigation.

## Boundary

Receipt Reader remains read-only. It does not rescore, certify, approve, reject, enforce, or override original receipts.

## Runtime impact

No scanner, scoring, MEI7 gate, Z-axis, Evidence Lab, World Lens, semantic pressure, witness hash, receipt schema, telemetry, or storage behavior changes.
