# Patch 204 — Recovery Note

If Patch 204 causes an unexpected issue, restore the previous `core/semantic_pressure_scanner.py` from the last known-good commit or from Patch 203 plus Patch 197 as appropriate.

This patch is intentionally narrow: it only updates the deterministic semantic scanner calibration for opaque capture-power claims. It does not alter module scoring, receipt schemas, external calls, telemetry, storage, certification, enforcement, or final-truth behavior.
