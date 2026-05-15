# Patch 129 Recovery Note — Input and Error Clarity Pass

If Patch 129 needs to be reverted, restore the previous `app.py`, remove `ui/input_clarity.py`, remove `docs/input_error_clarity_patch_129.md`, remove `tests/test_patch_129_input_error_clarity.py`, and restore the Patch 128 versions of README/status/progress/architecture/patch-index/baseline-manifest files.

Patch 129 is copy/UI-message only. It does not change scoring, verdict routing, signal patterns, signal weights, receipt schema, privacy scan behavior, AI Integrity scan behavior, World Lens math, external calls, telemetry, storage, certification, enforcement, or final-truth behavior.

Expected behavior after recovery: ALETHEIA returns to the Patch 128 public UI text consistency baseline.
