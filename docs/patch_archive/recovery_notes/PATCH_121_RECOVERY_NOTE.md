# Patch 121 Recovery Note - Shared Status / Notice Cards

Patch 121 starts the shared status/notice card layer.

## What changed

- Added `ui/status_cards.py`.
- Added `render_ai_integrity_boundary_cards(container=None)`.
- Replaced the inline AI Integrity boundary caption group in `app.py` with `render_ai_integrity_boundary_cards(st)`.
- Added `tests/test_patch_121_shared_status_notice_cards.py`.
- Updated patch status, progress, architecture, patch index, README, and protocol baseline manifest.

## Recovery steps

If Patch 121 needs to be reverted:

1. Restore the inline AI Integrity boundary captions in `app.py`.
2. Remove `render_ai_integrity_boundary_cards` from the app imports and call site.
3. Remove `ui/status_cards.py`.
4. Remove Patch 121 docs/tests/status entries.
5. Restore `data/protocol_baseline_manifest.json` to the Patch 120 baseline.

## Boundary

This patch is copy-only. It does not move scoring, verdict-routing, signal patterns, signal weights, receipt schemas, module routing, session state, uploads, downloads, privacy audit scan logic, AI Integrity scan logic, World Lens math, external calls, telemetry, analytics, storage, identity sync, certification, enforcement, privacy guarantee, or final truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
