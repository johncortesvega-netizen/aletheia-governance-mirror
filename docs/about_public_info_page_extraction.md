# About / Public Info Page Extraction

Patch 123 starts the low-risk page extraction phase by moving the in-app `Why ALETHEIA` page copy from `app.py` into `pages_ui/about_page.py`.

The extracted helper renders public explanation copy only. `app.py` remains the orchestrator: it owns the active tab, resolves the optional header image, and calls the page helper.

## Boundary

Patch 123 does not move scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, session state, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, or analysis behavior.

The page helper adds no external calls, no live model calls, no telemetry, no analytics, no storage or identity sync, no certification, no enforcement, no privacy guarantee, and no final truth claim.

The older root-level `about_page.py` remains in place for the standalone About page and historical tests. Patch 123 only extracts the About tab used by `app.py`.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
