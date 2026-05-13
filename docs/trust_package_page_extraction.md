# Trust Package Page Extraction

Patch 124 exposes the public trust package review route inside the app through `pages_ui/trust_package_page.py`.

The helper renders document pointers and review prompts only. The source of truth remains the documentation:

- `docs/public_trust_package.md`
- `docs/public_review_checklist.md`
- `docs/BOUNDARY.md`
- `docs/privacy_boundary.md`
- `docs/hosting_limits.md`
- `docs/signal_detection.md`
- `docs/SIGNAL_DICTIONARY.md`
- `docs/patch_index.md`

## Boundary

Patch 124 does not move scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, session state, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, or analysis behavior.

The page helper adds no external calls, no live model calls, no telemetry, no analytics, no storage or identity sync, no certification, no enforcement, no privacy guarantee, and no final truth claim.

`app.py` remains the orchestrator. It imports the helper and calls it from the Protocol Guide tab.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
