# Patch 139 — Unit Preview Header Entry Hotfix

Patch 139 keeps **Aletheia Unit Preview** as the single hook before the full module interface, but moves the active gate so it renders after the public ALETHEIA header and styling.

## Why this patch exists

The previous wiring could show a plain first Unit Preview screen before the polished app surface. That made the entry feel like two pages: a plain pre-header gate followed by the intended ALETHEIA surface.

Patch 139 removes that visible split. The first screen should now be the polished ALETHEIA header with the Unit Preview underneath it.

## Expected flow

1. Fresh session opens on the ALETHEIA header plus **Aletheia Unit Preview**.
2. The full module tabs remain hidden.
3. The user may preview a suggested review path.
4. The user clicks **Proceed to ALETHEIA**.
5. The full app opens directly.

## Boundary

Aletheia Unit Preview is a hook, not a scoring module. It suggests where to begin; it does not score, certify, approve, reject, route verdicts, create receipts, call module engines, store data, or replace the full modules.

No scoring, routing, taxonomy, receipt schema, signal behavior, AI Integrity behavior, Privacy Audit behavior, World Lens math, upload/download behavior, external-call behavior, telemetry, storage, certification, enforcement, privacy-guarantee, or final-truth behavior changed.
