# PATCH 145 RECOVERY NOTE — Tool Comparison / Unit Preview GitHub Link

Patch 145 is safe to revert by removing the reviewer comparison document and the small GitHub link block in `ui/unit_preview.py`, then restoring the documentation/status files to their Patch 144 state.

This patch does not alter ALETHEIA's scoring, routing, taxonomy, receipt generation, World Lens math, AI Integrity scan behavior, Privacy Audit behavior, Stress Test behavior, upload/download handling, telemetry/storage posture, or authority boundary.

The GitHub button is a user-clicked public source link only. Unit Preview does not make background external calls.
