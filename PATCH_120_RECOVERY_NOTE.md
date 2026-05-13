# Patch 120 Recovery Note - Module Intro Extraction Step 2

Patch 120 continues the copy-only module intro extraction started in Patch 119.

## What changed

- Extended `ui/module_intro.py`.
- Added `render_boundary_cases_intro(container=None)`.
- Added `render_consent_audit_intro(container=None)`.
- Replaced the inline Boundary Cases calibration `st.info(...)` block in `app.py`.
- Replaced the inline Consent-Audit heading and short intro `st.write(...)` block in `app.py`.
- Added `tests/test_patch_120_module_intro_extraction_step_2.py`.
- Updated patch status, progress, architecture, patch index, README, and protocol baseline manifest.

## Recovery steps

If Patch 120 needs to be reverted:

1. Restore the Boundary Cases inline `st.info(...)` text in `app.py`.
2. Restore the Consent-Audit inline `st.markdown(...)` and `st.write(...)` intro in `app.py`.
3. Remove the Patch 120 helper imports/calls from `app.py`.
4. Remove `render_boundary_cases_intro` and `render_consent_audit_intro` from `ui/module_intro.py`.
5. Remove Patch 120 docs/tests/status entries.
6. Restore `data/protocol_baseline_manifest.json` to the Patch 119 baseline.

## Boundary

This patch is copy-only. It does not move scoring, verdict-routing, signal patterns, signal weights, receipt schemas, module routing, session state, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, external calls, telemetry, analytics, storage, identity sync, certification, enforcement, privacy guarantee, or final truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
