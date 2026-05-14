# Patch 138 — Single Unit Preview Entry Hotfix

Patch 138 retires the old Start Page gate as an active UI path and keeps
**Aletheia Unit Preview** as the single pre-app entry surface.

## User-visible correction

Expected entry flow:

1. The app opens directly on Aletheia Unit Preview.
2. The user may preview a suggested review path.
3. The user clicks **Proceed to ALETHEIA**.
4. The full app opens directly.

The old Start Page / How to Start gate must not appear before Unit Preview, and
there must be no double-gate flash.

## Boundary

This is a wiring and validation hotfix only. It does not change scoring, verdict
routing, taxonomy, receipt schema, signal logic, AI Integrity behavior, Privacy
Audit behavior, World Lens math, uploads, downloads, storage, telemetry,
certification, enforcement, privacy guarantees, or final-truth behavior.

Humans keep the judgment.
