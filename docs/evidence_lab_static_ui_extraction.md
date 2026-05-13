# Evidence Lab Static UI Extraction

Patch 125 starts the Evidence Lab static UI extraction by moving stable introduction and public-data build guidance into `pages_ui/evidence_lab_page.py`.

The helper renders copy only:

- Evidence Lab page introduction.
- Public-data build guidance for WGI, population, V-Dem, and trust files.
- Modern-era scoring caveat for the public-data build flow.

## Boundary

Patch 125 does not move evidence processing, file uploads, dataframe logic, scoring, validation, receipts, downloads, module routing, session state, privacy audit scan logic, AI Integrity scan logic, World Lens math, or analysis behavior.

`app.py` remains the orchestrator for upload widgets, build buttons, session state, scoring, source diagnostics, downloads, and Evidence Lab / World Lens synchronization.

The page helper adds no external calls, no live model calls, no telemetry, no analytics, no storage or identity sync, no certification, no enforcement, no privacy guarantee, and no final truth claim.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
