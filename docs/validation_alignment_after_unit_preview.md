# Patch 137 — Validation Alignment After Unit Preview

Patch 137 is a test/check hygiene patch after the Patch 131–136 front-door sequence.

## Purpose

Patch 131 introduced a Start Page / How to Start gate. Patch 135 later replaced that front-door implementation with **Aletheia Unit Preview**, and Patch 136 stabilized it. The product behavior is still the same class of behavior: a session-state-only pre-app gate that appears before the full module interface.

Some older tests still expected the original `ui.start_page` import and exact Patch 131 manifest marker. That made local review fail even though the current app correctly uses `ui.unit_preview`. Patch 137 updates those checks so they validate the real boundary instead of the old implementation detail.

## What changed

- Patch 131 start-gate test now accepts either the original Start Page helper or the current Aletheia Unit Preview helper.
- Patch 132 stabilization test now checks the current session-state gate structurally instead of requiring the old exact import line.
- Patch 131 test/check hygiene test now accepts later baseline manifests as long as the manifest is valid UTF-8 without BOM and the relevant hygiene/test files are watched.
- The protocol baseline manifest is refreshed after human-reviewed test hygiene changes.

## Boundary preserved

This patch changes validation logic only. It does not change runtime UI behavior, scoring, verdict routing, taxonomy, receipts, receipt generation, signal regexes, signal weights, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, uploads, downloads, batch behavior, external calls, telemetry, analytics, storage, identity sync, certification, enforcement, privacy guarantee, or final-truth behavior.

ALETHEIA remains a mirror, not a throne. Humans keep the judgment.
